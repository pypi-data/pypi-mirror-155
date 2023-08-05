import logging
import re

from django.utils.translation import gettext as _

import braintree
from rest_framework import serializers

from wagtaildonate.api.serializers.utils import (
    get_pay_in_serializer_class,
    get_single_donation_serializer_class,
)
from wagtaildonate.utils.braintree import (
    filter_country_errors,
    filter_postal_code_errors,
    filter_street_address_errors,
    filter_user_card_errors,
    map_status,
)

logger = logging.getLogger(__name__)
SingleDonationSerializer = get_single_donation_serializer_class()
PayInSerializer = get_pay_in_serializer_class()


class BaseBraintreeDonationSerializer(serializers.Serializer):
    payment_method_nonce = serializers.CharField(max_length=255)
    device_data = serializers.CharField(required=False)

    class Meta:
        fields = [
            "device_data",
            "payment_method_nonce",
        ]

    def build_billing_data(self):
        """
        Get billing data ready to be added to the transaction.
        """
        billing_data = {}
        if self.context["payment_method"].should_send_name():
            billing_data["first_name"] = self.validated_data["first_name"]
            billing_data["last_name"] = self.validated_data["surname"]
        if self.context["payment_method"].should_send_postal_code():
            billing_data["postal_code"] = self.validated_data["postal_code"]
        if self.context["payment_method"].should_send_country_code():
            billing_data["country_code_alpha2"] = self.validated_data["country"]
        if self.context["payment_method"].should_send_street_address():
            billing_data["street_address"] = ",".join(
                [
                    self.validated_data["address_line_1"],
                    self.validated_data["address_line_2"],
                ]
            )
            billing_data["extended_address"] = self.validated_data["address_line_3"]
        if self.context["payment_method"].should_send_town():
            billing_data["locality"] = self.validated_data["town"]
        return billing_data

    def build_customer_data(self):
        customer_data = {}
        if self.context["payment_method"].should_send_name():
            customer_data["first_name"] = self.validated_data["first_name"]
            customer_data["last_name"] = self.validated_data["surname"]
        if self.context["payment_method"].should_send_email_address():
            customer_data["email"] = self.validated_data["email"]
        phone_number = self.validated_data["phone_number"]
        if self.context["payment_method"].should_send_phone_number() and phone_number:
            # If we use the PhoneNumber object.
            if hasattr(phone_number, "as_e164"):
                # Delete + as Braintree does not support it.
                customer_data["phone"] = phone_number.as_e164.lstrip("+")
            # If this is returned as a string, delete all non-digit characters.
            elif isinstance(phone_number, str):
                customer_data["phone"] = re.sub("[^0-9]", "", phone_number)
        return customer_data

    def build_transaction_data(self):
        """
        Build transaction data dictionary to be sent to Braintree.
        """
        # Basic transaction data.
        transaction_data = {
            "amount": self.validated_data["amount"],
            "payment_method_nonce": self.validated_data["payment_method_nonce"],
            "options": {"submit_for_settlement": True},
        }
        # Device data
        if self.validated_data.get("device_data"):
            transaction_data["device_data"] = self.validated_data["device_data"]
        # Merchant account ID
        merchant_account_id = self.context["payment_method"].get_merchant_account_id()
        if merchant_account_id:
            transaction_data["merchant_account_id"] = merchant_account_id
        # Billing data (AVS)
        billing_data = self.build_billing_data()
        if billing_data:
            transaction_data["billing"] = billing_data
        customer_data = self.build_customer_data()
        if customer_data:
            transaction_data["customer"] = customer_data
        return transaction_data

    @property
    def gateway(self):
        return self.context["payment_method"].get_gateway()

    def perform_transaction(self):
        try:
            return self.gateway.transaction.sale(self.build_transaction_data())
        except (
            TimeoutError,
            braintree.exceptions.down_for_maintenance_error.DownForMaintenanceError,
        ) as exception:
            logger.exception("Braintree server timed out")
            raise serializers.ValidationError(
                {
                    "payment_method_nonce": [
                        _("Connection to the server timed out. Please try again later.")
                    ]
                }
            ) from exception
        except braintree.exceptions.too_many_requests_error.TooManyRequestsError as exception:
            logger.exception("Too many requests to the Braintree account.")
            raise serializers.ValidationError(
                {
                    "payment_method_nonce": [
                        _("Connection to the server timed out. Please try again later.")
                    ]
                }
            ) from exception
        except (
            braintree.exceptions.server_error.ServerError,
            braintree.exceptions.unexpected_error.UnexpectedError,
            braintree.exceptions.upgrade_required_error.UpgradeRequiredError,
            braintree.exceptions.authorization_error.AuthorizationError,
            braintree.exceptions.authentication_error.AuthenticationError,
        ) as exception:
            logger.exception("Unexpected Braintree error.")
            raise serializers.ValidationError(
                {
                    "payment_method_nonce": [
                        _("Unexpected error occurred. Please try again later.")
                    ]
                }
            ) from exception

    def handle_unsuccessful_transaction(self, result):
        logger.info(
            "Braintree transaction unsuccessful: %s - %r",
            result.message,
            result.errors.deep_errors,
        )
        error_dict = {}
        # Card errors
        card_errors = filter_user_card_errors(result)
        if card_errors:
            error_dict["payment_method_nonce"] = card_errors
        # Postal code errors
        postal_code_errors = filter_postal_code_errors(result)
        if postal_code_errors:
            error_dict["postal_code"] = postal_code_errors
        # Country errors
        country_errors = filter_country_errors(result)
        if country_errors:
            error_dict["country"] = country_errors
        # Street address error.
        street_address_errors = filter_street_address_errors(result)
        if street_address_errors:
            error_dict["address_line_1"] = street_address_errors
        # If there's no errors but the transaction is unsuccessful, return a
        # generic error message.
        if not any(error_dict.values()):
            error_dict["payment_method_nonce"] = [
                _(
                    "Sorry there was an error processing your payment. "
                    "Please try again later or use a different card."
                )
            ]
        raise serializers.ValidationError(error_dict)

    def create(self, validated_data):
        result = self.perform_transaction()
        if not result.is_success:
            return self.handle_unsuccessful_transaction(result)

        # Delete non-database fields from the serializer so they are not saved
        # to the donation object in the database which would result in in
        # exception.
        validated_data.pop("payment_method_nonce")
        validated_data.pop("device_data", None)

        # Store Braintree transaction ID/status on the model.
        validated_data["transaction_id"] = result.transaction.id
        validated_data["transaction_status"] = map_status(result.transaction.status)
        validated_data["provider_transaction_status"] = result.transaction.status

        # Store 3D Secure info if it exists
        if result.transaction.three_d_secure_info:
            three_d_secure_info = result.transaction.three_d_secure_info
            validated_data["liability_shifted"] = three_d_secure_info.liability_shifted
            validated_data[
                "liability_shift_possible"
            ] = three_d_secure_info.liability_shift_possible
            validated_data["three_d_secure_status"] = three_d_secure_info.status

        return super().create(validated_data)


class BraintreeSingleDonationSerializer(
    BaseBraintreeDonationSerializer, SingleDonationSerializer  # noqa
):
    class Meta(BaseBraintreeDonationSerializer.Meta, SingleDonationSerializer.Meta):
        fields = (
            SingleDonationSerializer.Meta.fields
            + BaseBraintreeDonationSerializer.Meta.fields
        )


class BraintreePayInSerializer(
    BaseBraintreeDonationSerializer, PayInSerializer  # noqa
):
    class Meta(BaseBraintreeDonationSerializer.Meta, PayInSerializer.Meta):
        fields = (
            PayInSerializer.Meta.fields + BaseBraintreeDonationSerializer.Meta.fields
        )

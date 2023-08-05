import logging

from django.utils.translation import gettext_lazy as _

import gocardless_pro
from rest_framework import serializers

from wagtaildonate.api.serializers.utils import get_recurring_donation_serializer_class
from wagtaildonate.models.utils import get_recurring_donation_model

logger = logging.getLogger(__name__)


RecurringDonationSerializer = get_recurring_donation_serializer_class()


class GoCardlessDonationSerializer(RecurringDonationSerializer):  # noqa
    account_holder_name = serializers.CharField(required=True, write_only=True)
    sort_code = serializers.RegexField(r"^\d{6}$", required=True, write_only=True)
    account_number = serializers.RegexField(
        r"^\d{6,8}$", required=True, write_only=True
    )
    account_holder_confirmation = serializers.BooleanField(
        default=False, write_only=True
    )

    class Meta(RecurringDonationSerializer.Meta):
        model = get_recurring_donation_model()
        fields = RecurringDonationSerializer.Meta.fields + [
            "account_holder_name",
            "sort_code",
            "account_number",
            "account_holder_confirmation",
        ]

    def validate_account_holder_confirmation(self, value):
        if not value:
            raise serializers.ValidationError(
                _(
                    "You must confirm that you are authorised to set up "
                    "Direct Debit on this account."
                )
            )
        return value

    def create(self, validated_data):
        # FIXME: Prevent double-submission

        client = self.context["payment_method"].get_client()

        # Create customer
        try:
            customer = client.customers.create(
                params={
                    "given_name": validated_data["first_name"],
                    "family_name": validated_data["surname"],
                    "address_line1": validated_data["address_line_1"],
                    "address_line2": validated_data["address_line_2"],
                    "city": validated_data["town"],
                    "postal_code": validated_data["postal_code"],
                    "country_code": validated_data["country"],
                    "email": validated_data["email"],
                }
            )
        except gocardless_pro.errors.ValidationFailedError as e:
            self.handle_gocardless_exception(e)

        # Create bank account
        try:
            bank_account = client.customer_bank_accounts.create(
                params={
                    "account_holder_name": validated_data["account_holder_name"],
                    "branch_code": validated_data["sort_code"],
                    "account_number": validated_data["account_number"],
                    "country_code": "GB",
                    "currency": "GBP",
                    "links": {"customer": customer.id},
                }
            )
        except gocardless_pro.errors.ValidationFailedError as e:
            self.handle_gocardless_exception(e)

        try:
            # Create Direct Debit mandate
            mandate = client.mandates.create(
                params={"links": {"customer_bank_account": bank_account.id}}
            )

            # Create subscription
            subscription = client.subscriptions.create(
                params={
                    "interval_unit": "monthly",
                    "amount": int(validated_data["amount"] * 100),
                    "currency": "GBP",
                    "links": {"mandate": mandate.id},
                }
            )
        except gocardless_pro.errors.ValidationFailedError as e:
            self.handle_gocardless_exception(e)

        validated_data["subscription_id"] = subscription.id

        # Delete non-database fields.
        del validated_data["account_holder_name"]
        del validated_data["sort_code"]
        del validated_data["account_number"]
        del validated_data["account_holder_confirmation"]

        return super().create(validated_data)

    def handle_gocardless_exception(self, exception):
        logger.info("GoCardless transaction unsuccessful: %r", exception)
        if not isinstance(
            exception,
            (
                gocardless_pro.errors.ValidationFailedError,
                gocardless_pro.errors.InvalidStateError,
            ),
        ):
            logger.exception(
                "Unexpected exception raised by GoCardless while setting up a new Direct Debit"
            )
            raise serializers.ValidationError(
                {
                    "direct_debit_errors": [
                        _(
                            "There was an error with setting up your Direct Debit payment. Please try again later."
                        )
                    ]
                }
            )
        error_dict = {}
        account_number_errors = list(
            self.filter_account_number_errors(exception.errors)
        )
        sort_code_errors = list(self.filter_sort_code_errors(exception.errors))
        account_holder_name_errors = list(
            self.filter_account_holder_name_errors(exception.errors)
        )
        postal_code_errors = list(self.filter_postal_code_errors(exception.errors))
        if account_number_errors:
            error_dict["account_number"] = account_number_errors
        if sort_code_errors:
            error_dict["sort_code"] = sort_code_errors
        if account_holder_name_errors:
            error_dict["account_holder_name"] = account_holder_name_errors
        if postal_code_errors:
            error_dict["postal_code"] = postal_code_errors
        if not any(error_dict.values()):
            error_dict["direct_debit_errors"] = [
                _(
                    "Sorry. There was an error processing your Direct Debit payment. "
                    "Plase try again or contact us."
                )
            ]
        raise serializers.ValidationError(error_dict)

    def filter_account_number_errors(self, errors):
        for error in errors:
            if error.get("field") != "account_number":
                continue
            message = error.get("message")
            if message:
                yield f"Account number {message}"

    def filter_sort_code_errors(self, errors):
        for error in errors:
            if error.get("field") != "branch_code":
                continue
            message = error.get("message")
            if message:
                yield f"Sort code {message}"

    def filter_account_holder_name_errors(self, errors):
        for error in errors:
            if error.get("field") != "account_holder_name":
                continue
            message = error.get("message")
            if message:
                yield f"Account holder name {message}"

    def filter_postal_code_errors(self, errors):
        for error in errors:
            if error.get("field") != "postal_code":
                continue
            message = error.get("message")
            if message:
                yield f"Postal code {message}"

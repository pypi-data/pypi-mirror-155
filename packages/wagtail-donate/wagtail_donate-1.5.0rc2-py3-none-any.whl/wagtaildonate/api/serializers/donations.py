from decimal import Decimal

from django.utils.translation import gettext_lazy as _

from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from wagtaildonate.api.serializers.recaptcha import RecaptchaField
from wagtaildonate.models import BaseDonation
from wagtaildonate.models.utils import (
    get_pay_in_event_model,
    get_pay_in_model,
    get_recurring_donation_model,
    get_single_donation_model,
)
from wagtaildonate.settings import donate_settings

OTHER_EVENT_CODE = "other"


class BaseDonationSerializer(serializers.ModelSerializer):
    """
    Base serializer used for pay in, single and recurring donations.
    """

    phone_number = PhoneNumberField()
    recaptcha_token = RecaptchaField()

    class Meta:
        model = BaseDonation
        fields = [
            "donation_page",
            "payment_method",
            "id",
            "amount",
            "first_name",
            "surname",
            "email",
            "phone_number",
            "address_line_1",
            "address_line_2",
            "address_line_3",
            "town",
            "postal_code",
            "country",
            "on_behalf_of_organisation",
            "in_memory",
            "in_memory_of",
            "sms_consent",
            "phone_consent",
            "email_consent",
            "post_consent",
            "recaptcha_token",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "phone_number": {
                "required": donate_settings.PHONE_NUMBER_REQUIRED,
                "allow_blank": not donate_settings.PHONE_NUMBER_REQUIRED,
            },
            "email": {
                "required": donate_settings.EMAIL_REQUIRED,
                "allow_blank": not donate_settings.EMAIL_REQUIRED,
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # If RECAPTCHA_PRIVATE_KEY is not set, don't attempt to validate recaptcha
        if not donate_settings.RECAPTCHA_PRIVATE_KEY:
            self.fields.pop("recaptcha_token")

    def validate_amount(self, value):
        minimum_amount = Decimal(self.context.get("minimum_amount", Decimal("1.00")))
        maximum_amount = Decimal(
            self.context.get("maximum_amount", Decimal("10000.00"))
        )
        if value < minimum_amount:
            raise serializers.ValidationError(_(f"Minimum amount is {minimum_amount}."))
        if value > maximum_amount:
            raise serializers.ValidationError(_(f"Maximum amount is {maximum_amount}."))
        return value

    def validate(self, data):
        data = super().validate(data)
        # recaptcha_token isn't needed past this point
        data.pop("recaptcha_token", "")
        return data


class SingleDonationSerializer(BaseDonationSerializer):
    """
    Base serializer for single donations.
    """

    class Meta(BaseDonationSerializer.Meta):
        model = get_single_donation_model()
        fields = BaseDonationSerializer.Meta.fields + [
            "gift_aid_declaration",
        ]


class RecurringDonationSerializer(BaseDonationSerializer):
    """
    Base serializer for recurring donations.
    """

    class Meta(BaseDonationSerializer.Meta):
        model = get_recurring_donation_model()
        fields = BaseDonationSerializer.Meta.fields + [
            "gift_aid_declaration",
            "frequency",
        ]


class PayInSerializer(BaseDonationSerializer):
    class Meta(BaseDonationSerializer.Meta):
        model = get_pay_in_model()
        fields = BaseDonationSerializer.Meta.fields + [
            "event_name",
            "event_code",
            "fundraiser_reference",
        ]

    def validate(self, data):
        data = super().validate(data)

        if not donate_settings.PAY_IN_EVENTS_ENABLED:
            return data

        fundraiser_reference_required = False

        pay_in_event_model = get_pay_in_event_model()
        if data["event_code"] != OTHER_EVENT_CODE:
            try:
                event = pay_in_event_model.objects.get(event_code=data["event_code"])
            except pay_in_event_model.DoesNotExist:
                raise serializers.ValidationError(
                    {
                        "event_code": [
                            _(
                                "Pay-in event does not exist. Please select a valid event."
                            )
                        ]
                    }
                )
            fundraiser_reference_required = event.fundraiser_reference_required
        else:
            fundraiser_reference_required = (
                donate_settings.PAY_IN_OTHER_EVENT_REQUIRE_FUNDRAISER_REFERENCE
            )

        if fundraiser_reference_required and not data.get("fundraiser_reference"):
            raise serializers.ValidationError(
                {"fundraiser_reference": [_("Fundraiser reference must be entered.")]}
            )

        return data

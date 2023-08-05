import django

DEFAULTS = {
    # Payment methods list
    "PAYMENT_METHODS": [],
    # Contact details
    "PHONE_NUMBER_REQUIRED": True,
    "EMAIL_REQUIRED": True,
    # Base donation model and serializer
    "SINGLE_DONATION_MODEL": "wagtaildonate.SingleDonation",
    "SINGLE_DONATION_SERIALIZER_CLASS": "wagtaildonate.api.serializers.donations.SingleDonationSerializer",
    "RECURRING_DONATION_MODEL": "wagtaildonate.RecurringDonation",
    "RECURRING_DONATION_SERIALIZER_CLASS": "wagtaildonate.api.serializers.donations.RecurringDonationSerializer",
    "PAY_IN_MODEL": "wagtaildonate.PayIn",
    "PAY_IN_SERIALIZER_CLASS": "wagtaildonate.api.serializers.donations.PayInSerializer",
    "PAY_IN_EVENT_MODEL": "wagtaildonate.PayInEvent",
    "PAY_IN_EVENT_SERIALIZER_CLASS": "wagtaildonate.api.serializers.configuration.PayInEventSerializer",
    # Configuration endpoint
    "CONFIGURATION_CLASS": "wagtaildonate.configuration.Configuration",
    "CONFIGURATION_SERIALIZER_CLASS": "wagtaildonate.api.serializers.configuration.ConfigurationSerializer",
    # Wagtail Admin settings
    "DONATION_EXPORT_ENABLED": True,
    "DONATION_EXPORT_LOG_ENABLED": True,
    "DONATION_EXPORT_LOG_MODEL": "wagtaildonate.DonationExportLog",
    "THREE_D_SECURE_EXPORT_FIELDS": False,
    # Default page settings
    "GET_DEFAULT_DONATION_PAGE_INSTANCE_CALLABLE": None,
    # Address lookup
    "ADDRESS_LOOKUP": {
        "class": "wagtaildonate.address_lookups.generic.GenericAddressLookup",
    },
    # Minimum and maximum amount
    "MINIMUM_AMOUNT_PER_FREQUENCY": {
        "single": "1.00",
        "monthly": "1.00",
        "payin": "1.00",
    },
    "MAXIMUM_AMOUNT_PER_FREQUENCY": {
        "single": "10000",
        "monthly": "10000",
        "payin": "10000",
    },
    "PAY_IN_EVENTS_ENABLED": True,
    "PAY_IN_OTHER_EVENT_ENABLED": True,
    "PAY_IN_OTHER_EVENT_REQUIRE_FUNDRAISER_REFERENCE": True,
    # reCAPTCHA
    "RECAPTCHA_PUBLIC_KEY": "",
    "RECAPTCHA_PRIVATE_KEY": "",
    "RECAPTCHA_MINIMUM_SCORE": 0.5,
}


class WagtailDonateSettings:
    def __getattr__(self, attr):
        django_settings = getattr(django.conf.settings, "WAGTAIL_DONATE", {})

        try:
            # Check if present in user settings
            return django_settings[attr]
        except KeyError:
            return DEFAULTS[attr]


donate_settings = WagtailDonateSettings()

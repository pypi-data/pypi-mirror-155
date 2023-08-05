from wagtaildonate.address_lookups.utils import get_address_lookup
from wagtaildonate.countries import get_countries
from wagtaildonate.models.utils import get_pay_in_event_model
from wagtaildonate.payment_methods.utils import get_all_payment_methods
from wagtaildonate.settings import donate_settings


class Configuration:
    def __init__(
        self,
        *,
        checkout_url,
        pay_in_page_id,
        pay_in_success_url,
        allowed_frequencies=None,
        payment_method_context=None
    ):
        self.allowed_frequencies = allowed_frequencies
        self.payment_method_context = payment_method_context
        self.countries = self.get_countries()
        self.checkout_url = checkout_url
        self.payment_methods = self.get_payment_methods()
        self.address_lookup = self.get_address_lookup()
        self.pay_in_events = self.get_pay_in_events()
        self.pay_in_page_id = pay_in_page_id
        self.pay_in_success_url = pay_in_success_url

    def get_payment_methods(self):
        return list(
            get_all_payment_methods(
                allowed_frequencies=self.allowed_frequencies,
                payment_method_context=self.payment_method_context,
            )
        )

    def get_address_lookup(self):
        return get_address_lookup()

    def get_countries(self):
        return tuple(get_countries())

    def get_pay_in_events(self):
        if not donate_settings.PAY_IN_EVENTS_ENABLED:
            return []
        pay_in_event_model = get_pay_in_event_model()
        pay_in_events = list(pay_in_event_model.objects.all())
        if donate_settings.PAY_IN_OTHER_EVENT_ENABLED:
            pay_in_events.append(
                pay_in_event_model(
                    event_code="other",
                    event_name="Other",
                    fundraiser_reference_required=donate_settings.PAY_IN_OTHER_EVENT_REQUIRE_FUNDRAISER_REFERENCE,
                )
            )
        return pay_in_events


def get_configuration_class_string():
    from wagtaildonate.settings import donate_settings

    return donate_settings.CONFIGURATION_CLASS


def get_configuration_class():
    from django.utils.module_loading import import_string

    return import_string(get_configuration_class_string())

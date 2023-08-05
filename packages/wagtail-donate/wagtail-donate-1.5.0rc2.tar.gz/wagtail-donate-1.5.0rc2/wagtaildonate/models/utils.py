from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string

from wagtail import VERSION as WAGTAIL_VERSION

from wagtaildonate.settings import donate_settings


def get_default_donation_page():
    custom_func_path = donate_settings.GET_DEFAULT_DONATION_PAGE_INSTANCE_CALLABLE
    if custom_func_path is not None:
        custom_func = import_string(custom_func_path)
        return custom_func()

    if WAGTAIL_VERSION >= (3, 0):
        from wagtail.models import Page
    else:
        from wagtail.core.models import Page

    from wagtaildonate.models import AbstractDonationPage

    try:
        return Page.objects.type(AbstractDonationPage).specific().live()[0]
    except IndexError as exception:
        raise ImproperlyConfigured(
            "Default donation landing page is not created."
        ) from exception


def get_single_donation_model_string():
    from wagtaildonate.settings import donate_settings

    return donate_settings.SINGLE_DONATION_MODEL


def get_single_donation_model():
    from django.apps import apps

    return apps.get_model(get_single_donation_model_string())


def get_recurring_donation_model_string():
    from wagtaildonate.settings import donate_settings

    return donate_settings.RECURRING_DONATION_MODEL


def get_recurring_donation_model():
    from django.apps import apps

    return apps.get_model(get_recurring_donation_model_string())


def get_pay_in_model_string():
    from wagtaildonate.settings import donate_settings

    return donate_settings.PAY_IN_MODEL


def get_pay_in_model():
    from django.apps import apps

    return apps.get_model(get_pay_in_model_string())


def get_pay_in_event_model_string():
    from wagtaildonate.settings import donate_settings

    return donate_settings.PAY_IN_EVENT_MODEL


def get_pay_in_event_model():
    from django.apps import apps

    return apps.get_model(get_pay_in_event_model_string())


def get_pay_in_event_serializer_class():
    from wagtaildonate.settings import donate_settings

    return donate_settings.PAY_IN_EVENT_SERIALIZER_CLASS


def get_donation_export_log_model_string():
    from wagtaildonate.settings import donate_settings

    return donate_settings.DONATION_EXPORT_LOG_MODEL


def get_donation_export_log_model():
    from django.apps import apps

    return apps.get_model(get_donation_export_log_model_string())

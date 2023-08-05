from typing import Type

from rest_framework import serializers


def get_single_donation_serializer_string() -> str:
    from wagtaildonate.settings import donate_settings

    return donate_settings.SINGLE_DONATION_SERIALIZER_CLASS


def get_single_donation_serializer_class() -> Type[serializers.Serializer]:
    from django.utils.module_loading import import_string

    return import_string(get_single_donation_serializer_string())


def get_recurring_donation_serializer_string() -> str:
    from wagtaildonate.settings import donate_settings

    return donate_settings.RECURRING_DONATION_SERIALIZER_CLASS


def get_recurring_donation_serializer_class() -> Type[serializers.Serializer]:
    from django.utils.module_loading import import_string

    return import_string(get_recurring_donation_serializer_string())


def get_pay_in_serializer_string() -> str:
    from wagtaildonate.settings import donate_settings

    return donate_settings.PAY_IN_SERIALIZER_CLASS


def get_pay_in_serializer_class() -> Type[serializers.Serializer]:
    from django.utils.module_loading import import_string

    return import_string(get_pay_in_serializer_string())


def get_pay_in_event_serializer_string() -> str:
    from wagtaildonate.settings import donate_settings

    return donate_settings.PAY_IN_EVENT_SERIALIZER_CLASS


def get_pay_in_event_serializer_class() -> Type[serializers.Serializer]:
    from django.utils.module_loading import import_string

    return import_string(get_pay_in_event_serializer_string())


def get_configuration_serializer_string() -> str:
    from wagtaildonate.settings import donate_settings

    return donate_settings.CONFIGURATION_SERIALIZER_CLASS


def get_configuration_serializer_class() -> Type[serializers.Serializer]:
    from django.utils.module_loading import import_string

    return import_string(get_configuration_serializer_string())

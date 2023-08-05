from typing import Generator

from django.utils.module_loading import import_string

from wagtaildonate.exceptions import PaymentMethodNotFound
from wagtaildonate.payment_methods.base import PaymentMethod
from wagtaildonate.settings import donate_settings


def instantiate_payment_method(setting, klass=None, context=None) -> PaymentMethod:
    if klass is None:
        klass = import_string(setting["class"])
    return klass(setting.get("options", {}), context=context)


def get_payment_method(user_payment_method, context=None) -> PaymentMethod:
    for payment_method in donate_settings.PAYMENT_METHODS:
        klass = import_string(payment_method["class"])
        if klass.code == user_payment_method:
            return instantiate_payment_method(
                payment_method, klass=klass, context=context
            )
    raise PaymentMethodNotFound(user_payment_method)


def get_all_payment_methods(
    *, allowed_frequencies=None, payment_method_context=None
) -> Generator[PaymentMethod, None, None]:
    for payment_method in donate_settings.PAYMENT_METHODS:
        payment_method_object = instantiate_payment_method(
            payment_method, context=payment_method_context
        )
        if allowed_frequencies and not any(
            payment_method_object.is_frequency_supported(f) for f in allowed_frequencies
        ):
            continue
        yield payment_method_object

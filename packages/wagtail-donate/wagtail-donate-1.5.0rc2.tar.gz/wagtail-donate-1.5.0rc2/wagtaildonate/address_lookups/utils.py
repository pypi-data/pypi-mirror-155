from django.utils.module_loading import import_string

from wagtaildonate.address_lookups.base import AddressLookup
from wagtaildonate.settings import donate_settings


def instantiate_address_lookup(setting, klass=None) -> AddressLookup:
    if klass is None:
        klass = import_string(setting["class"])
    return klass(setting.get("options", {}))


def get_address_lookup() -> AddressLookup:
    return instantiate_address_lookup(donate_settings.ADDRESS_LOOKUP)

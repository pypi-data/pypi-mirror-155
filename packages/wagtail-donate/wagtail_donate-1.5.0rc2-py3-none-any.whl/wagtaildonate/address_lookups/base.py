from typing import Any, ClassVar, Dict

AddressLookupOptions = Dict[str, Any]


class AddressLookup:
    code: ClassVar[str]
    options: AddressLookupOptions
    assets: ClassVar[Dict[str, Any]] = None

    def __init__(self, options: AddressLookupOptions):
        self.options = options

    def get_frontend_options(self) -> AddressLookupOptions:
        return {}

    def get_assets(self):
        return self.assets or {}

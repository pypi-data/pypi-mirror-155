from wagtaildonate.address_lookups.base import AddressLookup


class GenericAddressLookup(AddressLookup):
    code = "generic"

    def get_frontend_options(self):
        return {
            "auto_complete_enabled": self.options.get("AUTO_COMPLETE_ENABLED", True)
        }

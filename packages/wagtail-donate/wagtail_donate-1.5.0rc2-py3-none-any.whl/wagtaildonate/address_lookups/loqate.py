from wagtaildonate.address_lookups.base import AddressLookup


class LoqateAddressLookup(AddressLookup):
    code = "loqate"
    assets = {
        "js": [{"src": "https://services.postcodeanywhere.co.uk/js/address-3.91.js"}],
        "css": [
            {
                "href": "https://services.postcodeanywhere.co.uk/css/address-3.91.css",
                "rel": "stylesheet",
                "type": "text/css",
            },
        ],
    }

    def get_frontend_options(self):
        return {
            "api_key": self.options["API_KEY"],
            "set_country_by_ip": self.options.get("SET_COUNTRY_BY_IP", True),
        }

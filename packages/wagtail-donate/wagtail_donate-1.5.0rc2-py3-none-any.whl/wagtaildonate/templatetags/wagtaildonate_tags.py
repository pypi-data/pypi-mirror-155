from django import template

from wagtaildonate.address_lookups.utils import get_address_lookup
from wagtaildonate.payment_methods.utils import get_all_payment_methods
from wagtaildonate.utils.assets import get_source_code_for_assets

register = template.Library()


@register.simple_tag
def payment_methods_assets(frequency=None):
    """
    Load assets in HTML for all active payment methods.
    """
    payment_methods = get_all_payment_methods()
    js_assets = []
    css_assets = []
    for payment_method in payment_methods:
        # Filter by frequency if supplied.
        if frequency is not None and not payment_method.is_frequency_supported(
            frequency
        ):
            continue
        method_assets = payment_method.get_assets()
        method_js_assets = method_assets.get("js", [])
        method_css_assets = method_assets.get("css", [])
        for method_js_asset in method_js_assets:
            # Eliminate duplicates.
            if method_js_asset not in js_assets:
                js_assets.append(method_js_asset)
        for method_css_asset in method_css_assets:
            # Eliminate duplicates.
            if method_css_asset not in css_assets:
                css_assets.append(method_css_assets)
    return get_source_code_for_assets({"js": js_assets, "css": css_assets})


@register.simple_tag
def address_lookups_assets(frequency=None):
    """
    Load assets in HTML for the current address lookup.
    """
    address_lookup = get_address_lookup()
    assets = address_lookup.get_assets()
    return get_source_code_for_assets(assets)

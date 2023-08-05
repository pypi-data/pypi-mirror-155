from xml.etree import ElementTree

from django.utils.safestring import mark_safe


def get_source_code_for_js_assets(assets):
    code = ""
    for asset in assets:
        script = ElementTree.Element("script", attrib=asset)
        code += ElementTree.tostring(script, encoding="unicode", method="html")
    return mark_safe(code)


def get_source_code_for_css_assets(assets):
    code = ""
    for asset in assets:
        link = ElementTree.Element("link", attrib=asset)
        code += ElementTree.tostring(link, encoding="unicode", method="html")
    return mark_safe(code)


def get_source_code_for_assets(assets):
    js_assets = assets.get("js", [])
    css_assets = assets.get("css", [])
    code = ""
    code += get_source_code_for_js_assets(js_assets)
    code += get_source_code_for_css_assets(css_assets)
    return mark_safe(code)

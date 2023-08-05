import os

__version__ = "1.5.0rc2"


def get_version():
    dev_tag = os.environ.get("WAGTAIL_DONATE_DEV_TAG")
    if not dev_tag:
        return __version__
    try:
        dev_tag = int(dev_tag)
    except (ValueError, TypeError):
        raise ValueError("Dev version tag has to be a number.")
    return f"{__version__}.dev{dev_tag}"


default_app_config = "wagtaildonate.apps.WagtailDonateConfig"

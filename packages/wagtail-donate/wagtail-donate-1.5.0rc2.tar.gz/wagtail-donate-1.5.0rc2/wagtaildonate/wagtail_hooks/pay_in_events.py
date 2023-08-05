from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from wagtaildonate.models.utils import get_pay_in_event_model
from wagtaildonate.settings import donate_settings


class PayInEventAdmin(ModelAdmin):
    model = get_pay_in_event_model()

    menu_icon = "doc-full-inverse"
    menu_order = 300
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("event_name", "event_code")


def register_pay_in_events_wagtail_hooks():
    if donate_settings.PAY_IN_EVENTS_ENABLED:
        modeladmin_register(PayInEventAdmin)

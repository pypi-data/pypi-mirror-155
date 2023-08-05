from wagtail import VERSION as WAGTAIL_VERSION
from wagtail.contrib.modeladmin.helpers import PermissionHelper
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from wagtaildonate.models import get_donation_export_log_model
from wagtaildonate.settings import donate_settings

if WAGTAIL_VERSION >= (3, 0):
    from wagtail import hooks
else:
    from wagtail.core import hooks


class ReadOnlyPermissionHelper(PermissionHelper):
    def user_can_edit_obj(self, *args, **kwargs):
        return False

    def user_can_delete_obj(self, *args, **kwargs):
        return False

    def user_can_create(self, *args, **kwargs):
        return False

    def get_all_model_permissions(self, *args, **kwargs):
        return (
            super()
            .get_all_model_permissions(*args, **kwargs)
            .filter(codename__startswith="view_")
        )


class DonationExportLogAdmin(ModelAdmin):
    model = get_donation_export_log_model()
    menu_label = "Export logs"
    menu_order = 1060
    permission_helper_class = ReadOnlyPermissionHelper
    inspect_view_enabled = True
    ordering = ["-created_at"]
    menu_icon = "list-ul"
    list_display = [
        "created_at",
        "donation_type",
        "datetime_from",
        "datetime_to",
        "get_user",
    ]
    list_filter = ["donation_type"]
    search_fields = ["user__pk", "user_name"]

    def get_user(self, obj):
        if obj.user:
            return obj.user
        return obj.user_name

    get_user.short_description = "User"

    # Copied from Wagtail to allow registering a custom menu hook.
    # https://github.com/wagtail/wagtail/blob/314a926f75f96275ccd9c84a568d7e588f13b258/wagtail/contrib/modeladmin/options.py#L30-L56
    # Related issue: https://github.com/wagtail/wagtail/issues/5302
    def register_with_wagtail(self):
        @hooks.register("register_permissions")
        def register_permissions():
            return self.get_permissions_for_registration()

        @hooks.register("register_admin_urls")
        def register_admin_urls():
            return self.get_admin_urls_for_registration()

        @hooks.register("register_payments_menu_item")
        def register_admin_menu_item():
            return self.get_menu_item()

        # Overriding the explorer page queryset is a somewhat 'niche' / experimental
        # operation, so only attach that hook if we specifically opt into it
        # by returning True from will_modify_explorer_page_queryset
        if self.will_modify_explorer_page_queryset():

            @hooks.register("construct_explorer_page_queryset")
            def construct_explorer_page_queryset(parent_page, queryset, request):
                return self.modify_explorer_page_queryset(
                    parent_page, queryset, request
                )


def register_export_log_wagtail_hooks():
    if donate_settings.DONATION_EXPORT_LOG_ENABLED:
        modeladmin_register(DonationExportLogAdmin)

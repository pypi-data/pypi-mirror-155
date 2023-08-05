from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from wagtail import VERSION as WAGTAIL_VERSION
from wagtail.admin.menu import MenuItem

from wagtaildonate.models.utils import (
    get_pay_in_model,
    get_recurring_donation_model,
    get_single_donation_model,
)
from wagtaildonate.settings import donate_settings

if WAGTAIL_VERSION >= (3, 0):
    from wagtail import hooks
else:
    from wagtail.core import hooks


def register_export_permissions():
    donation_model = get_single_donation_model()
    recurring_donation_model = get_recurring_donation_model()
    pay_in_model = get_pay_in_model()
    content_types = ContentType.objects.get_for_models(
        donation_model, recurring_donation_model, pay_in_model
    )
    return Permission.objects.filter(
        Q(content_type=content_types[donation_model], codename="can_export_donations")
        | Q(
            content_type=content_types[recurring_donation_model],
            codename="can_export_recurring_donations",
        )
        | Q(content_type=content_types[pay_in_model], codename="can_export_pay_ins")
    )


class ExportDonationsMenuItem(MenuItem):
    def is_shown(self, request):
        return request.user.has_perm("wagtaildonate.can_export_donations")


def register_export_donations_menu_item():
    return ExportDonationsMenuItem(
        _("Export donations"),
        reverse("wagtaildonate_admin:export"),
        classnames="icon icon-download",
        order=1050,
    )


class ExportRecurringDonationsMenuItem(MenuItem):
    def is_shown(self, request):
        return request.user.has_perm("wagtaildonate.can_export_recurring_donations")


def register_export_recurring_donations_menu_item():
    return ExportRecurringDonationsMenuItem(
        _("Export recurring donations"),
        reverse("wagtaildonate_admin:export_recurring"),
        classnames="icon icon-download",
        order=1051,
    )


class ExportPayInsMenuItem(MenuItem):
    def is_shown(self, request):
        return request.user.has_perm("wagtaildonate.can_export_pay_ins")


def register_export_pay_ins_menu_item():
    return ExportPayInsMenuItem(
        _("Export pay ins"),
        reverse("wagtaildonate_admin:export_pay_ins"),
        classnames="icon icon-download",
        order=1052,
    )


def register_export_wagtail_hooks():
    if donate_settings.DONATION_EXPORT_ENABLED:
        hooks.register("register_permissions", register_export_permissions)
        hooks.register(
            "register_payments_menu_item", register_export_donations_menu_item
        )
        hooks.register(
            "register_payments_menu_item", register_export_recurring_donations_menu_item
        )
        hooks.register("register_payments_menu_item", register_export_pay_ins_menu_item)

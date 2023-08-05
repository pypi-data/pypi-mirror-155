from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _


class DonationExportLog(models.Model):
    DONATION_TYPE_SINGLE = "single"
    DONATION_TYPE_RECURRING = "recurring"
    DONATION_TYPE_PAY_IN = "pay_in"
    DONATION_TYPE_CHOICES = [
        (DONATION_TYPE_SINGLE, _("Single")),
        (DONATION_TYPE_RECURRING, _("Recurring")),
        (DONATION_TYPE_PAY_IN, _("Pay in")),
    ]

    donation_type = models.CharField(max_length=10, choices=DONATION_TYPE_CHOICES)

    datetime_from = models.DateTimeField()
    datetime_to = models.DateTimeField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, null=True)
    # In case the user gets deleted.
    user_name = models.CharField(blank=True, max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    remote_addr = models.CharField(
        blank=True, max_length=255, verbose_name=_("REMOTE_ADDR")
    )
    remote_host = models.CharField(
        blank=True, max_length=255, verbose_name=_("REMOTE_HOST")
    )
    x_forwarded_for = models.CharField(
        blank=True, max_length=255, verbose_name=_("X-Forwarded-For")
    )
    user_agent = models.CharField(blank=True, max_length=255)

    class Meta:
        default_permissions = ["view"]

    def __str__(self):
        return gettext("DonationExportLog object")

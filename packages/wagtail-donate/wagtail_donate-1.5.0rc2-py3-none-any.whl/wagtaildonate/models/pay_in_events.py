from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail import VERSION as WAGTAIL_VERSION

if WAGTAIL_VERSION >= (3, 0):
    from wagtail.admin.panels import FieldPanel
else:
    from wagtail.admin.edit_handlers import FieldPanel


class AbstractPayInEvent(models.Model):
    event_code = models.CharField(max_length=50, unique=True)
    event_name = models.CharField(max_length=255)
    fundraiser_reference_required = models.BooleanField()

    panels = [
        FieldPanel("event_code"),
        FieldPanel("event_name"),
        FieldPanel("fundraiser_reference_required"),
    ]

    class Meta:
        abstract = True
        verbose_name = _("Pay In Event")
        verbose_name_plural = _("Pay In Events")

    def __str__(self):
        return self.event_code


class PayInEvent(AbstractPayInEvent):
    pass

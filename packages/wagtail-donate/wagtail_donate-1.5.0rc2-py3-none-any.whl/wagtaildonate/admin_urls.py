from django.urls import path

from wagtaildonate.admin_views.export import (
    DonationExportView,
    PayInExportView,
    RecurringDonationExportView,
)
from wagtaildonate.settings import donate_settings

app_name = "wagtaildonate"

urlpatterns = []

if donate_settings.DONATION_EXPORT_ENABLED:
    urlpatterns += [
        path("export/single/", DonationExportView.as_view(), name="export"),
        path(
            "export/recurring/",
            RecurringDonationExportView.as_view(),
            name="export_recurring",
        ),
        path("export/payins/", PayInExportView.as_view(), name="export_pay_ins"),
    ]

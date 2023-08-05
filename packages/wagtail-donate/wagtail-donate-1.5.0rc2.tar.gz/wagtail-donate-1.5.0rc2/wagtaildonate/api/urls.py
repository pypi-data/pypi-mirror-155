from django.urls import path

from wagtaildonate.api.views.configuration import DonationsConfigurationAPIView
from wagtaildonate.api.views.donations import DonationsCreateAPIView

app_name = "api"

urlpatterns = [
    path("donations/", DonationsCreateAPIView.as_view(), name="donations-create"),
    path(
        "configuration/donations/",
        DonationsConfigurationAPIView.as_view(),
        name="configuration-donations",
    ),
]

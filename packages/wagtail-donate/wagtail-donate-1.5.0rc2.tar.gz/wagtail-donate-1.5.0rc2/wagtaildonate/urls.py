from django.urls import include, path

from wagtaildonate.api import urls as api_urls
from wagtaildonate.views import DonateCheckoutView

app_name = "wagtaildonate"

urlpatterns = [
    path("", DonateCheckoutView.as_view(), name="donate-checkout"),
    path("api/", include(api_urls, namespace="api")),
]

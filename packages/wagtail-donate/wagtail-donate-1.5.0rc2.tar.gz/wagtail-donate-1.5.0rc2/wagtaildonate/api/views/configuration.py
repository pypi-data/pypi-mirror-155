from typing import ClassVar, List, Optional, Type

from wagtail import VERSION as WAGTAIL_VERSION

from rest_framework import generics, permissions, serializers
from rest_framework.reverse import reverse

from wagtaildonate.api.metadata import HiddenMetadata
from wagtaildonate.api.serializers.utils import get_configuration_serializer_class
from wagtaildonate.configuration import get_configuration_class
from wagtaildonate.models import AbstractDonationFundraisingPayInPage
from wagtaildonate.payment_methods.base import PaymentMethod

if WAGTAIL_VERSION >= (3, 0):
    from wagtail.models import Page
else:
    from wagtail.core.models import Page


class BaseConfigurationAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    checkout_url_pattern: ClassVar[Optional[str]] = "wagtaildonate:api:donations-create"
    allowed_frequencies: ClassVar[Optional[List[str]]] = None

    # Hide data on the OPTIONS request.
    metadata_class = HiddenMetadata

    def get_serializer_class(self) -> Type[serializers.Serializer]:
        return get_configuration_serializer_class()

    def get_allowed_frequencies(self) -> List[str]:
        return self.allowed_frequencies or []

    def get_checkout_url(self) -> str:
        try:
            current_app = self.request.current_app
        except AttributeError:
            try:
                current_app = self.request.resolver_match.namespace
            except AttributeError:
                current_app = None
        return self.request.build_absolute_uri(
            reverse(
                self.checkout_url_pattern,
                current_app=current_app,
                request=self.request,
            )
        )

    def get_pay_in_page(self) -> Page:
        return (
            Page.objects.live()
            .public()
            .specific()
            .filter(Page.objects.type_q(AbstractDonationFundraisingPayInPage))
            .first()
        )

    def get_pay_in_success_url(self, pay_in_page: Page) -> str:
        return pay_in_page.get_thank_you_page_url(self.request)

    def get_object_kwargs(self, **kwargs):
        kwargs.setdefault("checkout_url", self.get_checkout_url())
        kwargs.setdefault("allowed_frequencies", self.get_allowed_frequencies())
        pay_in_page = self.get_pay_in_page()
        if pay_in_page:
            kwargs.setdefault("pay_in_page_id", pay_in_page.pk)
            kwargs.setdefault(
                "pay_in_success_url", self.get_pay_in_success_url(pay_in_page)
            )
        else:
            kwargs.setdefault("pay_in_page_id", 0)
            kwargs.setdefault("pay_in_success_url", "")
        return kwargs

    def get_object(self):
        klass = get_configuration_class()
        return klass(**self.get_object_kwargs())


class DonationsConfigurationAPIView(BaseConfigurationAPIView):
    allowed_frequencies = [
        PaymentMethod.FREQUENCY_SINGLE,
        PaymentMethod.FREQUENCY_MONTHLY,
        PaymentMethod.FREQUENCY_PAYIN,
    ]

    def get_object_kwargs(self, **kwargs):
        return super().get_object_kwargs(**kwargs)

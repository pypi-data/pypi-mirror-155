from decimal import Decimal
from typing import Dict, Optional, Type

from django.db import models

from wagtail import VERSION as WAGTAIL_VERSION

from rest_framework import generics, permissions, serializers, status
from rest_framework.response import Response

from wagtaildonate.api.metadata import HiddenMetadata
from wagtaildonate.api.serializers.payment_method import (
    PaymentMethodAndFrequencySerializer,
)
from wagtaildonate.models import get_default_donation_page
from wagtaildonate.payment_methods.base import PaymentMethod
from wagtaildonate.settings import donate_settings

if WAGTAIL_VERSION >= (3, 0):
    from wagtail.models import Page
else:
    from wagtail.core.models import Page


class DonationsCreateAPIView(generics.CreateAPIView):
    """
    Make donations.
    """

    donation_id: Optional[int]

    # This view is available to all the users.
    permission_classes = [permissions.AllowAny]

    # Make this view CSRF exempt.
    authentication_classes = []

    # Hide data on the OPTIONS request.
    metadata_class = HiddenMetadata

    # Initial serializer that validates payment_method and frequency.
    # It will return appropriate payment method and serializer class for the
    # specific payment method.
    serializer_class = PaymentMethodAndFrequencySerializer

    def __init__(self, *args, **kwargs):
        self.donation_id = None
        super().__init__(*args, **kwargs)

    def create(self, request, *args, **kwargs) -> Response:
        """
        Only return ID when the donation is created.
        https://github.com/encode/django-rest-framework/blob/acbd9d8222e763c7f9c7dc2de23c430c702e06d4/rest_framework/mixins.py#L16-L21
        """
        super().create(request, *args, **kwargs)
        return Response({"id": self.donation_id}, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer: PaymentMethodAndFrequencySerializer) -> None:
        """
        Create donation object after payment method and frequency is correct.
        https://github.com/encode/django-rest-framework/blob/acbd9d8222e763c7f9c7dc2de23c430c702e06d4/rest_framework/mixins.py#L23-L24
        """
        # Get payment method from the serializer.
        self.payment_method = serializer.validated_data["payment_method"]

        # Try to create the donation entry in the Wagtail database.
        # If exception wasn't raised, assume it's created.
        donation = self.create_donation(serializer)

        # Set self.donation_id for use in self.create()
        self.donation_id = donation.pk

    def get_payment_method_serializer_class(
        self, *, payment_method: PaymentMethod, frequency: str, **kwargs
    ) -> Type[serializers.Serializer]:
        """
        Get serializer class for the given payment method and frequency.
        """
        return payment_method.get_serializer_class_for_frequency(frequency)

    def get_payment_method_serializer_context(
        self, *, frequency: str, **kwargs
    ) -> Dict[str, any]:
        """
        Extra context provided to the serializer class context.
        """
        return {
            **self.get_serializer_context(),
            "minimum_amount": self.get_minimum_amount_for_frequency(frequency),
            "maximum_amount": self.get_maximum_amount_for_frequency(frequency),
            **kwargs,
        }

    def get_payment_method_serializer(
        self, *args, payment_method: PaymentMethod, frequency: str, **kwargs
    ) -> serializers.Serializer:
        """
        Instantiate payment method serializer class.
        """
        serializer_class = self.get_payment_method_serializer_class(
            payment_method=payment_method, frequency=frequency
        )
        kwargs.setdefault(
            "context",
            self.get_payment_method_serializer_context(
                frequency=frequency, payment_method=payment_method, **kwargs
            ),
        )
        kwargs.pop("frequency", None)
        return serializer_class(*args, **kwargs)

    def create_donation(
        self, initial_serializer: PaymentMethodAndFrequencySerializer
    ) -> models.Model:
        """
        Call payment method serializer to validate and sanitise the input
        of the donation specific data; and create the donation object.
        """
        payment_serializer = self.get_payment_method_serializer(
            data=self.request.data, **initial_serializer.validated_data
        )
        payment_serializer.is_valid(raise_exception=True)
        donation = self.perform_create_donation(payment_serializer)
        self.perform_after_create_donation(donation)
        return donation

    def get_minimum_amount_for_frequency(self, frequency: str) -> Decimal:
        return Decimal(donate_settings.MINIMUM_AMOUNT_PER_FREQUENCY.get(frequency))

    def get_maximum_amount_for_frequency(self, frequency: str) -> Decimal:
        return Decimal(donate_settings.MAXIMUM_AMOUNT_PER_FREQUENCY.get(frequency))

    def perform_create_donation(
        self, payment_serializer: serializers.Serializer
    ) -> models.Model:
        """
        Save the donation object to the database.
        """
        return payment_serializer.save()

    def get_donation_page(self, donation: models.Model) -> Page:
        """
        Get donation page that is associated with the donation.
        """
        if donation.donation_page:
            return donation.donation_page.specific
        return get_default_donation_page().specific

    def perform_after_create_donation(self, donation: models.Model) -> None:
        """
        Additional tasks that happen after creating a donation.
        """
        self.prepare_request_for_thank_you_page(donation)
        self.send_thank_you_email(donation)

    def send_thank_you_email(self, donation: models.Model) -> None:
        donation_page = self.get_donation_page(donation)
        if hasattr(donation_page, "send_thank_you_email"):
            donation_page.send_thank_you_email(donation)

    def prepare_request_for_thank_you_page(self, donation: models.Model) -> None:
        donation_page = self.get_donation_page(donation)
        if hasattr(donation_page, "prepare_request_for_thank_you_page"):
            donation_page.prepare_request_for_thank_you_page(self.request, donation)

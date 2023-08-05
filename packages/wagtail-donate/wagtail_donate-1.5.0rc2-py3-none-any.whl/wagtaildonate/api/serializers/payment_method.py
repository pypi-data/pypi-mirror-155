from rest_framework import serializers

from wagtaildonate.exceptions import PaymentMethodNotFound
from wagtaildonate.payment_methods.base import PaymentMethod
from wagtaildonate.payment_methods.utils import get_payment_method


class PaymentMethodField(serializers.Field):
    """
    Retrieve payment method based on its code.
    """

    def __init__(self, *args, **kwargs):
        self.max_length = int(kwargs.pop("max_length", 255))
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data: str) -> PaymentMethod:
        if not isinstance(data, str):
            msg = "Incorrect type. Expected a string, but got %s."
            raise serializers.ValidationError(msg % type(data).__name__)

        if len(data) > self.max_length:
            raise serializers.ValidationError("String is too long.")
        try:
            payment_method_context = self.context.get("payment_method_context")
            payment_method = get_payment_method(data, payment_method_context)
        except PaymentMethodNotFound as e:
            raise serializers.ValidationError("Payment method not configured") from e

        return payment_method

    def to_representation(self, value: PaymentMethod) -> str:
        return value.code


class PaymentMethodAndFrequencySerializer(serializers.Serializer):
    """
    Validate payment method and frequency.
    """

    payment_method = PaymentMethodField()
    frequency = serializers.CharField(max_length=255)

    def validate(self, data):
        if not data["payment_method"].is_frequency_supported(data["frequency"]):
            raise serializers.ValidationError(
                {"frequency": ["The frequency is not supported by the payment method."]}
            )
        return data

from rest_framework import serializers

from wagtaildonate.api.serializers.utils import get_pay_in_event_serializer_class
from wagtaildonate.models.utils import get_pay_in_event_model


class CountrySerializer(serializers.Serializer):
    code = serializers.CharField(source="alpha_2")
    name = serializers.CharField()


class PaymentMethodSerializer(serializers.Serializer):
    code = serializers.CharField()
    options = serializers.JSONField(source="get_frontend_options")
    supported_frequencies = serializers.ReadOnlyField(
        source="get_supported_frequencies"
    )


class AddressLookupSerializer(serializers.Serializer):
    code = serializers.CharField()
    options = serializers.JSONField(source="get_frontend_options")


class PayInEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_pay_in_event_model()
        fields = [
            "event_code",
            "event_name",
            "fundraiser_reference_required",
        ]


class ConfigurationSerializer(serializers.Serializer):
    checkout_url = serializers.URLField()
    address_lookup = AddressLookupSerializer()
    payment_methods = PaymentMethodSerializer(many=True)
    countries = CountrySerializer(many=True)
    pay_in_events = get_pay_in_event_serializer_class()(many=True)
    pay_in_page_id = serializers.IntegerField()
    pay_in_success_url = serializers.URLField()

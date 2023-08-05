from typing import Any, ClassVar, Dict, List, Type

from rest_framework import serializers

from wagtaildonate.transaction_status import TransactionStatus

PaymentMethodOptions = Dict[str, Any]


class PaymentMethod:
    FREQUENCY_PAYIN = "payin"
    FREQUENCY_SINGLE = "single"
    FREQUENCY_MONTHLY = "monthly"
    code: ClassVar[str]
    assets: ClassVar[Dict[str, Any]] = None
    serializer_classes: ClassVar[Dict[str, Type[serializers.Serializer]]] = {}
    options: PaymentMethodOptions
    context: Dict[str, Any]

    def __init__(
        self, options: PaymentMethodOptions, *, context: Dict[str, Any] = None
    ):
        self.options = options
        self.context = context

        if self.context is None:
            self.context = {}

    def get_frontend_options(self) -> PaymentMethodOptions:
        return {}

    def get_transaction_status_for_transaction(
        self, transaction_id: str
    ) -> TransactionStatus:
        raise NotImplementedError(
            "get_transaction_status_for_transaction method is not implemented"
        )

    def get_assets(self) -> Dict[str, Any]:
        if self.assets is not None:
            return self.assets.copy()
        return {}

    def get_supported_frequencies(self) -> List[str]:
        return list(self.serializer_classes.keys())

    def is_frequency_supported(self, frequency: str) -> bool:
        return frequency in self.get_supported_frequencies()

    def get_serializer_class_for_frequency(
        self, frequency: str
    ) -> Type[serializers.Serializer]:
        return self.serializer_classes[frequency]

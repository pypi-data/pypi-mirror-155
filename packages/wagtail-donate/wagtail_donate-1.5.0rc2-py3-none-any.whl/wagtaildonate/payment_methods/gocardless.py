import logging

import gocardless_pro

from wagtaildonate.api.serializers.gocardless import GoCardlessDonationSerializer
from wagtaildonate.payment_methods.base import PaymentMethod

logger = logging.getLogger(__name__)


class GoCardlessPaymentMethod(PaymentMethod):
    code = "gocardless"
    serializer_classes = {
        "monthly": GoCardlessDonationSerializer,
    }

    def get_client(self):
        return gocardless_pro.Client(
            access_token=self.options["ACCESS_TOKEN"],
            environment=self.options.get("ENVIRONMENT", "live"),
        )

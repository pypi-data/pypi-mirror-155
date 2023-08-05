from typing import Optional

from django.core.exceptions import ImproperlyConfigured

import braintree

from wagtaildonate.api.serializers.braintree import (
    BraintreePayInSerializer,
    BraintreeSingleDonationSerializer,
)
from wagtaildonate.exceptions import TransactionNotFound
from wagtaildonate.payment_methods.base import PaymentMethod
from wagtaildonate.transaction_status import TransactionStatus
from wagtaildonate.utils.braintree import map_status


class BraintreeMixin:
    serializer_classes = {
        "single": BraintreeSingleDonationSerializer,
        "payin": BraintreePayInSerializer,
    }
    assets = {
        "js": [
            {"src": "https://js.braintreegateway.com/web/3.76.4/js/client.min.js"},
            {
                "src": "https://js.braintreegateway.com/web/3.76.4/js/data-collector.min.js"
            },
        ]
    }

    def get_frontend_options(self):
        return {
            "client_authorization": self.get_client_token(),
        }

    def get_config(self):
        merchant_id = self.options.get("MERCHANT_ID", None)
        public_key = self.options.get("PUBLIC_KEY", None)
        private_key = self.options.get("PRIVATE_KEY", None)

        if None in [merchant_id, public_key, private_key]:
            raise ImproperlyConfigured(
                "One or more of these options have not been defined: "
                "MERCHANT_ID, PUBLIC_KEY, PRIVATE_KEY"
            )
        if self.options.get("SANDBOX", False):
            environment = braintree.Environment.Sandbox
        else:
            environment = braintree.Environment.Production
        return merchant_id, public_key, private_key, environment

    def get_gateway(self):
        merchant_id, public_key, private_key, environment = self.get_config()
        return braintree.BraintreeGateway(
            braintree.Configuration(
                environment,
                merchant_id=merchant_id,
                public_key=public_key,
                private_key=private_key,
            )
        )

    def get_transaction_status_for_transaction(self, transaction_id, gateway=None):
        if gateway is None:
            gateway = self.get_gateway()
        try:
            transaction = gateway.transaction.find(transaction_id)
        except braintree.exceptions.not_found_error.NotFoundError as e:
            raise TransactionNotFound from e
        return TransactionStatus(
            provider_transaction_status=transaction.status,
            transaction_status=map_status(transaction.status),
        )

    def get_client_token(self):
        return self.get_gateway().client_token.generate(
            {"merchant_account_id": self.get_merchant_account_id()}
        )

    def get_merchant_account_id(self) -> Optional[str]:
        merchant_account_id = self.context.get("braintree_merchant_account_id")
        if merchant_account_id:
            return merchant_account_id

        return self.options.get("MERCHANT_ACCOUNT_ID")

    def should_send_postal_code(self) -> bool:
        return self.options.get("SEND_POSTAL_CODE", False)

    def should_send_country_code(self) -> bool:
        return self.options.get("SEND_COUNTRY_CODE", False)

    def should_send_street_address(self) -> bool:
        return self.options.get("SEND_STREET_ADDRESS", False)

    def should_send_name(self) -> bool:
        return self.options.get("SEND_NAME", False)

    def should_send_town(self) -> bool:
        return self.options.get("SEND_TOWN", False)

    def should_send_email_address(self) -> bool:
        return self.options.get("SEND_EMAIL_ADDRESS", False)

    def should_send_phone_number(self) -> bool:
        return self.options.get("SEND_PHONE_NUMBER", False)


class BraintreeCreditCardPaymentMethod(BraintreeMixin, PaymentMethod):
    code = "braintree_credit_card"
    assets = {
        **BraintreeMixin.assets,
        "js": BraintreeMixin.assets.get("js", [])
        + [
            {
                "src": "https://js.braintreegateway.com/web/3.76.4/js/hosted-fields.min.js"
            },
            {
                "src": "https://js.braintreegateway.com/web/3.76.4/js/three-d-secure.min.js"
            },
        ],
    }

    def get_frontend_options(self):
        return {
            **super().get_frontend_options(),
            "send_cardholder_name": self.options.get("SEND_CARDHOLDER_NAME", False),
            "send_billing_address": self.options.get("SEND_BILLING_ADDRESS", False),
            "three_d_secure_enabled": self.options.get("THREE_D_SECURE_ENABLED", False),
        }


class BraintreePayPalPaymentMethod(BraintreeMixin, PaymentMethod):
    code = "braintree_paypal"
    assets = {
        **BraintreeMixin.assets,
        "js": BraintreeMixin.assets.get("js", [])
        + [
            {"src": "https://www.paypalobjects.com/api/checkout.js"},
            {
                "src": "https://js.braintreegateway.com/web/3.76.4/js/paypal-checkout.min.js"
            },
        ],
    }

    def get_frontend_options(self):
        return {
            **super().get_frontend_options(),
            "sandbox": self.options.get("SANDBOX", False),
            "currency": self.options.get("CURRENCY", "USD"),
            "auto_fill_shipping_address": self.options.get(
                "AUTOFILL_SHIPPING_ADDRESS", False
            ),
            "auto_fill_phone_number": self.options.get("AUTOFILL_PHONE_NUMBER", False),
            "auto_fill_name": self.options.get("AUTOFILL_NAME", False),
            "auto_fill_email_address": self.options.get(
                "AUTOFILL_EMAIL_ADDRESS", False
            ),
            "locale": self.options.get("LOCALE"),
            "display_name": self.options.get("DISPLAY_NAME"),
            # PayPal checkout button settings
            # https://developer.paypal.com/docs/archive/checkout/how-to/customize-button/
            "tagline": self.options.get("BUTTON_TAGLINE"),
            "label": self.options.get("BUTTON_LABEL"),
            "size": self.options.get("BUTTON_SIZE"),
            "shape": self.options.get("BUTTON_SHAPE"),
            "height": self.options.get("BUTTON_HEIGHT"),
            "color": self.options.get("BUTTON_COLOR"),
        }


class BraintreeApplePayPaymentMethod(BraintreeMixin, PaymentMethod):
    code = "braintree_apple_pay"
    assets = {
        **BraintreeMixin.assets,
        "js": BraintreeMixin.assets.get("js", [])
        + [{"src": "https://js.braintreegateway.com/web/3.76.4/js/apple-pay.min.js"}],
    }

    def get_frontend_options(self):
        return {
            **super().get_frontend_options(),
            "auto_fill_billing_address": self.options.get(
                "AUTOFILL_BILLING_ADDRESS", False
            ),
            "auto_fill_phone_number": self.options.get("AUTOFILL_PHONE_NUMBER", False),
            "auto_fill_name": self.options.get("AUTOFILL_NAME", False),
            "auto_fill_email_address": self.options.get(
                "AUTOFILL_EMAIL_ADDRESS", False
            ),
            "display_name": self.options.get("DISPLAY_NAME", "Donations"),
            "line_item_label": self.options.get("LINE_ITEM_LABEL", "Donation"),
        }


class BraintreeGooglePayPaymentMethod(BraintreeMixin, PaymentMethod):
    code = "braintree_google_pay"
    assets = {
        **BraintreeMixin.assets,
        "js": BraintreeMixin.assets.get("js", [])
        + [
            {"src": "https://pay.google.com/gp/p/js/pay.js"},
            {
                "src": "https://js.braintreegateway.com/web/3.76.4/js/google-payment.min.js"
            },
        ],
    }

    def get_frontend_options(self):
        return {
            **super().get_frontend_options(),
            "sandbox": self.options.get("SANDBOX", False),
            "currency": self.options.get("CURRENCY", "USD"),
            "google_merchant_id": self.options.get("GOOGLE_MERCHANT_ID"),
            "auto_fill_billing_address": self.options.get(
                "AUTOFILL_BILLING_ADDRESS", False
            ),
            "auto_fill_phone_number": self.options.get("AUTOFILL_PHONE_NUMBER", False),
            "auto_fill_name": self.options.get("AUTOFILL_NAME", False),
            "auto_fill_email_address": self.options.get(
                "AUTOFILL_EMAIL_ADDRESS", False
            ),
            # Google Pay button settings
            # https://developers.google.com/pay/api/web/reference/request-objects#ButtonOptions
            "button_type": self.options.get("BUTTON_TYPE"),
            "button_color": self.options.get("BUTTON_COLOR"),
        }

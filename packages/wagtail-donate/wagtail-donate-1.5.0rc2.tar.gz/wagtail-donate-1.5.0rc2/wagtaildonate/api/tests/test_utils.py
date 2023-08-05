from django.test import TestCase, override_settings


@override_settings(
    WAGTAIL_DONATE={
        "BRAINTREE_SANDBOX": True,
        "BRAINTREE_PUBLIC_KEY": "mock-public-key",
        "BRAINTREE_PRIVATE_KEY": "mock-private-key",
        "BRAINTREE_MERCHANT_ID": "mock-merchan-it",
    }
)
class TestBraintreeUtils(TestCase):
    def test_get_config(self):
        pass

    def test_get_gateway(self):
        pass

    def test_get_client_token(self):
        pass

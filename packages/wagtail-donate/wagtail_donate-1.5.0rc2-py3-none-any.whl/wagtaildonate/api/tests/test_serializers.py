from decimal import Decimal

from django.test import TestCase, override_settings

import rest_framework

from wagtaildonate.api.serializers.braintree import BraintreeSingleDonationSerializer
from wagtaildonate.api.serializers.donations import (
    PayInSerializer,
    RecurringDonationSerializer,
    SingleDonationSerializer,
)
from wagtaildonate.api.serializers.payment_method import (
    PaymentMethodAndFrequencySerializer,
)
from wagtaildonate.models import PayIn, PayInEvent, RecurringDonation, SingleDonation


@override_settings(
    WAGTAIL_DONATE={
        "PAYMENT_METHODS": [
            {
                "class": "wagtaildonate.payment_methods.braintree.BraintreePayPalPaymentMethod",
                "options": {
                    "SANDBOX": True,
                    "MERCHANT_ID": "--------------",
                    "MERCHANT_ACCOUNT_ID": "---",
                    "PUBLIC_KEY": "---",
                    "PRIVATE_KEY": "----",
                    "CURRENCY": "GBP",
                    "BUTTON_TAGLINE": "false",
                    "BUTTON_LABEL": "paypal",
                    "BUTTON_SIZE": "responsive",
                    "BUTTON_HEIGHT": 50,
                    "BUTTON_SHAPE": "rect",
                    "AUTOFILL_SHIPPING_ADDRESS": True,
                    "AUTOFILL_PHONE_NUMBER": True,
                    "AUTOFILL_NAME": True,
                    "AUTOFILL_EMAIL_ADDRESS": True,
                    "DISPLAY_NAME": "Wagtail Donate",
                    "LOCALE": "en_GB",
                },
            },
        ],
    }
)
class TestPaymentMethodAndFrequencySerializer(TestCase):
    def test_payment_method_required(self):
        with self.assertRaises(rest_framework.exceptions.ValidationError) as cm:
            PaymentMethodAndFrequencySerializer(data={}).is_valid(raise_exception=True)
        detail = cm.exception.detail
        self.assertIn("payment_method", detail)
        self.assertTrue(len(detail["payment_method"]), 1)
        self.assertEqual(detail["payment_method"][0].code, "required")

    def test_frequency_required(self):
        with self.assertRaises(rest_framework.exceptions.ValidationError) as cm:
            PaymentMethodAndFrequencySerializer(data={}).is_valid(raise_exception=True)
        detail = cm.exception.detail
        self.assertIn("frequency", detail)
        self.assertTrue(len(detail["frequency"]), 1)
        self.assertEqual(detail["frequency"][0].code, "required")

    def test_invalid_payment_method_not_accepted(self):
        with self.assertRaises(rest_framework.exceptions.ValidationError) as cm:
            PaymentMethodAndFrequencySerializer(
                data={"payment_method": "some_payment_method", "frequency": "single"}
            ).is_valid(raise_exception=True)
        detail = cm.exception.detail
        self.assertIn("payment_method", detail)
        self.assertTrue(len(detail["payment_method"]), 1)
        self.assertEqual(detail["payment_method"][0].code, "invalid")

    def test_valid_payment_method_and_frequency_accepted(self):
        from wagtaildonate.payment_methods.braintree import BraintreePayPalPaymentMethod

        serializer = PaymentMethodAndFrequencySerializer(
            data={"payment_method": "braintree_paypal", "frequency": "single"}
        )
        serializer.is_valid(raise_exception=True)
        self.assertIsInstance(
            serializer.validated_data["payment_method"], BraintreePayPalPaymentMethod
        )

    def test_valid_payment_method_and_invalid_frequency_not_accepted(self):
        with self.assertRaises(rest_framework.exceptions.ValidationError) as cm:
            serializer = PaymentMethodAndFrequencySerializer(
                data={"payment_method": "braintree_paypal", "frequency": "monthly"}
            )
            serializer.is_valid(raise_exception=True)
        detail = cm.exception.detail
        self.assertIn("frequency", detail)
        self.assertTrue(len(detail["frequency"]), 1)
        self.assertEqual(detail["frequency"][0].code, "invalid")
        self.assertEqual(
            str(detail["frequency"][0]),
            "The frequency is not supported by the payment method.",
        )


class TestSingleDonationSerializer(TestCase):
    def test_amount_required(self):
        """Assert that the amount field is required"""
        with self.assertRaises(rest_framework.exceptions.ValidationError) as cm:
            SingleDonationSerializer(data={}).is_valid(raise_exception=True)
        detail = cm.exception.detail
        self.assertIn("amount", detail)
        self.assertTrue(len(detail["amount"]), 1)
        self.assertEqual(detail["amount"][0].code, "required")

    def test_payment_method_required(self):
        with self.assertRaises(rest_framework.exceptions.ValidationError) as cm:
            SingleDonationSerializer(data={}).is_valid(raise_exception=True)
        detail = cm.exception.detail
        self.assertIn("payment_method", detail)
        self.assertTrue(len(detail["payment_method"]), 1)
        self.assertEqual(detail["payment_method"][0].code, "required")

    def test_phone_invalid_not_accepted(self):
        """Assert that invalid phone numbers are not accepted"""
        with self.assertRaises(rest_framework.exceptions.ValidationError) as cm:
            SingleDonationSerializer(
                data={"phone_number": "i am not a phone number"}
            ).is_valid(raise_exception=True)
        detail = cm.exception.detail
        self.assertIn("phone_number", detail)
        self.assertTrue(len(detail["phone_number"]), 1)
        self.assertEqual(detail["phone_number"][0].code, "invalid")

    def test_phone_international_accepted(self):
        """
        Assert that a valid international phone number does not
        raise any validation errors regarding the phone number.
        """
        with self.assertRaises(rest_framework.exceptions.ValidationError) as cm:
            SingleDonationSerializer(
                data={"phone_number": "+44 7771234567"}  # Fake international UK number
            ).is_valid(raise_exception=True)
        self.assertNotIn("phone_number", cm.exception.detail)

    @override_settings(PHONENUMBER_DEFAULT_REGION="GB")
    def test_phone_national_accepted(self):
        """
        Assert that a valid national phone number does not
        raise any validation errors regarding the phone number.
        """
        with self.assertRaises(rest_framework.exceptions.ValidationError) as cm:
            SingleDonationSerializer(
                data={"phone_number": "07771234567"}  # Fake national UK number
            ).is_valid(raise_exception=True)
        self.assertNotIn("phone_number", cm.exception.detail)

    def test_create_no_giftaid(self):
        """Assert that a Donation can be created from a serializer"""
        serializer = SingleDonationSerializer(
            data={
                "payment_method": "dummy_payment_method",
                "transaction_id": "test_id",
                "amount": 50,
                "first_name": "Alice",
                "surname": "Johnson",
                "email": "ajohnson@example.com",
                "phone_number": "+44 7771234567",  # Fake international UK number
                "address_line_1": "2nd floor",
                "address_line_2": "123 Test Street",
                "town": "Test Town",
                "postal_code": "TST1 1AB",
                "country": "GB",
                "on_behalf_of_organisation": False,
                "gift_aid_declaration": False,
                "in_memory": False,
                "in_memory_of": "",
            }
        )
        self.assertTrue(serializer.is_valid(raise_exception=True))
        donation = serializer.save()
        self.assertTrue(SingleDonation.objects.filter(id=donation.id).exists())

    def test_default_minimum_amount_fails(self):
        serializer = SingleDonationSerializer(
            data={
                "payment_method": "dummy_payment_method",
                "transaction_id": "test_id",
                "amount": "0.99",
                "first_name": "Alice",
                "surname": "Johnson",
                "email": "ajohnson@example.com",
                "phone_number": "+44 7771234567",  # Fake international UK number
                "address_line_1": "2nd floor",
                "address_line_2": "123 Test Street",
                "town": "Test Town",
                "postal_code": "TST1 1AB",
                "country": "GB",
                "on_behalf_of_organisation": False,
                "gift_aid_declaration": False,
                "in_memory": False,
                "in_memory_of": "",
            }
        )
        with self.assertRaises(rest_framework.exceptions.ValidationError) as cm:
            serializer.is_valid(raise_exception=True)
        detail = cm.exception.detail
        self.assertIn("amount", detail)
        self.assertTrue(len(detail["amount"]), 1)
        self.assertEqual(detail["amount"][0].code, "invalid")
        self.assertEqual(str(detail["amount"][0]), "Minimum amount is 1.00.")

    def test_default_minimum_amount_passes(self):
        serializer = SingleDonationSerializer(
            data={
                "payment_method": "dummy_payment_method",
                "transaction_id": "test_id",
                "amount": "1.00",
                "first_name": "Alice",
                "surname": "Johnson",
                "email": "ajohnson@example.com",
                "phone_number": "+44 7771234567",  # Fake international UK number
                "address_line_1": "2nd floor",
                "address_line_2": "123 Test Street",
                "town": "Test Town",
                "postal_code": "TST1 1AB",
                "country": "GB",
                "on_behalf_of_organisation": False,
                "gift_aid_declaration": False,
                "in_memory": False,
                "in_memory_of": "",
            }
        )
        serializer.is_valid(raise_exception=True)
        donation = serializer.save()
        self.assertEqual(donation.amount, Decimal("1.00"))

    def test_default_maximum_amount_fails(self):
        serializer = SingleDonationSerializer(
            data={
                "payment_method": "dummy_payment_method",
                "transaction_id": "test_id",
                "amount": "10000.01",
                "first_name": "Alice",
                "surname": "Johnson",
                "email": "ajohnson@example.com",
                "phone_number": "+44 7771234567",  # Fake international UK number
                "address_line_1": "2nd floor",
                "address_line_2": "123 Test Street",
                "town": "Test Town",
                "postal_code": "TST1 1AB",
                "country": "GB",
                "on_behalf_of_organisation": False,
                "gift_aid_declaration": False,
                "in_memory": False,
                "in_memory_of": "",
            }
        )
        with self.assertRaises(rest_framework.exceptions.ValidationError) as cm:
            serializer.is_valid(raise_exception=True)
        detail = cm.exception.detail
        self.assertIn("amount", detail)
        self.assertTrue(len(detail["amount"]), 1)
        self.assertEqual(detail["amount"][0].code, "invalid")
        self.assertEqual(str(detail["amount"][0]), "Maximum amount is 10000.00.")

    def test_default_maximum_amount_passes(self):
        serializer = SingleDonationSerializer(
            data={
                "payment_method": "dummy_payment_method",
                "transaction_id": "test_id",
                "amount": "10000.00",
                "first_name": "Alice",
                "surname": "Johnson",
                "email": "ajohnson@example.com",
                "phone_number": "+44 7771234567",  # Fake international UK number
                "address_line_1": "2nd floor",
                "address_line_2": "123 Test Street",
                "town": "Test Town",
                "postal_code": "TST1 1AB",
                "country": "GB",
                "on_behalf_of_organisation": False,
                "gift_aid_declaration": False,
                "in_memory": False,
                "in_memory_of": "",
            }
        )
        serializer.is_valid(raise_exception=True)
        donation = serializer.save()
        self.assertEqual(donation.amount, Decimal("10000.00"))

    def test_custom_minimum_amount_fails(self):
        serializer = SingleDonationSerializer(
            context={"minimum_amount": Decimal("1.50")},
            data={
                "payment_method": "dummy_payment_method",
                "transaction_id": "test_id",
                "amount": "1.49",
                "first_name": "Alice",
                "surname": "Johnson",
                "email": "ajohnson@example.com",
                "phone_number": "+44 7771234567",  # Fake international UK number
                "address_line_1": "2nd floor",
                "address_line_2": "123 Test Street",
                "town": "Test Town",
                "postal_code": "TST1 1AB",
                "country": "GB",
                "on_behalf_of_organisation": False,
                "gift_aid_declaration": False,
                "in_memory": False,
                "in_memory_of": "",
            },
        )
        with self.assertRaises(rest_framework.exceptions.ValidationError) as cm:
            serializer.is_valid(raise_exception=True)
        detail = cm.exception.detail
        self.assertIn("amount", detail)
        self.assertTrue(len(detail["amount"]), 1)
        self.assertEqual(detail["amount"][0].code, "invalid")
        self.assertEqual(str(detail["amount"][0]), "Minimum amount is 1.50.")

    def test_custom_maximum_amount_fails(self):
        serializer = SingleDonationSerializer(
            context={"maximum_amount": Decimal("3.05")},
            data={
                "payment_method": "dummy_payment_method",
                "transaction_id": "test_id",
                "amount": "3.06",
                "first_name": "Alice",
                "surname": "Johnson",
                "email": "ajohnson@example.com",
                "phone_number": "+44 7771234567",  # Fake international UK number
                "address_line_1": "2nd floor",
                "address_line_2": "123 Test Street",
                "town": "Test Town",
                "postal_code": "TST1 1AB",
                "country": "GB",
                "on_behalf_of_organisation": False,
                "gift_aid_declaration": False,
                "in_memory": False,
                "in_memory_of": "",
            },
        )
        with self.assertRaises(rest_framework.exceptions.ValidationError) as cm:
            serializer.is_valid(raise_exception=True)
        detail = cm.exception.detail
        self.assertIn("amount", detail)
        self.assertTrue(len(detail["amount"]), 1)
        self.assertEqual(detail["amount"][0].code, "invalid")
        self.assertEqual(str(detail["amount"][0]), "Maximum amount is 3.05.")


class TestBraintreeSingleDonationSerializer(TestCase):
    def test_payment_method_nonce_requred(self):
        with self.assertRaises(rest_framework.exceptions.ValidationError) as cm:
            BraintreeSingleDonationSerializer(data={}).is_valid(raise_exception=True)
        detail = cm.exception.detail
        self.assertIn("payment_method_nonce", detail)
        self.assertTrue(len(detail["payment_method_nonce"]), 1)
        self.assertEqual(detail["payment_method_nonce"][0].code, "required")

    def test_amount_required(self):
        with self.assertRaises(rest_framework.exceptions.ValidationError) as cm:
            BraintreeSingleDonationSerializer(data={}).is_valid(raise_exception=True)
        detail = cm.exception.detail
        self.assertIn("amount", detail)
        self.assertTrue(len(detail["amount"]), 1)
        self.assertEqual(detail["amount"][0].code, "required")


class TestRecurringDonationSerializer(TestCase):
    def test_payment_method_required(self):
        with self.assertRaises(rest_framework.exceptions.ValidationError) as cm:
            SingleDonationSerializer(data={}).is_valid(raise_exception=True)
        detail = cm.exception.detail
        self.assertIn("payment_method", detail)
        self.assertTrue(len(detail["payment_method"]), 1)
        self.assertEqual(detail["payment_method"][0].code, "required")

    def test_amount_required(self):
        """Assert that the amount field is required"""
        with self.assertRaises(rest_framework.exceptions.ValidationError) as cm:
            RecurringDonationSerializer(data={}).is_valid(raise_exception=True)
        detail = cm.exception.detail
        self.assertIn("amount", detail)
        self.assertTrue(len(detail["amount"]), 1)
        self.assertEqual(detail["amount"][0].code, "required")

    def test_frequency_required(self):
        """Assert that the frequency field is required"""
        with self.assertRaises(rest_framework.exceptions.ValidationError) as cm:
            RecurringDonationSerializer(data={}).is_valid(raise_exception=True)
        detail = cm.exception.detail
        self.assertIn("frequency", detail)
        self.assertTrue(len(detail["frequency"]), 1)
        self.assertEqual(detail["frequency"][0].code, "required")

    def test_phone_invalid_not_accepted(self):
        """Assert that invalid phone numbers are not accepted"""
        with self.assertRaises(rest_framework.exceptions.ValidationError) as cm:
            RecurringDonationSerializer(
                data={"phone_number": "i am not a phone number"}
            ).is_valid(raise_exception=True)
        detail = cm.exception.detail
        self.assertIn("phone_number", detail)
        self.assertTrue(len(detail["phone_number"]), 1)
        self.assertEqual(detail["phone_number"][0].code, "invalid")

    def test_phone_international_accepted(self):
        """
        Assert that a valid international phone number does not
        raise any validation errors regarding the phone number.
        """
        with self.assertRaises(rest_framework.exceptions.ValidationError) as cm:
            RecurringDonationSerializer(
                data={"phone_number": "+44 7771234567"}  # Fake international UK number
            ).is_valid(raise_exception=True)
        self.assertNotIn("phone_number", cm.exception.detail)

    @override_settings(PHONENUMBER_DEFAULT_REGION="GB")
    def test_phone_national_accepted(self):
        """
        Assert that a valid national phone number does not
        raise any validation errors regarding the phone number.
        """
        with self.assertRaises(rest_framework.exceptions.ValidationError) as cm:
            RecurringDonationSerializer(
                data={"phone_number": "07771234567"}  # Fake national UK number
            ).is_valid(raise_exception=True)
        self.assertNotIn("phone_number", cm.exception.detail)

    def test_create_no_giftaid(self):
        """Assert that a Donation can be created from a serializer"""
        serializer = RecurringDonationSerializer(
            data={
                "payment_method": "dummy_payment_method",
                "transaction_id": "test_id",
                "amount": 50,
                "frequency": "monthly",
                "first_name": "Alice",
                "surname": "Johnson",
                "email": "ajohnson@example.com",
                "phone_number": "+44 7771234567",  # Fake international UK number
                "address_line_1": "2nd floor",
                "address_line_2": "123 Test Street",
                "town": "Test Town",
                "postal_code": "TST1 1AB",
                "country": "GB",
                "on_behalf_of_organisation": False,
                "gift_aid_declaration": False,
                "in_memory": False,
                "in_memory_of": "",
            }
        )
        self.assertTrue(serializer.is_valid(raise_exception=True))
        donation = serializer.save()
        self.assertTrue(RecurringDonation.objects.filter(id=donation.id).exists())


base_pay_in_data = {
    "payment_method": "dummy_payment_method",
    "transaction_id": "test_id",
    "amount": 50,
    "frequency": "single",
    "first_name": "Alice",
    "surname": "Johnson",
    "email": "ajohnson@example.com",
    "phone_number": "+44 7771234567",  # Fake international UK number
    "address_line_1": "2nd floor",
    "address_line_2": "123 Test Street",
    "town": "Test Town",
    "postal_code": "TST1 1AB",
    "country": "GB",
    "on_behalf_of_organisation": False,
    "in_memory": False,
    "in_memory_of": "",
}


class TestPayInSerializer(TestCase):
    def setUp(self):
        self.pay_in_event_1 = PayInEvent.objects.create(
            event_code="evt1",
            event_name="Event 1",
            fundraiser_reference_required=False,
        )
        self.pay_in_event_2 = PayInEvent.objects.create(
            event_code="evt2",
            event_name="Event 2",
            fundraiser_reference_required=True,
        )

    @override_settings(WAGTAIL_DONATE={"PAY_IN_EVENTS_ENABLED": False})
    def test_create_with_pay_in_events_disabled(self):
        serializer = PayInSerializer(data=base_pay_in_data)
        self.assertTrue(serializer.is_valid(raise_exception=True))
        donation = serializer.save()
        self.assertTrue(PayIn.objects.filter(id=donation.id).exists())

    def test_create_with_pay_in_event_doesnt_require_urn(self):
        serializer = PayInSerializer(
            data={
                **base_pay_in_data,
                "event_code": self.pay_in_event_1.event_code,
                "event_name": self.pay_in_event_1.event_name,
            }
        )
        self.assertTrue(serializer.is_valid(raise_exception=True))
        donation = serializer.save()
        self.assertTrue(PayIn.objects.filter(id=donation.id).exists())
        self.assertEqual(donation.event_code, self.pay_in_event_1.event_code)

    def test_create_with_pay_in_event_requires_fundraiser_reference(self):
        # create should fail if fundraiser reference is not provided
        serializer = PayInSerializer(
            data={
                **base_pay_in_data,
                "event_code": self.pay_in_event_2.event_code,
                "event_name": self.pay_in_event_2.event_name,
            }
        )
        with self.assertRaises(rest_framework.exceptions.ValidationError) as cm:
            serializer.is_valid(raise_exception=True)
        detail = cm.exception.detail
        self.assertIn("fundraiser_reference", detail)
        self.assertEqual(
            str(detail["fundraiser_reference"][0]),
            "Fundraiser reference must be entered.",
        )

        # create should succeed and donation created if fundraiser reference is provided
        serializer = PayInSerializer(
            data={
                **base_pay_in_data,
                "event_code": self.pay_in_event_2.event_code,
                "event_name": self.pay_in_event_2.event_name,
                "fundraiser_reference": "abcd1234",
            }
        )
        self.assertTrue(serializer.is_valid(raise_exception=True))
        donation = serializer.save()
        self.assertTrue(PayIn.objects.filter(id=donation.id).exists())
        self.assertEqual(donation.event_code, self.pay_in_event_2.event_code)

    @override_settings(
        WAGTAIL_DONATE={"PAY_IN_OTHER_EVENT_REQUIRE_FUNDRAISER_REFERENCE": False}
    )
    def test_create_with_other_pay_in_event_doesnt_require_fundraiser_reference(self):
        serializer = PayInSerializer(
            data={**base_pay_in_data, "event_code": "other", "event_name": "test name"}
        )
        self.assertTrue(serializer.is_valid(raise_exception=True))
        donation = serializer.save()
        self.assertTrue(PayIn.objects.filter(id=donation.id).exists())
        self.assertEqual(donation.event_code, "other")

    def test_create_with_other_pay_in_event_requires_fundraiser_reference(self):
        # create should fail if fundraiser reference is not provided
        serializer = PayInSerializer(
            data={**base_pay_in_data, "event_code": "other", "event_name": "test name"}
        )
        with self.assertRaises(rest_framework.exceptions.ValidationError) as cm:
            serializer.is_valid(raise_exception=True)
        detail = cm.exception.detail
        self.assertIn("fundraiser_reference", detail)
        self.assertEqual(
            str(detail["fundraiser_reference"][0]),
            "Fundraiser reference must be entered.",
        )

        # create should succeed and donation created if fundraiser reference is provided
        serializer = PayInSerializer(
            data={
                **base_pay_in_data,
                "event_code": "other",
                "event_name": "test name",
                "fundraiser_reference": "abcd1234",
            }
        )
        self.assertTrue(serializer.is_valid(raise_exception=True))
        donation = serializer.save()
        self.assertTrue(PayIn.objects.filter(id=donation.id).exists())
        self.assertEqual(donation.event_code, "other")

    def test_create_with_invalid_pay_in_event(self):
        serializer = PayInSerializer(
            data={**base_pay_in_data, "event_code": "invalid_event_code"}
        )
        with self.assertRaises(rest_framework.exceptions.ValidationError) as cm:
            serializer.is_valid(raise_exception=True)
        detail = cm.exception.detail
        self.assertIn("event_code", detail)
        self.assertEqual(
            str(detail["event_code"][0]),
            "Pay-in event does not exist. Please select a valid event.",
        )

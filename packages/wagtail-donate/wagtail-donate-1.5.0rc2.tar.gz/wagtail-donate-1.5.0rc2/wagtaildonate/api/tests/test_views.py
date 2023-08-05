from django.test import TestCase, override_settings
from django.urls import reverse

from wagtail import VERSION as WAGTAIL_VERSION

from wagtaildonate.factories import (
    DonationFundraisingPayInPageFactory,
    DonationPageFactory,
)
from wagtaildonate.models import PayInEvent

if WAGTAIL_VERSION >= (3, 0):
    from wagtail.models import Page, Site
else:
    from wagtail.core.models import Page, Site


class TestDonationConfigurationAPIView(TestCase):
    def setUp(self):
        root_page = Page.objects.get(id=1)
        Site.objects.create(hostname="test", port=80, root_page=root_page)
        self.donation_page = DonationPageFactory()
        self.pay_in_page = DonationFundraisingPayInPageFactory()
        PayInEvent.objects.create(
            event_code="evt1",
            event_name="Event 1",
            fundraiser_reference_required=True,
        )

    def test_pay_in_page_detail_in_response(self):
        response = self.client.get(reverse("wagtaildonate:api:configuration-donations"))
        self.assertEqual(response.status_code, 200)
        configuration_data = response.json()
        self.assertEqual(
            configuration_data["pay_in_page_id"],
            self.pay_in_page.id,
        )
        self.assertEqual(
            configuration_data["pay_in_success_url"],
            self.pay_in_page.get_thank_you_page_url(),
        )

    @override_settings(WAGTAIL_DONATE={"PAY_IN_EVENTS_ENABLED": False})
    def test_no_pay_in_events_when_disabled(self):
        response = self.client.get(reverse("wagtaildonate:api:configuration-donations"))
        self.assertEqual(response.status_code, 200)
        configuration_data = response.json()
        self.assertEqual(len(configuration_data["pay_in_events"]), 0)

    def test_correct_pay_in_events_other_event_enabled(self):
        response = self.client.get(reverse("wagtaildonate:api:configuration-donations"))
        self.assertEqual(response.status_code, 200)
        configuration_data = response.json()
        self.assertEqual(len(configuration_data["pay_in_events"]), 2)
        self.assertEqual(configuration_data["pay_in_events"][0]["event_code"], "evt1")
        self.assertEqual(configuration_data["pay_in_events"][1]["event_code"], "other")

    @override_settings(WAGTAIL_DONATE={"PAY_IN_OTHER_EVENT_ENABLED": False})
    def test_correct_pay_in_events_other_event_disabled(self):
        response = self.client.get(reverse("wagtaildonate:api:configuration-donations"))
        self.assertEqual(response.status_code, 200)
        configuration_data = response.json()
        self.assertEqual(len(configuration_data["pay_in_events"]), 1)
        self.assertEqual(configuration_data["pay_in_events"][0]["event_code"], "evt1")

    def test_correct_other_event_fundraiser_reference_required_enabled(self):
        response = self.client.get(reverse("wagtaildonate:api:configuration-donations"))
        self.assertEqual(response.status_code, 200)
        configuration_data = response.json()
        self.assertEqual(len(configuration_data["pay_in_events"]), 2)
        self.assertEqual(configuration_data["pay_in_events"][1]["event_code"], "other")
        self.assertTrue(
            configuration_data["pay_in_events"][1]["fundraiser_reference_required"]
        )

    @override_settings(
        WAGTAIL_DONATE={"PAY_IN_OTHER_EVENT_REQUIRE_FUNDRAISER_REFERENCE": False}
    )
    def test_correct_other_event_fundraiser_reference_required_disabled(self):
        response = self.client.get(reverse("wagtaildonate:api:configuration-donations"))
        self.assertEqual(response.status_code, 200)
        configuration_data = response.json()
        self.assertEqual(len(configuration_data["pay_in_events"]), 2)
        self.assertEqual(configuration_data["pay_in_events"][1]["event_code"], "other")
        self.assertFalse(
            configuration_data["pay_in_events"][1]["fundraiser_reference_required"]
        )

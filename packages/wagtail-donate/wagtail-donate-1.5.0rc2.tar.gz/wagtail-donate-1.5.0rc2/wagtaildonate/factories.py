import string
from decimal import Decimal

from wagtail import VERSION as WAGTAIL_VERSION

import factory
import factory.django
import factory.fuzzy

from wagtaildonate.models import SingleDonation
from wagtaildonate.tests.testapp.models import (
    TestDonationCampaignPage,
    TestDonationFundraisingPayInPage,
    TestDonationPage,
)

if WAGTAIL_VERSION >= (3, 0):
    from wagtail.models import Page
else:
    from wagtail.core.models import Page


class DonationPageFactory(factory.django.DjangoModelFactory):
    title = factory.Sequence(lambda n: "donation_page_%d" % n)
    slug = factory.Sequence(lambda n: "donation_page_%d" % n)
    thank_you_email_subject = ""
    thank_you_email_content = ""

    class Meta:
        model = TestDonationPage

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        root_page = Page.objects.all().order_by("depth").first()
        donation_page = model_class(*args, **kwargs)
        root_page.add_child(instance=donation_page)
        donation_page.save()
        return donation_page


class DonationCampaignPageFactory(factory.django.DjangoModelFactory):
    title = factory.Sequence(lambda n: "donation_campaign_page_%d" % n)
    slug = factory.Sequence(lambda n: "donation_campaign_page_%d" % n)
    thank_you_email_subject = ""
    thank_you_email_content = ""

    class Meta:
        model = TestDonationCampaignPage

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        root_page = Page.objects.all().order_by("depth").first()
        donation_campaign_page = model_class(*args, **kwargs)
        root_page.add_child(instance=donation_campaign_page)
        donation_campaign_page.save()
        return donation_campaign_page


class DonationFundraisingPayInPageFactory(factory.django.DjangoModelFactory):
    title = factory.Sequence(lambda n: "donation_campaign_page_%d" % n)
    slug = factory.Sequence(lambda n: "donation_campaign_page_%d" % n)
    thank_you_email_subject = ""
    thank_you_email_content = ""

    class Meta:
        model = TestDonationFundraisingPayInPage

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        root_page = Page.objects.all().order_by("depth").first()
        donation_fundraising_pay_in_page = model_class(*args, **kwargs)
        root_page.add_child(instance=donation_fundraising_pay_in_page)
        donation_fundraising_pay_in_page.save()
        return donation_fundraising_pay_in_page


class DonationFactory(factory.django.DjangoModelFactory):
    transaction_id = factory.fuzzy.FuzzyText(
        length=6, chars=string.digits + string.ascii_letters
    )
    transaction_status = ""
    amount = Decimal(10.00)

    first_name = factory.Faker("first_name", locale="en_GB")
    surname = factory.Faker("last_name", locale="en_GB")
    email = factory.Faker("safe_email", locale="en_GB")
    phone_number = factory.Faker("phone_number", locale="en_GB")

    address_line_1 = factory.Faker("secondary_address", locale="en_GB")
    address_line_2 = factory.Faker("street_address", locale="en_GB")
    town = factory.Faker("city", locale="en_GB")
    postal_code = factory.Faker("postcode", locale="en_GB")
    country = "GB"

    on_behalf_of_organisation = False
    gift_aid_declaration = False
    in_memory = False

    class Meta:
        model = SingleDonation

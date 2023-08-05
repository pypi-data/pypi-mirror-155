from decimal import Decimal
from typing import ClassVar, List, Optional
from urllib.parse import urlsplit, urlunsplit

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from django.http import Http404, HttpResponse, HttpResponseRedirect, QueryDict
from django.urls import reverse
from django.views.generic.base import TemplateView

from wagtail import VERSION as WAGTAIL_VERSION

from wagtaildonate.models import AbstractDonationLandingPage, AbstractPayInLandingPage
from wagtaildonate.models.utils import get_default_donation_page
from wagtaildonate.payment_methods.base import PaymentMethod
from wagtaildonate.settings import donate_settings

if WAGTAIL_VERSION >= (3, 0):
    from wagtail.models import Page
else:
    from wagtail.core.models import Page


CAMPAIGN_PAGE_ID_PARAM = "campaign"


class AmountForm(forms.Form):
    amount = forms.DecimalField(decimal_places=2)


class FrequencyForm(forms.Form):
    frequency = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        allowed_frequencies = kwargs.pop("allowed_frequencies")
        default_frequency = kwargs.pop("default_frequency", None)
        super().__init__(*args, **kwargs)
        self.fields["frequency"].choices = [
            [value] * 2 for value in allowed_frequencies
        ]
        if default_frequency:
            self.fields["frequency"].initial = default_frequency
            self.fields["frequency"].required = False

    def clean_frequency(self):
        """
        If no frequency provided but the default is set, return the default one.
        """
        data = self.cleaned_data["frequency"]
        initial = self["frequency"].initial
        if not data and initial:
            return initial
        return data


class CampaignPageForm(forms.Form):
    def __init__(self, *args, **kwargs):
        queryset = kwargs.pop("queryset")
        super().__init__(*args, **kwargs)
        self.fields[CAMPAIGN_PAGE_ID_PARAM] = forms.ModelChoiceField(queryset=queryset)


class BaseCheckoutView(TemplateView):
    campaign_page: Optional[Page]
    amount: Optional[int]
    frequency: Optional[str]
    allowed_frequencies: ClassVar[List[str]] = []

    def __init__(self, *args, **kwargs):
        self.campaign_page = None
        self.amount = None
        self.frequency = None
        super().__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        campaign_page_response = self.validate_campaign_page()
        if campaign_page_response is not None:
            return campaign_page_response

        frequency_response = self.validate_frequency()
        if frequency_response is not None:
            return frequency_response

        amount_response = self.validate_amount()
        if amount_response is not None:
            return amount_response

        return super().dispatch(request, *args, **kwargs)

    def get_allowed_frequencies(self) -> List[str]:
        return self.allowed_frequencies.copy()

    def get_default_frequency(self) -> Optional[str]:
        allowed_frequencies = tuple(self.get_allowed_frequencies())
        if len(allowed_frequencies) == 1:
            return allowed_frequencies[0]
        return

    def get_campaign_page_queryset(self) -> QuerySet:
        return Page.objects.live().public().specific()

    def amount_within_allowed_range(self, amount) -> bool:
        minimum_amount = Decimal(
            donate_settings.MINIMUM_AMOUNT_PER_FREQUENCY.get(self.frequency)
        )
        maximum_amount = Decimal(
            donate_settings.MAXIMUM_AMOUNT_PER_FREQUENCY.get(self.frequency)
        )
        if amount < minimum_amount or amount > maximum_amount:
            return False
        return True

    def validate_amount(self) -> Optional[HttpResponse]:
        form = AmountForm(self.request.GET)
        if not form.is_valid() or not self.amount_within_allowed_range(
            form.cleaned_data["amount"]
        ):
            return self.redirect_to_campaign_page()
        self.amount = form.cleaned_data["amount"]

    def validate_frequency(self) -> Optional[HttpResponse]:
        form = FrequencyForm(
            self.request.GET,
            allowed_frequencies=self.get_allowed_frequencies(),
            default_frequency=self.get_default_frequency(),
        )
        if not form.is_valid():
            return self.redirect_to_campaign_page()
        self.frequency = form.cleaned_data["frequency"]

    def validate_campaign_page(self) -> Optional[HttpResponse]:
        form = CampaignPageForm(
            self.request.GET, queryset=self.get_campaign_page_queryset()
        )
        if not form.is_valid():
            return self.get_campaign_page_does_not_exist_response()
        self.campaign_page = form.cleaned_data[CAMPAIGN_PAGE_ID_PARAM]

    def get_campaign_page_does_not_exist_response(self) -> HttpResponse:
        raise Http404("Page does not exist.")

    def get_campaign_page_url(self) -> str:
        return self.campaign_page.get_url(self.request)

    def get_thank_you_page_url(self) -> str:
        if hasattr(self, "get_thank_you_page_url"):
            return self.campaign_page.get_thank_you_page_url(self.request)
        return self.get_campaign_page_url()

    def redirect_to_campaign_page(self) -> HttpResponseRedirect:
        return HttpResponseRedirect(self.get_campaign_page_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            success_url=self.get_thank_you_page_url(),
            amount=self.amount,
            frequency=self.frequency,
            campaign_page=self.campaign_page,
            recaptcha_site_key=donate_settings.RECAPTCHA_PUBLIC_KEY,
            configuration_url=self.get_configuration_url(),
        )
        return context

    def get_configuration_url(self) -> str:
        return reverse("wagtaildonate:api:configuration-donations")


class DonateCheckoutView(BaseCheckoutView):
    template_name = "wagtaildonate/checkout.html"
    allowed_frequencies = [
        PaymentMethod.FREQUENCY_SINGLE,
        PaymentMethod.FREQUENCY_MONTHLY,
        PaymentMethod.FREQUENCY_PAYIN,
    ]

    def get_campaign_page_queryset(self) -> QuerySet:
        return (
            super()
            .get_campaign_page_queryset()
            .filter(
                Page.objects.type_q(AbstractDonationLandingPage)
                | Page.objects.type_q(AbstractPayInLandingPage)
            )
        )

    def get_default_campaign_page(self) -> Page:
        return get_default_donation_page()

    def get_campaign_page_does_not_exist_response(self) -> HttpResponse:
        try:
            default_campaign_page = self.get_default_campaign_page()
        except ObjectDoesNotExist:
            return super().get_campaign_page_does_not_exist_response()
        # Redirect to the checkout form with a right page ID if the page ID
        # provided by user is missing or invalid.
        split_url = list(urlsplit(self.request.get_full_path()))
        query_dict = QueryDict(split_url[3], mutable=True)
        query_dict[CAMPAIGN_PAGE_ID_PARAM] = default_campaign_page.pk
        split_url[3] = query_dict.urlencode()
        return HttpResponseRedirect(urlunsplit(split_url))

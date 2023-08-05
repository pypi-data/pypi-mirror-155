import logging

from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from wagtail import VERSION as WAGTAIL_VERSION
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.images import get_image_model_string

import premailer

from wagtaildonate import constants
from wagtaildonate.admin_forms import DonationAdminForm
from wagtaildonate.settings import donate_settings
from wagtaildonate.utils.blocks import ThankYouBlock
from wagtaildonate.utils.rich_text import rich_text_to_plain_text

if WAGTAIL_VERSION >= (3, 0):
    from wagtail import blocks
    from wagtail.admin.panels import (
        FieldPanel,
        InlinePanel,
        MultiFieldPanel,
        ObjectList,
        TabbedInterface,
    )
    from wagtail.fields import StreamField
    from wagtail.models import Orderable, Page
else:
    from wagtail.admin.edit_handlers import (
        FieldPanel,
        InlinePanel,
        MultiFieldPanel,
        ObjectList,
        StreamFieldPanel,
        TabbedInterface,
    )
    from wagtail.core import blocks
    from wagtail.core.fields import StreamField
    from wagtail.core.models import Orderable, Page
    from wagtail.images.edit_handlers import ImageChooserPanel


image_model = get_image_model_string()

logger = logging.getLogger(__name__)


class EmailParagraphBlock(blocks.RichTextBlock):
    class Meta:
        features = ["bold", "italic", "link", "ol", "ul"]

    def render_as_text(self, value, context=None):
        """
        Renders the paragraph, then converts the resulting HTML into text.
        """
        return rich_text_to_plain_text(self.render_basic(value, context=context))


class EmailStreamBlock(blocks.StreamBlock):
    paragraph = EmailParagraphBlock()

    def render_as_text(self, value, context=None):
        def render_child(child):
            if hasattr(child.block, "render_as_text"):
                return child.block.render_as_text(child.value, context=context)
            else:
                return child.block.render_basic(child.value, context=context)

        return "\n\n".join(map(render_child, value))


class SuggestedAmount(Orderable):
    amount = models.IntegerField()
    panels = [FieldPanel("amount")]

    def __str__(self):
        return str(self.amount)

    class Meta:
        abstract = True


class AbstractDonationLandingPage(Page):
    class Meta:
        abstract = True


class ThankYouRoutablePageMixin(RoutablePageMixin):

    """
    When a donation is completed, the user is presented with a 'Thank You' page.
    The values show on the thank you page will be set on the donation page.
    Using RoutablePageMixin, provide the donation pages with the functionality
    to render these valuse at /thank-you. Also ensure that the thank you page
    can be previewed.
    """

    preview_modes = [("/", "Page"), ("/thank-you/", "Thank you page")]

    thank_you_template = "wagtaildonate/thank_you.html"

    def get_thank_you_data(self):
        """
        Get thank you page content with fallback from the default donation page.
        """
        from wagtaildonate.models import get_default_donation_page

        thank_you_data = {}
        default_donation_page = get_default_donation_page()
        field_names = ["thank_you_strapline", "thank_you_page_content"]
        for field_name in field_names:
            # Try the current object first and revert to the default page.
            field_value = getattr(self, field_name, None)
            if not field_value:
                field_value = getattr(default_donation_page, field_name, None)
            if field_value:
                thank_you_data[field_name] = field_value
        return thank_you_data

    @route(r"^thank-you/$")
    def thank_you_page(self, request, *args, **kwargs):
        if (
            "donation_id" not in request.session
            or "donation_name" not in request.session
            or "donation_amount" not in request.session
        ):
            return HttpResponseRedirect(self.get_url(request))

        thank_you_data = self.get_thank_you_data()
        donation_amount = request.session.pop("donation_amount")
        donation_name = request.session.pop("donation_name")
        in_memory_of = request.session.pop("in_memory_of", False)
        gift_aid_declaration = request.session.pop("gift_aid_declaration", False)
        del request.session["donation_id"]

        return render(
            request,
            self.thank_you_template,
            {
                "page": self,
                "thank_you_data": thank_you_data,
                "donation_amount": donation_amount,
                "donation_name": donation_name,
                "in_memory_of": in_memory_of,
                "gift_aid_declaration": gift_aid_declaration,
            },
        )

    def get_thank_you_page_url(self, request=None):
        thank_you_path = self.reverse_subpage("thank_you_page")
        base_url = self.get_url(request)
        if not base_url.endswith("/"):
            base_url += "/"
        return base_url + thank_you_path

    def serve_preview(self, request, mode_name):
        view, args, kwargs = self.resolve_subpage(mode_name)
        request.is_preview = True

        # Add session data for a dummy preview
        request.session["donation_id"] = "0"
        request.session["donation_amount"] = "10.00"
        request.session["donation_name"] = "John Smith"
        request.session["in_memory_of"] = "Joe Bloggs"
        request.session["gift_aid_declaration"] = True

        return view(request, *args, **kwargs)

    def prepare_request_for_thank_you_page(self, request, donation):
        """
        Save data in session so they can be read by the thank you page.
        """
        request.session["donation_id"] = donation.pk
        request.session["donation_name"] = f"{donation.first_name} {donation.surname}"
        # Format amount to string before saving to session as the default JSON
        # serializer does not like Decimal objects.
        request.session["donation_amount"] = "{:.2f}".format(donation.amount)
        request.session["in_memory_of"] = donation.in_memory_of
        request.session["gift_aid_declaration"] = getattr(
            donation, "gift_aid_declaration", None
        )


class ThankYouEmailMixin(models.Model):
    thank_you_email_subject = models.CharField(max_length=255, blank=True)
    thank_you_email_content = (
        StreamField(EmailStreamBlock(required=False), blank=True, use_json_field=True)
        if WAGTAIL_VERSION >= (3, 0)
        else StreamField(EmailStreamBlock(required=False), blank=True)
    )

    class Meta:
        abstract = True

    thank_you_email_email_panels = (
        [
            FieldPanel("thank_you_email_subject"),
            FieldPanel("thank_you_email_content"),
        ]
        if WAGTAIL_VERSION >= (3, 0)
        else [
            FieldPanel("thank_you_email_subject"),
            StreamFieldPanel("thank_you_email_content"),
        ]
    )

    def get_thank_you_email_data(self):
        """
        Get thank you page content with fallback from the default donation page.
        """
        from wagtaildonate.models import get_default_donation_page

        thank_you_data = {}
        default_donation_page = get_default_donation_page()
        field_names = ["thank_you_email_content", "thank_you_email_subject"]
        for field_name in field_names:
            # Try the current object first and revert to the default page.
            field_value = getattr(self, field_name, None)
            if not field_value:
                field_value = getattr(default_donation_page, field_name, None)
            if field_value:
                thank_you_data[field_name] = field_value
        return thank_you_data

    def render_email_text(self, donation, thank_you_email_data):
        context = {"donation": donation}
        thank_you_email_content = thank_you_email_data.get("thank_you_email_content")
        if thank_you_email_content:
            block = thank_you_email_content.stream_block
            context["content"] = block.render_as_text(
                thank_you_email_content, context=context
            )
        return render_to_string("wagtaildonate/email/thank_you.txt", context)

    def render_email_html(self, donation, thank_you_email_data):
        context = {"donation": donation}
        thank_you_email_content = thank_you_email_data.get("thank_you_email_content")
        if thank_you_email_content:
            block = thank_you_email_content.stream_block
            context["content"] = block.render(thank_you_email_content, context=context)
        return premailer.transform(
            render_to_string("wagtaildonate/email/thank_you.html", context)
        )

    def prepare_thank_you_email(self, donation):
        thank_you_email_data = self.get_thank_you_email_data()
        message = EmailMultiAlternatives(
            thank_you_email_data.get("thank_you_email_subject", _("Thank you")),
            self.render_email_text(donation, thank_you_email_data),
            to=[donation.email],
        )
        message.attach_alternative(
            self.render_email_html(donation, thank_you_email_data), "text/html"
        )
        return message

    def send_thank_you_email(self, donation):
        if donation.email:
            message = self.prepare_thank_you_email(donation)
            message.send()
            logger.info(
                "Sent thank you email to %s for %s (ID: %d)",
                message.to,
                type(donation).__name__,
                donation.pk,
            )


def get_min_max_amounts_for_context(frequency):
    min_amount = donate_settings.MINIMUM_AMOUNT_PER_FREQUENCY.get(frequency)
    max_amount = donate_settings.MAXIMUM_AMOUNT_PER_FREQUENCY.get(frequency)
    return {
        f"minimum_{frequency}_donation_amount": min_amount,
        f"maximum_{frequency}_donation_amount": max_amount,
    }


class DonationLandingPageBase(
    ThankYouEmailMixin, ThankYouRoutablePageMixin, AbstractDonationLandingPage
):
    """The abstract base class for other donation page classes
    to extend."""

    base_form_class = DonationAdminForm

    introduction = models.TextField(blank=True)
    hero_image = models.ForeignKey(
        image_model, null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )
    hero_summary_text = models.TextField(blank=True)
    allow_single_donations = models.BooleanField(default=False)
    allow_regular_donations = models.BooleanField(default=False)
    show_other_amount_option = models.BooleanField(
        default=False,
        help_text=_("Offer the user the option to specify a custom amount."),
    )
    default_donation_frequency = models.CharField(
        max_length=20,
        choices=constants.FREQUENCY_CHOICES,
        default=constants.SINGLE,
        help_text=_(
            "Default donation frequency to prompt the user with. "
            "Only applies if both single and regular donations are allowed."
        ),
    )
    thank_you_strapline = models.TextField(blank=True)
    thank_you_page_content = (
        StreamField(ThankYouBlock(required=False), blank=True, use_json_field=True)
        if WAGTAIL_VERSION >= (3, 0)
        else StreamField(ThankYouBlock(required=False), blank=True)
    )

    # Checkout view specific
    checkout_hero_image = models.ForeignKey(
        image_model, null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )
    checkout_hero_summary_text = models.TextField(blank=True)

    content_panels = (
        Page.content_panels
        + [
            FieldPanel("introduction"),
            MultiFieldPanel(
                [FieldPanel("hero_image"), FieldPanel("hero_summary_text")],
                heading="Hero",
            ),
            MultiFieldPanel(
                [
                    FieldPanel("allow_single_donations"),
                    FieldPanel("allow_regular_donations"),
                    FieldPanel("default_donation_frequency"),
                    FieldPanel("show_other_amount_option"),
                    InlinePanel(
                        "suggested_amounts_single",
                        label="Suggested single amounts",
                        max_num=3,
                    ),
                    InlinePanel(
                        "suggested_amounts_regular",
                        label="Suggested regular amounts",
                        max_num=3,
                    ),
                ],
                heading="Donation configuration",
            ),
            MultiFieldPanel(
                [
                    FieldPanel("checkout_hero_image"),
                    FieldPanel("checkout_hero_summary_text"),
                ],
                heading="Checkout Page",
            ),
        ]
        if WAGTAIL_VERSION >= (3, 0)
        else Page.content_panels
        + [
            FieldPanel("introduction"),
            MultiFieldPanel(
                [ImageChooserPanel("hero_image"), FieldPanel("hero_summary_text")],
                heading="Hero",
            ),
            MultiFieldPanel(
                [
                    FieldPanel("allow_single_donations"),
                    FieldPanel("allow_regular_donations"),
                    FieldPanel("default_donation_frequency"),
                    FieldPanel("show_other_amount_option"),
                    InlinePanel(
                        "suggested_amounts_single",
                        label="Suggested single amounts",
                        max_num=3,
                    ),
                    InlinePanel(
                        "suggested_amounts_regular",
                        label="Suggested regular amounts",
                        max_num=3,
                    ),
                ],
                heading="Donation configuration",
            ),
            MultiFieldPanel(
                [
                    ImageChooserPanel("checkout_hero_image"),
                    FieldPanel("checkout_hero_summary_text"),
                ],
                heading="Checkout Page",
            ),
        ]
    )

    thank_you_panels = (
        [
            FieldPanel("thank_you_strapline"),
            FieldPanel("thank_you_page_content"),
        ]
        if WAGTAIL_VERSION >= (3, 0)
        else [
            FieldPanel("thank_you_strapline"),
            StreamFieldPanel("thank_you_page_content"),
        ]
    )

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Content"),
            ObjectList(thank_you_panels, heading="Thank you page settings"),
            ObjectList(
                ThankYouEmailMixin.thank_you_email_email_panels,
                heading="Email settings",
            ),
        ]
    )

    def get_donation_values(self):
        return {
            "suggested_amounts_single": self.suggested_amounts_single.all(),
            "suggested_amounts_regular": self.suggested_amounts_regular.all(),
        }

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context.update(self.get_donation_values())
        context.update(get_min_max_amounts_for_context("single"))
        context.update(get_min_max_amounts_for_context("monthly"))
        return context

    class Meta:
        abstract = True


class AbstractDonationPage(DonationLandingPageBase):
    """The DonationPage acts as the default Donate page.
    Only one of these can exists. It's to ensure that we can
    fall back to values not specified on individual
    campgain/fundraising pages and also so there is always a
    donation method available"""

    max_count = 1

    class Meta:
        abstract = True


class AbstractDonationCampaignPage(DonationLandingPageBase):
    """Similar to DonationLandingPage but more than one can exist"""

    template_name = "wagtaildonate/donation_campaign_page.html"

    class Meta:
        abstract = True


class AbstractPayInLandingPage(Page):
    class Meta:
        abstract = True


class AbstractDonationFundraisingPayInPage(
    ThankYouEmailMixin, ThankYouRoutablePageMixin, AbstractPayInLandingPage
):
    """Simple one-off form for fundraising pay-in
    This does not require any amount fields so only extends Page"""

    introduction = models.TextField(blank=True)
    hero_image = models.ForeignKey(
        image_model, null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )
    hero_summary_text = models.TextField(blank=True)
    thank_you_strapline = models.TextField(blank=True)
    thank_you_page_content = (
        StreamField(ThankYouBlock(required=False), blank=True, use_json_field=True)
        if WAGTAIL_VERSION >= (3, 0)
        else StreamField(ThankYouBlock(required=False), blank=True)
    )

    content_panels = (
        Page.content_panels
        + [
            FieldPanel("introduction"),
            MultiFieldPanel(
                [FieldPanel("hero_image"), FieldPanel("hero_summary_text")],
                heading="Hero",
            ),
        ]
        if WAGTAIL_VERSION >= (3, 0)
        else Page.content_panels
        + [
            FieldPanel("introduction"),
            MultiFieldPanel(
                [ImageChooserPanel("hero_image"), FieldPanel("hero_summary_text")],
                heading="Hero",
            ),
        ]
    )

    thank_you_panels = (
        [
            FieldPanel("thank_you_strapline"),
            FieldPanel("thank_you_page_content"),
        ]
        if WAGTAIL_VERSION >= (3, 0)
        else [
            FieldPanel("thank_you_strapline"),
            StreamFieldPanel("thank_you_page_content"),
        ]
    )

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Content"),
            ObjectList(thank_you_panels, heading="Thank you page settings"),
            ObjectList(
                ThankYouEmailMixin.thank_you_email_email_panels,
                heading="Email settings",
            ),
        ]
    )

    thank_you_template = "wagtaildonate/thank_you_fundraising.html"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context.update(get_min_max_amounts_for_context("payin"))
        return context

    class Meta:
        abstract = True

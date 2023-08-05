import logging

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from wagtaildonate.countries import country_choices
from wagtaildonate.models.query import DonationQuerySet
from wagtaildonate.payment_methods.base import PaymentMethod
from wagtaildonate.payment_methods.utils import get_payment_method
from wagtaildonate.utils.currency import format_gbp

logger = logging.getLogger(__name__)


class OptIns(models.Model):
    sms_consent = models.BooleanField(
        null=True, default=None, blank=True, verbose_name=_("SMS consent")
    )
    phone_consent = models.BooleanField(null=True, default=None, blank=True)
    post_consent = models.BooleanField(null=True, default=None, blank=True)
    email_consent = models.BooleanField(null=True, blank=True, default=None)

    class Meta:
        abstract = True


class GiftAid(models.Model):
    gift_aid_declaration = models.BooleanField(_("Gift Aid"))

    class Meta:
        abstract = True


class TransactionMixin(models.Model):
    STATUS_SETTLING = "settling"
    STATUS_SETTLED = "settled"
    STATUS_FAILED = "failed"  # Refer to provider_transaction_status for reason
    STATUS_UNKNOWN = "unknown"  # Refer to provider_transaction_status
    STATUS_CHOICES = [
        (STATUS_SETTLING, _("Settling")),
        (STATUS_SETTLED, _("Settled")),
        (STATUS_FAILED, _("Failed")),
        (STATUS_UNKNOWN, _("Unknown")),
    ]

    transaction_id = models.CharField(_("Transaction ID"), max_length=50)
    transaction_status = models.CharField(max_length=100, choices=STATUS_CHOICES)
    # If the payment provider returned a more specific or unknown status. Refer to this field for details
    provider_transaction_status = models.CharField(max_length=100, blank=True)

    # 3D Secure related fields
    # liability_shifted indicates that 3D Secure verification has taken place successfully
    # and fraud liability has been shifted from the merchant to the card issuer.
    # liability_shift_possible indicates that the card is enrolled in 3D Secure and liabilty
    # can be shifted from merchant to issuer.
    # three_d_secure_status holds the 3D Secure verification result from the provider.
    liability_shifted = models.BooleanField(blank=True, default=False)
    liability_shift_possible = models.BooleanField(blank=True, default=False)
    three_d_secure_status = models.CharField(max_length=100, blank=True, default="")

    is_recurring = False
    objects = DonationQuerySet.as_manager()

    class Meta:
        abstract = True

    def is_settling(self) -> bool:
        return self.transaction_status == self.STATUS_SETTLING

    def update_settlement_status(
        self, commit: bool = True, output_non_commit_log: bool = False
    ):
        payment_method = self.get_payment_method()
        new_status = payment_method.get_transaction_status_for_transaction(
            self.transaction_id
        )
        if self.provider_transaction_status == new_status.provider_transaction_status:
            # No need to update, already the same status.
            return
        old_status = self.transaction_status
        old_provider_status = self.provider_transaction_status
        self.provider_transaction_status = new_status.provider_transaction_status
        self.transaction_status = new_status.transaction_status
        if commit:
            logger.info(
                "Update transaction status for %s (ID: %d), %s (%s) -> %s (%s)",
                type(self).__name__,
                self.pk,
                old_status,
                old_provider_status,
                new_status.transaction_status,
                new_status.provider_transaction_status,
            )
            self.save(
                update_fields=["provider_transaction_status", "transaction_status"]
            )
        elif output_non_commit_log:
            logger.info(
                "Non-commit update transaction status for %s (ID: %d), %s (%s) -> %s (%s), %s (ID: %s)",
                type(self).__name__,
                self.pk,
                old_status,
                old_provider_status,
                new_status.transaction_status,
                new_status.provider_transaction_status,
                self.payment_method,
                self.transaction_id,
            )


class BaseDonation(OptIns, models.Model):
    donation_page = models.ForeignKey(
        "wagtailcore.Page", on_delete=models.SET_NULL, null=True, related_name="+"
    )
    payment_method = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    first_name = models.CharField(_("First name"), max_length=100)
    surname = models.CharField(_("Surname"), max_length=100)
    email = models.EmailField(_("Email address"), max_length=255, blank=True)
    phone_number = PhoneNumberField(_("Phone number"), blank=True)
    address_line_1 = models.CharField(_("Address line 1"), max_length=255)
    address_line_2 = models.CharField(_("Address line 2"), max_length=255, blank=True)
    address_line_3 = models.CharField(_("Address line 3"), max_length=255, blank=True)
    town = models.CharField(_("Town"), max_length=255)
    postal_code = models.CharField(_("Postal code"), max_length=50)
    country = models.CharField(_("Country"), max_length=255, choices=country_choices())
    on_behalf_of_organisation = models.BooleanField(_("On behalf of organisation"))
    in_memory = models.BooleanField(_("In memory"))
    in_memory_of = models.CharField(_("In memory of"), max_length=60, blank=True)
    created_at = models.DateTimeField(_("Created at"), default=timezone.now)

    def save(self, *args, **kwargs):
        # If there is no pk, thus meaning that this donation is being created
        # log the donation as succesful.
        if self.pk is None:
            super().save(*args, **kwargs)
            logger.info("%s created (ID: %d)", type(self).__name__, self.pk)
            return
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        logger.info("%s deleted (ID: %d)", type(self).__name__, self.pk)
        return super().delete(*args, **kwargs)

    def formatted_amount(self) -> str:
        return format_gbp(self.amount)

    def get_payment_method(self) -> PaymentMethod:
        return get_payment_method(self.payment_method)

    class Meta:
        abstract = True


class AbstractSingleDonation(GiftAid, TransactionMixin, BaseDonation):
    class Meta:
        abstract = True
        verbose_name = _("Donation")
        verbose_name_plural = _("Donations")
        permissions = (("can_export_donations", _("Can export donate transactions")),)


class AbstractRecurringDonation(GiftAid, BaseDonation):
    FREQUENCY_MONTHLY = "monthly"
    FREQUENCY_CHOICES = [
        (FREQUENCY_MONTHLY, _("Monthly")),
    ]

    subscription_id = models.CharField(_("Subscription ID"), max_length=50)
    frequency = models.CharField(max_length=100, choices=FREQUENCY_CHOICES)

    is_recurring = True

    class Meta:
        abstract = True
        verbose_name = _("Recurring Donation")
        verbose_name_plural = _("Recurring Donations")
        permissions = (
            (
                "can_export_recurring_donations",
                _("Can export recurring donate transactions"),
            ),
        )


class AbstractPayIn(TransactionMixin, BaseDonation):
    """
    Pay ins are very similar to one-off donations with an exception of not
    supporting Gift Aid and of allowing pay in event details to be stored
    """

    event_name = models.CharField(max_length=255, blank=True)
    event_code = models.CharField(max_length=50, blank=True)
    fundraiser_reference = models.CharField(max_length=50, blank=True)

    class Meta:
        abstract = True
        permissions = (("can_export_pay_ins", _("Can export pay ins")),)


class SingleDonation(AbstractSingleDonation):
    pass


class RecurringDonation(AbstractRecurringDonation):
    pass


class PayIn(AbstractPayIn):
    pass

import logging

from django.core.management.base import BaseCommand
from django.db import transaction as transaction

from wagtaildonate.exceptions import TransactionNotFound
from wagtaildonate.models.utils import get_pay_in_model, get_single_donation_model

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Update settlement status for non-settled transaction"

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **options):
        models = [get_single_donation_model(), get_pay_in_model()]

        dry_run = options["dry_run"]
        if dry_run:
            logger.info(
                "Dry running updating settlement status of settling transactions."
            )
        else:
            logger.info("Updating settlement status of settling transactions.")

        for model in models:
            self.handle_model(model, dry_run=dry_run)

    def handle_model(self, model, dry_run=False):
        queryset = model.objects.settling().values_list("pk", flat=True)
        for donation_pk in queryset.iterator():
            if dry_run:
                donation = model.objects.get(pk=donation_pk)
                try:
                    donation.update_settlement_status(
                        commit=False, output_non_commit_log=True
                    )
                except TransactionNotFound:
                    logger.exception(
                        "Could not load remote transaction data for %s (ID: %s).",
                        type(donation).__name__,
                        donation.pk,
                    )
            else:
                with transaction.atomic():
                    # Lock this donation instance for update so nothing else tries to
                    # update it.
                    donation = model.objects.select_for_update().get(pk=donation_pk)
                    if not donation.is_settling():
                        # Skip this iteration because the transaction is not settling
                        # anymore.
                        continue
                    try:
                        donation.update_settlement_status()
                    except TransactionNotFound:
                        logger.exception(
                            "Could not load remote transaction data for %s (ID: %s).",
                            type(donation).__name__,
                            donation.pk,
                        )

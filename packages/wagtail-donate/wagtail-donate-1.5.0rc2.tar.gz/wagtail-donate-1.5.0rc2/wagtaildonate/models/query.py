from django.db import models


class DonationQuerySet(models.QuerySet):
    def settling(self):
        return self.filter(transaction_status=self.model.STATUS_SETTLING)

    def failed(self):
        return self.filter(transaction_status=self.model.STATUS_FAILED)

    def settled(self):
        return self.filter(transaction_status=self.model.STATUS_SETTLED)

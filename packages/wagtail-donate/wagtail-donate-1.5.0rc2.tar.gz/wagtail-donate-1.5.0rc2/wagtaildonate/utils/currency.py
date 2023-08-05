from decimal import Decimal

from django.contrib.humanize.templatetags.humanize import intcomma


def format_gbp(amount) -> str:
    # Convert to decimal as Donation.amount could be a string on create
    amount = Decimal(amount)

    pounds = int(amount)
    pence = int((amount - pounds) * 100)
    return f"£{intcomma(pounds)}.{str(pence).zfill(2)}"

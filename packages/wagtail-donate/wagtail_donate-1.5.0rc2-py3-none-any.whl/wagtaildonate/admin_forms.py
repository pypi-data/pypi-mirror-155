from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from wagtail.admin.forms import WagtailAdminPageForm
from wagtail.admin.widgets import AdminDateInput


class DonationAdminForm(WagtailAdminPageForm):
    def clean(self):
        cleaned_data = super().clean()

        # At least one of monthly or single is enabled
        if (
            not cleaned_data["allow_single_donations"]
            and not cleaned_data["allow_regular_donations"]
        ):
            self.add_error(
                "allow_single_donations",
                _("Please allow at least one donation option."),
            )

        # If 'show other' amount field is not true, donation values must be added
        # according to allowed frequency regular/single
        if not cleaned_data.get("show_other_amount_option"):
            single_amount_forms = self.formsets.get("suggested_amounts_single")
            if (
                single_amount_forms
                and len(single_amount_forms) < 1
                and cleaned_data.get("allow_single_donations")
            ):
                self.add_error(
                    "allow_single_donations", _("Please add donation values.")
                )

            regular_amount_forms = self.formsets.get("suggested_amounts_regular")
            if (
                regular_amount_forms
                and len(regular_amount_forms) < 1
                and cleaned_data.get("allow_regular_donations")
            ):
                self.add_error(
                    "allow_regular_donations", _("Please add donation values.")
                )

        return cleaned_data


def today():
    return timezone.now().date()


class DateRangeForm(forms.Form):

    from_date = forms.DateField(widget=AdminDateInput, initial=today)
    to_date = forms.DateField(widget=AdminDateInput, initial=today)

    def clean_from_date(self):
        from_date = self.cleaned_data["from_date"]
        if from_date > today():
            raise forms.ValidationError(_("Date cannot be in the future"))
        return from_date

    def clean_to_date(self):
        to_date = self.cleaned_data["to_date"]
        if to_date > today():
            raise forms.ValidationError(_("Date cannot be in the future"))
        return to_date

    def clean(self):
        from_date = self.cleaned_data.get("from_date")
        to_date = self.cleaned_data.get("to_date")
        if to_date and from_date and to_date < from_date:
            # swap them around
            self.cleaned_data["from_date"] = to_date
            self.cleaned_data["to_date"] = from_date

import django.db.models.deletion
from django.db import migrations, models

import modelcluster.fields
from wagtail.images import get_image_model_string

image_model = get_image_model_string()


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("wagtailcore", "0041_group_collection_permissions_verbose_name_plural"),
        migrations.swappable_dependency(get_image_model_string()),
    ]

    operations = [
        migrations.CreateModel(
            name="DonationCampaignPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.Page",
                    ),
                ),
                ("introduction", models.TextField(blank=True)),
                ("hero_summary_text", models.TextField(blank=True)),
                ("allow_single_donations", models.BooleanField(default=False)),
                ("allow_regular_donations", models.BooleanField(default=False)),
                (
                    "show_other_amount_option",
                    models.BooleanField(
                        default=False,
                        help_text="Offer the user the option to specify a custom amount.",
                    ),
                ),
                (
                    "default_donation_frequency",
                    models.CharField(
                        choices=[("single", "single"), ("regular", "regular")],
                        default="single",
                        help_text="Default donation frequency to prompt the user with. Only applies if both weekly and monthly donations are allowed.",
                        max_length=20,
                    ),
                ),
                (
                    "hero_image",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=image_model,
                    ),
                ),
            ],
            options={"abstract": False},
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="DonationFundraisingPayInPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.Page",
                    ),
                ),
            ],
            options={"abstract": False},
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="DonationPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.Page",
                    ),
                ),
                ("introduction", models.TextField(blank=True)),
                ("hero_summary_text", models.TextField(blank=True)),
                ("allow_single_donations", models.BooleanField(default=False)),
                ("allow_regular_donations", models.BooleanField(default=False)),
                (
                    "show_other_amount_option",
                    models.BooleanField(
                        default=False,
                        help_text="Offer the user the option to specify a custom amount.",
                    ),
                ),
                (
                    "default_donation_frequency",
                    models.CharField(
                        choices=[("single", "single"), ("regular", "regular")],
                        default="single",
                        help_text="Default donation frequency to prompt the user with. Only applies if both weekly and monthly donations are allowed.",
                        max_length=20,
                    ),
                ),
                (
                    "hero_image",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=image_model,
                    ),
                ),
            ],
            options={"abstract": False},
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="SuggestedDonationDonatePagePlacementSingle",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "sort_order",
                    models.IntegerField(blank=True, editable=False, null=True),
                ),
                ("amount", models.IntegerField()),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="suggested_amounts_donate_page_single",
                        to="wagtaildonate.DonationPage",
                    ),
                ),
            ],
            options={"abstract": False},
        ),
        migrations.CreateModel(
            name="SuggestedDonationDonatePagePlacementRegular",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "sort_order",
                    models.IntegerField(blank=True, editable=False, null=True),
                ),
                ("amount", models.IntegerField()),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="suggested_amounts_donate_page_regular",
                        to="wagtaildonate.DonationPage",
                    ),
                ),
            ],
            options={"abstract": False},
        ),
        migrations.CreateModel(
            name="SuggestedDonationCampaignPagePlacementSingle",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "sort_order",
                    models.IntegerField(blank=True, editable=False, null=True),
                ),
                ("amount", models.IntegerField()),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="suggested_amounts_campaign_page_single",
                        to="wagtaildonate.DonationCampaignPage",
                    ),
                ),
            ],
            options={"abstract": False},
        ),
        migrations.CreateModel(
            name="SuggestedDonationCampaignPagePlacementRegular",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "sort_order",
                    models.IntegerField(blank=True, editable=False, null=True),
                ),
                ("amount", models.IntegerField()),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="suggested_amounts_campaign_page_regular",
                        to="wagtaildonate.DonationCampaignPage",
                    ),
                ),
            ],
            options={"abstract": False},
        ),
    ]

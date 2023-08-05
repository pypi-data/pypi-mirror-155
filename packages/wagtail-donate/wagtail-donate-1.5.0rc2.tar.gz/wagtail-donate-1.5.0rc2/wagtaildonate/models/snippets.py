from django.db import models

from wagtail import VERSION as WAGTAIL_VERSION
from wagtail.images import get_image_model_string
from wagtail.snippets.models import register_snippet

if WAGTAIL_VERSION >= (3, 0):
    from wagtail import blocks
    from wagtail.admin.panels import FieldPanel
    from wagtail.fields import RichTextField, StreamField
else:
    from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
    from wagtail.core import blocks
    from wagtail.core.fields import RichTextField, StreamField
    from wagtail.images.edit_handlers import ImageChooserPanel

image_model = get_image_model_string()


@register_snippet
class ThankYouCTASnippet(models.Model):
    title = models.CharField(max_length=255)
    summary = RichTextField(blank=True, max_length=255)

    image = models.ForeignKey(
        image_model, null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )

    link = (
        StreamField(
            blocks.StreamBlock(
                [
                    (
                        "external_link",
                        blocks.StructBlock(
                            [("url", blocks.URLBlock()), ("title", blocks.CharBlock())],
                            icon="link",
                        ),
                    ),
                    (
                        "internal_link",
                        blocks.StructBlock(
                            [
                                ("page", blocks.PageChooserBlock()),
                                ("title", blocks.CharBlock(required=False)),
                            ],
                            icon="link",
                        ),
                    ),
                ],
                max_num=1,
                required=True,
            ),
            blank=True,
            use_json_field=True,
        )
        if WAGTAIL_VERSION >= (3, 0)
        else StreamField(
            blocks.StreamBlock(
                [
                    (
                        "external_link",
                        blocks.StructBlock(
                            [("url", blocks.URLBlock()), ("title", blocks.CharBlock())],
                            icon="link",
                        ),
                    ),
                    (
                        "internal_link",
                        blocks.StructBlock(
                            [
                                ("page", blocks.PageChooserBlock()),
                                ("title", blocks.CharBlock(required=False)),
                            ],
                            icon="link",
                        ),
                    ),
                ],
                max_num=1,
                required=True,
            ),
            blank=True,
        )
    )

    panels = (
        [
            FieldPanel("title"),
            FieldPanel("summary"),
            FieldPanel("image"),
            FieldPanel("link"),
        ]
        if WAGTAIL_VERSION >= (3, 0)
        else [
            FieldPanel("title"),
            FieldPanel("summary"),
            ImageChooserPanel("image"),
            StreamFieldPanel("link"),
        ]
    )

    def get_link_text(self):
        # Link is required, so we should always have
        # an element with index 0
        block = self.link[0]

        title = block.value["title"]
        if block.block_type == "external_link":
            return title

        # Title is optional for internal_link
        # so fallback to page's title, if it's empty
        return title or block.value["page"].title

    def get_link_url(self):
        # Link is required, so we should always have
        # an element with index 0
        block = self.link[0]

        if block.block_type == "external_link":
            return block.value["url"]

        return block.value["page"].get_url()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Thank you CTA snippet"

from wagtail import VERSION as WAGTAIL_VERSION

if WAGTAIL_VERSION >= (3, 0):
    from wagtail import blocks
else:
    from wagtail.core import blocks


class DonateBlock(blocks.StructBlock):
    donation_page = blocks.PageChooserBlock()

    class Meta:
        icon = "plus-inverse"
        template = "wagtaildonate/streamfield/blocks/donate_block.html"

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)

        donation_page = value["donation_page"].specific
        context["donation_page"] = donation_page
        context.update(donation_page.get_donation_values())

        return context

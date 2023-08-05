from wagtail import VERSION as WAGTAIL_VERSION
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock

if WAGTAIL_VERSION >= (3, 0):
    from wagtail import blocks
else:
    from wagtail.core import blocks


class ImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    caption = blocks.CharBlock(required=False)

    class Meta:
        icon = "image"
        template = "wagtaildonate/streamfield/blocks/image_block.html"


class DocumentBlock(blocks.StructBlock):
    document = DocumentChooserBlock()
    title = blocks.CharBlock(required=False)

    class Meta:
        icon = "doc-full-inverse"
        template = "wagtaildonate/streamfield/blocks/document_block.html"


class QuoteBlock(blocks.StructBlock):
    quote = blocks.CharBlock(classname="title")
    attribution = blocks.CharBlock(required=False)

    class Meta:
        icon = "openquote"
        template = "wagtaildonate/streamfield/blocks/quote_block.html"


class ThankYouBlock(blocks.StreamBlock):
    heading = blocks.CharBlock(
        classname="full title",
        icon="title",
        template="wagtaildonate/streamfield/blocks/heading_block.html",
    )
    paragraph = blocks.RichTextBlock()
    image = ImageBlock()
    document = DocumentBlock()
    quote = QuoteBlock()
    video = EmbedBlock()
    call_to_action = SnippetChooserBlock(
        "wagtaildonate.ThankYouCTASnippet",
        template="wagtaildonate/streamfield/blocks/thank_you_cta_block.html",
    )

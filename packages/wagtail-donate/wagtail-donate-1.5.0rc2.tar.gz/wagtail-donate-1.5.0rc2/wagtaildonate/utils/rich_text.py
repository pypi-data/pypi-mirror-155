from bs4 import BeautifulSoup, NavigableString


# Taken from (Sorry. flake8 made me chop it in half!)
# https://github.com/wagtail/wagtail-localize/blob/316757bb80bf0370a36eb4efad18
# ca47905102a2/wagtail_localize/translation/segments/html.py#L230-L263
def extract_html_elements(soup):
    """
    Extracts HTML elements from a fragment. Returns the plain text representation
    of the HTML document and an array of elements including their span, type and attributes.
    For example:
    text, elements = extract_html_elements("This is a paragraph. <b>This is some bold <i>and now italic</i></b> text")
    text == "This is a paragraph. This is some bold and now italic text"
    elements == [(39, 53, 'i', {}), (21, 53, 'b', {})]
    """
    texts = []
    cursor = {"current": 0}
    elements = []

    def walk(soup):
        for element in soup.children:
            if isinstance(element, NavigableString):
                texts.append(element)
                cursor["current"] += len(element)

            else:
                start = cursor["current"]
                walk(element)
                end = cursor["current"]

                elements.append((start, end, element.name, element.attrs.copy()))

    walk(soup)

    return "".join(texts), elements


def rich_text_to_plain_text(value):
    """
    Converts rich text field values into plain text.

    All HTML tags are removed, blocks are separated by new lines and list items are prefixed.

    Doesn't yet handle headings, links or inline formatting.
    """
    soup = BeautifulSoup(value, "html.parser")
    lines = []

    def process_block_tag(tag, newline_prefix=""):
        # TODO: Extract link URLs
        text, elements = extract_html_elements(tag)

        # Insert line breaks
        line_breaks = []
        for start, end, tag_name, attrs in elements:
            if tag_name == "br":
                line_breaks.append(start)

        if line_breaks:
            new_text = ""
            cursor = 0

            for pos in line_breaks:
                # Insert text up until the line break
                if pos > cursor:
                    new_text += text[cursor:pos]
                    cursor = pos

                # Insert line break
                new_text += "\n"

                # Insert newline prefix
                new_text += newline_prefix

            # Insert text after last line break
            if cursor < len(text):
                # Black and flake8 disagree on how to format this line
                new_text += text[cursor : len(text)]  # noqa

            text = new_text

        return text

    def process_paragraph(tag):
        lines.append(process_block_tag(tag))
        lines.append("")

    def process_unordered_list(tag):
        for list_item in tag:
            lines.append(" * " + process_block_tag(list_item, newline_prefix="   "))

        lines.append("")

    def process_ordered_list(tag):
        for i, list_item in enumerate(tag):
            prefix = "{}. ".format(i + 1)
            lines.append(
                prefix + process_block_tag(list_item, newline_prefix=" " * len(prefix))
            )

        lines.append("")

    def walk(tag):
        if tag.name == "div":
            # Step into div tags
            for child in tag:
                walk(child)

        elif tag.name in ["p", "h1", "h2", "h3", "h4", "h5", "h6"]:
            process_paragraph(tag)

        elif tag.name == "ul":
            process_unordered_list(tag)

        elif tag.name == "ol":
            process_ordered_list(tag)

        else:
            # Ignore everything else
            return

    for tag in soup:
        walk(tag)

    return "\n".join(lines).strip("\n")

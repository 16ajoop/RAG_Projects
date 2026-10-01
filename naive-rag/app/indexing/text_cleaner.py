import re


def clean_text(text):
    # Remove extra spaces and tabs
    text = re.sub(r"[ \t]+", " ", text)

    # Remove spaces at the beginning and end of each line
    text = re.sub(r" *\n *", "\n", text)

    # Remove excessive blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    # Remove spaces at the beginning and end of the whole text
    text = text.strip()

    return text
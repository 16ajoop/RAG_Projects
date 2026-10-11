import re

def clean_text(text: str) -> str:
    # Replace non-breaking spaces with normal spaces
    text = text.replace("\xa0", " ")

    cleaned_lines = []

    for line in text.splitlines():
        # Remove extra spaces/tabs
        line = re.sub(r"[\t]+", " ", line)

        # Remove spaces at beginning and end
        line = line.strip()

        # Keep only non-empty lines
        if line:
            cleaned_lines.append(line)

    # Join the cleaned lines while preserving line structure
    return "\n".join(cleaned_lines)
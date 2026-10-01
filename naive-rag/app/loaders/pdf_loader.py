import pymupdf


def load_pdf(file_path):
    document = pymupdf.open(
        "data/documents/cognition_ai_employee_handbook.pdf"
    )

    pages = []

    for page_number, page in enumerate(document):
        text = page.get_text()

        pages.append({
            "page_number": page_number + 1,
            "text": text
        })

    document.close()

    return pages
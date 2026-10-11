import pymupdf

def load_pdf(file_path: str) -> str:
    documents = pymupdf.open(file_path)

    text = ""

    for page in documents:
        text += page.get_text()

    documents.close()

    return text
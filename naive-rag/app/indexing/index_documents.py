from app.loaders.pdf_loader import load_pdf
from app.indexing.text_cleaner import clean_text
from app.indexing.chunker import chunk_text
from app.indexing.embedder import create_embedding
from app.indexing.vector_store import add_document


PDF_PATH = "data/documents/cognition_ai_employee_handbook.pdf"


def index_document(pdf_path):
    # Step 1: Load PDF
    pages = load_pdf(pdf_path)

    chunk_count = 0

    # Process each page
    for page in pages:

        # Step 2: Clean text
        cleaned_text = clean_text(page["text"])

        # Step 3: Create chunks
        chunks = chunk_text(cleaned_text)

        # Process each chunk
        for chunk in chunks:

            # Step 4: Create embedding
            embedding = create_embedding(chunk)

            # Step 5: Create unique ID
            document_id = f"page_{page['page_number']}_chunk_{chunk_count}"

            # Step 6: Store in ChromaDB
            add_document(
                document_id=document_id,
                text=chunk,
                embedding=embedding,
                metadata={
                    "page": page["page_number"]
                }
            )

            chunk_count += 1

    print("Indexing completed.")
    print("Total chunks indexed:", chunk_count)


if __name__ == "__main__":
    index_document(PDF_PATH)
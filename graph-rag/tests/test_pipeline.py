from app.loaders.pdf_loader import load_pdf
from app.processing.cleaner import clean_text
from app.processing.chunker import chunk_text
from app.graph.entity_extractor import extract_entities
from app.graph.relationship_extractor import extract_relationships
from app.graph.graph_builder import build_graph_data

from app.graph.graph_database import get_graph

PDF_PATH = "data/documents/company_knowledge_base_graphrag.pdf"


# Stage 2: PDF Loading Test

def test_pdf_loader():
    text = load_pdf(PDF_PATH)

    assert text is not None
    assert len(text) > 0

    print("PDF loaded successfully")
    print(f"Characters extracted: {len(text)}")

    return text


# Stage 3: Text Cleaning Test

def test_text_cleaning(text):
    cleaned_text = clean_text(text)

    assert cleaned_text is not None
    assert len(cleaned_text) > 0

    # Check that important information still exists
    assert "AITech" in cleaned_text
    assert "Pooja V" in cleaned_text
    assert "GraphMind" in cleaned_text

    print("\nText cleaning successful")
    print(f"Characters after cleaning: {len(cleaned_text)}")

    print("\n--- First 1000 characters after cleaning ---\n")
    print(cleaned_text[:1000])

    return cleaned_text

# Stage 4: Chunking Test

def test_chunking(cleaned_text):
    chunks = chunk_text(cleaned_text)

    assert chunks is not None
    assert len(chunks) > 0

    print("\nChunking successful")
    print(f"Total chunks created: {len(chunks)}")

    for i, chunk in enumerate(chunks[:3]):
        print(f"\n--- Chunk {i + 1} ---")
        print(f"Length: {len(chunk)} characters")
        print(chunk)

    return chunks

# Stage 5: Entity Extraction Test
def test_entity_extraction(chunks):
    # Start with one chunk for testing
    entities = extract_entities(chunks[0])

    assert entities is not None
    assert len(entities) > 0

    print("\nEntity extraction successful")
    print(f"Entities found: {len(entities)}")

    for entity in entities:
        print(f"- {entity['name']} [{entity['type']}]")

    return entities

def test_relationship_extraction(chunks, entities):
    relationships = extract_relationships(
        chunks[0],
        entities
    )

    assert relationships is not None

    print("\nRelationship extraction successful")
    print(f"Relationships found: {len(relationships)}")

    for relationship in relationships:
        print(
            f"- {relationship['source']} "
            f"--[{relationship['relationship']}]--> "
            f"{relationship['target']}"
        )

    return relationships



def test_graph_data(chunks):
    """
    Build the complete graph data from all document chunks.
    """

    entities, relationships = build_graph_data(chunks)

    assert entities is not None
    assert relationships is not None

    assert len(entities) > 0

    print("\n" + "=" * 50)
    print("GRAPH DATA EXTRACTION SUCCESSFUL")
    print("=" * 50)

    print(f"\nUnique entities: {len(entities)}")
    print(f"Unique relationships: {len(relationships)}")

    print("\n--- ENTITIES ---")

    for entity in entities:
        print(
            f"- {entity['name']} "
            f"[{entity['type']}]"
        )

    print("\n--- RELATIONSHIPS ---")

    for relationship in relationships:
        print(
            f"- {relationship['source']} "
            f"--[{relationship['relationship']}]--> "
            f"{relationship['target']}"
        )

    return entities, relationships

# FALKODB TEST
def test_falkordb_connection():
    graph = get_graph()

    result = graph.query(
        "RETURN 'FalkorDB connection successful!' AS message"
    )

    message = result.result_set[0][0]

    assert message == "FalkorDB connection successful!"

    print("\nFalkorDB connection successful!")



if __name__ == "__main__":
    raw_text = test_pdf_loader()

    cleaned_text = test_text_cleaning(raw_text)

    chunks = test_chunking(cleaned_text)

    # Stage 7:
    # Extract entities and relationships from all chunks
    # and prepare the final graph data.
    entities, relationships = test_graph_data(chunks)


import json
from pathlib import Path

from app.graph.graph_extractor import extract_graph_data


PROGRESS_PATH = Path("data/graph_extraction_progress.json")
FINAL_PATH = Path("data/graph_data.json")


def save_progress(
    processed_chunks: list[int],
    entities: list[dict],
    relationships: list[dict],
) -> None:
    """Save successful extraction progress."""

    PROGRESS_PATH.parent.mkdir(parents=True, exist_ok=True)

    progress_data = {
        "processed_chunks": sorted(set(processed_chunks)),
        "entities": entities,
        "relationships": relationships,
    }

    with open(PROGRESS_PATH, "w", encoding="utf-8") as file:
        json.dump(progress_data, file, indent=2, ensure_ascii=False)


def load_progress() -> tuple[list[int], list[dict], list[dict]]:
    """Load saved progress, if available."""

    if not PROGRESS_PATH.exists():
        return [], [], []

    try:
        with open(PROGRESS_PATH, "r", encoding="utf-8") as file:
            progress_data = json.load(file)

        if not isinstance(progress_data, dict):
            raise ValueError("Progress file must contain a JSON object.")

        processed = progress_data.get("processed_chunks", [])
        entities = progress_data.get("entities", [])
        relationships = progress_data.get("relationships", [])

        if not isinstance(processed, list):
            processed = []
        if not isinstance(entities, list):
            entities = []
        if not isinstance(relationships, list):
            relationships = []

        return processed, entities, relationships

    except (json.JSONDecodeError, OSError, ValueError) as error:
        print(f"Could not load saved progress: {error}")
        print("Starting with empty extraction progress.")
        return [], [], []


def deduplicate_entities(entities: list[dict]) -> list[dict]:
    """Keep one valid copy of each entity."""

    unique = []
    seen = set()

    for entity in entities:
        if not isinstance(entity, dict):
            continue

        name = entity.get("name")
        entity_type = entity.get("type")

        if not isinstance(name, str) or not isinstance(entity_type, str):
            continue

        name = name.strip()
        entity_type = entity_type.strip().upper()

        if not name or not entity_type:
            continue

        key = (name.casefold(), entity_type)

        if key not in seen:
            seen.add(key)
            unique.append({"name": name, "type": entity_type})

    return unique


def deduplicate_relationships(
    relationships: list[dict],
) -> list[dict]:
    """Keep one valid copy of each relationship."""

    unique = []
    seen = set()

    for relationship in relationships:
        if not isinstance(relationship, dict):
            continue

        source = relationship.get("source")
        relation = relationship.get("relationship")
        target = relationship.get("target")

        if not all(
            isinstance(value, str)
            for value in (source, relation, target)
        ):
            continue

        source = source.strip()
        relation = relation.strip().upper()
        target = target.strip()

        if not source or not relation or not target:
            continue

        key = (
            source.casefold(),
            relation,
            target.casefold(),
        )

        if key not in seen:
            seen.add(key)
            unique.append({
                "source": source,
                "relationship": relation,
                "target": target,
            })

    return unique


def build_graph_data(
    chunks: list[str],
) -> tuple[list[dict], list[dict]]:
    """Extract graph data one chunk at a time with resumable progress."""

    processed_chunks, all_entities, all_relationships = load_progress()

    # Keep only valid chunk numbers for the current document.
    processed_chunks = sorted({
        number
        for number in processed_chunks
        if isinstance(number, int) and 1 <= number <= len(chunks)
    })

    all_entities = deduplicate_entities(all_entities)
    all_relationships = deduplicate_relationships(all_relationships)

    print(
        f"\nAlready processed chunks: "
        f"{len(processed_chunks)}/{len(chunks)}"
    )

    for index, chunk in enumerate(chunks):
        chunk_number = index + 1

        if chunk_number in processed_chunks:
            print(f"\nSkipping chunk {chunk_number} (already processed)")
            continue

        print(f"\nProcessing chunk {chunk_number}/{len(chunks)}...")

        try:
            entities, relationships = extract_graph_data(chunk)

            # Empty results may mean extraction failed or the chunk
            # contained no graphable information. Do not silently mark
            # them as successful; retry/debug them instead.
            if not entities and not relationships:
                print(
                    f"Chunk {chunk_number} returned no graph data. "
                    "It has NOT been marked as processed."
                )
                continue

            all_entities.extend(entities)
            all_relationships.extend(relationships)

            all_entities = deduplicate_entities(all_entities)
            all_relationships = deduplicate_relationships(all_relationships)

            processed_chunks.append(chunk_number)

            save_progress(
                processed_chunks,
                all_entities,
                all_relationships,
            )

            print(
                f"Chunk {chunk_number} saved: "
                f"{len(entities)} entities, "
                f"{len(relationships)} relationships."
            )

        except Exception as error:
            print(f"\nError processing chunk {chunk_number}: {error}")
            print("Previous successful progress has been preserved.")
            raise

    # Save the current accumulated graph, even if some chunks need retrying.
    graph_data = {
        "entities": deduplicate_entities(all_entities),
        "relationships": deduplicate_relationships(all_relationships),
    }

    FINAL_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(FINAL_PATH, "w", encoding="utf-8") as file:
        json.dump(graph_data, file, indent=2, ensure_ascii=False)

    incomplete = sorted(
        set(range(1, len(chunks) + 1)) - set(processed_chunks)
    )

    print("\n" + "=" * 50)
    print("GRAPH DATA EXTRACTION SUMMARY")
    print("=" * 50)
    print(f"Unique entities: {len(graph_data['entities'])}")
    print(f"Unique relationships: {len(graph_data['relationships'])}")
    print(f"Processed chunks: {len(processed_chunks)}/{len(chunks)}")
    print(f"Chunks needing retry: {incomplete}")
    print(f"Saved to: {FINAL_PATH}")

    return graph_data["entities"], graph_data["relationships"]


if __name__ == "__main__":
    from app.loaders.pdf_loader import load_pdf
    from app.processing.cleaner import clean_text
    from app.processing.chunker import chunk_text

    pdf_path = "data/documents/company_knowledge_base_graphrag.pdf"

    print("Loading PDF...")
    text = load_pdf(pdf_path)

    print("Cleaning text...")
    cleaned_text = clean_text(text)

    print("Creating chunks...")
    chunks = chunk_text(cleaned_text)

    print(f"Created {len(chunks)} chunks.")
    build_graph_data(chunks)

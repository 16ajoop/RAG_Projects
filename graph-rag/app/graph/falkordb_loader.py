
import json
import re
from pathlib import Path

from falkordb import FalkorDB


GRAPH_NAME = "aitch_graph"
DATA_PATH = Path("data/graph_data.json")


def safe_identifier(value: str) -> str:
    """Allow only safe identifiers for Cypher labels and relationship types."""
    if not re.fullmatch(r"[A-Z][A-Z0-9_]*", value):
        raise ValueError(f"Unsafe graph identifier: {value!r}")
    return value


def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"{DATA_PATH} not found. Run the graph extraction pipeline first."
        )

    with DATA_PATH.open("r", encoding="utf-8") as file:
        data = json.load(file)

    entities = data["entities"]
    relationships = data["relationships"]

    db = FalkorDB(host="localhost", port=6379)
    graph = db.select_graph(GRAPH_NAME)

    # Map entity names to their labels for relationship matching.
    entity_types = {}
    for entity in entities:
        name = entity["name"].strip()
        label = safe_identifier(entity["type"])
        entity_types[name] = label

        query = f"""
        MERGE (n:{label} {{name: $name}})
        SET n.type = $type
        """
        graph.query(
            query,
            {"name": name, "type": entity["type"]},
        )

    imported_relationships = 0
    skipped_relationships = []

    for rel in relationships:
        source = rel["source"].strip()
        target = rel["target"].strip()
        relation_type = safe_identifier(rel["relationship"])

        source_label = entity_types.get(source)
        target_label = entity_types.get(target)

        if not source_label or not target_label:
            skipped_relationships.append((source, relation_type, target))
            continue

        query = f"""
        MATCH (a:{source_label} {{name: $source}})
        MATCH (b:{target_label} {{name: $target}})
        MERGE (a)-[:{relation_type}]->(b)
        """
        graph.query(
            query,
            {"source": source, "target": target},
        )
        imported_relationships += 1

    node_result = graph.query(
        "MATCH (n) RETURN count(n) AS total"
    ).result_set
    relationship_result = graph.query(
        "MATCH ()-[r]->() RETURN count(r) AS total"
    ).result_set

    print("\nFalkorDB import complete")
    print(f"Graph: {GRAPH_NAME}")
    print(f"Entities in JSON: {len(entities)}")
    print(f"Relationships in JSON: {len(relationships)}")
    print(f"Relationships processed: {imported_relationships}")
    print(f"Relationships skipped: {len(skipped_relationships)}")
    print(f"Nodes currently in database: {node_result[0][0]}")
    print(f"Edges currently in database: {relationship_result[0][0]}")

    if skipped_relationships:
        print("\nRelationships with missing entity endpoints:")
        for edge in skipped_relationships:
            print(f"  {edge[0]} -[{edge[1]}]-> {edge[2]}")

    db.close()


if __name__ == "__main__":
    main()
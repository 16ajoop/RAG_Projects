import json
from app.graph.graph_database import get_graph

GRAPH_DATA_PATH = "data/graph_data.json"

def load_graph_data():
    """
    Load entities and relationships from graph_data.json
    into FalkorDB.
    """

    with open(GRAPH_DATA_PATH, "r", encoding = "utf-8") as file:
        graph_data = json.load(file)

    entities = graph_data["entities"]
    relationships = graph_data["relationships"]

    graph = get_graph()

    # Create entity nodes
    for entity in entities:
        query = """
        MERGE (n:Entity {name: $name})
        SET n.type = $type
        """

        graph.query(
            query,
            params={
                "name": entity["name"],
                "type": entity["type"],
            },
        )

    # Create relationships
    for relationship in relationships:
        query = f"""
        MATCH (source:Entity {{name: $source}})
        MATCH (target:Entity {{name: $target}})
        MERGE (source)-[:{relationship["relationship"]}]->(target)
        """

        graph.query(
            query,
            params={
                "source": relationship["source"],
                "target": relationship["target"],
            },
        )

    print(f"Loaded {len(entities)} entities.")
    print(f"Loaded {len(relationships)} relationships.")


if __name__ == "__main__":
    load_graph_data()
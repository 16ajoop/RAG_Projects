
from falkordb import FalkorDB


def main():
    db = FalkorDB(host="localhost", port=6379)
    graph = db.select_graph("aitch_graph")

    query = """
    MATCH (p:PROJECT {name: 'GraphMind'})
    OPTIONAL MATCH (p)-[r]-(related)
    RETURN p.name, type(r), related.name, labels(related)
    """

    result = graph.query(query)

    print("\nGraphMind and its connected entities:\n")

    for project, relationship, entity, entity_labels in result.result_set:
        print(
            f"Project: {project} | "
            f"Relationship: {relationship} | "
            f"Entity: {entity} | "
            f"Type: {entity_labels}"
        )

    db.close()


if __name__ == "__main__":
    main()
import networkx as nx

from app.graph.graph_database import get_graph

def load_graph_from_falkordb():
    """
    Read all entities and relationships from FalkorDB
    and build an undirected NetworkX graph.
    """

    graph = get_graph()

    nx_graph = nx.Graph()

    # Load ALL entities first
    node_result = graph.query(
        """
        MATCH (n:Entity)
        RETURN n.name
        """
    )

    for row in node_result.result_set:
        nx_graph.add_node(row[0])

    # Load relationships
    relationship_result = graph.query(
        """
        MATCH (a:Entity)-[r]->(b:Entity)
        RETURN a.name, b.name
        """
    )

    for row in relationship_result.result_set:
        source = row[0]
        target = row[1]

        nx_graph.add_edge(source, target)

    return nx_graph


def detect_communities(nx_graph):
    """
    Detect communities using NetworkX's
    greedy modularity algorithm.
    """

    communities = nx.community.greedy_modularity_communities(nx_graph)

    return communities


if __name__ == "__main__":
    graph = load_graph_from_falkordb()

    print(f"Nodes: {graph.number_of_nodes()}")
    print(f"Edges: {graph.number_of_edges()}")

    communities = detect_communities(graph)

    print(f"\nCommunities found: {len(communities)}")

    for index, community in enumerate(communities):
        print(f"\nCommunity {index}")
        print("-" * 30)

        for entity in sorted(community):
            print(entity)
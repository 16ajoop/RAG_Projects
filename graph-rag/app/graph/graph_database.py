from falkordb import FalkorDB

FALKORDB_HOST = "localhost"
FALKORDB_PORT = 6379
GRAPH_NAME = "AITechGraph"

def get_graph():
    """
    Connect to FalkorDB and return the AITechGraph graph.
    """
    db = FalkorDB(
        host = FALKORDB_HOST,
        port = FALKORDB_PORT
    )

    return db.select_graph(GRAPH_NAME)
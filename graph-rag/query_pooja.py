from app.graph.graph_database import get_graph

graph = get_graph()

query = """
MATCH (p:Entity {name: 'Pooja V'})-[r]->(x)
RETURN type(r), x.name, x.type
"""

result = graph.query(query)

for row in result.result_set:
    print(row)
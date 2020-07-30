import json


with open("./city_nodes.json", 'r') as f:
    nodes_json = f.read()
with open("./city_edges.json", 'r') as f:
    edges_json = f.read()

nodes = json.loads(nodes_json)
edges = json.loads(edges_json)

with open("./city_nodes.json", 'w') as f:
    json_nodes = json.dumps(nodes, sort_keys=True, indent=4, separators=(',', ': '))
    f.write(json_nodes)

with open("./city_edges.json", 'w') as f:
    json_edges = json.dumps(edges, sort_keys=True, indent=4, separators=(',', ': '))
    f.write(json_edges)
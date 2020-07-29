import json

'''
nodes_book = {
    "Oradea"            : {"value":30, "x":10, "y":10, "is_fixed":True},
    "Zerind"            : {"value":30},
    "Arad"              : {"value":30},
    "Timisoara"         : {"value":30},
    "Lugoj"             : {"value":30},
    "Mehadia"           : {"value":30},
    "Dobreta"           : {"value":30},
    "Craiova"           : {"value":30},
    "Pitesti"           : {"value":30},
    "Rimnicu Vilcea"    : {"value":30},
    "Sibiu"             : {"value":30},
    "Fagaras"           : {"value":30},
    "Bucharest"         : {"value":30},
    "Giurgiu"           : {"value":30},
    "Urziceni"          : {"value":30},
    "Vaslui"            : {"value":30},
    "Iasi"              : {"value":30},
    "Neamt"             : {"value":30},
    "Hirsova"           : {"value":30},
    "Eforie"            : {"value":30},
}
edges_book = [
        {"source":"Oradea", "target":"Zerind", "value":71},
        {"source":"Oradea", "target":"Sibiu", "value":151},
        {"source":"Zerind", "target":"Arad", "value":75},
        {"source":"Arad", "target":"Sibiu", "value":140},
        {"source":"Arad", "target":"Timisoara", "value":118},
        {"source":"Timisoara", "target":"Lugoj", "value":111},
        {"source":"Lugoj", "target":"Mehadia", "value":70},
        {"source":"Mehadia", "target":"Dobreta", "value":75},
        {"source":"Dobreta", "target":"Craiova", "value":120},
        {"source":"Craiova", "target":"Rimnicu Vilcea", "value":146},
        {"source":"Craiova", "target":"Pitesti", "value":138},
        {"source":"Rimnicu Vilcea", "target":"Sibiu", "value":80},
        {"source":"Rimnicu Vilcea", "target":"Pitesti", "value":97},
        {"source":"Pitesti", "target":"Bucharest", "value":101},
        {"source":"Sibiu", "target":"Fagaras", "value":99},
        {"source":"Fagaras", "target":"Bucharest", "value":211},
        {"source":"Bucharest", "target":"Giurgiu", "value":90},
        {"source":"Bucharest", "target":"Urziceni", "value":85},
        {"source":"Urziceni", "target":"Vaslui", "value":142},
        {"source":"Urziceni", "target":"Hirsova", "value":98},
        {"source":"Hirsova", "target":"Eforie", "value":86},
        {"source":"Vaslui", "target":"Iasi", "value":92},
        {"source":"Iasi", "target":"Neamt", "value":87}
    ]
'''

# nodes = json.dumps(nodes_book)
# print(nodes)
# # edges = json.dumps(edges_book)
# # print(edges)

with open("./romania/city_nodes.json", 'r') as f:
    nodes_json = f.read()
with open("./romania/city_edges.json", 'r') as f:
    edges_json = f.read()

nodes = json.loads(nodes_json)
edges = json.loads(edges_json)

print(nodes)
print(type(nodes))

print(edges)
print(type(edges))

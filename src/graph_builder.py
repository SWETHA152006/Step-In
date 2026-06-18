import json, math

def save_graph(nodes, edges, floor=1):
    with open(f"data/floor{floor}/nodes.json", "w") as f:
        json.dump(nodes, f, indent=2)
    with open(f"data/floor{floor}/edges.json", "w") as f:
        json.dump(edges, f, indent=2)

def load_graph(floor=1):
    try:
        nodes = json.load(open(f"data/floor{floor}/nodes.json"))
        edges = json.load(open(f"data/floor{floor}/edges.json"))
    except FileNotFoundError:
        nodes, edges = [], []
    return nodes, edges

def euclidean(a, b):
    return math.sqrt((a["x"]-b["x"])**2 + (a["y"]-b["y"])**2)
    
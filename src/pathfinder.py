import json
import networkx as nx
from src.graph_builder import load_graph, euclidean


def find_path_single_floor(start_id, goal_id, floor=1):
    nodes, edges = load_graph(floor)
    node_map = {n["id"]: n for n in nodes}

    G = nx.Graph()
    for n in nodes:
        G.add_node(n["id"])

    for e in edges:
        a, b = node_map[e["from"]], node_map[e["to"]]
        G.add_edge(e["from"], e["to"], weight=euclidean(a, b))

    path = nx.shortest_path(G, start_id, goal_id, weight="weight")
    return path, node_map


def get_vertical_node(nodes, preferred_type=None):
    vertical_nodes = [
        n for n in nodes
        if "Stair" in n["label"] or "Elevator" in n["label"]
    ]

    if not vertical_nodes:
        return None

    if preferred_type:
        for node in vertical_nodes:
            if preferred_type.lower() in node["label"].lower():
                return node

    return vertical_nodes[0]


def detect_connector_type(label):
    label_lower = label.lower()
    if "elevator" in label_lower:
        return "Elevator"
    if "stair" in label_lower:
        return "Stair"
    return "Connector"


def find_path_multi_floor(start_id, start_floor, goal_id, goal_floor):
    """
    Returns a list of route steps.
    Each item is either:
    - ("path", floor_num, path, node_map)
    - ("transition", from_floor, to_floor, connector_type)
    """

    if start_floor == goal_floor:
        path, node_map = find_path_single_floor(start_id, goal_id, start_floor)
        return [("path", start_floor, path, node_map)]

    try:
        with open("data/stairs.json", "r") as f:
            stairs_data = json.load(f)
    except Exception:
        stairs_data = []

    start_nodes, _ = load_graph(start_floor)
    goal_nodes, _ = load_graph(goal_floor)

    preferred_type = None
    if stairs_data:
        preferred_type = stairs_data[0].get("type")

    start_connector = get_vertical_node(start_nodes, preferred_type)
    goal_connector = get_vertical_node(goal_nodes, preferred_type)

    if not start_connector or not goal_connector:
        path, node_map = find_path_single_floor(start_id, goal_id, start_floor)
        return [("path", start_floor, path, node_map)]

    connector_type = detect_connector_type(start_connector["label"])

    path1, nm1 = find_path_single_floor(start_id, start_connector["id"], start_floor)
    path2, nm2 = find_path_single_floor(goal_connector["id"], goal_id, goal_floor)

    return [
        ("path", start_floor, path1, nm1),
        ("transition", start_floor, goal_floor, connector_type),
        ("path", goal_floor, path2, nm2),
    ]

import streamlit as st
from src.graph_builder import load_graph
from src.pathfinder import find_path_multi_floor
from src.renderer import draw_path
import math
import base64

PIXELS_PER_METRE = 713 / 12
FLOOR_NAMES = {1: "Floor 1", 2: "Floor 2", 3: "Floor 3"}
FLOOR_ICONS = {1: "1️⃣", 2: "2️⃣", 3: "3️⃣"}

ROOM_ICONS = {
    "Entrance": "🚪", "Bedroom": "🛏️", "Bathroom": "🚿",
    "Kitchen": "🍳", "Dining": "🍽️", "Living": "🛋️",
    "Utility": "🔧", "Stair": "🪜", "Elevator": "🛗",
    "Office": "💼", "Conference": "📋", "Lobby": "🏛️",
}

def get_icon(label):
    for key, icon in ROOM_ICONS.items():
        if key.lower() in label.lower():
            return icon
    return "📍"

def img_to_base64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None

st.set_page_config(page_title="Step-in Navigation", layout="wide")

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
        font-family: 'Segoe UI', sans-serif;
    }
    section[data-testid="stSidebar"] {
        background: #111111 !important;
        border-right: 1px solid #333;
    }
    section[data-testid="stSidebar"] * { color: #ccc !important; }
    .route-card {
        background: linear-gradient(135deg, #1a1a1a, #222222);
        border: 1px solid #333;
        border-radius: 16px;
        padding: 20px 24px;
        margin: 10px 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #1e1e1e, #2a2a2a);
        border: 1px solid #444;
        border-radius: 14px;
        padding: 20px;
        text-align: center;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #c0c0c0, #ffffff, #a0a0a0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-label {
        font-size: 0.78rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-top: 4px;
    }
    .floor-badge {
        background: #222;
        border: 1px solid #444;
        color: #aaa;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 8px;
    }
    .stButton > button {
        background: linear-gradient(135deg, #2a2a2a, #3a3a3a) !important;
        color: #ddd !important;
        border: 1px solid #555 !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

logo_b64 = img_to_base64("assets/logo.png")
logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="height:70px; border-radius:12px;">' if logo_b64 else "🧭"

st.markdown(f"""
<div style='background: linear-gradient(135deg, #1a1a1a, #2a2a2a);
     border:1px solid #333; border-radius:20px; padding:24px 32px;
     margin-bottom:24px; display:flex; align-items:center; gap:20px;'>
    {logo_html}
    <div>
        <h1 style='background: linear-gradient(135deg, #c0c0c0, #fff, #a8a8a8);
             -webkit-background-clip:text; -webkit-text-fill-color:transparent;
             font-size:2rem; font-weight:800; margin:0;'>Step-in</h1>
        <p style='color:#666; margin:4px 0 0; font-size:0.85rem;
             letter-spacing:2px; text-transform:uppercase;'>Multi-Floor Indoor Navigation</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Floor selector
st.markdown("<div class='route-card'>", unsafe_allow_html=True)
st.markdown("**🏢 Select Floors**")
col1, col2 = st.columns(2)
with col1:
    start_floor = st.selectbox("Start Floor", [1, 2, 3],
        format_func=lambda x: f"{FLOOR_ICONS[x]} {FLOOR_NAMES[x]}")
with col2:
    goal_floor = st.selectbox("Destination Floor", [1, 2, 3],
        format_func=lambda x: f"{FLOOR_ICONS[x]} {FLOOR_NAMES[x]}")
st.markdown("</div>", unsafe_allow_html=True)

# Load rooms for selected floors
start_nodes, _ = load_graph(start_floor)
goal_nodes, _ = load_graph(goal_floor)

start_rooms = [n for n in start_nodes if not any(
    k in n["label"] for k in ["Door", "Hallway", "Corridor"])]
goal_rooms = [n for n in goal_nodes if not any(
    k in n["label"] for k in ["Door", "Hallway", "Corridor"])]

start_labels = {n["id"]: n["label"] for n in start_nodes}
goal_labels = {n["id"]: n["label"] for n in goal_nodes}

st.markdown("<div class='route-card'>", unsafe_allow_html=True)
st.markdown("**📍 Select Rooms**")
col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    st.markdown("**🟢 Start Room**")
    start_id = st.selectbox("start_room", [n["id"] for n in start_rooms],
        format_func=lambda x: f"{get_icon(start_labels[x])} {start_labels[x]}",
        label_visibility="collapsed")
with col2:
    st.markdown("**🔴 Destination Room**")
    goal_id = st.selectbox("goal_room", [n["id"] for n in goal_rooms],
        format_func=lambda x: f"{get_icon(goal_labels[x])} {goal_labels[x]}",
        label_visibility="collapsed")
with col3:
    st.markdown("&nbsp;")
    find = st.button("🔍 Find Route", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

if find:
    try:
        segments = find_path_multi_floor(start_id, start_floor, goal_id, goal_floor)

        # Calculate total distance (only path segments, skip transitions)
        total_px = 0
        floors_used = []
        for segment in segments:
            if segment[0] != "path":
                continue
            _, floor_num, path, node_map = segment
            floors_used.append(floor_num)
            for i in range(len(path) - 1):
                a = node_map[path[i]]
                b = node_map[path[i + 1]]
                total_px += math.sqrt((a["x"] - b["x"])**2 + (a["y"] - b["y"])**2)

        total_metres = total_px / PIXELS_PER_METRE
        walk_seconds = int(total_metres / 1.4)

        # Metrics row
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""<div class='metric-card'>
                <div class='metric-value'>📏 {total_metres:.1f}m</div>
                <div class='metric-label'>Total Distance</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class='metric-card'>
                <div class='metric-value'>⏱️ {walk_seconds}s</div>
                <div class='metric-label'>Walking Time</div>
            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class='metric-card'>
                <div class='metric-value'>🏢 {len(set(floors_used))}</div>
                <div class='metric-label'>Floors</div>
            </div>""", unsafe_allow_html=True)

        # Multi-floor route summary
        if len(set(floors_used)) > 1:
            path_floors = list(dict.fromkeys(floors_used))
            floor_route = " → ".join([
                f"{FLOOR_ICONS[f]} {FLOOR_NAMES[f]}" for f in path_floors
            ])
            st.markdown(f"""
            <div class='route-card' style='text-align:center; margin-top:12px;'>
                <div style='font-size:0.85rem; color:#666; letter-spacing:1px;
                     text-transform:uppercase;'>Multi-floor Route</div>
                <div style='margin-top:8px; font-size:1.1rem; color:#fff;
                     font-weight:600;'>{floor_route}</div>
                <div style='margin-top:6px; font-size:0.85rem; color:#555;'>
                    Use stairs or elevator between floors
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Render each segment
        path_segment_count = sum(1 for s in segments if s[0] == "path")
        rendered = 0

        for idx, segment in enumerate(segments):

            # Transition card
            if segment[0] == "transition":
                _, from_floor, to_floor, connector_type = segment
                icon = "🪜" if connector_type == "Stair" else "🛗"
                st.markdown(f"""
                <div style='text-align:center; padding:16px; margin:8px 0;
                     background:#1a1a1a; border:1px solid #333; border-radius:12px;
                     color:#bbb; font-size:1rem; font-weight:600; letter-spacing:0.5px;'>
                    {icon} Take {connector_type} from
                    {FLOOR_ICONS[from_floor]} {FLOOR_NAMES[from_floor]}
                    → {FLOOR_ICONS[to_floor]} {FLOOR_NAMES[to_floor]}
                </div>
                """, unsafe_allow_html=True)
                continue

            # Path segment
            _, floor_num, path, node_map = segment
            rendered += 1

            st.markdown(
                f"<div class='floor-badge'>{FLOOR_ICONS[floor_num]} "
                f"{FLOOR_NAMES[floor_num]}</div>",
                unsafe_allow_html=True
            )

            output = draw_path(
                f"assets/floor{floor_num}/floorplan.png", node_map, path
            )

            col_map, col_steps = st.columns([3, 1])

            with col_map:
                st.markdown("<div class='route-card'>", unsafe_allow_html=True)
                st.image(output, width=900)
                st.markdown("</div>", unsafe_allow_html=True)

            with col_steps:
                st.markdown("<div class='route-card'>", unsafe_allow_html=True)
                st.markdown("**📋 Directions**")
                labels = {n["id"]: n["label"] for n in load_graph(floor_num)[0]}
                room_path = [
                    n for n in path
                    if not any(
                        k in labels.get(n, "")
                        for k in ["Door", "Hallway", "Corridor"]
                    )
                ]
                is_first_segment = rendered == 1
                is_last_segment = rendered == path_segment_count

                for i, nid in enumerate(room_path):
                    label = labels.get(nid, str(nid))
                    icon = get_icon(label)
                    if i == 0 and is_first_segment:
                        color = "#22c55e"
                    elif i == len(room_path) - 1 and is_last_segment:
                        color = "#ef4444"
                    else:
                        color = "#888888"
                    st.markdown(f"""
                    <div style='display:flex; align-items:center; padding:8px 0;
                         border-bottom:1px solid #2a2a2a;'>
                        <span style='background:{color}; color:white; border-radius:50%;
                             width:26px; height:26px; display:inline-flex;
                             align-items:center; justify-content:center;
                             font-size:0.75rem; font-weight:700;
                             margin-right:10px; flex-shrink:0;'>{i+1}</span>
                        <span style='color:#ccc;'>{icon} {label}</span>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"No path found: {e}")
        
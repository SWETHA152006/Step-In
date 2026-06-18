import streamlit as st
from PIL import Image, ImageDraw
from src.graph_builder import save_graph, load_graph

st.title("Map Editor — place nodes")

floor = st.selectbox("Select Floor to Edit", [1, 2, 3], format_func=lambda x: f"Floor {x}")
img = Image.open(f"assets/floor{floor}/floorplan.png")
W, H = img.size

# Display width in the app
DISPLAY_W = 700
scale = DISPLAY_W / W

nodes, edges = load_graph(floor)

st.subheader("1. Your floor plan")
st.image(img, width=DISPLAY_W)
st.caption(f"Image size: {W}x{H}px | Displayed at: {DISPLAY_W}x{int(H*scale)}px")

st.info(f"When you click on the displayed image, multiply your click position by {round(1/scale, 2)} to get real coordinates. OR just use the room coordinates below directly.")

st.subheader("2. Add nodes — click a room on the image above, estimate position")

# Show a scaled coordinate helper
with st.expander("📍 How to find coordinates"):
    st.write(f"The image is displayed at {DISPLAY_W}px wide but the real image is {W}px wide.")
    st.write(f"Scale factor: {round(1/scale,2)}x")
    st.write("Example: if a room looks like it's at x=350 on screen, real X = 350 × 2.17 ≈ 760")
    cx = st.number_input("Screen X (what you see on display)", 0, DISPLAY_W, 300)
    cy = st.number_input("Screen Y (what you see on display)", 0, int(H*scale), 300)
    st.success(f"Real coordinates → X: {int(cx/scale)}, Y: {int(cy/scale)}")

with st.form("add_nodes"):
    col1, col2, col3 = st.columns(3)
    label = col1.text_input("Room name", placeholder="e.g. Kitchen")
    x = col2.number_input("X (real pixels)", min_value=0, max_value=W, value=400)
    y = col3.number_input("Y (real pixels)", min_value=0, max_value=H, value=400)
    add = st.form_submit_button("Add node")

if add and label:
    new_id = len(nodes)
    nodes.append({"id": new_id, "x": int(x), "y": int(y), "label": label})
    save_graph(nodes, edges, floor)
    st.success(f"Added node {new_id}: {label} at ({x}, {y})")

if nodes:
    st.subheader("3. Current nodes")
    for n in nodes:
        st.write(f"**{n['id']}** — {n['label']} at ({n['x']}, {n['y']})")

    st.subheader("4. Connect nodes")
    with st.form("add_edges"):
        col1, col2 = st.columns(2)
        from_id = col1.number_input("From node ID", min_value=0, value=0)
        to_id = col2.number_input("To node ID", min_value=0, value=1)
        add_edge = st.form_submit_button("Add edge")

    if add_edge:
        edges.append({"from": int(from_id), "to": int(to_id)})
        save_graph(nodes, edges, floor)
        st.success(f"Connected node {from_id} → {to_id}")

    st.write(f"Total edges: {len(edges)}")

    if st.button("Clear all nodes and edges"):
        save_graph([], [], floor)
        st.rerun()

    st.subheader("5. Preview nodes on map")
    preview = img.copy().convert("RGB")
    draw = ImageDraw.Draw(preview)
    for n in nodes:
        x, y = n["x"], n["y"]
        draw.ellipse([x-18, y-18, x+18, y+18], fill="red")
        draw.text((x+20, y-10), n["label"], fill="red")
    st.image(preview, width=DISPLAY_W)
    
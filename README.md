# 🧭 Step-in — Indoor Navigation System

Step-in is a blueprint-based indoor navigation prototype that helps users find the shortest walking path between rooms inside a building — across multiple floors.

Built with Python, Streamlit, NetworkX (Dijkstra pathfinding), and OpenCV.

---

## ✨ Features

- 📍 **Blueprint-based navigation** — upload any floor plan image and place rooms/doors as nodes
- 🧮 **Shortest path routing** — Dijkstra's algorithm finds the optimal route via NetworkX
- 🚪 **Realistic corridor routing** — paths travel through actual doorways and hallways, not straight through walls
- 🏢 **Multi-floor support** — navigate across Floor 1, Floor 2, Floor 3 via staircases or elevator
- 📏 **Distance & walking time** — see route length in metres and estimated walking time
- 🎨 **Branded dark UI** — silver gradient theme with step-by-step directions panel

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Pathfinding | NetworkX (Dijkstra) |
| Image Processing | OpenCV, Pillow |
| Graph Storage | JSON |

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/SWETHA152006/Step-In.git
cd Step-In
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
streamlit run app.py
```

The app will open automatically at `http://localhost:8501`

---

## 📁 Project Structure

```
Step-In/
├── app.py                  # Home page
├── requirements.txt
├── assets/
│   ├── floor1/floorplan.png
│   ├── floor2/floorplan.png
│   ├── floor3/floorplan.png
│   └── logo.png
├── data/
│   ├── floor1/ (nodes.json, edges.json)
│   ├── floor2/
│   └── floor3/
├── src/
│   ├── graph_builder.py    # Save/load graph data
│   ├── pathfinder.py       # Dijkstra shortest path logic
│   └── renderer.py         # Draws route on floor plan
└── pages/
    ├── 1_Map_Editor.py     # Place rooms & doors on the map
    └── 2_Find_Route.py     # Select start/destination, view route
```

---

## 🗺️ How to Use

1. Go to **Map Editor** → select a floor → add room nodes with X,Y coordinates
2. Connect nodes with edges to form corridors and doorways
3. Go to **Find Route** → select start floor/room and destination floor/room
4. Click **Find Route** to see the shortest path drawn on the map, with distance and step-by-step directions

---

## 🔭 Roadmap

- [ ] QR code-based real-time positioning
- [ ] Mobile app (Flutter)
- [ ] AR navigation overlay
- [ ] Emergency exit routing

---

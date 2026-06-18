import streamlit as st
import base64

def img_to_base64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None

st.set_page_config(page_title="Step-in", page_icon="assets/logo.png", layout="wide")

logo_b64 = img_to_base64("assets/logo.png")

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
    }
    section[data-testid="stSidebar"] {
        background: #111111 !important;
        border-right: 1px solid #333;
    }
    section[data-testid="stSidebar"] * { color: #ccc !important; }

    /* Push nav links down */
    section[data-testid="stSidebar"] > div {
        padding-top: 0 !important;
    }
    [data-testid="stSidebarNav"] {
        margin-top: 0 !important;
        padding-top: 8px !important;
    }
    /* Style the nav links */
    [data-testid="stSidebarNav"] a {
        padding: 8px 16px !important;
    }
    [data-testid="stSidebarNav"] a span {
        color: #aaa !important;
        font-size: 0.9rem !important;
    }
    [data-testid="stSidebarNav"] a[aria-current="page"] span {
        color: #fff !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# Logo at very top of sidebar
if logo_b64:
    st.sidebar.markdown(f"""
    <div style='display:flex; align-items:center; gap:10px;
         padding:20px 16px 16px; border-bottom:1px solid #2a2a2a; margin-bottom:4px;'>
        <img src="data:image/png;base64,{logo_b64}"
             style="height:40px; width:40px; border-radius:10px; object-fit:cover;">
        <div>
            <div style='color:#e0e0e0; font-weight:700; font-size:1.05rem;
                 letter-spacing:0.5px;'>Step-in</div>
            <div style='color:#555; font-size:0.68rem;
                 letter-spacing:1.5px; text-transform:uppercase;'>Indoor Nav</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Home page
if logo_b64:
    st.markdown(f"""
    <div style='display:flex; flex-direction:column; align-items:center;
         justify-content:center; min-height:70vh; text-align:center;'>
        <img src="data:image/png;base64,{logo_b64}"
             style="height:200px; border-radius:24px; margin-bottom:28px;
             box-shadow: 0 8px 32px rgba(0,0,0,0.6);">
        <h1 style='background: linear-gradient(135deg, #c0c0c0, #ffffff, #a8a8a8);
             -webkit-background-clip:text; -webkit-text-fill-color:transparent;
             font-size:3rem; font-weight:800; margin:0;'>Step-in</h1>
        <p style='color:#555; font-size:0.85rem; letter-spacing:2.5px;
             text-transform:uppercase; margin:8px 0 40px;'>Indoor Navigation System</p>
        <div style='display:flex; gap:16px;'>
            <a href='/Map_Editor' target='_self'
               style='background:#1a1a1a; border:1px solid #3a3a3a; color:#bbb;
               padding:14px 28px; border-radius:12px; text-decoration:none;
               font-weight:600; font-size:0.95rem; letter-spacing:0.3px;'>🗺️ Map Editor</a>
            <a href='/Find_Route' target='_self'
               style='background:#1a1a1a; border:1px solid #3a3a3a; color:#bbb;
               padding:14px 28px; border-radius:12px; text-decoration:none;
               font-weight:600; font-size:0.95rem; letter-spacing:0.3px;'>🧭 Find Route</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
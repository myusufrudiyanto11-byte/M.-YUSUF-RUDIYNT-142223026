import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime

# ══════════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="🏗️ CraneMon — Maintenance Intelligence",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════
# GLOBAL STYLE — Dark Green Industrial
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Root ── */
:root {
    --bg-base:    #080d0a;
    --bg-card:    #0f1a12;
    --bg-card2:   #152019;
    --bg-border:  #1e3324;
    --green-1:    #00e676;
    --green-2:    #69f0ae;
    --green-3:    #1de9b6;
    --green-dim:  #2e7d52;
    --amber:      #ffca28;
    --red:        #ff5252;
    --blue:       #40c4ff;
    --text-pri:   #e8f5e9;
    --text-sec:   #81c784;
    --text-dim:   #4a7c5a;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background: var(--bg-base) !important;
}

/* ── App background ── */
.stApp {
    background: radial-gradient(ellipse at 0% 0%, #0a1f0e 0%, #080d0a 50%, #050a07 100%) !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a1a0d 0%, #060e08 100%) !important;
    border-right: 1px solid #1e3324 !important;
}
[data-testid="stSidebar"] * { color: var(--text-pri) !important; }
[data-testid="stSidebarContent"] { padding-top: 0 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0a1a0d; }
::-webkit-scrollbar-thumb { background: #1e4d2b; border-radius: 3px; }

/* ── Metric cards ── */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #0f1a12 0%, #152019 100%) !important;
    border: 1px solid #1e3324 !important;
    border-radius: 12px !important;
    padding: 18px 20px !important;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
}
[data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(0,230,118,0.12) !important;
    border-color: #2e7d52 !important;
}
[data-testid="stMetric"]::before {
    content: '';
    position: absolute; top: 0; left: 0;
    width: 3px; height: 100%;
    background: linear-gradient(180deg, #00e676, #1de9b6);
    border-radius: 3px 0 0 3px;
}
[data-testid="stMetricLabel"] { color: #4a7c5a !important; font-size: 0.72rem !important; text-transform: uppercase; letter-spacing: 0.8px; }
[data-testid="stMetricValue"] { color: #e8f5e9 !important; font-size: 1.65rem !important; font-weight: 700 !important; }

/* ── Section headers ── */
.sec-header {
    display: flex; align-items: center; gap: 10px;
    background: linear-gradient(90deg, #0f1a12, transparent);
    border-left: 3px solid #00e676;
    border-radius: 0 6px 6px 0;
    padding: 9px 16px;
    margin: 22px 0 14px 0;
    font-size: 0.88rem; font-weight: 600;
    color: #a5d6a7; letter-spacing: 0.3px;
}

/* ── KPI hero card ── */
.hero-card {
    background: linear-gradient(135deg, #0a1f0e 0%, #0f2a14 50%, #0a1f0e 100%);
    border: 1px solid #1e4d2b;
    border-radius: 16px;
    padding: 24px 30px 20px;
    margin-bottom: 22px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 4px 40px rgba(0,230,118,0.06);
}
.hero-card::after {
    content: '';
    position: absolute; top: -60px; right: -60px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(0,230,118,0.06) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-size: 1.55rem; font-weight: 800;
    color: #e8f5e9; letter-spacing: -0.3px;
}
.hero-sub {
    font-size: 0.8rem; color: #4a7c5a;
    margin-top: 3px; font-family: 'JetBrains Mono', monospace;
}
.hero-badge {
    display: inline-block;
    background: rgba(0,230,118,0.12);
    border: 1px solid rgba(0,230,118,0.3);
    color: #00e676; border-radius: 20px;
    padding: 3px 12px; font-size: 0.7rem;
    font-weight: 600; margin-left: 10px;
    vertical-align: middle;
}

/* ── Status badges ── */
.tag-ok   { background:rgba(0,230,118,0.1); color:#00e676; border:1px solid rgba(0,230,118,0.3); border-radius:20px; padding:2px 10px; font-size:0.72rem; font-weight:600; }
.tag-warn { background:rgba(255,202,40,0.1); color:#ffca28; border:1px solid rgba(255,202,40,0.3); border-radius:20px; padding:2px 10px; font-size:0.72rem; font-weight:600; }
.tag-crit { background:rgba(255,82,82,0.1);  color:#ff5252; border:1px solid rgba(255,82,82,0.3);  border-radius:20px; padding:2px 10px; font-size:0.72rem; font-weight:600; }

/* ── Alert banners ── */
.alert-crit {
    background: linear-gradient(90deg, rgba(255,82,82,0.08), rgba(255,82,82,0.02));
    border: 1px solid rgba(255,82,82,0.35);
    border-left: 3px solid #ff5252;
    border-radius: 8px; padding: 10px 14px; margin: 5px 0;
    color: #ff8a80; font-size: 0.82rem;
}
.alert-warn {
    background: linear-gradient(90deg, rgba(255,202,40,0.08), rgba(255,202,40,0.02));
    border: 1px solid rgba(255,202,40,0.3);
    border-left: 3px solid #ffca28;
    border-radius: 8px; padding: 10px 14px; margin: 5px 0;
    color: #ffe082; font-size: 0.82rem;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #0a1a0d !important;
    border-radius: 10px !important;
    padding: 5px !important; gap: 4px;
    border: 1px solid #1e3324;
}
.stTabs [data-baseweb="tab"] {
    color: #4a7c5a !important;
    border-radius: 7px !important;
    font-weight: 500 !important; font-size: 0.82rem;
    padding: 8px 16px !important;
    transition: all 0.2s;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #1a4d2b, #0f3320) !important;
    color: #00e676 !important;
    box-shadow: 0 0 12px rgba(0,230,118,0.15) !important;
}

/* ── Selectbox / inputs ── */
[data-testid="stSelectbox"] > div > div {
    background: #0f1a12 !important;
    border: 1px solid #1e3324 !important;
    border-radius: 8px !important;
    color: #a5d6a7 !important;
}
.stSlider [data-baseweb="slider"] { accent-color: #00e676; }

/* ── Dataframe ── */
[data-testid="stDataFrame"] { border-radius: 10px !important; }
iframe { border-radius: 10px; }

/* ── Pulse animation ── */
@keyframes pulse-green {
    0%, 100% { box-shadow: 0 0 0 0 rgba(0,230,118,0.3); }
    50%       { box-shadow: 0 0 0 6px rgba(0,230,118,0); }
}
.pulse { animation: pulse-green 2.5s infinite; }

/* ── Number counter animation ── */
@keyframes fadeSlideUp {
    from { opacity:0; transform: translateY(10px); }
    to   { opacity:1; transform: translateY(0); }
}
.fade-up { animation: fadeSlideUp 0.5s ease forwards; }

/* ── Progress bar ── */
.prog-bar-wrap { background:#0f1a12; border-radius:20px; height:8px; overflow:hidden; margin:4px 0; }
.prog-bar-fill { height:100%; border-radius:20px; transition: width 1s ease; }

/* ── Footer ── */
.footer {
    text-align:center; padding: 16px 0 6px;
    color: #2e7d52; font-size: 0.72rem;
    font-family: 'JetBrains Mono', monospace;
    border-top: 1px solid #0f1a12;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════
@st.cache_data
def load_data():
    bd = pd.DataFrame({
        "ID": [f"BD-{str(i).zfill(4)}" for i in range(1,121)],
        "Tanggal": ["2024-01-04","2024-01-13","2024-01-14","2024-01-16","2024-01-17","2024-01-17","2024-01-23","2024-01-24","2024-01-29","2024-02-03",
                    "2024-02-05","2024-02-06","2024-02-10","2024-02-10","2024-02-14","2024-02-17","2024-02-17","2024-02-19","2024-02-21","2024-02-22",
                    "2024-02-22","2024-02-27","2024-03-04","2024-03-12","2024-03-12","2024-03-14","2024-03-20","2024-03-22","2024-03-24","2024-03-24",
                    "2024-03-28","2024-04-08","2024-04-11","2024-04-17","2024-04-18","2024-04-18","2024-04-20","2024-04-21","2024-04-22","2024-04-22",
                    "2024-04-24","2024-04-26","2024-04-27","2024-04-29","2024-04-29","2024-05-05","2024-05-05","2024-05-06","2024-05-15","2024-05-15",
                    "2024-05-16","2024-05-17","2024-05-18","2024-05-20","2024-05-22","2024-05-22","2024-05-22","2024-05-28","2024-05-30","2024-06-10",
                    "2024-06-10","2024-06-15","2024-06-21","2024-06-23","2024-06-25","2024-06-30","2024-07-02","2024-07-04","2024-07-05","2024-07-08",
                    "2024-07-12","2024-07-13","2024-07-13","2024-07-13","2024-07-21","2024-07-24","2024-08-02","2024-08-04","2024-08-04","2024-08-17",
                    "2024-08-20","2024-08-22","2024-08-23","2024-08-24","2024-09-12","2024-09-15","2024-09-30","2024-10-01","2024-10-06","2024-10-06",
                    "2024-10-09","2024-10-12","2024-10-14","2024-10-17","2024-10-22","2024-10-28","2024-10-29","2024-11-04","2024-11-05","2024-11-07",
                    "2024-11-12","2024-11-17","2024-11-21","2024-11-21","2024-11-23","2024-11-23","2024-11-25","2024-11-27","2024-11-28","2024-12-01",
                    "2024-12-04","2024-12-09","2024-12-12","2024-12-15","2024-12-16","2024-12-18","2024-12-23","2024-12-25","2024-12-25","2024-12-26"],
        "Bulan": ["January","January","January","January","January","January","January","January","January","February",
                  "February","February","February","February","February","February","February","February","February","February",
                  "February","February","March","March","March","March","March","March","March","March",
                  "March","April","April","April","April","April","April","April","April","April",
                  "April","April","April","April","April","May","May","May","May","May",
                  "May","May","May","May","May","May","May","May","May","June",
                  "June","June","June","June","June","June","July","July","July","July",
                  "July","July","July","July","July","July","August","August","August","August",
                  "August","August","August","August","September","September","September","October","October","October",
                  "October","October","October","October","October","October","October","November","November","November",
                  "November","November","November","November","November","November","November","November","November","December",
                  "December","December","December","December","December","December","December","December","December","December"],
        "Crane ID": ["HC-05","HC-04","HC-04","HC-02","HC-05","HC-01","HC-01","HC-01","HC-01","HC-03",
                     "HC-03","HC-03","HC-01","HC-02","HC-05","HC-02","HC-05","HC-01","HC-02","HC-01",
                     "HC-02","HC-02","HC-04","HC-04","HC-01","HC-01","HC-04","HC-04","HC-01","HC-02",
                     "HC-04","HC-04","HC-05","HC-02","HC-01","HC-01","HC-05","HC-05","HC-01","HC-02",
                     "HC-02","HC-01","HC-05","HC-03","HC-02","HC-05","HC-02","HC-02","HC-02","HC-01",
                     "HC-01","HC-04","HC-01","HC-05","HC-01","HC-02","HC-04","HC-02","HC-04","HC-04",
                     "HC-04","HC-01","HC-01","HC-03","HC-05","HC-04","HC-05","HC-01","HC-04","HC-03",
                     "HC-04","HC-04","HC-05","HC-04","HC-04","HC-01","HC-02","HC-01","HC-01","HC-04",
                     "HC-01","HC-01","HC-02","HC-05","HC-04","HC-05","HC-01","HC-03","HC-02","HC-04",
                     "HC-01","HC-05","HC-03","HC-02","HC-04","HC-02","HC-05","HC-02","HC-04","HC-03",
                     "HC-01","HC-02","HC-02","HC-04","HC-03","HC-03","HC-05","HC-05","HC-01","HC-04",
                     "HC-04","HC-04","HC-03","HC-04","HC-01","HC-05","HC-04","HC-03","HC-03","HC-02"],
        "Kategori": ["Electrical/Control","Electrical/Control","Motor/Drive","Mechanical","Electrical/Control","Motor/Drive","Electrical/Control","Motor/Drive","Electrical/Control","Electrical/Control",
                     "Electrical/Control","Electrical/Control","Motor/Drive","Planned Overhaul","Electrical/Control","Electrical/Control","Electrical/Control","Electrical/Control","Electrical/Control","Mechanical",
                     "Mechanical","Electrical/Control","Mechanical","Mechanical","Motor/Drive","Electrical/Control","Mechanical","Electrical/Control","Planned Overhaul","Mechanical",
                     "Mechanical","Electrical/Control","Electrical/Control","Electrical/Control","Electrical/Control","Planned Overhaul","Electrical/Control","Electrical/Control","Electrical/Control","Motor/Drive",
                     "Electrical/Control","Electrical/Control","Electrical/Control","Electrical/Control","Motor/Drive","Electrical/Control","Electrical/Control","Motor/Drive","Mechanical","Motor/Drive",
                     "Motor/Drive","Motor/Drive","Electrical/Control","Motor/Drive","Electrical/Control","Motor/Drive","Electrical/Control","Mechanical","Motor/Drive","Electrical/Control",
                     "Planned Overhaul","Electrical/Control","Planned Overhaul","Mechanical","Planned Overhaul","Motor/Drive","Mechanical","Electrical/Control","Mechanical","Mechanical",
                     "Mechanical","Motor/Drive","Electrical/Control","Mechanical","Mechanical","Electrical/Control","Motor/Drive","Mechanical","Electrical/Control","Electrical/Control",
                     "Motor/Drive","Planned Overhaul","Electrical/Control","Electrical/Control","Mechanical","Electrical/Control","Electrical/Control","Electrical/Control","Motor/Drive","Electrical/Control",
                     "Electrical/Control","Planned Overhaul","Electrical/Control","Electrical/Control","Mechanical","Electrical/Control","Motor/Drive","Mechanical","Electrical/Control","Mechanical",
                     "Electrical/Control","Electrical/Control","Mechanical","Planned Overhaul","Electrical/Control","Mechanical","Electrical/Control","Electrical/Control","Motor/Drive","Electrical/Control",
                     "Electrical/Control","Mechanical","Electrical/Control","Electrical/Control","Electrical/Control","Electrical/Control","Planned Overhaul","Electrical/Control","Electrical/Control","Electrical/Control"],
        "Komponen": ["Kabel Power","Kabel Power","Rem Motor","Hook","Sensor Limit","Rem Motor","Panel Kontrol","Gearbox","Kabel Power","Relay",
                     "Kabel Power","Panel Kontrol","Rem Motor","Penggantian Oli","Panel Kontrol","Kabel Power","Sensor Limit","Relay","Kabel Power","Hook",
                     "Struktur Girder","Kabel Power","Hook","Wire Rope","Gearbox","Panel Kontrol","Struktur Girder","Panel Kontrol","Overhaul Berkala","Hook",
                     "Hook","Kontaktor","Sensor Limit","Panel Kontrol","Panel Kontrol","Penggantian Oli","Kontaktor","Kontaktor","Kabel Power","Inverter",
                     "Sensor Limit","Kontaktor","Kontaktor","Relay","Inverter","Kabel Power","Kontaktor","Rem Motor","Sheave","Inverter",
                     "Motor Hoist","Motor Travel","Kontaktor","Inverter","Relay","Inverter","Kabel Power","Hook","Inverter","Kontaktor",
                     "Penggantian Oli","Relay","Kalibrasi","Struktur Girder","Penggantian Oli","Rem Motor","Struktur Girder","Panel Kontrol","Sheave","Wire Rope",
                     "Sheave","Motor Travel","Sensor Limit","Hook","Bearing","Relay","Motor Hoist","Hook","Kabel Power","Sensor Limit",
                     "Motor Hoist","Inspeksi Rutin","Sensor Limit","Sensor Limit","Hook","Panel Kontrol","Sensor Limit","Panel Kontrol","Motor Travel","Kontaktor",
                     "Sensor Limit","Overhaul Berkala","Panel Kontrol","Sensor Limit","Wire Rope","Sensor Limit","Gearbox","Bearing","Panel Kontrol","Sheave",
                     "Panel Kontrol","Panel Kontrol","Hook","Penggantian Oli","Sensor Limit","Hook","Panel Kontrol","Kontaktor","Rem Motor","Kabel Power",
                     "Kontaktor","Sheave","Kabel Power","Sensor Limit","Relay","Sensor Limit","Overhaul Berkala","Relay","Kabel Power","Kontaktor"],
        "Keparahan": ["Tinggi","Rendah","Sedang","Rendah","Sedang","Rendah","Sedang","Rendah","Tinggi","Rendah",
                      "Sedang","Sedang","Rendah","Tinggi","Rendah","Rendah","Sedang","Tinggi","Tinggi","Rendah",
                      "Sedang","Sedang","Sedang","Sedang","Sedang","Sedang","Rendah","Rendah","Tinggi","Rendah",
                      "Tinggi","Sedang","Sedang","Sedang","Sedang","Rendah","Rendah","Rendah","Sedang","Sedang",
                      "Sedang","Tinggi","Sedang","Rendah","Sedang","Rendah","Sedang","Rendah","Sedang","Tinggi",
                      "Rendah","Rendah","Rendah","Rendah","Sedang","Sedang","Rendah","Sedang","Sedang","Rendah",
                      "Tinggi","Tinggi","Tinggi","Sedang","Sedang","Tinggi","Sedang","Rendah","Tinggi","Sedang",
                      "Sedang","Rendah","Sedang","Sedang","Rendah","Sedang","Tinggi","Rendah","Tinggi","Rendah",
                      "Sedang","Sedang","Rendah","Rendah","Sedang","Sedang","Sedang","Sedang","Rendah","Sedang",
                      "Sedang","Sedang","Rendah","Sedang","Rendah","Sedang","Tinggi","Tinggi","Sedang","Sedang",
                      "Tinggi","Tinggi","Rendah","Sedang","Sedang","Sedang","Sedang","Rendah","Rendah","Tinggi",
                      "Tinggi","Tinggi","Rendah","Tinggi","Sedang","Sedang","Sedang","Tinggi","Tinggi","Sedang"],
        "Jam Repair": [4.5,0.7,0.6,1.1,2.2,1.5,1.2,3.3,10.6,4.0,0.6,1.6,11.0,3.2,0.6,5.8,1.0,4.9,4.2,1.8,
                       1.7,4.4,0.9,4.9,0.6,1.6,2.1,1.5,3.5,7.2,1.6,5.6,2.1,9.1,1.9,2.6,3.3,7.7,13.2,1.3,
                       3.5,1.7,3.9,3.6,8.8,8.3,5.6,0.8,1.7,7.0,1.0,0.8,2.9,4.2,3.6,0.8,11.3,5.3,1.2,3.6,
                       7.9,2.2,1.5,1.1,3.0,1.0,4.1,5.5,2.6,4.1,1.9,2.4,0.6,0.9,3.4,2.8,2.7,2.2,5.9,1.0,
                       3.7,2.9,1.8,0.6,2.4,1.1,3.5,2.6,0.7,9.0,2.3,10.2,0.8,0.7,5.6,3.5,1.5,14.5,1.8,4.7,
                       2.6,2.0,1.7,3.5,3.8,0.8,2.2,1.0,0.8,4.2,1.9,13.3,5.0,0.9,0.7,4.6,1.5,0.5,2.8,11.0],
        "Downtime": [6.2,2.9,3.0,2.0,3.3,2.7,2.7,4.1,12.7,5.4,2.9,3.1,13.1,5.5,1.8,7.0,3.1,5.8,6.2,2.5,
                     2.3,6.2,2.8,6.4,1.3,3.1,4.1,2.3,5.7,8.8,2.3,7.8,3.0,10.2,4.3,3.7,4.8,8.7,14.2,3.3,
                     5.1,2.6,4.4,4.4,9.6,10.6,7.2,3.1,2.9,9.1,3.3,2.6,4.8,5.2,5.8,2.0,12.6,6.8,3.1,4.5,
                     9.1,4.6,2.8,2.7,3.7,2.5,6.0,7.6,4.1,6.2,2.6,4.0,1.2,2.4,4.1,4.6,3.8,2.9,7.8,2.0,
                     4.8,4.6,3.8,1.2,3.1,2.5,4.1,4.8,2.5,10.7,3.9,12.5,1.3,1.8,6.7,5.8,2.4,15.8,4.2,6.7,
                     4.8,2.5,4.1,4.9,5.8,2.3,4.5,3.0,2.7,4.9,3.1,15.3,6.6,2.4,1.4,6.3,3.7,2.9,5.3,12.5],
        "Teknisi": ["Dani P.","Dani P.","Budi S.","Eko W.","Eko W.","Budi S.","Dani P.","Dani P.","Dani P.","Agus R.",
                    "Eko W.","Agus R.","Budi S.","Eko W.","Fajar M.","Dani P.","Eko W.","Dani P.","Budi S.","Budi S.",
                    "Dani P.","Fajar M.","Eko W.","Dani P.","Budi S.","Agus R.","Agus R.","Agus R.","Fajar M.","Eko W.",
                    "Budi S.","Dani P.","Eko W.","Budi S.","Budi S.","Fajar M.","Budi S.","Agus R.","Eko W.","Dani P.",
                    "Dani P.","Eko W.","Agus R.","Budi S.","Eko W.","Budi S.","Dani P.","Dani P.","Dani P.","Budi S.",
                    "Dani P.","Fajar M.","Agus R.","Fajar M.","Dani P.","Agus R.","Fajar M.","Eko W.","Agus R.","Budi S.",
                    "Dani P.","Agus R.","Dani P.","Budi S.","Dani P.","Dani P.","Budi S.","Eko W.","Budi S.","Fajar M.",
                    "Dani P.","Eko W.","Budi S.","Fajar M.","Agus R.","Dani P.","Dani P.","Budi S.","Eko W.","Eko W.",
                    "Eko W.","Fajar M.","Eko W.","Fajar M.","Eko W.","Eko W.","Dani P.","Fajar M.","Eko W.","Eko W.",
                    "Agus R.","Eko W.","Eko W.","Dani P.","Dani P.","Fajar M.","Fajar M.","Eko W.","Dani P.","Eko W.",
                    "Eko W.","Budi S.","Budi S.","Budi S.","Dani P.","Budi S.","Eko W.","Agus R.","Fajar M.","Dani P.",
                    "Eko W.","Agus R.","Fajar M.","Fajar M.","Dani P.","Fajar M.","Dani P.","Dani P.","Fajar M.","Eko W."],
        "Biaya": [4953862,1889795,445240,582909,4488532,4554433,3697075,4249220,4308584,4574639,
                  213382,535911,4126783,4662086,3599538,3396989,1065056,226448,645533,2821835,
                  4121951,4883613,1647274,3603235,558455,1657174,3588999,682374,173797,4123853,
                  1431076,3866886,1348529,4908516,4950436,722023,2023033,4906325,4946198,2052242,
                  3885477,4772732,4293668,2099206,4606842,4702341,1018285,2413542,4289678,3603211,
                  1147394,3637697,4626743,1292300,3108918,912295,1346487,257923,2288128,3998434,
                  2610126,3392574,2995627,1017556,370924,2681316,3281253,64187,2819918,2644467,
                  4700748,1509847,2599087,2753222,4338038,4373924,1934422,2103888,3526583,2096689,
                  1885772,2140426,4505457,3629760,2224256,2056939,2017074,725934,1331823,2825634,
                  3574419,4051196,3565005,3706057,3441654,4530553,277348,1574453,1825535,2384185,
                  212598,387709,1328275,4780919,1457517,4904359,3377378,904810,394512,628451,
                  935324,3703130,4564521,2301464,3831601,3229192,1575383,2904969,135153,4148488],
        "Status": ["Pending","Selesai","Selesai","Pending","Selesai","Selesai","Selesai","Selesai","Selesai","Selesai",
                   "Selesai","Selesai","Selesai","Selesai","Selesai","Selesai","Selesai","Selesai","Selesai","Selesai",
                   "Selesai","Pending","Selesai","Pending","Pending","Selesai","Selesai","Pending","Selesai","Pending",
                   "Pending","Selesai","Selesai","Selesai","Pending","Selesai","Pending","Selesai","Selesai","Selesai",
                   "Selesai","Selesai","Selesai","Selesai","Selesai","Selesai","Selesai","Selesai","Pending","Selesai",
                   "Selesai","Selesai","Selesai","Pending","Selesai","Selesai","Selesai","Selesai","Selesai","Selesai",
                   "Selesai","Selesai","Pending","Selesai","Selesai","Pending","Selesai","Selesai","Selesai","Pending",
                   "Selesai","Selesai","Selesai","Pending","Pending","Selesai","Selesai","Pending","Selesai","Selesai",
                   "Selesai","Selesai","Selesai","Pending","Selesai","Selesai","Selesai","Selesai","Selesai","Pending",
                   "Pending","Selesai","Selesai","Pending","Selesai","Selesai","Selesai","Selesai","Pending","Pending",
                   "Selesai","Selesai","Selesai","Selesai","Selesai","Selesai","Selesai","Selesai","Selesai","Selesai",
                   "Pending","Selesai","Pending","Selesai","Selesai","Selesai","Pending","Selesai","Selesai","Selesai"],
    })
    bd["Tanggal"] = pd.to_datetime(bd["Tanggal"])

    oee = pd.DataFrame({
        "Bulan": ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Des"],
        "BulanNum": list(range(1,13)),
        "JamTersedia": [510,494,510,502,487,491,513,503,497,520,510,496],
        "JamProduksi": [505,431,468,469,472,404,452,402,385,505,502,490],
        "Downtime":    [49.6,25.3,59.8,23.5,25.8,46.9,51.6,10.7,37.7,53.6,27.0,15.7],
        "Produksi":    [8381,10382,10254,9029,11042,9132,9213,10187,10856,10351,11954,8267],
        "Cacat":       [33,20,32,34,17,18,11,24,8,11,33,35],
        "Availability":[90.3,94.9,88.3,95.3,94.7,90.4,89.9,97.9,92.4,89.7,94.7,96.8],
        "Performance": [99.0,87.2,91.8,93.4,96.9,82.3,88.1,79.9,77.5,97.1,98.4,98.8],
        "Quality":     [93.5,95.4,93.2,92.8,96.4,95.5,97.6,94.0,97.9,97.8,93.4,92.9],
        "OEE":         [83.6,78.9,75.5,82.6,88.5,71.1,77.3,73.5,70.1,85.2,87.0,88.8],
        "BiayaMaint":  [14872907,17382271,16099514,12735573,22980610,24783253,
                        12633068,9247419,9237236,14540844,6723916,18445510],
    })

    sp = pd.DataFrame({
        "Kode": ["SP-001","SP-002","SP-003","SP-004","SP-005","SP-006","SP-007","SP-008","SP-009","SP-010",
                 "SP-011","SP-012","SP-013","SP-014","SP-015","SP-016","SP-017","SP-018","SP-019","SP-020"],
        "Nama": ["Kontaktor 3P 25A","Relay Thermal 10A","Kabel NYY 4x6mm","Inverter 5.5kW","Bearing 6205ZZ",
                 "Bearing 6306-2RS","Wire Rope 12mm","Hook C-Type 5T","Oli Gearbox SAE90","Grease Bearing",
                 "Motor Brake Pad","Limit Switch","Panel Indikator","Sheave Block 5T","Fuse 16A",
                 "Gearbox Worm 1:40","Terminal Block","Seal Kit Gearbox","Push Button NO","Power Supply 24VDC"],
        "Kategori": ["Electrical","Electrical","Electrical","Motor/Drive","Mechanical","Mechanical","Mechanical",
                     "Mechanical","Consumable","Consumable","Motor/Drive","Electrical","Electrical","Mechanical",
                     "Electrical","Motor/Drive","Electrical","Mechanical","Electrical","Electrical"],
        "Stok":    [31,9,35,28,36,13,11,28,18,14,7,9,19,44,34,2,5,43,48,11],
        "StokMin": [4,7,9,7,3,7,4,10,7,7,6,4,7,7,10,9,6,7,5,9],
        "Status":  ["Aman","Rendah","Aman","Aman","Aman","Aman","Aman","Aman","Aman","Aman",
                    "Rendah","Aman","Aman","Aman","Aman","Kritis","Kritis","Aman","Aman","Rendah"],
        "Harga":   [2445202,382274,971600,2493453,441215,365524,681545,1246630,1929345,2498756,
                    649906,275140,1866943,1713243,1861093,1376914,2437559,2441955,1998423,2087447],
        "Supplier":["Toko Jaya Teknik","Mitra Elektrik","Abadi Spare Parts","Abadi Spare Parts","Mitra Elektrik",
                    "Mitra Elektrik","Toko Jaya Teknik","Toko Jaya Teknik","Toko Jaya Teknik","Mitra Elektrik",
                    "Sumber Makmur","Mitra Elektrik","Toko Jaya Teknik","Sumber Makmur","Toko Jaya Teknik",
                    "Sumber Makmur","Toko Jaya Teknik","Toko Jaya Teknik","Abadi Spare Parts","Toko Jaya Teknik"],
        "LeadTime":[3,2,8,5,11,4,7,4,11,7,14,13,8,9,10,1,13,13,5,8],
    })

    mtbf = pd.DataFrame({
        "Crane":    ["HC-01","HC-02","HC-03","HC-04","HC-05"],
        "Breakdown":[31,25,14,30,20],
        "Downtime": [158.1,140.8,60.4,144.2,94.4],
        "Repair":   [110.5,103.1,36.0,100.0,66.7],
        "MTBF":     [183.3,228.0,412.8,189.9,287.3],
        "MTTR":     [3.6,4.1,2.6,3.3,3.3],
    })
    return bd, oee, sp, mtbf

bd, oee, sp, mtbf = load_data()

# ══════════════════════════════════════════════════════════════
# CHART HELPERS
# ══════════════════════════════════════════════════════════════
GRN  = ["#00e676","#69f0ae","#1de9b6","#40c4ff","#ffca28","#ff5252"]
CMAP = {"HC-01":"#00e676","HC-02":"#69f0ae","HC-03":"#1de9b6","HC-04":"#40c4ff","HC-05":"#ffca28"}

def dark_fig(fig, h=340, margin=(10,10,30,10)):
    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=h,
        margin=dict(l=margin[0],r=margin[1],t=margin[2],b=margin[3]),
        font=dict(family="Inter", size=11, color="#81c784"),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10, color="#a5d6a7")),
    )
    fig.update_xaxes(gridcolor="#0f1a12", linecolor="#1e3324")
    fig.update_yaxes(gridcolor="#0f1a12", linecolor="#1e3324")
    return fig

MONTH_ORDER = ["January","February","March","April","May","June",
               "July","August","September","October","November","December"]

# ══════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:20px 0 16px;">
        <div style="font-size:3rem; line-height:1;">🏗️</div>
        <div style="font-size:1.05rem; font-weight:800; color:#00e676; letter-spacing:1px; margin-top:8px;">CRANEMON</div>
        <div style="font-size:0.7rem; color:#2e7d52; font-family:'JetBrains Mono',monospace; margin-top:3px;">
            MAINTENANCE INTELLIGENCE
        </div>
    </div>
    <hr style="border-color:#1e3324; margin:0 0 16px;">
    """, unsafe_allow_html=True)

    st.markdown("**⚙️ Filter & Kontrol**")

    cranes = ["Semua"] + sorted(bd["Crane ID"].unique())
    sel_crane = st.selectbox("🏗️ Crane ID", cranes)

    months = ["Semua"] + MONTH_ORDER
    sel_bulan = st.selectbox("📅 Bulan", months)

    cats = ["Semua"] + sorted(bd["Kategori"].unique())
    sel_kat = st.selectbox("🔧 Kategori", cats)

    kep_opts = ["Semua", "Tinggi", "Sedang", "Rendah"]
    sel_kep = st.selectbox("⚠️ Keparahan", kep_opts)

    stat_opts = ["Semua", "Selesai", "Pending"]
    sel_stat = st.selectbox("✅ Status", stat_opts)

    st.markdown("<hr style='border-color:#1e3324;'>", unsafe_allow_html=True)

    # Live stats sidebar
    total_bd = len(bd)
    total_dt = bd["Downtime"].sum()
    pending_n = (bd["Status"] == "Pending").sum()
    avg_oee_val = oee["OEE"].mean()

    st.markdown(f"""
    <div style="display:grid; gap:8px; margin-top:4px;">
        <div style="background:#0a1a0d; border:1px solid #1e3324; border-left:3px solid #00e676;
             border-radius:8px; padding:10px 14px;">
            <div style="color:#2e7d52; font-size:0.67rem; text-transform:uppercase; letter-spacing:0.8px;">Total Breakdown</div>
            <div style="color:#00e676; font-size:1.45rem; font-weight:700; font-family:'JetBrains Mono',monospace;">{total_bd}</div>
        </div>
        <div style="background:#0a1a0d; border:1px solid #1e3324; border-left:3px solid #ffca28;
             border-radius:8px; padding:10px 14px;">
            <div style="color:#2e7d52; font-size:0.67rem; text-transform:uppercase; letter-spacing:0.8px;">Total Downtime</div>
            <div style="color:#ffca28; font-size:1.45rem; font-weight:700; font-family:'JetBrains Mono',monospace;">{total_dt:.0f}<span style="font-size:0.75rem; color:#2e7d52;"> Jam</span></div>
        </div>
        <div style="background:#0a1a0d; border:1px solid #1e3324; border-left:3px solid #ff5252;
             border-radius:8px; padding:10px 14px;">
            <div style="color:#2e7d52; font-size:0.67rem; text-transform:uppercase; letter-spacing:0.8px;">Pending Repair</div>
            <div style="color:#ff5252; font-size:1.45rem; font-weight:700; font-family:'JetBrains Mono',monospace;">{pending_n}</div>
        </div>
        <div style="background:#0a1a0d; border:1px solid #1e3324; border-left:3px solid #1de9b6;
             border-radius:8px; padding:10px 14px;">
            <div style="color:#2e7d52; font-size:0.67rem; text-transform:uppercase; letter-spacing:0.8px;">Avg OEE 2024</div>
            <div style="color:#1de9b6; font-size:1.45rem; font-weight:700; font-family:'JetBrains Mono',monospace;">{avg_oee_val:.1f}<span style="font-size:0.75rem; color:#2e7d52;">%</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <hr style="border-color:#1e3324; margin-top:16px;">
    <div style="color:#2e7d52; font-size:0.65rem; font-family:'JetBrains Mono',monospace; text-align:center; padding-top:4px;">
        DATA PERIODE: JAN – DES 2024
    </div>
    """, unsafe_allow_html=True)

# ── Apply filters ──────────────────────────────────────────
df = bd.copy()
if sel_crane != "Semua": df = df[df["Crane ID"] == sel_crane]
if sel_bulan != "Semua": df = df[df["Bulan"] == sel_bulan]
if sel_kat   != "Semua": df = df[df["Kategori"] == sel_kat]
if sel_kep   != "Semua": df = df[df["Keparahan"] == sel_kep]
if sel_stat  != "Semua": df = df[df["Status"] == sel_stat]

# ══════════════════════════════════════════════════════════════
# HERO HEADER
# ══════════════════════════════════════════════════════════════
filter_info = f"Filter aktif: {sel_crane} | {sel_bulan} | {sel_kat} | {sel_kep} | {sel_stat}"
st.markdown(f"""
<div class="hero-card fade-up">
  <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:12px;">
    <div>
      <div class="hero-title">
        🏗️ CraneMon
        <span class="hero-badge pulse">● LIVE</span>
      </div>
      <div class="hero-sub">HOIST CRANE MAINTENANCE INTELLIGENCE SYSTEM // 2024</div>
    </div>
    <div style="text-align:right;">
      <div style="color:#2e7d52; font-size:0.68rem; font-family:'JetBrains Mono',monospace;">{filter_info}</div>
      <div style="color:#00e676; font-size:0.78rem; margin-top:4px; font-weight:600;">
        {len(df)} / {total_bd} records ditampilkan
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════
t1, t2, t3, t4, t5 = st.tabs([
    "⚡ Command Center",
    "🔍 Breakdown Deep-Dive",
    "📈 OEE & Produksi",
    "🔩 Spare Parts",
    "🔮 Forecasting",
])

# ╔══════════════════════════════════════════════════════════════╗
# ║  TAB 1 — COMMAND CENTER                                      ║
# ╚══════════════════════════════════════════════════════════════╝
with t1:
    n_bd    = len(df)
    dt_sum  = df["Downtime"].sum()
    cost_sum= df["Biaya"].sum()
    pending = (df["Status"] == "Pending").sum()
    selesai = (df["Status"] == "Selesai").sum()
    avg_rep = df["Jam Repair"].mean() if n_bd else 0
    tinggi_n= (df["Keparahan"] == "Tinggi").sum()

    c1,c2,c3,c4,c5,c6,c7 = st.columns(7)
    c1.metric("📋 Breakdown",     n_bd,        f"dari {total_bd}")
    c2.metric("⏱️ Downtime",      f"{dt_sum:.0f}j")
    c3.metric("💰 Biaya",         f"Rp{cost_sum/1e6:.1f}M")
    c4.metric("⚠️ Pending",       pending,     delta=f"-{selesai} selesai", delta_color="inverse")
    c5.metric("🔴 Keparahan Tinggi", tinggi_n)
    c6.metric("⏰ Avg Repair",    f"{avg_rep:.1f}j")
    c7.metric("🏆 Best Crane",    "HC-03",     "MTBF 412j")

    st.markdown("---")

    # ── Row A: Tren + Radar ───────────────────────────────────
    ca, cb = st.columns([3,2])

    with ca:
        st.markdown('<div class="sec-header">📈 Tren Breakdown & Downtime Bulanan</div>', unsafe_allow_html=True)
        bd_m = df.groupby("Bulan").agg(Breakdown=("ID","count"), Downtime=("Downtime","sum")).reset_index()
        bd_m["ord"] = bd_m["Bulan"].map({b:i for i,b in enumerate(MONTH_ORDER)})
        bd_m = bd_m.sort_values("ord")

        fig = make_subplots(specs=[[{"secondary_y":True}]])
        fig.add_trace(go.Bar(
            x=bd_m["Bulan"], y=bd_m["Breakdown"],
            name="Breakdown",
            marker=dict(
                color=bd_m["Breakdown"],
                colorscale=[[0,"#0a2e14"],[0.5,"#1a5c2a"],[1,"#00e676"]],
                showscale=False,
                line=dict(color="#00e676", width=0.5),
            ),
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=bd_m["Bulan"], y=bd_m["Downtime"],
            name="Downtime (jam)", mode="lines+markers",
            line=dict(color="#ffca28", width=2.5),
            marker=dict(size=7, color="#ffca28",
                        line=dict(color="#0a1a0d", width=2)),
            fill="tozeroy", fillcolor="rgba(255,202,40,0.05)",
        ), secondary_y=True)
        fig.update_yaxes(title_text="Breakdown", secondary_y=False, title_font_color="#00e676")
        fig.update_yaxes(title_text="Downtime (jam)", secondary_y=True, title_font_color="#ffca28")
        dark_fig(fig, 320)
        fig.update_xaxes(tickangle=-30, tickfont_size=10)
        st.plotly_chart(fig, use_container_width=True)

    with cb:
        st.markdown('<div class="sec-header">🕸️ Profil Crane — Radar</div>', unsafe_allow_html=True)
        cats_radar = ["Breakdown","MTBF Norm","MTTR Inv","Downtime Norm","Repair"]
        mtbf_n = mtbf.copy()
        mtbf_n["MTBF_N"] = mtbf_n["MTBF"] / mtbf_n["MTBF"].max() * 10
        mtbf_n["MTTR_I"] = (1 - (mtbf_n["MTTR"] - mtbf_n["MTTR"].min()) / (mtbf_n["MTTR"].max() - mtbf_n["MTTR"].min())) * 10
        mtbf_n["DT_N"]   = (1 - (mtbf_n["Downtime"] - mtbf_n["Downtime"].min()) / (mtbf_n["Downtime"].max() - mtbf_n["Downtime"].min())) * 10
        mtbf_n["BD_N"]   = (1 - (mtbf_n["Breakdown"] - mtbf_n["Breakdown"].min()) / (mtbf_n["Breakdown"].max() - mtbf_n["Breakdown"].min())) * 10
        mtbf_n["R_N"]    = (1 - (mtbf_n["Repair"] - mtbf_n["Repair"].min()) / (mtbf_n["Repair"].max() - mtbf_n["Repair"].min())) * 10

        CMAP_RGBA = {
            "HC-01": "rgba(0,230,118,0.08)",
            "HC-02": "rgba(105,240,174,0.08)",
            "HC-03": "rgba(29,233,182,0.08)",
            "HC-04": "rgba(64,196,255,0.08)",
            "HC-05": "rgba(255,202,40,0.08)",
        }
        fig = go.Figure()
        for _, row in mtbf_n.iterrows():
            crane_id = row["Crane"]
            vals = [row["BD_N"], row["MTBF_N"], row["MTTR_I"], row["DT_N"], row["R_N"]]
            vals += [vals[0]]
            fig.add_trace(go.Scatterpolar(
                r=vals,
                theta=cats_radar + [cats_radar[0]],
                name=crane_id,
                line=dict(color=CMAP[crane_id], width=2),
                fill="toself",
                fillcolor=CMAP_RGBA[crane_id],
            ))
        dark_fig(fig, 320)
        fig.update_layout(polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0,10], gridcolor="#1e3324",
                            tickfont=dict(color="#2e7d52", size=8)),
            angularaxis=dict(gridcolor="#1e3324", tickfont=dict(color="#a5d6a7", size=9)),
        ))
        st.plotly_chart(fig, use_container_width=True)

    # ── Row B: Kategori donut + Keparahan + Status ────────────
    cb1, cb2, cb3 = st.columns(3)

    with cb1:
        st.markdown('<div class="sec-header">🗂️ Kategori Kerusakan</div>', unsafe_allow_html=True)
        kat_cnt = df.groupby("Kategori").size().reset_index(name="n")
        fig = px.pie(kat_cnt, values="n", names="Kategori",
                     color_discrete_sequence=GRN, hole=0.52)
        fig.update_traces(textposition="outside", textinfo="percent+label",
                          textfont_size=9,
                          marker=dict(line=dict(color="#080d0a", width=2)))
        dark_fig(fig, 290)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with cb2:
        st.markdown('<div class="sec-header">⚠️ Tingkat Keparahan</div>', unsafe_allow_html=True)
        kep_map = {"Tinggi":"#ff5252","Sedang":"#ffca28","Rendah":"#00e676"}
        kep_cnt = df.groupby("Keparahan").size().reset_index(name="n")
        kep_cnt["ord"] = kep_cnt["Keparahan"].map({"Tinggi":0,"Sedang":1,"Rendah":2})
        kep_cnt = kep_cnt.sort_values("ord")
        fig = go.Figure(go.Bar(
            x=kep_cnt["Keparahan"], y=kep_cnt["n"],
            marker_color=[kep_map[k] for k in kep_cnt["Keparahan"]],
            text=kep_cnt["n"], textposition="outside",
            width=0.5,
        ))
        dark_fig(fig, 290)
        st.plotly_chart(fig, use_container_width=True)

    with cb3:
        st.markdown('<div class="sec-header">✅ Status Perbaikan</div>', unsafe_allow_html=True)
        stat_cnt = df.groupby("Status").size().reset_index(name="n")
        fig = px.pie(stat_cnt, values="n", names="Status",
                     color="Status",
                     color_discrete_map={"Selesai":"#00e676","Pending":"#ffca28"},
                     hole=0.55)
        fig.update_traces(textposition="outside", textinfo="percent+label",
                          textfont_size=10,
                          marker=dict(line=dict(color="#080d0a", width=2)))
        dark_fig(fig, 290)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    # ── Row C: MTBF/MTTR Grouped ─────────────────────────────
    st.markdown('<div class="sec-header">📊 MTBF & MTTR per Crane</div>', unsafe_allow_html=True)
    c_m1, c_m2 = st.columns(2)

    with c_m1:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name="MTBF (Jam)", x=mtbf["Crane"], y=mtbf["MTBF"],
            marker=dict(color=list(CMAP.values()), opacity=0.9,
                        line=dict(color="#00e676", width=0.8)),
            text=mtbf["MTBF"], textposition="outside",
        ))
        fig.add_hline(y=300, line_dash="dot", line_color="rgba(0,230,118,0.3)",
                      annotation_text="Target MTBF 300j",
                      annotation_font_color="#2e7d52", annotation_font_size=9)
        dark_fig(fig, 280)
        fig.update_layout(title=dict(text="MTBF — Mean Time Between Failure",
                                     font=dict(color="#69f0ae", size=12)))
        st.plotly_chart(fig, use_container_width=True)

    with c_m2:
        fig = go.Figure()
        for i, row in mtbf.iterrows():
            fig.add_trace(go.Bar(
                name=row["Crane"], x=[row["Crane"]],
                y=[row["MTTR"]],
                marker_color=list(CMAP.values())[i],
                width=0.5,
                text=[f"{row['MTTR']}j"], textposition="outside",
            ))
        fig.add_hline(y=3.0, line_dash="dot", line_color="rgba(255,202,40,0.4)",
                      annotation_text="Target MTTR < 3j",
                      annotation_font_color="#ffca28", annotation_font_size=9)
        dark_fig(fig, 280)
        fig.update_layout(showlegend=False,
                          title=dict(text="MTTR — Mean Time To Repair",
                                     font=dict(color="#69f0ae", size=12)))
        st.plotly_chart(fig, use_container_width=True)

# ╔══════════════════════════════════════════════════════════════╗
# ║  TAB 2 — BREAKDOWN DEEP-DIVE                                 ║
# ╚══════════════════════════════════════════════════════════════╝
with t2:
    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="sec-header">🔥 Heatmap Downtime: Crane × Bulan</div>', unsafe_allow_html=True)
        pivot = df.groupby(["Crane ID","Bulan"])["Downtime"].sum().reset_index()
        heat  = pivot.pivot(index="Crane ID", columns="Bulan", values="Downtime").fillna(0)
        existing = [m for m in MONTH_ORDER if m in heat.columns]
        heat = heat[existing]
        fig = px.imshow(heat,
                        color_continuous_scale=[[0,"#080d0a"],[0.3,"#0f3320"],
                                                [0.6,"#1a5c2a"],[1,"#00e676"]],
                        text_auto=".1f", aspect="auto",
                        labels=dict(color="Downtime (Jam)"))
        fig.update_traces(textfont_size=9)
        dark_fig(fig, 260)
        fig.update_coloraxes(colorbar_tickfont_color="#81c784")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown('<div class="sec-header">🔧 Top 10 Komponen Bermasalah</div>', unsafe_allow_html=True)
        top_k = (df.groupby("Komponen")
                   .agg(Frekuensi=("ID","count"), Downtime=("Downtime","sum"))
                   .reset_index()
                   .sort_values("Frekuensi", ascending=True)
                   .tail(10))
        fig = go.Figure(go.Bar(
            x=top_k["Frekuensi"], y=top_k["Komponen"],
            orientation="h",
            marker=dict(
                color=top_k["Frekuensi"],
                colorscale=[[0,"#0a2e14"],[1,"#00e676"]],
                showscale=False,
                line=dict(color="#1e3324", width=0.5),
            ),
            text=top_k["Frekuensi"], textposition="outside",
            customdata=top_k["Downtime"],
            hovertemplate="<b>%{y}</b><br>Frekuensi: %{x}<br>Total Downtime: %{customdata:.1f} jam<extra></extra>",
        ))
        dark_fig(fig, 320)
        st.plotly_chart(fig, use_container_width=True)

    # ── Teknisi workload ───────────────────────────────────────
    st.markdown('<div class="sec-header">👷 Workload Teknisi</div>', unsafe_allow_html=True)
    tek = (df.groupby("Teknisi")
             .agg(Penugasan=("ID","count"),
                  JamRepair=("Jam Repair","sum"),
                  AvgRepair=("Jam Repair","mean"),
                  Downtime=("Downtime","sum"))
             .reset_index()
             .sort_values("Penugasan", ascending=False))

    ct1, ct2 = st.columns([3,2])
    with ct1:
        fig = make_subplots(specs=[[{"secondary_y":True}]])
        fig.add_trace(go.Bar(
            x=tek["Teknisi"], y=tek["Penugasan"],
            name="Penugasan", marker_color="#00e676",
            opacity=0.85,
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=tek["Teknisi"], y=tek["JamRepair"],
            name="Total Jam Repair", mode="lines+markers",
            line=dict(color="#ffca28", width=2.5),
            marker=dict(size=8, color="#ffca28",
                        line=dict(color="#080d0a", width=2)),
        ), secondary_y=True)
        dark_fig(fig, 300)
        st.plotly_chart(fig, use_container_width=True)

    with ct2:
        fig = px.bar(tek, x="AvgRepair", y="Teknisi", orientation="h",
                     color="AvgRepair",
                     color_continuous_scale=[[0,"#0a3320"],[1,"#ff5252"]],
                     text=tek["AvgRepair"].apply(lambda x: f"{x:.1f}j"),
                     labels={"AvgRepair":"Avg Repair (Jam)"},
                     title="Rata-rata Waktu Repair per Teknisi")
        fig.update_traces(textposition="outside")
        dark_fig(fig, 300)
        fig.update_layout(coloraxis_showscale=False,
                          title_font_color="#69f0ae")
        st.plotly_chart(fig, use_container_width=True)

    # ── Cost analysis ─────────────────────────────────────────
    st.markdown('<div class="sec-header">💰 Analisis Biaya Material</div>', unsafe_allow_html=True)
    cc1, cc2, cc3 = st.columns(3)

    with cc1:
        biaya_crane = df.groupby("Crane ID")["Biaya"].sum().reset_index()
        fig = px.bar(biaya_crane.sort_values("Biaya"),
                     x="Biaya", y="Crane ID", orientation="h",
                     color="Crane ID", color_discrete_map=CMAP,
                     text=biaya_crane.sort_values("Biaya")["Biaya"].apply(lambda x: f"Rp{x/1e6:.1f}M"))
        fig.update_traces(textposition="outside")
        dark_fig(fig, 270)
        fig.update_layout(showlegend=False, title=dict(text="Biaya per Crane",font=dict(color="#69f0ae",size=11)))
        st.plotly_chart(fig, use_container_width=True)

    with cc2:
        biaya_kat = df.groupby("Kategori")["Biaya"].sum().reset_index()
        fig = px.pie(biaya_kat, values="Biaya", names="Kategori",
                     color_discrete_sequence=GRN, hole=0.45)
        fig.update_traces(textinfo="percent+label", textfont_size=9,
                          marker=dict(line=dict(color="#080d0a",width=2)))
        dark_fig(fig, 270)
        fig.update_layout(showlegend=False,
                          title=dict(text="Biaya per Kategori",font=dict(color="#69f0ae",size=11)))
        st.plotly_chart(fig, use_container_width=True)

    with cc3:
        biaya_bln = df.groupby("Bulan")["Biaya"].sum().reset_index()
        biaya_bln["ord"] = biaya_bln["Bulan"].map({b:i for i,b in enumerate(MONTH_ORDER)})
        biaya_bln = biaya_bln.sort_values("ord")
        fig = px.area(biaya_bln, x="Bulan", y="Biaya",
                      color_discrete_sequence=["#00e676"])
        fig.update_traces(fill="tozeroy", fillcolor="rgba(0,230,118,0.07)",
                          line=dict(width=2))
        dark_fig(fig, 270)
        fig.update_layout(title=dict(text="Biaya per Bulan",font=dict(color="#69f0ae",size=11)))
        fig.update_yaxes(tickformat=".2s")
        fig.update_xaxes(tickangle=-40, tickfont_size=9)
        st.plotly_chart(fig, use_container_width=True)

    # ── Log tabel ─────────────────────────────────────────────
    st.markdown('<div class="sec-header">📋 Log Breakdown — Detail Rekaman</div>', unsafe_allow_html=True)
    disp = df[["ID","Tanggal","Crane ID","Kategori","Komponen","Keparahan","Jam Repair","Downtime","Teknisi","Biaya","Status"]].copy()
    disp["Tanggal"] = disp["Tanggal"].dt.strftime("%d %b %Y")
    disp["Biaya"]   = disp["Biaya"].apply(lambda x: f"Rp {x:,.0f}")
    st.dataframe(disp.reset_index(drop=True), use_container_width=True, height=360)
    csv = df.to_csv(index=False).encode()
    st.download_button("⬇️ Export CSV", csv, "breakdown_filtered.csv", "text/csv")

# ╔══════════════════════════════════════════════════════════════╗
# ║  TAB 3 — OEE & PRODUKSI                                      ║
# ╚══════════════════════════════════════════════════════════════╝
with t3:
    # KPI
    o1,o2,o3,o4,o5,o6 = st.columns(6)
    o1.metric("Avg OEE",         f"{oee['OEE'].mean():.1f}%",       "target 85%")
    o2.metric("Avg Availability", f"{oee['Availability'].mean():.1f}%")
    o3.metric("Avg Performance",  f"{oee['Performance'].mean():.1f}%")
    o4.metric("Avg Quality",      f"{oee['Quality'].mean():.1f}%")
    o5.metric("Total Produksi",   f"{oee['Produksi'].sum():,} unit")
    o6.metric("Total Biaya Maint",f"Rp{oee['BiayaMaint'].sum()/1e6:.0f}M")

    st.markdown("---")

    # ── OEE Multi-line ────────────────────────────────────────
    st.markdown('<div class="sec-header">📊 Tren OEE Components Sepanjang 2024</div>', unsafe_allow_html=True)
    fig = go.Figure()
    cfg = [
        ("OEE","#00e676","solid",3),
        ("Availability","#69f0ae","dash",2),
        ("Performance","#ffca28","dot",2),
        ("Quality","#40c4ff","dashdot",2),
    ]
    for col, clr, dash, w in cfg:
        fig.add_trace(go.Scatter(
            x=oee["Bulan"], y=oee[col],
            name=col, mode="lines+markers",
            line=dict(color=clr, width=w, dash=dash),
            marker=dict(size=7, color=clr, line=dict(color="#080d0a", width=2)),
        ))
    fig.add_hrect(y0=85, y1=100, fillcolor="rgba(0,230,118,0.04)",
                  line_width=0, annotation_text="World Class Zone",
                  annotation_font_color="#2e7d52", annotation_font_size=9)
    fig.add_hline(y=85, line_dash="dot", line_color="rgba(0,230,118,0.4)",
                  annotation_text="Benchmark 85%",
                  annotation_position="bottom right",
                  annotation_font_color="#00e676")
    dark_fig(fig, 360)
    fig.update_yaxes(range=[60,105], ticksuffix="%")
    fig.update_xaxes(tickangle=-30)
    st.plotly_chart(fig, use_container_width=True)

    # ── Produksi + Biaya ──────────────────────────────────────
    cp1, cp2 = st.columns(2)
    with cp1:
        st.markdown('<div class="sec-header">🏭 Produksi vs Produk Cacat</div>', unsafe_allow_html=True)
        fig = make_subplots(specs=[[{"secondary_y":True}]])
        fig.add_trace(go.Bar(
            x=oee["Bulan"], y=oee["Produksi"],
            name="Total Produksi",
            marker=dict(color=oee["Produksi"],
                        colorscale=[[0,"#0a2e14"],[1,"#00e676"]],
                        showscale=False),
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=oee["Bulan"], y=oee["Cacat"],
            name="Produk Cacat",
            mode="lines+markers",
            line=dict(color="#ff5252", width=2),
            marker=dict(size=7, color="#ff5252", line=dict(color="#080d0a",width=2)),
        ), secondary_y=True)
        dark_fig(fig, 310)
        fig.update_xaxes(tickangle=-30, tickfont_size=9)
        st.plotly_chart(fig, use_container_width=True)

    with cp2:
        st.markdown('<div class="sec-header">💸 Biaya Maintenance vs Downtime</div>', unsafe_allow_html=True)
        fig = make_subplots(specs=[[{"secondary_y":True}]])
        fig.add_trace(go.Bar(
            x=oee["Bulan"], y=oee["BiayaMaint"]/1e6,
            name="Biaya (Juta Rp)",
            marker=dict(color="#1de9b6", opacity=0.7),
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=oee["Bulan"], y=oee["Downtime"],
            name="Downtime (jam)",
            mode="lines+markers",
            line=dict(color="#ffca28", width=2),
            marker=dict(size=7, color="#ffca28", line=dict(color="#080d0a",width=2)),
        ), secondary_y=True)
        dark_fig(fig, 310)
        fig.update_xaxes(tickangle=-30, tickfont_size=9)
        st.plotly_chart(fig, use_container_width=True)

    # ── Jam tersedia vs aktual ─────────────────────────────────
    st.markdown('<div class="sec-header">⏱️ Jam Tersedia vs Jam Aktual Produksi</div>', unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=oee["Bulan"], y=oee["JamTersedia"],
                         name="Jam Tersedia", marker_color="#1e3324", width=0.4))
    fig.add_trace(go.Bar(x=oee["Bulan"], y=oee["JamProduksi"],
                         name="Jam Aktual", marker_color="#00e676", opacity=0.85, width=0.4))
    dark_fig(fig, 280)
    fig.update_layout(barmode="overlay")
    fig.update_xaxes(tickangle=-30, tickfont_size=9)
    st.plotly_chart(fig, use_container_width=True)

    # ── OEE tabel ─────────────────────────────────────────────
    with st.expander("📋 Tabel Data OEE & Produksi"):
        disp_oee = oee.copy()
        disp_oee["BiayaMaint"] = disp_oee["BiayaMaint"].apply(lambda x: f"Rp {x:,.0f}")
        st.dataframe(disp_oee, use_container_width=True)

# ╔══════════════════════════════════════════════════════════════╗
# ║  TAB 4 — SPARE PARTS                                         ║
# ╚══════════════════════════════════════════════════════════════╝
with t4:
    # Alerts
    kritis = sp[sp["Status"] == "Kritis"]
    rendah = sp[sp["Status"] == "Rendah"]

    if len(kritis):
        for _, r in kritis.iterrows():
            st.markdown(f"""
            <div class="alert-crit">
                🚨 <b>KRITIS</b> &nbsp;|&nbsp; {r['Kode']} — {r['Nama']}
                &nbsp;&nbsp;·&nbsp;&nbsp; Stok: <b>{r['Stok']}</b> unit (Min: {r['StokMin']})
                &nbsp;&nbsp;·&nbsp;&nbsp; Lead Time: <b>{r['LeadTime']} hari</b>
                &nbsp;&nbsp;·&nbsp;&nbsp; Supplier: {r['Supplier']}
            </div>""", unsafe_allow_html=True)
    if len(rendah):
        for _, r in rendah.iterrows():
            st.markdown(f"""
            <div class="alert-warn">
                ⚠️ <b>RENDAH</b> &nbsp;|&nbsp; {r['Kode']} — {r['Nama']}
                &nbsp;&nbsp;·&nbsp;&nbsp; Stok: <b>{r['Stok']}</b> unit (Min: {r['StokMin']})
                &nbsp;&nbsp;·&nbsp;&nbsp; Lead Time: <b>{r['LeadTime']} hari</b>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # KPI
    s1,s2,s3,s4 = st.columns(4)
    total_val = (sp["Stok"]*sp["Harga"]).sum()
    s1.metric("Total Jenis Part", len(sp))
    s2.metric("🚨 Status Kritis",  len(kritis))
    s3.metric("⚠️ Stok Rendah",   len(rendah))
    s4.metric("Nilai Total Stok",  f"Rp {total_val/1e6:.1f}M")

    st.markdown("---")

    cs1, cs2 = st.columns([3,2])
    with cs1:
        st.markdown('<div class="sec-header">📦 Status Stok Semua Part</div>', unsafe_allow_html=True)
        clr_stok = {"Aman":"#00e676","Rendah":"#ffca28","Kritis":"#ff5252"}
        sp_sorted = sp.sort_values("Stok")
        fig = go.Figure()
        for status, clr in clr_stok.items():
            sub = sp_sorted[sp_sorted["Status"]==status]
            if len(sub):
                fig.add_trace(go.Bar(
                    x=sub["Stok"], y=sub["Nama"], orientation="h",
                    name=status, marker_color=clr, marker_opacity=0.85,
                    text=sub["Stok"], textposition="outside",
                    textfont_size=9,
                ))
        dark_fig(fig, 520)
        fig.update_layout(barmode="stack", legend_traceorder="reversed")
        st.plotly_chart(fig, use_container_width=True)

    with cs2:
        st.markdown('<div class="sec-header">🏷️ Distribusi Kategori</div>', unsafe_allow_html=True)
        cat_stok = sp.groupby("Kategori")["Stok"].sum().reset_index()
        fig = px.pie(cat_stok, values="Stok", names="Kategori",
                     color_discrete_sequence=GRN, hole=0.5)
        fig.update_traces(textinfo="percent+label", textfont_size=10,
                          marker=dict(line=dict(color="#080d0a",width=2)))
        dark_fig(fig, 260)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown('<div class="sec-header">🏢 Distribusi Supplier</div>', unsafe_allow_html=True)
        sup = sp.groupby("Supplier").size().reset_index(name="n")
        fig = px.pie(sup, values="n", names="Supplier",
                     color_discrete_sequence=GRN[::-1], hole=0.45)
        fig.update_traces(textinfo="percent+label", textfont_size=9,
                          marker=dict(line=dict(color="#080d0a",width=2)))
        dark_fig(fig, 240)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    # ── Scatter Stok vs Lead Time ──────────────────────────────
    st.markdown('<div class="sec-header">📡 Risk Map: Stok vs Lead Time (ukuran = harga)</div>', unsafe_allow_html=True)
    fig = px.scatter(sp, x="LeadTime", y="Stok",
                     size="Harga", color="Status",
                     color_discrete_map=clr_stok,
                     hover_name="Nama",
                     hover_data={"Kode":True,"Supplier":True,"LeadTime":True,"Stok":True},
                     labels={"LeadTime":"Lead Time (Hari)","Stok":"Stok (Unit)"},
                     size_max=30)
    fig.add_hline(y=sp["StokMin"].mean(), line_dash="dash",
                  line_color="rgba(255,82,82,0.3)",
                  annotation_text="Avg Stok Minimum",
                  annotation_font_color="#ff5252", annotation_font_size=9)
    dark_fig(fig, 320)
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📋 Tabel Spare Parts Lengkap"):
        disp_sp = sp.copy()
        disp_sp["Harga"] = disp_sp["Harga"].apply(lambda x: f"Rp {x:,.0f}")
        disp_sp["Nilai Stok"] = (sp["Stok"] * sp["Harga"]).apply(lambda x: f"Rp {x:,.0f}")
        st.dataframe(disp_sp, use_container_width=True)

# ╔══════════════════════════════════════════════════════════════╗
# ║  TAB 5 — FORECASTING                                         ║
# ╚══════════════════════════════════════════════════════════════╝
with t5:
    st.markdown("""
    <div style="background:linear-gradient(90deg,rgba(0,230,118,0.05),transparent);
         border:1px solid #1e3324; border-left:3px solid #00e676;
         border-radius:8px; padding:12px 16px; margin-bottom:18px; color:#81c784; font-size:0.83rem;">
        🔮 <b>Forecasting Engine</b> — Menggunakan metode Linear Regression & Moving Average
        untuk memproyeksikan tren breakdown dan OEE ke depan. Hasil bersifat estimasi berdasarkan pola historis 2024.
    </div>
    """, unsafe_allow_html=True)

    fc1, fc2 = st.columns([2,1])
    with fc1:
        target_metric = st.selectbox("📊 Pilih Metrik Forecast",
                                     ["Jumlah Breakdown", "Total Downtime (Jam)", "OEE (%)", "Biaya Maintenance (Juta Rp)"])
    with fc2:
        forecast_months = st.slider("Proyeksi ke depan (bulan)", 1, 6, 3)

    # ── Prepare series ─────────────────────────────────────────
    bd_monthly = (bd.groupby("Bulan")
                    .agg(Breakdown=("ID","count"), Downtime=("Downtime","sum"))
                    .reset_index())
    bd_monthly["ord"] = bd_monthly["Bulan"].map({b:i for i,b in enumerate(MONTH_ORDER)})
    bd_monthly = bd_monthly.sort_values("ord")

    month_labels_hist = bd_monthly["Bulan"].tolist()
    x_hist = np.arange(len(month_labels_hist))

    if target_metric == "Jumlah Breakdown":
        y_hist = bd_monthly["Breakdown"].values
        unit, color_fc = "Breakdown", "#00e676"
    elif target_metric == "Total Downtime (Jam)":
        y_hist = bd_monthly["Downtime"].values
        unit, color_fc = "Jam", "#ffca28"
    elif target_metric == "OEE (%)":
        y_hist = oee["OEE"].values
        month_labels_hist = oee["Bulan"].tolist()
        x_hist = np.arange(12)
        unit, color_fc = "%", "#1de9b6"
    else:
        y_hist = oee["BiayaMaint"].values / 1e6
        month_labels_hist = oee["Bulan"].tolist()
        x_hist = np.arange(12)
        unit, color_fc = "Juta Rp", "#40c4ff"

    # ── Linear regression ──────────────────────────────────────
    coeffs  = np.polyfit(x_hist, y_hist, deg=1)
    poly    = np.poly1d(coeffs)
    trend_y = poly(x_hist)

    # Future
    x_future = np.arange(len(x_hist), len(x_hist) + forecast_months)
    y_future  = poly(x_future)

    # Moving average (window=3)
    ma_y = pd.Series(y_hist).rolling(3, min_periods=1).mean().values

    # Future labels
    all_months = MONTH_ORDER * 2
    last_idx   = MONTH_ORDER.index(month_labels_hist[-1])
    future_labels = [all_months[(last_idx + i + 1) % 12] + " '25"
                     for i in range(forecast_months)]

    # Confidence band (±1 std of residuals)
    residuals = y_hist - trend_y
    std_res   = residuals.std()
    ci_upper  = y_future + 1.5 * std_res
    ci_lower  = y_future - 1.5 * std_res

    # ── Plot ───────────────────────────────────────────────────
    st.markdown(f'<div class="sec-header">📈 Forecast: {target_metric}</div>', unsafe_allow_html=True)

    fig = go.Figure()

    # Actual
    fig.add_trace(go.Scatter(
        x=month_labels_hist, y=y_hist,
        name="Aktual", mode="lines+markers",
        line=dict(color=color_fc, width=2.5),
        marker=dict(size=8, color=color_fc, line=dict(color="#080d0a",width=2)),
    ))

    # Moving Average
    fig.add_trace(go.Scatter(
        x=month_labels_hist, y=ma_y,
        name="Moving Avg (3bln)", mode="lines",
        line=dict(color="#ffca28", width=1.5, dash="dot"),
    ))

    # Trend line (extended)
    all_x_labels = month_labels_hist + future_labels
    all_trend_y  = list(trend_y) + list(y_future)
    fig.add_trace(go.Scatter(
        x=all_x_labels, y=all_trend_y,
        name="Trend (Regresi Linear)", mode="lines",
        line=dict(color="rgba(255,255,255,0.2)", width=1.5, dash="dash"),
    ))

    # Confidence band
    fig.add_trace(go.Scatter(
        x=future_labels + future_labels[::-1],
        y=list(ci_upper) + list(ci_lower[::-1]),
        fill="toself",
        fillcolor=f"rgba(0,230,118,0.07)",
        line=dict(color="rgba(0,0,0,0)"),
        name="Interval Kepercayaan (±1.5σ)",
        hoverinfo="skip",
    ))

    # Forecast line
    fig.add_trace(go.Scatter(
        x=future_labels, y=y_future,
        name=f"Proyeksi {forecast_months} Bulan",
        mode="lines+markers",
        line=dict(color=color_fc, width=2.5, dash="dot"),
        marker=dict(size=9, color=color_fc, symbol="diamond",
                    line=dict(color="#080d0a", width=2)),
    ))

    # Separator — pakai add_shape karena add_vline tidak support categorical x-axis
    separator_x = len(month_labels_hist) - 0.5
    fig.add_shape(
        type="line",
        x0=separator_x, x1=separator_x,
        y0=0, y1=1,
        xref="x", yref="paper",
        line=dict(dash="dot", color="rgba(255,255,255,0.15)", width=1.5),
    )
    fig.add_annotation(
        x=separator_x, y=1,
        xref="x", yref="paper",
        text="▶ Proyeksi mulai",
        showarrow=False,
        font=dict(color="#2e7d52", size=9),
        xanchor="left", yanchor="top",
    )

    dark_fig(fig, 400)
    fig.update_xaxes(tickangle=-30)
    st.plotly_chart(fig, use_container_width=True)

    # ── Forecast table ─────────────────────────────────────────
    st.markdown('<div class="sec-header">📋 Hasil Proyeksi</div>', unsafe_allow_html=True)
    fc_df = pd.DataFrame({
        "Bulan Proyeksi": future_labels,
        f"Nilai Forecast ({unit})": [round(v,2) for v in y_future],
        f"Batas Atas ({unit})": [round(v,2) for v in ci_upper],
        f"Batas Bawah ({unit})": [max(0,round(v,2)) for v in ci_lower],
        "Metode": ["Linear Regression"] * forecast_months,
    })
    st.dataframe(fc_df, use_container_width=True)

    # ── Trend insight ──────────────────────────────────────────
    trend_dir = "📉 Menurun" if coeffs[0] < 0 else "📈 Meningkat"
    trend_rate = abs(coeffs[0])
    col_ins = color_fc
    st.markdown(f"""
    <div style="background:#0a1a0d; border:1px solid #1e3324; border-left:3px solid {col_ins};
         border-radius:10px; padding:14px 18px; margin-top:10px;">
        <div style="color:#2e7d52; font-size:0.68rem; text-transform:uppercase; letter-spacing:0.8px; margin-bottom:8px;">
            💡 Insight Otomatis
        </div>
        <div style="color:#a5d6a7; font-size:0.85rem; line-height:1.6;">
            Tren <b style="color:{col_ins};">{target_metric}</b> bersifat <b>{trend_dir}</b>
            dengan laju rata-rata <b style="color:{col_ins};">{trend_rate:.2f} {unit}/bulan</b>.
            <br>
            Proyeksi {forecast_months} bulan ke depan menunjukkan nilai berkisar
            <b style="color:{col_ins};">{max(0,y_future.min()):.1f} – {y_future.max():.1f} {unit}</b>.
            <br>
            {'⚠️ Perlu perhatian — tren meningkat dapat berdampak pada efisiensi operasional.' if coeffs[0] > 0 else '✅ Tren positif — terus pertahankan performa maintenance.'}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="footer">
    ⬡ CRANEMON v2.0 &nbsp;·&nbsp; HOIST CRANE MAINTENANCE INTELLIGENCE SYSTEM &nbsp;·&nbsp; 2024<br>
    Built with Streamlit & Plotly
</div>
""", unsafe_allow_html=True)

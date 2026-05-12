# =========================================================
# app.py
# Clinexa AI — AI-Powered Clinical Intelligence Platform
# =========================================================

import streamlit as st

from utils.pdf_reader import extract_text_from_pdf
from utils.ai_engine import (
    cached_summary,
    cached_notes,
    medical_chatbot,
)
from utils.priority_engine import detect_priority
from utils.export_pdf import create_pdf


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Clinexa AI · Clinical Intelligence",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# PREMIUM STYLING
# =========================================================

st.markdown("""
<style>

/* =====================================================
   FONTS
===================================================== */
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=IBM+Plex+Sans:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400&display=swap');

/* =====================================================
   DESIGN TOKENS
===================================================== */
:root {
    --bg-root:      #0c1017;
    --bg-panel:     #111720;
    --bg-card:      #151d2a;
    --bg-card-hi:   #1a2235;
    --bg-inset:     #0f1620;

    --border-dim:   rgba(255,255,255,0.055);
    --border-mid:   rgba(255,255,255,0.10);
    --border-hi:    rgba(255,255,255,0.16);

    --txt-primary:  #e8edf5;
    --txt-secondary:#7d8fa8;
    --txt-muted:    #3d4f68;
    --txt-white:    #ffffff;

    --teal:         #0ea5e9;
    --teal-dim:     rgba(14,165,233,0.12);
    --teal-glow:    rgba(14,165,233,0.22);
    --teal-border:  rgba(14,165,233,0.20);

    --red:          #f43f5e;
    --red-dim:      rgba(244,63,94,0.10);
    --red-border:   rgba(244,63,94,0.20);

    --amber:        #f59e0b;
    --amber-dim:    rgba(245,158,11,0.10);
    --amber-border: rgba(245,158,11,0.20);

    --yellow:       #eab308;
    --yellow-dim:   rgba(234,179,8,0.10);
    --yellow-border:rgba(234,179,8,0.20);

    --green:        #22c55e;
    --green-dim:    rgba(34,197,94,0.10);
    --green-border: rgba(34,197,94,0.20);

    --r-xs:  8px;
    --r-sm:  12px;
    --r-md:  18px;
    --r-lg:  24px;
    --r-xl:  30px;

    --shadow-sm:  0 2px 8px rgba(0,0,0,0.35);
    --shadow-md:  0 4px 20px rgba(0,0,0,0.40);
    --shadow-lg:  0 8px 40px rgba(0,0,0,0.50);
}

/* =====================================================
   GLOBAL RESET
===================================================== */
*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

.stApp {
    background-color: var(--bg-root);
    color: var(--txt-primary);
}

#MainMenu, footer { visibility: hidden; }

header[data-testid="stHeader"] {
    background: transparent !important;
    visibility: visible !important;
}

[data-testid="collapsedControl"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    position: fixed !important;
    top: 16px !important;
    left: 16px !important;
    z-index: 999999 !important;
    background: var(--bg-card) !important;
    border-radius: var(--r-sm) !important;
    padding: 6px !important;
    border: 1px solid var(--border-dim) !important;
    backdrop-filter: blur(12px) !important;
}

.block-container {
    padding: 2.75rem 3rem 3rem 3rem;
    max-width: 1320px;
}

/* =====================================================
   SIDEBAR
===================================================== */
section[data-testid="stSidebar"] {
    background-color: var(--bg-panel);
    border-right: 1px solid var(--border-dim);
    width: 272px !important;
}

section[data-testid="stSidebar"] > div {
    padding: 2rem 1.4rem;
}

.brand {
    display: flex;
    align-items: center;
    gap: 13px;
    padding-bottom: 1.8rem;
    margin-bottom: 1.8rem;
    border-bottom: 1px solid var(--border-dim);
}

.brand-mark {
    width: 40px;
    height: 40px;
    border-radius: var(--r-sm);
    background: linear-gradient(135deg, var(--teal) 0%, #6366f1 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    flex-shrink: 0;
    box-shadow: 0 0 0 1px rgba(14,165,233,0.30), 0 6px 18px rgba(14,165,233,0.25);
}

.brand-name {
    font-family: 'Syne', sans-serif;
    font-size: 18px;
    font-weight: 700;
    color: var(--txt-white);
    letter-spacing: -0.3px;
    line-height: 1;
    margin-bottom: 3px;
}

.brand-sub {
    font-size: 10.5px;
    color: var(--txt-muted);
    text-transform: uppercase;
    letter-spacing: 0.09em;
    font-weight: 500;
}

.nav-label {
    font-size: 9.5px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--txt-muted);
    padding: 0 4px;
    margin-bottom: 8px;
}

/* Radio nav */
.stRadio > label { display: none !important; }
.stRadio > div { display: flex; flex-direction: column; gap: 3px; }
.stRadio [role="radio"] { background: transparent !important; border: none !important; }
.stRadio label {
    display: flex !important;
    align-items: center !important;
    gap: 9px !important;
    padding: 10px 12px !important;
    border-radius: var(--r-xs) !important;
    font-size: 13.5px !important;
    font-weight: 500 !important;
    color: var(--txt-secondary) !important;
    cursor: pointer !important;
    transition: all 0.15s ease !important;
    border: 1px solid transparent !important;
    letter-spacing: 0.01em !important;
}
.stRadio label:hover {
    color: var(--txt-primary) !important;
    background: rgba(255,255,255,0.04) !important;
}
.stRadio input[type="radio"] { display: none !important; }

.sys-status {
    margin-top: 1rem;
    padding: 13px 14px;
    background: var(--green-dim);
    border: 1px solid var(--green-border);
    border-radius: var(--r-sm);
    display: flex;
    align-items: center;
    gap: 9px;
    font-size: 12.5px;
    color: var(--green);
    font-weight: 500;
}

.sys-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--green);
    flex-shrink: 0;
    animation: breathe 2.2s ease-in-out infinite;
}

@keyframes breathe {
    0%, 100% { opacity: 1; box-shadow: 0 0 0 0 rgba(34,197,94,0.5); }
    50%       { opacity: 0.7; box-shadow: 0 0 0 5px rgba(34,197,94,0); }
}

/* =====================================================
   PAGE HEADER
===================================================== */
.ph {
    margin-bottom: 2.75rem;
    animation: rise 0.5s cubic-bezier(0.16,1,0.3,1) both;
}

.ph-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: var(--teal-dim);
    border: 1px solid var(--teal-border);
    color: var(--teal);
    font-size: 10.5px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.10em;
    padding: 5px 13px;
    border-radius: 999px;
    margin-bottom: 20px;
}

.ph-title {
    font-family: 'Syne', sans-serif;
    font-size: 48px;
    font-weight: 700;
    color: var(--txt-white);
    line-height: 1.08;
    letter-spacing: -1.5px;
    margin-bottom: 16px;
}

.ph-title em {
    font-style: normal;
    background: linear-gradient(90deg, var(--teal), #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.ph-desc {
    font-size: 15px;
    color: var(--txt-secondary);
    line-height: 1.80;
    max-width: 600px;
    font-weight: 300;
}

@keyframes rise {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* =====================================================
   SECTION DIVIDER
===================================================== */
.sdiv {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 2rem 0 1.2rem;
}

.sdiv-label {
    font-size: 10px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--txt-muted);
    white-space: nowrap;
    font-family: 'Syne', sans-serif;
}

.sdiv-line {
    flex: 1;
    height: 1px;
    background: var(--border-dim);
}

/* =====================================================
   METRIC CARDS
===================================================== */
.m-card {
    background: var(--bg-card);
    border: 1px solid var(--border-dim);
    border-radius: var(--r-lg);
    padding: 26px 28px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s ease, transform 0.22s ease, box-shadow 0.22s ease;
    animation: rise 0.5s cubic-bezier(0.16,1,0.3,1) both;
}

.m-card::before {
    content: '';
    position: absolute;
    left: 0; top: 20%; bottom: 20%;
    width: 3px;
    border-radius: 0 3px 3px 0;
    background: var(--teal);
    opacity: 0;
    transition: opacity 0.2s ease;
}

.m-card:hover {
    border-color: var(--border-mid);
    transform: translateY(-3px);
    box-shadow: var(--shadow-lg);
}

.m-card:hover::before { opacity: 1; }

.m-icon {
    font-size: 22px;
    margin-bottom: 18px;
    display: block;
    filter: opacity(0.85);
}

.m-value {
    font-family: 'Syne', sans-serif;
    font-size: 50px;
    font-weight: 700;
    color: var(--txt-white);
    line-height: 1;
    letter-spacing: -2px;
    margin-bottom: 8px;
}

.m-label {
    font-size: 12.5px;
    color: var(--txt-secondary);
    font-weight: 500;
    margin-bottom: 6px;
    letter-spacing: 0.01em;
}

.m-delta {
    font-size: 11.5px;
    font-weight: 500;
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 3px 9px;
    border-radius: 999px;
}

.delta-pos { background: var(--green-dim); color: var(--green); border: 1px solid var(--green-border); }
.delta-neg { background: var(--red-dim);   color: var(--red);   border: 1px solid var(--red-border); }

/* =====================================================
   CARD
===================================================== */
.card {
    background: var(--bg-card);
    border: 1px solid var(--border-dim);
    border-radius: var(--r-lg);
    padding: 26px 28px;
    margin-bottom: 18px;
    box-shadow: var(--shadow-sm);
    transition: border-color 0.2s ease;
    animation: rise 0.45s cubic-bezier(0.16,1,0.3,1) both;
}

.card:hover { border-color: var(--border-mid); }

.card-head {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 18px;
}

.card-head-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--teal);
    flex-shrink: 0;
}

.card-head-label {
    font-family: 'Syne', sans-serif;
    font-size: 10.5px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--txt-muted);
}

.card-body {
    font-size: 14px;
    color: var(--txt-secondary);
    line-height: 1.85;
    font-weight: 300;
}

/* =====================================================
   ACTIVITY FEED
===================================================== */
.act-item {
    display: flex;
    align-items: flex-start;
    gap: 14px;
    padding: 14px 0;
    border-bottom: 1px solid var(--border-dim);
}

.act-item:first-child { padding-top: 0; }
.act-item:last-child  { border-bottom: none; padding-bottom: 0; }

.act-ring {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 13px;
    flex-shrink: 0;
    margin-top: 1px;
}

.act-body { flex: 1; }

.act-title {
    font-size: 13.5px;
    font-weight: 500;
    color: var(--txt-primary);
    margin-bottom: 3px;
    line-height: 1.4;
}

.act-meta {
    font-size: 11.5px;
    color: var(--txt-muted);
    font-weight: 400;
}

/* =====================================================
   SYSTEM STATUS ROWS
===================================================== */
.sys-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 0;
    border-bottom: 1px solid var(--border-dim);
}

.sys-row:first-child { padding-top: 0; }
.sys-row:last-child  { border-bottom: none; padding-bottom: 0; }

.sys-name {
    font-size: 13px;
    color: var(--txt-secondary);
    font-weight: 400;
    display: flex;
    align-items: center;
    gap: 8px;
}

.sys-name-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    flex-shrink: 0;
}

.sys-badge {
    font-size: 11px;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 999px;
    letter-spacing: 0.02em;
}

.badge-online  { background: var(--green-dim);  color: var(--green);  border: 1px solid var(--green-border); }
.badge-active  { background: var(--teal-dim);   color: var(--teal);   border: 1px solid var(--teal-border); }

/* =====================================================
   PRIORITY DISPLAY
===================================================== */
.priority-wrap {
    padding: 22px 26px;
    border-radius: var(--r-md);
    display: flex;
    align-items: center;
    gap: 18px;
    border: 1px solid;
    animation: rise 0.4s ease both;
}

.priority-ring {
    width: 46px;
    height: 46px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    flex-shrink: 0;
    position: relative;
}

.priority-ring::after {
    content: '';
    position: absolute;
    inset: -4px;
    border-radius: 50%;
    border: 2px solid currentColor;
    opacity: 0.3;
    animation: ring-spin 3s linear infinite;
}

@keyframes ring-spin {
    from { transform: rotate(0deg); }
    to   { transform: rotate(360deg); }
}

.priority-info { flex: 1; }

.priority-label {
    font-family: 'Syne', sans-serif;
    font-size: 18px;
    font-weight: 700;
    letter-spacing: -0.3px;
    margin-bottom: 4px;
}

.priority-sub {
    font-size: 13px;
    font-weight: 300;
    opacity: 0.75;
    line-height: 1.5;
}

.p-emergency {
    background: var(--red-dim);
    border-color: var(--red-border);
    color: #fb7185;
}
.p-emergency .priority-ring {
    background: rgba(244,63,94,0.15);
    animation: pulse-red 1.1s ease-in-out infinite;
}
@keyframes pulse-red {
    0%, 100% { box-shadow: 0 0 0 0 rgba(244,63,94,0.5); }
    50%       { box-shadow: 0 0 0 10px rgba(244,63,94,0); }
}

.p-high {
    background: var(--amber-dim);
    border-color: var(--amber-border);
    color: #fbbf24;
}
.p-high .priority-ring {
    background: rgba(245,158,11,0.15);
    animation: pulse-amber 1.6s ease-in-out infinite;
}
@keyframes pulse-amber {
    0%, 100% { box-shadow: 0 0 0 0 rgba(245,158,11,0.4); }
    50%       { box-shadow: 0 0 0 8px rgba(245,158,11,0); }
}

.p-medium {
    background: var(--yellow-dim);
    border-color: var(--yellow-border);
    color: #fde047;
}
.p-medium .priority-ring { background: rgba(234,179,8,0.15); }

.p-low {
    background: var(--green-dim);
    border-color: var(--green-border);
    color: #4ade80;
}
.p-low .priority-ring { background: rgba(34,197,94,0.15); }

/* =====================================================
   FILE UPLOADER
===================================================== */
[data-testid="stFileUploader"] {
    background: var(--bg-card) !important;
    border: 1.5px dashed rgba(14,165,233,0.20) !important;
    border-radius: var(--r-lg) !important;
    transition: border-color 0.2s ease !important;
}

[data-testid="stFileUploader"]:hover {
    border-color: rgba(14,165,233,0.40) !important;
}

[data-testid="stFileUploader"] section {
    padding: 42px 28px !important;
    text-align: center;
}

[data-testid="stFileUploader"] p,
[data-testid="stFileUploader"] small,
[data-testid="stFileUploader"] span {
    color: var(--txt-secondary) !important;
}

/* =====================================================
   TEXTAREA
===================================================== */
.stTextArea textarea {
    background: var(--bg-inset) !important;
    color: var(--txt-primary) !important;
    border: 1px solid var(--border-dim) !important;
    border-radius: var(--r-md) !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-size: 13.5px !important;
    line-height: 1.75 !important;
    font-weight: 300 !important;
    transition: border-color 0.18s ease !important;
    resize: vertical !important;
}

.stTextArea textarea:focus {
    border-color: var(--teal-border) !important;
    box-shadow: 0 0 0 3px var(--teal-dim) !important;
}

.stTextArea label {
    color: var(--txt-muted) !important;
    font-size: 10.5px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.10em !important;
    font-family: 'Syne', sans-serif !important;
}

/* =====================================================
   BUTTONS
===================================================== */
.stButton > button,
.stDownloadButton > button {
    background: var(--teal) !important;
    color: var(--bg-root) !important;
    border: none !important;
    border-radius: var(--r-sm) !important;
    padding: 0.7rem 1.6rem !important;
    font-size: 13.5px !important;
    font-weight: 700 !important;
    font-family: 'Syne', sans-serif !important;
    letter-spacing: 0.04em !important;
    transition: all 0.18s ease !important;
    box-shadow: 0 4px 14px rgba(14,165,233,0.30) !important;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 22px rgba(14,165,233,0.42) !important;
    background: #38bdf8 !important;
}

.stButton > button:active,
.stDownloadButton > button:active {
    transform: translateY(0) !important;
}

.stDownloadButton button:focus,
.stDownloadButton button:active {
    opacity: 1 !important;
    filter: brightness(1) !important;
}

/* =====================================================
   CHAT
===================================================== */
.chat-empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 380px;
    gap: 16px;
    text-align: center;
    background: var(--bg-card);
    border: 1px solid var(--border-dim);
    border-radius: var(--r-xl);
    padding: 48px 40px;
}

.chat-empty-icon {
    width: 64px;
    height: 64px;
    border-radius: 50%;
    background: var(--teal-dim);
    border: 1px solid var(--teal-border);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 26px;
    margin-bottom: 4px;
}

.chat-empty-title {
    font-family: 'Syne', sans-serif;
    font-size: 17px;
    font-weight: 700;
    color: var(--txt-primary);
    letter-spacing: -0.3px;
}

.chat-empty-sub {
    font-size: 13.5px;
    color: var(--txt-muted);
    font-weight: 300;
    max-width: 320px;
    line-height: 1.7;
}

[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 6px 0 !important;
    margin-bottom: 2px !important;
}

[data-testid="chatAvatarIcon-assistant"] {
    background: linear-gradient(135deg, var(--teal), #6366f1) !important;
    border-radius: var(--r-xs) !important;
}

[data-testid="chatAvatarIcon-user"] {
    background: var(--bg-card-hi) !important;
    border: 1px solid var(--border-mid) !important;
    border-radius: var(--r-xs) !important;
}

[data-testid="stChatInput"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-mid) !important;
    border-radius: var(--r-md) !important;
}

[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: var(--txt-primary) !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-size: 14px !important;
    border: none !important;
    box-shadow: none !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: var(--txt-muted) !important;
}

/* =====================================================
   UPLOAD EMPTY STATE
===================================================== */
.upload-empty {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 200px;
    gap: 12px;
    background: var(--bg-card);
    border: 1.5px dashed var(--border-mid);
    border-radius: var(--r-lg);
    padding: 48px;
    text-align: center;
    margin-top: -6px;
}

.upload-empty-icon {
    font-size: 30px;
    filter: opacity(0.4);
    margin-bottom: 6px;
}

.upload-empty-title {
    font-size: 14.5px;
    color: var(--txt-secondary);
    font-weight: 500;
}

.upload-empty-sub {
    font-size: 13px;
    color: var(--txt-muted);
    font-weight: 300;
}

/* =====================================================
   MISC
===================================================== */
.stSpinner > div { border-top-color: var(--teal) !important; }

::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.07); border-radius: 999px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.13); }

@media (max-width: 900px) {
    .block-container { padding: 1.5rem 1.25rem; }
    .ph-title { font-size: 34px; }
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("""
    <div class="brand">
        <div class="brand-mark">🩺</div>
        <div>
            <div class="brand-name">Clinexa AI</div>
            <div class="brand-sub">Clinical Intelligence</div>
        </div>
    </div>
    <div class="nav-label">Workspace</div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        [
            "📊  Dashboard",
            "📄  Upload & Analysis",
            "💬  Medical Assistant",
        ],
        label_visibility="collapsed"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="sys-status">
        <div class="sys-dot"></div>
        All AI systems operational
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# ROUTING
# =========================================================

is_dashboard = "Dashboard" in page
is_upload    = "Upload" in page
is_chat      = "Assistant" in page


# =========================================================
# DASHBOARD
# =========================================================

if is_dashboard:

    st.markdown("""
    <div class="ph">
        <div class="ph-badge">⬡ &nbsp;Overview</div>
        <div class="ph-title">Clinical <em>Intelligence</em><br>Dashboard</div>
        <div class="ph-desc">
            Real-time overview of AI report processing, patient triage,
            documentation, and system health across the clinical platform.
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3, gap="small")

    with c1:
        st.markdown("""
        <div class="m-card">
            <span class="m-icon">📋</span>
            <div class="m-value">124</div>
            <div class="m-label">Reports Processed</div>
            <span class="m-delta delta-pos">↑ 12% this week</span>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="m-card">
            <span class="m-icon">🚨</span>
            <div class="m-value">18</div>
            <div class="m-label">Critical Cases</div>
            <span class="m-delta delta-neg">↑ 3 since yesterday</span>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="m-card">
            <span class="m-icon">🧠</span>
            <div class="m-value">97%</div>
            <div class="m-label">AI Accuracy</div>
            <span class="m-delta delta-pos">↑ 0.4% this month</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    left, right = st.columns([1.45, 1], gap="large")

    with left:
        st.markdown("""
        <div class="card">
            <div class="card-head">
                <div class="card-head-dot"></div>
                <div class="card-head-label">Recent Activity</div>
            </div>
            <div class="act-item">
                <div class="act-ring" style="background:rgba(244,63,94,0.12);color:#fb7185;">🚨</div>
                <div class="act-body">
                    <div class="act-title">Emergency cardiac case flagged — Patient #A-2847</div>
                    <div class="act-meta">2 minutes ago &nbsp;·&nbsp; Emergency Priority</div>
                </div>
            </div>
            <div class="act-item">
                <div class="act-ring" style="background:rgba(245,158,11,0.12);color:#fbbf24;">📝</div>
                <div class="act-body">
                    <div class="act-title">AI doctor notes generated — Patient #B-1193</div>
                    <div class="act-meta">17 minutes ago &nbsp;·&nbsp; High Priority</div>
                </div>
            </div>
            <div class="act-item">
                <div class="act-ring" style="background:rgba(14,165,233,0.12);color:var(--teal);">📊</div>
                <div class="act-body">
                    <div class="act-title">Batch of 6 reports analyzed successfully</div>
                    <div class="act-meta">43 minutes ago &nbsp;·&nbsp; Mixed Priority</div>
                </div>
            </div>
            <div class="act-item">
                <div class="act-ring" style="background:rgba(34,197,94,0.12);color:var(--green);">⬇</div>
                <div class="act-body">
                    <div class="act-title">Discharge summary exported — Patient #C-0042</div>
                    <div class="act-meta">1 hour ago &nbsp;·&nbsp; Low Priority</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown("""
        <div class="card">
            <div class="card-head">
                <div class="card-head-dot" style="background:var(--green);"></div>
                <div class="card-head-label">System Status</div>
            </div>
            <div class="sys-row">
                <div class="sys-name">
                    <div class="sys-name-dot" style="background:var(--green);"></div>
                    AI Summary Engine
                </div>
                <span class="sys-badge badge-online">Online</span>
            </div>
            <div class="sys-row">
                <div class="sys-name">
                    <div class="sys-name-dot" style="background:var(--green);"></div>
                    PDF Parser
                </div>
                <span class="sys-badge badge-online">Online</span>
            </div>
            <div class="sys-row">
                <div class="sys-name">
                    <div class="sys-name-dot" style="background:var(--teal);"></div>
                    Priority Engine
                </div>
                <span class="sys-badge badge-active">Active</span>
            </div>
            <div class="sys-row">
                <div class="sys-name">
                    <div class="sys-name-dot" style="background:var(--green);"></div>
                    Export Module
                </div>
                <span class="sys-badge badge-online">Online</span>
            </div>
            <div class="sys-row">
                <div class="sys-name">
                    <div class="sys-name-dot" style="background:var(--green);"></div>
                    Medical Assistant
                </div>
                <span class="sys-badge badge-online">Online</span>
            </div>
        </div>

        <div class="card">
            <div class="card-head">
                <div class="card-head-dot" style="background:#818cf8;"></div>
                <div class="card-head-label">Platform Overview</div>
            </div>
            <div class="card-body">
                Clinexa AI streamlines clinical workflows through intelligent
                report summarization, automated patient prioritization,
                AI-generated doctor notes, and integrated clinical assistance —
                built for modern healthcare environments.
            </div>
        </div>
        """, unsafe_allow_html=True)


# =========================================================
# MEDICAL ASSISTANT
# =========================================================

elif is_chat:

    st.markdown("""
    <div class="ph">
        <div class="ph-badge">💬 &nbsp;AI Assistant</div>
        <div class="ph-title">Medical <em>AI</em><br>Assistant</div>
        <div class="ph-desc">
            Ask any clinical or healthcare-related question and receive
            accurate, AI-powered assistance from the Clinexa engine.
        </div>
    </div>
    """, unsafe_allow_html=True)

    question = st.chat_input("Ask a clinical or medical question…")

    if not question:
        st.markdown("""
        <div class="chat-empty-state">
            <div class="chat-empty-icon">🩺</div>
            <div class="chat-empty-title">AI Assistant Ready</div>
            <div class="chat-empty-sub">
                Type a healthcare question below to begin.
                Powered by the Clinexa clinical AI engine.
            </div>
        </div>
        """, unsafe_allow_html=True)

    else:
        with st.chat_message("user"):
            st.write(question)

        with st.spinner("Generating clinical response…"):
            response = medical_chatbot(question)

        with st.chat_message("assistant"):
            st.write(response)


# =========================================================
# UPLOAD & ANALYSIS
# =========================================================

else:

    st.markdown("""
    <div class="ph">
        <div class="ph-badge">📄 &nbsp;Report Analysis</div>
        <div class="ph-title">Upload Patient<br><em>Medical Report</em></div>
        <div class="ph-desc">
            Upload a PDF medical report to receive an AI-generated summary,
            patient priority classification, and structured clinical notes.
        </div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload PDF Medical Report",
        type=["pdf"],
        label_visibility="collapsed"
    )

    if not uploaded_file:
        st.markdown("""
        <div class="upload-empty">
            <div class="upload-empty-icon">📂</div>
            <div class="upload-empty-title">No report uploaded yet</div>
            <div class="upload-empty-sub">Use the file picker above to upload a patient PDF</div>
        </div>
        """, unsafe_allow_html=True)

    if uploaded_file:

        # ── Extract ──────────────────────────────────────
        with st.spinner("Extracting report content…"):
            report_text = extract_text_from_pdf(uploaded_file)

        st.markdown("""
        <div class="sdiv">
            <div class="sdiv-label">Extracted Content</div>
            <div class="sdiv-line"></div>
        </div>
        """, unsafe_allow_html=True)

        st.text_area(
            "Report Content",
            report_text,
            height=220,
            label_visibility="collapsed"
        )

        # ── Summary ──────────────────────────────────────
        with st.spinner("Generating AI medical summary…"):
            summary = cached_summary(report_text)

        st.markdown("""
        <div class="sdiv">
            <div class="sdiv-label">AI Medical Summary</div>
            <div class="sdiv-line"></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="card">
            <div class="card-head">
                <div class="card-head-dot"></div>
                <div class="card-head-label">Summary</div>
            </div>
            <div class="card-body">{summary}</div>
        </div>
        """, unsafe_allow_html=True)

        # ── Priority ─────────────────────────────────────
        priority = detect_priority(report_text)

        st.markdown("""
        <div class="sdiv">
            <div class="sdiv-label">Appointment Priority</div>
            <div class="sdiv-line"></div>
        </div>
        """, unsafe_allow_html=True)

        priority_map = {
            "Emergency": {
                "cls":  "p-emergency",
                "icon": "🚨",
                "desc": "Requires immediate medical attention — escalate now",
            },
            "High": {
                "cls":  "p-high",
                "icon": "⚠️",
                "desc": "Urgent follow-up required within 24 hours",
            },
            "Medium": {
                "cls":  "p-medium",
                "icon": "🕐",
                "desc": "Schedule follow-up within the next few days",
            },
            "Low": {
                "cls":  "p-low",
                "icon": "✓",
                "desc": "Routine follow-up — no immediate concern",
            },
        }

        p = priority_map.get(priority, priority_map["Low"])

        st.markdown(f"""
        <div class="priority-wrap {p['cls']}">
            <div class="priority-ring">{p['icon']}</div>
            <div class="priority-info">
                <div class="priority-label">{priority} Priority</div>
                <div class="priority-sub">{p['desc']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Doctor Notes ─────────────────────────────────
        with st.spinner("Generating structured doctor notes…"):
            notes = cached_notes(report_text)

        st.markdown("""
        <div class="sdiv">
            <div class="sdiv-label">AI Doctor Notes</div>
            <div class="sdiv-line"></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="card">
            <div class="card-head">
                <div class="card-head-dot" style="background:#818cf8;"></div>
                <div class="card-head-label">Clinical Notes</div>
            </div>
            <div class="card-body">{notes}</div>
        </div>
        """, unsafe_allow_html=True)

        # ── Export ───────────────────────────────────────
        st.markdown("""
        <div class="sdiv">
            <div class="sdiv-label">Export</div>
            <div class="sdiv-line"></div>
        </div>
        """, unsafe_allow_html=True)

        pdf_path = create_pdf(summary, notes, priority)

        with open(pdf_path, "rb") as file:
            st.download_button(
                label="⬇  Download Full Clinical Report",
                data=file,
                file_name="clinexa_report.pdf",
                mime="application/pdf"
            )
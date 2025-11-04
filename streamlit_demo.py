# ─────────────────── CUSTOM CSS (Airbus Light Theme) ───────────────────
st.markdown("""
    <style>
    /* GLOBAL LAYOUT */
    body, .stApp {
        background-color: #ffffff; /* white background */
        color: #0a2342; /* Airbus dark navy text */
        font-family: "Helvetica Neue", sans-serif;
    }

    /* TITLE + HEADERS */
    h1, h2, h3 {
        color: #0a2342 !important;
        font-weight: 600;
    }

    /* TABS */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #f5f7fa;
        border-radius: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #0a2342 !important;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        border-bottom: 3px solid #005bbb !important; /* Airbus blue */
        font-weight: 600;
    }

    /* METRIC CARDS */
    [data-testid="stMetricValue"] {
        color: #005bbb !important;
        font-weight: 700 !important;
    }
    [data-testid="stMetricDelta"] {
        color: #0078d7 !important;
    }

    /* BUTTONS */
    div.stButton > button {
        background-color: #005bbb;
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: 600;
        padding: 0.5em 1em;
        transition: 0.2s;
    }
    div.stButton > button:hover {
        background-color: #003f87;
        transform: scale(1.03);
    }

    /* INPUTS */
    textarea, input[type="text"], select {
        background-color: #ffffff;
        color: #0a2342;
        border-radius: 6px;
        border: 1px solid #ccd6e0;
        padding: 0.4em;
    }

    /* ALERT COLORS */
    .stAlert {
        border-radius: 8px;
        padding: 1em;
        font-weight: 500;
    }
    .stAlert[data-baseweb="alert"][class*="success"] {
        background-color: #e6f2ff !important;
        color: #003f87 !important;
        border-left: 5px solid #005bbb;
    }
    .stAlert[data-baseweb="alert"][class*="warning"] {
        background-color: #fff5e6 !important;
        color: #6e4b00 !important;
        border-left: 5px solid #ffb100;
    }
    .stAlert[data-baseweb="alert"][class*="error"] {
        background-color: #fde8e8 !important;
        color: #8b0000 !important;
        border-left: 5px solid #d32f2f;
    }

    /* FOOTER */
    footer, .stCaption, .css-1lsmgbg {
        color: #4b6382;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================
# CINESCOPE — MOVIE RATINGS & VIEWER INTELLIGENCE
# Complete Streamlit application
# ============================================================
# Run:
#   pip install streamlit pandas plotly
#   streamlit run app.py
#
# Expected data:
#   dataset/movies.csv   -> movieId, title, genres
#   dataset/ratings.csv  -> userId (optional), movieId, rating
#
# Design direction:
#   Editorial application workspace inspired by the supplied
#   EcoSort AI reference: clear navigation, hero, overview,
#   workspaces, status labels, data panels and restrained styling.
#   This is an independent CineScope design, not a copy of branding.
# ============================================================

from pathlib import Path
import re
import html

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ------------------------------------------------------------
# 1. PAGE CONFIG
# ------------------------------------------------------------

st.set_page_config(
    page_title="CineScope | Movie Intelligence",
    page_icon="🎞️",
    layout="wide",
    initial_sidebar_state="auto",
)


# ------------------------------------------------------------
# 2. DESIGN SYSTEM
# ------------------------------------------------------------

BG = "#EEF5F1"
SURFACE = "#FFFFFF"
SURFACE_SOFT = "#DFEDE6"
INK = "#10231C"
MUTED = "#4F6A5E"
LINE = "#C3D8CD"
ACCENT = "#176B50"
ACCENT_DARK = "#0F4A38"
ACCENT_PALE = "#DDF0E7"
ORANGE = "#E0862B"
ORANGE_PALE = "#FDEEDC"
CHART_COLORS = ["#176B50", "#E0862B", "#6FB39A", "#3C8DAD", "#F2B84B", "#0F4A38"]

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

    :root {
        --bg: #EEF5F1;
        --surface: #FFFFFF;
        --ink: #10231C;
        --muted: #4F6A5E;
        --line: #C3D8CD;
        --accent: #176B50;
        --accent-dark: #0F4A38;
        --orange: #E0862B;
        --accent-pale: #DDF0E7;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        color: var(--ink);
    }

    .stApp {
        background: var(--bg);
    }

    [data-testid="stHeader"] {
        background: rgba(238,245,241,.94);
        border-bottom: 1px solid rgba(16,35,28,.10);
    }

    [data-testid="stToolbar"] { right: 1rem; }

    .block-container {
        max-width: 1500px;
        padding-top: 1.55rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3, h4 {
        font-family: 'Manrope', sans-serif !important;
        color: var(--ink);
        letter-spacing: -.035em;
    }

    p, label, .stCaption, [data-testid="stMarkdownContainer"] {
        color: var(--ink);
    }

    section[data-testid="stSidebar"] {
        background: #DFEDE6;
        border-right: 1px solid #B5CDC0;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.25rem;
    }

    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #2E4A3F;
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 8px 4px 22px;
    }

    .brand-mark {
        width: 42px;
        height: 42px;
        display: grid;
        place-items: center;
        border-radius: 12px;
        background: #0F4A38;
        color: white;
        font-size: 21px;
        font-weight: 800;
    }

    .brand-name {
        font-family: 'Manrope', sans-serif;
        font-size: 20px;
        font-weight: 800;
        letter-spacing: -.8px;
        line-height: 1.1;
        color: #10231C;
    }

    .brand-caption {
        font-size: 9px;
        font-weight: 700;
        letter-spacing: 1.8px;
        color: #4F6A5E;
        margin-top: 4px;
    }

    .side-label {
        color: #5A7568;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 1.5px;
        margin: 13px 0 8px;
    }

    .side-note {
        border: 1px solid #BBD2C6;
        border-radius: 10px;
        padding: 12px;
        background: rgba(255,255,255,.55);
        font-size: 12px;
        line-height: 1.6;
        color: #3F5C50;
    }

    .eyebrow {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 6px 10px;
        border-radius: 5px;
        background: #F2B84B;
        color: #10231C;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 1.3px;
        text-transform: uppercase;
    }

    .hero {
        position: relative;
        overflow: hidden;
        background: linear-gradient(120deg, #0B3B2D 0%, #0F4A38 55%, #176B50 100%);
        border: 1px solid #0F4A38;
        border-radius: 16px;
        padding: 34px 36px;
        margin: 4px 0 22px;
    }

    .hero:after {
        content: '✳';
        position: absolute;
        right: 5%;
        top: -35px;
        font-size: 190px;
        line-height: 1;
        color: #FFFFFF;
        opacity: .12;
        pointer-events: none;
    }

    .hero h1 {
        font-family: 'Manrope', sans-serif !important;
        font-size: clamp(34px, 4.2vw, 58px);
        line-height: 1.04;
        letter-spacing: -2.8px;
        max-width: 720px;
        margin: 16px 0 12px;
        color: #FFFFFF;
        font-weight: 800;
    }

    .hero p {
        color: #DDF0E7;
        max-width: 720px;
        font-size: 14px;
        line-height: 1.8;
        margin: 0;
    }

    .hero-meta {
        display: flex;
        gap: 9px;
        flex-wrap: wrap;
        margin-top: 20px;
    }

    .meta-chip {
        border: 1px solid rgba(255,255,255,.45);
        border-radius: 6px;
        padding: 7px 10px;
        font-size: 11px;
        font-weight: 700;
        color: #FFFFFF;
        background: rgba(255,255,255,.14);
    }

    .section-head {
        display: flex;
        justify-content: space-between;
        align-items: end;
        gap: 14px;
        margin: 26px 0 12px;
        padding-bottom: 10px;
        border-bottom: 1px solid var(--line);
    }

    .section-head h2 {
        font-size: 19px;
        font-weight: 800;
        margin: 0;
        letter-spacing: -.6px;
    }

    .section-head p {
        font-size: 11px;
        color: var(--muted);
        margin: 4px 0 0;
    }

    .section-tag {
        color: var(--accent-dark);
        background: var(--accent-pale);
        border-radius: 5px;
        padding: 6px 9px;
        font-size: 9px;
        font-weight: 800;
        letter-spacing: 1px;
        white-space: nowrap;
    }

    [data-testid="stMetric"] {
        background: var(--surface);
        border: 1px solid var(--line);
        border-radius: 11px;
        padding: 17px 18px;
        box-shadow: 0 2px 8px rgba(23,107,80,.10);
    }

    [data-testid="stMetricLabel"] {
        color: #4F6A5E !important;
        font-size: 11px !important;
        font-weight: 700 !important;
    }

    [data-testid="stMetricValue"] {
        color: #10231C !important;
        font-family: 'Manrope', sans-serif;
        font-size: 27px !important;
        font-weight: 800 !important;
        letter-spacing: -1px;
    }

    [data-testid="stMetricDelta"] { font-size: 10px; }

    .panel {
        background: #FFFFFF;
        border: 1px solid #C3D8CD;
        border-radius: 11px;
        padding: 17px 18px;
        margin-bottom: 12px;
    }

    .panel-title {
        color: #10231C;
        font-family: 'Manrope', sans-serif;
        font-size: 14px;
        font-weight: 800;
        margin-bottom: 4px;
    }

    .panel-subtitle {
        color: #5A7568;
        font-size: 11px;
        margin-bottom: 12px;
    }

    .quick-card {
        min-height: 112px;
        background: #FFFFFF;
        border: 1px solid #C3D8CD;
        border-radius: 11px;
        padding: 16px;
    }

    .quick-icon {
        display: inline-grid;
        place-items: center;
        width: 30px;
        height: 30px;
        border-radius: 8px;
        background: #DDF0E7;
        color: #0F4A38;
        font-size: 15px;
        margin-bottom: 10px;
    }

    .quick-title {
        font-family: 'Manrope', sans-serif;
        font-size: 13px;
        font-weight: 800;
        color: #10231C;
        margin-bottom: 4px;
    }

    .quick-copy {
        color: #4F6A5E;
        font-size: 11px;
        line-height: 1.5;
    }

    .status-pill {
        display: inline-block;
        padding: 5px 8px;
        border-radius: 5px;
        background: #DDF0E7;
        color: #0F4A38;
        font-size: 9px;
        font-weight: 800;
        letter-spacing: .8px;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 5px;
        border-bottom: 1px solid #C3D8CD;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #4F6A5E;
        border-radius: 6px 6px 0 0;
        font-weight: 700;
        font-size: 12px;
        padding: 10px 14px;
    }

    .stTabs [aria-selected="true"] {
        color: #0F4A38 !important;
        background: #DDF0E7 !important;
    }

    .stTabs [data-baseweb="tab-highlight"] {
        background: #176B50 !important;
    }

    div[data-testid="stPlotlyChart"],
    div[data-testid="stDataFrame"] {
        background: white;
        border: 1px solid #C3D8CD;
        border-radius: 10px;
        overflow: hidden;
    }

    div[data-testid="stButton"] button,
    div[data-testid="stDownloadButton"] button {
        border: 1px solid #176B50;
        background: #176B50;
        color: white;
        border-radius: 7px;
        font-weight: 700;
        min-height: 38px;
        transition: .18s ease;
    }

    div[data-testid="stButton"] button:hover,
    div[data-testid="stDownloadButton"] button:hover {
        background: #0F4A38;
        border-color: #0F4A38;
        color: white;
    }

    [data-baseweb="select"] > div,
    [data-baseweb="input"] > div {
        background: white;
        border-color: #BBD2C6;
        border-radius: 7px;
    }

    input, textarea { border-radius: 7px !important; }

    [data-testid="stSlider"] [role="slider"] {
        background: #176B50;
    }

    hr {
        border-color: #C3D8CD;
        margin: 22px 0;
    }

    .empty-state {
        border: 1px dashed #B5CDC0;
        border-radius: 10px;
        padding: 24px;
        text-align: center;
        color: #4F6A5E;
        background: rgba(255,255,255,.55);
        font-size: 12px;
    }

    .footer {
        border-top: 1px solid #C3D8CD;
        margin-top: 38px;
        padding: 18px 5px;
        text-align: center;
        color: #5A7568;
        font-size: 11px;
        line-height: 1.8;
    }

    .footer strong { color: #0F4A38; }

    .stApp, [data-testid="stAppViewContainer"] { overflow-x: hidden; }

    @media (max-width: 900px) {
        .block-container { padding-left: 1.2rem; padding-right: 1.2rem; }
        .hero { padding: 28px 24px; }
    }

    @media (max-width: 700px) {
        .block-container { padding: 3.2rem .8rem 2rem; }

        /* stack columns, but keep KPI cards two per row */
        [data-testid="stHorizontalBlock"] { flex-wrap: wrap !important; gap: .7rem !important; }
        [data-testid="stHorizontalBlock"] > [data-testid="stColumn"],
        [data-testid="stHorizontalBlock"] > [data-testid="column"] {
            flex: 1 1 100% !important; min-width: 100% !important; width: 100% !important;
        }
        [data-testid="stHorizontalBlock"]:has([data-testid="stMetric"]) > [data-testid="stColumn"],
        [data-testid="stHorizontalBlock"]:has([data-testid="stMetric"]) > [data-testid="column"] {
            flex: 1 1 calc(50% - .5rem) !important; min-width: calc(50% - .5rem) !important; width: calc(50% - .5rem) !important;
        }

        .hero { padding: 22px 18px; border-radius: 14px; }
        .hero h1 { font-size: clamp(21px, 6vw, 28px); letter-spacing: -.8px; line-height: 1.18; }
        .hero h1 br { display: none; }
        .hero p { font-size: 13px; line-height: 1.65; }
        .hero:after { right: -20px; font-size: 120px; }
        .meta-chip { font-size: 10px; padding: 6px 8px; }

        .section-head { flex-wrap: wrap; align-items: flex-start; }
        .section-head h2 { font-size: 17px; }

        [data-testid="stMetric"] { padding: 12px 13px; }
        [data-testid="stMetricValue"] { font-size: 20px !important; }
        [data-testid="stMetricLabel"] { font-size: 9.5px !important; }

        .stTabs [data-baseweb="tab-list"] { overflow-x: auto; flex-wrap: nowrap; }
        .stTabs [data-baseweb="tab"] { white-space: nowrap; padding: 9px 11px; }

        div[data-testid="stPlotlyChart"], div[data-testid="stDataFrame"] { overflow-x: auto; }
        div[data-testid="stButton"] button, div[data-testid="stDownloadButton"] button { min-height: 44px; }
        input, textarea { font-size: 16px !important; }
        .quick-card { min-height: 0; }
        .footer { font-size: 10px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ------------------------------------------------------------
# 3. PLOTLY STYLE
# ------------------------------------------------------------

def style_chart(fig, height=360, show_legend=True):
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FFFFFF",
        font=dict(family="DM Sans, sans-serif", color="#2E4A3F", size=11),
        title=dict(font=dict(family="Manrope, sans-serif", size=14, color="#10231C")),
        height=height,
        margin=dict(l=18, r=18, t=55, b=25),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=10),
        ),
        showlegend=show_legend,
        hoverlabel=dict(
            bgcolor="#10231C",
            font_color="#FFFFFF",
            bordercolor="#10231C",
        ),
    )
    fig.update_xaxes(
        automargin=True,
        showgrid=True,
        gridcolor="#E4EEE8",
        zeroline=False,
        linecolor="#C9DBD1",
    )
    fig.update_yaxes(
        automargin=True,
        showgrid=True,
        gridcolor="#E4EEE8",
        zeroline=False,
        linecolor="#C9DBD1",
    )
    return fig


# ------------------------------------------------------------
# 4. DATA DISCOVERY AND LOADING
# ------------------------------------------------------------

def find_file(filename):
    root = Path(__file__).resolve().parent
    candidates = [
        root / "dataset" / filename,
        root / "data" / filename,
        root / filename,
        root / "ml-latest-small" / filename,
        root / "ml-latest" / filename,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


@st.cache_data(show_spinner="Preparing the movie intelligence workspace…")
def load_data(movies_path, ratings_path):
    movies = pd.read_csv(movies_path, usecols=["movieId", "title", "genres"])
    ratings = pd.read_csv(ratings_path, usecols=["movieId", "rating"])

    movies["movieId"] = pd.to_numeric(movies["movieId"], errors="coerce")
    ratings["movieId"] = pd.to_numeric(ratings["movieId"], errors="coerce")
    ratings["rating"] = pd.to_numeric(ratings["rating"], errors="coerce")

    movies = movies.dropna(subset=["movieId", "title", "genres"]).copy()
    ratings = ratings.dropna(subset=["movieId", "rating"]).copy()

    movies["movieId"] = movies["movieId"].astype("int64")
    ratings["movieId"] = ratings["movieId"].astype("int64")

    ratings = ratings[ratings["rating"].between(0.5, 5.0)].copy()

    stats = (
        ratings.groupby("movieId")["rating"]
        .agg(
            average_rating="mean",
            rating_count="count",
            rating_std="std",
        )
        .reset_index()
    )

    global_mean = float(ratings["rating"].mean()) if not ratings.empty else 0.0
    minimum_votes = 20

    stats["weighted_rating"] = (
        (stats["rating_count"] / (stats["rating_count"] + minimum_votes))
        * stats["average_rating"]
        + (minimum_votes / (stats["rating_count"] + minimum_votes)) * global_mean
    )

    movies["release_year"] = pd.to_numeric(
        movies["title"].str.extract(r"\((\d{4})\)\s*$")[0],
        errors="coerce",
    )

    catalog = movies.merge(stats, on="movieId", how="left")
    for col in ["average_rating", "rating_count", "rating_std", "weighted_rating"]:
        catalog[col] = catalog[col].fillna(0)

    catalog["rating_count"] = catalog["rating_count"].astype("int64")
    catalog["genre_list"] = catalog["genres"].apply(
        lambda value: [
            item for item in str(value).split("|")
            if item and item != "(no genres listed)"
        ]
    )

    global_distribution = (
        ratings["rating"].value_counts().sort_index()
        .rename_axis("rating").reset_index(name="count")
    )

    rating_distribution = (
        ratings.groupby(["movieId", "rating"])
        .size().reset_index(name="count")
    )

    return catalog, ratings, rating_distribution, global_distribution, global_mean


movies_file = find_file("movies.csv")
ratings_file = find_file("ratings.csv")

if movies_file is None or ratings_file is None:
    st.markdown(
        """
        <div class="hero">
            <span class="eyebrow">CINESCOPE · SETUP REQUIRED</span>
            <h1>Your movie intelligence workspace starts here.</h1>
            <p>Add the two MovieLens CSV files to the dataset folder to open the dashboard.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.error(
        "Dataset files were not found. Required files: "
        "`dataset/movies.csv` and `dataset/ratings.csv`."
    )
    st.code(
        "Movie-Ratings-Analysis/\n"
        "├── app.py\n"
        "└── dataset/\n"
        "    ├── movies.csv\n"
        "    └── ratings.csv",
        language="text",
    )
    st.stop()

try:
    catalog, ratings, rating_distribution, global_distribution, global_mean = load_data(
        str(movies_file), str(ratings_file)
    )
except Exception as exc:
    st.error("The dataset could not be loaded. Check the CSV columns and file contents.")
    st.exception(exc)
    st.stop()

if catalog.empty:
    st.error("The movie catalogue is empty.")
    st.stop()


# ------------------------------------------------------------
# 5. SIDEBAR WORKSPACE NAVIGATION AND FILTERS
# ------------------------------------------------------------

st.sidebar.markdown(
    """
    <div class="brand">
        <div class="brand-mark">C</div>
        <div>
            <div class="brand-name">CineScope</div>
            <div class="brand-caption">MOVIE INTELLIGENCE</div>
        </div>
    </div>
    <div class="side-label">WORKSPACE</div>
    """,
    unsafe_allow_html=True,
)

page = st.sidebar.radio(
    "Navigate",
    [
        "Overview",
        "Movie Explorer",
        "Popularity Rankings",
        "Rating Intelligence",
        "Genre Insights",
        "Release Trends",
        "Full Catalogue",
    ],
    label_visibility="collapsed",
)

st.sidebar.markdown("---")
st.sidebar.markdown('<div class="side-label">DATA FILTERS</div>', unsafe_allow_html=True)

search_text = st.sidebar.text_input(
    "Find a movie",
    placeholder="Search title…",
)

all_genres = sorted({
    genre for genres in catalog["genre_list"] for genre in genres
})
selected_genres = st.sidebar.multiselect(
    "Genres",
    options=all_genres,
    default=[],
    placeholder="All genres",
)

years = catalog["release_year"].dropna()
if not years.empty:
    year_min, year_max = int(years.min()), int(years.max())
    if year_min < year_max:
        selected_years = st.sidebar.slider(
            "Release period",
            min_value=year_min,
            max_value=year_max,
            value=(year_min, year_max),
        )
    else:
        selected_years = (year_min, year_max)
else:
    selected_years = None

minimum_ratings = st.sidebar.number_input(
    "Minimum rating count",
    min_value=0,
    value=0,
    step=10,
)

sort_option = st.sidebar.selectbox(
    "Sort catalogue by",
    [
        "Weighted Popularity",
        "Average Rating",
        "Most Rated",
        "Movie Title",
    ],
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    <div class="side-note">
        <b>DATASET STATUS</b><br>
        Movie and rating records are loaded from your local CSV files.
        Dashboard figures are calculated from the loaded dataset.
    </div>
    """,
    unsafe_allow_html=True,
)

if st.sidebar.button("↻ Refresh dataset", use_container_width=True):
    st.cache_data.clear()
    st.rerun()


# ------------------------------------------------------------
# 6. FILTERED CATALOGUE
# ------------------------------------------------------------

filtered = catalog.copy()

if search_text.strip():
    filtered = filtered[
        filtered["title"].str.contains(
            search_text.strip(), case=False, na=False, regex=False
        )
    ]

if selected_genres:
    filtered = filtered[
        filtered["genre_list"].apply(
            lambda genres: any(genre in genres for genre in selected_genres)
        )
    ]

if selected_years is not None:
    filtered = filtered[
        filtered["release_year"].between(
            selected_years[0], selected_years[1], inclusive="both"
        ) | filtered["release_year"].isna()
    ]

filtered = filtered[filtered["rating_count"] >= minimum_ratings]

if sort_option == "Weighted Popularity":
    filtered = filtered.sort_values(
        ["weighted_rating", "rating_count"], ascending=[False, False]
    )
elif sort_option == "Average Rating":
    filtered = filtered.sort_values(
        ["average_rating", "rating_count"], ascending=[False, False]
    )
elif sort_option == "Most Rated":
    filtered = filtered.sort_values("rating_count", ascending=False)
else:
    filtered = filtered.sort_values("title")


# ------------------------------------------------------------
# 7. REUSABLE UI HELPERS
# ------------------------------------------------------------

def section(title, description="", tag=""):
    tag_html = f'<span class="section-tag">{html.escape(tag)}</span>' if tag else ""
    st.markdown(
        f"""
        <div class="section-head">
            <div>
                <h2>{html.escape(title)}</h2>
                <p>{html.escape(description)}</p>
            </div>
            {tag_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def empty_state(message):
    st.markdown(
        f'<div class="empty-state">{html.escape(message)}</div>',
        unsafe_allow_html=True,
    )


def metric_row():
    a, b, c, d = st.columns(4)
    a.metric("MOVIES IN CATALOGUE", f"{len(catalog):,}")
    b.metric("VIEWER RATINGS", f"{len(ratings):,}")
    c.metric("DATASET AVERAGE", f"{global_mean:.2f} / 5")
    d.metric("MATCHING MOVIES", f"{len(filtered):,}")


def chart_empty(df, message):
    if df.empty:
        empty_state(message)
        return True
    return False


# ------------------------------------------------------------
# 8. TOP APPLICATION BAR + HERO
# ------------------------------------------------------------

top_left, top_right = st.columns([3, 1])
with top_left:
    st.markdown(
        '<div style="font-size:10px;font-weight:800;letter-spacing:1.7px;color:#4F6A5E;">'
        'CINESCOPE / MOVIE DATA INTELLIGENCE</div>',
        unsafe_allow_html=True,
    )
with top_right:
    st.markdown(
        '<div style="text-align:right;"><span class="status-pill">● DATA WORKSPACE ACTIVE</span></div>',
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div class="hero">
        <span class="eyebrow">MOVIE DATA INTELLIGENCE PLATFORM</span>
        <h1>Analysis of Movie Ratings and Viewer Preferences <br>for Understanding Popularity Patterns <br>and Entertainment Trends</h1>
        <p>
            Explore audience behaviour, uncover genre patterns, compare movie popularity
            and understand how entertainment trends evolve over time.
        </p>
        <div class="hero-meta">
            <span class="meta-chip">✳ Audience insights</span>
            <span class="meta-chip">▥ Rating analytics</span>
            <span class="meta-chip">⌁ Popularity modelling</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ------------------------------------------------------------
# 9. OVERVIEW PAGE
# ------------------------------------------------------------

if page == "Overview":
    section(
        "Operational snapshot",
        "A quick read of the movie catalogue and viewer activity.",
        "LIVE FROM DATASET",
    )
    metric_row()

    section(
        "Explore the workspace",
        "Jump into a focused view of the movie dataset.",
        "QUICK ACCESS",
    )

    quick_cols = st.columns(3)
    quick_items = [
        ("⌕", "Movie explorer", "Search a title and inspect its rating profile."),
        ("↗", "Popularity rankings", "Compare movies using weighted popularity."),
        ("◷", "Release trends", "Explore how movie releases change over time."),
    ]
    for col, item in zip(quick_cols, quick_items):
        with col:
            st.markdown(
                f"""
                <div class="quick-card">
                    <div class="quick-icon">{item[0]}</div>
                    <div class="quick-title">{item[1]}</div>
                    <div class="quick-copy">{item[2]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    left, right = st.columns([1.25, 1])
    with left:
        section("Most popular titles", "Top titles based on weighted popularity.")
        top = filtered.head(10).sort_values("weighted_rating", ascending=True)
        if not chart_empty(top, "No movies match the selected filters."):
            fig = px.bar(
                top,
                x="weighted_rating",
                y="title",
                orientation="h",
                color_discrete_sequence=[ACCENT],
                hover_data={"average_rating": ":.2f", "rating_count": ":,"},
                labels={
                    "weighted_rating": "Weighted score",
                    "title": "Movie",
                    "average_rating": "Average rating",
                    "rating_count": "Ratings",
                },
            )
            fig.update_layout(yaxis_title="", xaxis_range=[0, 5])
            style_chart(fig, height=390, show_legend=False)
            st.plotly_chart(fig, use_container_width=True)

    with right:
        section("Rating distribution", "How viewers use the 0.5–5 rating scale.")
        if not chart_empty(global_distribution, "No rating data available."):
            fig = px.bar(
                global_distribution,
                x="rating",
                y="count",
                color_discrete_sequence=[ORANGE],
                labels={"rating": "Viewer rating", "count": "Number of ratings"},
            )
            fig.update_traces(marker_line_width=0)
            fig.update_layout(xaxis=dict(tickmode="linear", dtick=0.5))
            style_chart(fig, height=390, show_legend=False)
            st.plotly_chart(fig, use_container_width=True)

    section("Genre pulse", "Genres with the largest number of titles in the current selection.")
    genre_rows = []
    for _, row in filtered.iterrows():
        for genre in row["genre_list"]:
            genre_rows.append({"Genre": genre, "Movie": row["movieId"]})
    if genre_rows:
        genre_count = (
            pd.DataFrame(genre_rows).groupby("Genre")["Movie"]
            .nunique().sort_values(ascending=False).head(8).reset_index(name="Movies")
        )
        fig = px.bar(
            genre_count.sort_values("Movies"),
            x="Movies",
            y="Genre",
            orientation="h",
            color_discrete_sequence=[ACCENT],
            labels={"Movies": "Number of movies"},
        )
        fig.update_layout(yaxis_title="")
        style_chart(fig, height=330, show_legend=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        empty_state("No genre information available for the current selection.")


# ------------------------------------------------------------
# 10. MOVIE EXPLORER
# ------------------------------------------------------------

elif page == "Movie Explorer":
    section(
        "Movie explorer",
        "Find a title and inspect the audience response behind it.",
        "TITLE LOOKUP",
    )

    search_base = catalog.copy()
    if search_text.strip():
        search_base = search_base[
            search_base["title"].str.contains(
                search_text.strip(), case=False, na=False, regex=False
            )
        ]

    if search_base.empty:
        empty_state("No matching titles. Try another movie name or clear the search.")
    else:
        options = search_base.sort_values("title")["title"].tolist()
        selected_title = st.selectbox(
            "Select a movie",
            options=options,
            index=0,
        )
        movie = search_base[search_base["title"] == selected_title].iloc[0]
        movie_id = int(movie["movieId"])

        st.markdown(
            f"""
            <div class="panel">
                <span class="status-pill">MOVIE PROFILE</span>
                <div style="font-family:Manrope,sans-serif;font-size:25px;font-weight:800;
                            letter-spacing:-1px;margin:12px 0 5px;color:#10231C;">
                    {html.escape(str(movie["title"]))}
                </div>
                <div style="color:#4F6A5E;font-size:12px;">
                    {html.escape(str(movie["genres"]).replace("|", "  ·  "))}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("AVERAGE RATING", f'{movie["average_rating"]:.2f} / 5')
        m2.metric("TOTAL RATINGS", f'{int(movie["rating_count"]):,}')
        m3.metric("WEIGHTED SCORE", f'{movie["weighted_rating"]:.2f} / 5')
        year_label = str(int(movie["release_year"])) if pd.notna(movie["release_year"]) else "Unknown"
        m4.metric("RELEASE YEAR", year_label)

        left, right = st.columns([1.1, 1])
        with left:
            section("Audience rating breakdown", "Count of ratings received at each score.")
            dist = rating_distribution[rating_distribution["movieId"] == movie_id].copy()
            if dist.empty:
                empty_state("This title has no viewer ratings in the dataset.")
            else:
                fig = px.bar(
                    dist.sort_values("rating"),
                    x="rating",
                    y="count",
                    text="count",
                    color_discrete_sequence=[ACCENT],
                    labels={"rating": "Rating score", "count": "Number of viewers"},
                )
                fig.update_traces(textposition="outside")
                fig.update_layout(xaxis=dict(tickmode="linear", dtick=0.5))
                style_chart(fig, height=360, show_legend=False)
                st.plotly_chart(fig, use_container_width=True)

        with right:
            section("What the score means", "A quick explanation of the ranking fields.")
            st.markdown(
                f"""
                <div class="panel">
                    <div class="panel-title">Average rating</div>
                    <div class="panel-subtitle">The arithmetic mean of all ratings for this movie.</div>
                    <div style="font-size:25px;font-weight:800;color:#0F4A38;">{movie["average_rating"]:.2f}<span style="font-size:12px;color:#5A7568;"> / 5</span></div>
                </div>
                <div class="panel">
                    <div class="panel-title">Weighted popularity</div>
                    <div class="panel-subtitle">Balances the movie's average with the overall dataset mean.</div>
                    <div style="font-size:25px;font-weight:800;color:#E0862B;">{movie["weighted_rating"]:.2f}<span style="font-size:12px;color:#5A7568;"> / 5</span></div>
                </div>
                <div class="panel">
                    <div class="panel-title">Rating consistency</div>
                    <div class="panel-subtitle">Standard deviation of the movie's ratings.</div>
                    <div style="font-size:20px;font-weight:800;color:#10231C;">{(movie["rating_std"] if pd.notna(movie["rating_std"]) else 0):.2f}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ------------------------------------------------------------
# 11. POPULARITY RANKINGS
# ------------------------------------------------------------

elif page == "Popularity Rankings":
    section(
        "Popularity rankings",
        "Compare audience scores while accounting for the number of ratings.",
        "RANKING ENGINE",
    )
    ranking = filtered[filtered["rating_count"] > 0].copy()
    if ranking.empty:
        empty_state("No rated movies match the selected filters.")
    else:
        ranking["Rank"] = range(1, len(ranking) + 1)
        left, right = st.columns([1.2, 1])
        with left:
            chart_data = ranking.head(20).sort_values("weighted_rating")
            fig = px.bar(
                chart_data,
                x="weighted_rating",
                y="title",
                orientation="h",
                color="average_rating",
                color_continuous_scale=["#FBE0BF", "#E0862B", "#176B50"],
                hover_data={"rating_count": ":,", "average_rating": ":.2f"},
                labels={
                    "weighted_rating": "Weighted popularity",
                    "title": "Movie",
                    "average_rating": "Average rating",
                    "rating_count": "Rating count",
                },
            )
            fig.update_layout(yaxis_title="", coloraxis_colorbar_title="Avg. rating")
            style_chart(fig, height=650, show_legend=False)
            st.plotly_chart(fig, use_container_width=True)
        with right:
            section("Top 10 titles", "Highest weighted popularity scores.")
            top10 = ranking.head(10)
            for _, row in top10.iterrows():
                st.markdown(
                    f"""
                    <div class="panel" style="padding:11px 14px;">
                        <div style="display:flex;justify-content:space-between;gap:12px;">
                            <div style="font-size:12px;font-weight:700;color:#10231C;">
                                {html.escape(str(row["title"]))}
                            </div>
                            <div style="font-size:12px;font-weight:800;color:#0F4A38;white-space:nowrap;">
                                {row["weighted_rating"]:.2f}
                            </div>
                        </div>
                        <div style="font-size:10px;color:#5A7568;margin-top:5px;">
                            {int(row["rating_count"]):,} ratings · Average {row["average_rating"]:.2f}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        section("Ranking table", "Use the filtered catalogue to compare individual titles.")
        table = ranking[
            ["Rank", "title", "genres", "release_year", "average_rating",
             "rating_count", "weighted_rating"]
        ].copy()
        table.columns = [
            "Rank", "Movie title", "Genres", "Release year",
            "Average rating", "Rating count", "Weighted popularity",
        ]
        st.dataframe(
            table,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Average rating": st.column_config.NumberColumn(format="%.2f"),
                "Weighted popularity": st.column_config.NumberColumn(format="%.2f"),
                "Rating count": st.column_config.NumberColumn(format="%d"),
                "Release year": st.column_config.NumberColumn(format="%d"),
            },
        )


# ------------------------------------------------------------
# 12. RATING INTELLIGENCE
# ------------------------------------------------------------

elif page == "Rating Intelligence":
    section(
        "Rating intelligence",
        "Understand how viewers score movies and how rating volume relates to score.",
        "AUDIENCE SIGNALS",
    )
    left, right = st.columns(2)
    with left:
        section("Overall rating distribution", "Frequency of each rating value.")
        fig = px.bar(
            global_distribution,
            x="rating",
            y="count",
            color_discrete_sequence=[ORANGE],
            labels={"rating": "Rating", "count": "Number of ratings"},
        )
        fig.update_layout(xaxis=dict(tickmode="linear", dtick=0.5))
        style_chart(fig, height=370, show_legend=False)
        st.plotly_chart(fig, use_container_width=True)

    with right:
        section("Rating volume by movie", "Movies with more ratings appear further to the right.")
        rated = filtered[filtered["rating_count"] > 0].copy()
        if rated.empty:
            empty_state("No rated movies match your filters.")
        else:
            scatter = rated
            if len(scatter) > 5000:
                scatter = scatter.sample(5000, random_state=42)
            fig = px.scatter(
                scatter,
                x="rating_count",
                y="average_rating",
                color="weighted_rating",
                hover_name="title",
                hover_data=["genres", "release_year"],
                color_continuous_scale=["#FBE0BF", "#E0862B", "#176B50"],
                labels={
                    "rating_count": "Number of ratings",
                    "average_rating": "Average rating",
                    "weighted_rating": "Weighted popularity",
                },
            )
            style_chart(fig, height=370, show_legend=False)
            st.plotly_chart(fig, use_container_width=True)
            if len(rated) > len(scatter):
                st.caption("Scatter plot uses a 5,000-movie sample for responsiveness.")

    section("Rating summary", "Summary statistics for the full ratings dataset.")
    summary = ratings["rating"].describe().to_frame("Rating value").round(3)
    st.dataframe(summary, use_container_width=True)


# ------------------------------------------------------------
# 13. GENRE INSIGHTS
# ------------------------------------------------------------

elif page == "Genre Insights":
    section(
        "Genre intelligence",
        "Explore the size and average audience response of each movie genre.",
        "CONTENT PATTERNS",
    )
    records = []
    for _, row in filtered.iterrows():
        for genre in row["genre_list"]:
            records.append({
                "Genre": genre,
                "movieId": row["movieId"],
                "Average rating": row["average_rating"],
                "Rating count": row["rating_count"],
            })

    if not records:
        empty_state("No genre information is available for the current filters.")
    else:
        genre_data = pd.DataFrame(records)
        summary = (
            genre_data.groupby("Genre")
            .agg(
                Movies=("movieId", "nunique"),
                **{
                    "Average rating": ("Average rating", "mean"),
                    "Total ratings": ("Rating count", "sum"),
                },
            )
            .reset_index()
            .sort_values("Movies", ascending=False)
        )

        a, b = st.columns(2)
        with a:
            section("Catalogue by genre", "Number of distinct titles in each genre.")
            fig = px.bar(
                summary.sort_values("Movies"),
                x="Movies",
                y="Genre",
                orientation="h",
                color_discrete_sequence=[ACCENT],
            )
            fig.update_layout(yaxis_title="")
            style_chart(fig, height=430, show_legend=False)
            st.plotly_chart(fig, use_container_width=True)

        with b:
            section("Average rating by genre", "Unweighted average of movie-level ratings.")
            fig = px.bar(
                summary.sort_values("Average rating"),
                x="Average rating",
                y="Genre",
                orientation="h",
                color_discrete_sequence=[ORANGE],
            )
            fig.update_layout(yaxis_title="", xaxis_range=[0, 5])
            style_chart(fig, height=430, show_legend=False)
            st.plotly_chart(fig, use_container_width=True)

        section("Genre register", "Detailed summary for the selected catalogue.")
        st.dataframe(
            summary,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Average rating": st.column_config.NumberColumn(format="%.2f"),
                "Total ratings": st.column_config.NumberColumn(format="%d"),
            },
        )
        st.caption(
            "Movies can belong to multiple genres. Genre totals therefore overlap "
            "and may exceed the number of unique movies."
        )


# ------------------------------------------------------------
# 14. RELEASE TRENDS
# ------------------------------------------------------------

elif page == "Release Trends":
    section(
        "Release trends",
        "Track catalogue growth and movie-level audience scores across release years.",
        "TIME SERIES",
    )
    yearly = filtered.dropna(subset=["release_year"]).copy()
    if yearly.empty:
        empty_state("No release-year information is available for the current filters.")
    else:
        yearly["release_year"] = yearly["release_year"].astype(int)
        yearly_summary = (
            yearly.groupby("release_year")
            .agg(
                Movies=("movieId", "nunique"),
                **{
                    "Mean movie rating": ("average_rating", "mean"),
                    "Total ratings": ("rating_count", "sum"),
                },
            )
            .reset_index()
            .sort_values("release_year")
        )

        a, b = st.columns(2)
        with a:
            section("Movie releases", "Number of titles in the dataset by release year.")
            fig = px.line(
                yearly_summary,
                x="release_year",
                y="Movies",
                markers=True,
                color_discrete_sequence=[ACCENT],
                labels={"release_year": "Release year"},
            )
            fig.update_layout(xaxis_title="Release year")
            style_chart(fig, height=370, show_legend=False)
            st.plotly_chart(fig, use_container_width=True)

        with b:
            section("Average movie rating", "Unweighted mean of movie-level average ratings.")
            fig = px.line(
                yearly_summary,
                x="release_year",
                y="Mean movie rating",
                markers=True,
                color_discrete_sequence=[ORANGE],
                labels={"release_year": "Release year"},
            )
            fig.update_layout(xaxis_title="Release year", yaxis_range=[0, 5])
            style_chart(fig, height=370, show_legend=False)
            st.plotly_chart(fig, use_container_width=True)

        section("Yearly register", "Annual catalogue and rating summary.")
        st.dataframe(
            yearly_summary,
            use_container_width=True,
            hide_index=True,
            column_config={
                "release_year": st.column_config.NumberColumn("Release year", format="%d"),
                "Mean movie rating": st.column_config.NumberColumn(format="%.2f"),
                "Total ratings": st.column_config.NumberColumn(format="%d"),
            },
        )


# ------------------------------------------------------------
# 15. FULL CATALOGUE
# ------------------------------------------------------------

elif page == "Full Catalogue":
    section(
        "Full movie catalogue",
        "Search, sort, inspect and export the filtered movie records.",
        "DATA REGISTER",
    )
    st.markdown(
        f'<span class="status-pill">{len(filtered):,} MATCHING RECORDS</span>',
        unsafe_allow_html=True,
    )
    display = filtered[
        [
            "title", "genres", "release_year", "average_rating",
            "rating_count", "weighted_rating", "rating_std",
        ]
    ].copy()
    display.columns = [
        "Movie title", "Genres", "Release year", "Average rating",
        "Rating count", "Weighted popularity", "Rating deviation",
    ]
    st.dataframe(
        display,
        use_container_width=True,
        hide_index=True,
        height=560,
        column_config={
            "Release year": st.column_config.NumberColumn(format="%d"),
            "Average rating": st.column_config.NumberColumn(format="%.2f"),
            "Rating count": st.column_config.NumberColumn(format="%d"),
            "Weighted popularity": st.column_config.NumberColumn(format="%.2f"),
            "Rating deviation": st.column_config.NumberColumn(format="%.2f"),
        },
    )

    csv = display.to_csv(index=False).encode("utf-8")
    st.download_button(
        "↓ Export filtered catalogue (CSV)",
        data=csv,
        file_name="cinescope_filtered_catalogue.csv",
        mime="text/csv",
    )


# ------------------------------------------------------------
# 16. FOOTER / PROJECT NOTE
# ------------------------------------------------------------

st.markdown(
    """
    <div class="footer">
        <strong>CineScope · Movie Ratings & Viewer Intelligence</strong><br>
        Built with Python, Pandas, Streamlit and Plotly.<br>
        An academic data analysis project exploring audience ratings,
        popularity patterns, genres and entertainment trends.
    </div>
    """,
    unsafe_allow_html=True,
)
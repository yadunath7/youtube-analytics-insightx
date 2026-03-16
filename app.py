"""
app.py
------
YouTube Trending Videos 2025 — Interactive Analytics Dashboard
Built with Streamlit + Plotly
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

from data_loader import load_data, CATEGORIES

# ──────────────────────────────────────────────────────────────────────────────
# Page config  (must be first Streamlit call)
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="YouTube Trending 2025 · Analytics",
    page_icon="▶️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────────────────
# Custom CSS — dark premium theme
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
/* Global */
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700;900&display=swap');
html, body, [class*="css"] { font-family: 'Roboto', sans-serif; }

/* Premium Animations */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes pulseGlow {
    0% { box-shadow: 0 0 10px rgba(255, 0, 0, 0.2); }
    50% { box-shadow: 0 0 20px rgba(255, 0, 0, 0.6); }
    100% { box-shadow: 0 0 10px rgba(255, 0, 0, 0.2); }
}
.stApp {
    animation: fadeUp 0.8s ease-out forwards;
}

/* Premium Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1A1A1A 0%, #0F0F0F 100%);
    border-right: 1px solid rgba(255, 255, 255, 0.05);
}
[data-testid="stSidebar"] .stMarkdown h2 {
    color: #FFFFFF;
    font-size: 1.25rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 0px;
}
[data-testid="stSidebar"] .stMultiSelect label, [data-testid="stSidebar"] .stDateInput label, [data-testid="stSidebar"] .stSlider label {
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    color: #AAAAAA !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding-bottom: 5px;
}
[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background-color: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 8px;
    transition: all 0.3s ease;
}
[data-testid="stSidebar"] div[data-baseweb="select"] > div:hover {
    border-color: rgba(255,0,0,0.5);
    background-color: rgba(255,255,255,0.05);
}
[data-testid="stSidebar"] hr {
    margin: 1.5rem 0 !important;
    border-color: rgba(255,255,255,0.05) !important;
}

/* Premium KPI cards (Glassmorphism & Neon Hover) */
.kpi-wrapper {
    animation: fadeUp 0.6s ease-out both;
}
.kpi-wrapper:nth-child(1) { animation-delay: 0.1s; }
.kpi-wrapper:nth-child(2) { animation-delay: 0.2s; }
.kpi-wrapper:nth-child(3) { animation-delay: 0.3s; }
.kpi-wrapper:nth-child(4) { animation-delay: 0.4s; }
.kpi-wrapper:nth-child(5) { animation-delay: 0.5s; }

.kpi-card {
    background: linear-gradient(145deg, rgba(33,33,33,0.9), rgba(20,20,20,0.9));
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 24px 20px;
    text-align: center;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    height: 140px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, #FF0000, #FF4D4D);
    opacity: 0;
    transition: opacity 0.3s ease;
}
.kpi-card:hover {
    transform: translateY(-5px) scale(1.02);
    box-shadow: 0 15px 30px rgba(0, 0, 0, 0.6), 0 0 15px rgba(255, 0, 0, 0.3);
    border-color: rgba(255, 0, 0, 0.3);
}
.kpi-card:hover::before {
    opacity: 1;
}
.kpi-icon {
    font-size: 1.5rem;
    color: #FF4D4D;
    margin-bottom: 8px;
}
.kpi-value {
    font-size: 2rem;
    font-weight: 700;
    color: #F1F1F1;
    line-height: 1.1;
}
.kpi-label {
    font-size: 0.78rem;
    font-weight: 500;
    color: #AAAAAA;
    margin-top: 6px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.kpi-delta {
    font-size: 0.75rem;
    color: #AAAAAA;
    margin-top: 4px;
}

/* Section headers */
.section-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #FFFFFF;
    margin: 35px 0 15px 0;
    padding-left: 12px;
    border-left: 4px solid #FF0000;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    display: flex;
    align-items: center;
    gap: 10px;
}

/* Custom Logo Header */
.logo-container {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
    animation: fadeUp 0.8s ease-out;
}
.logo-icon {
    background: #FF0000;
    color: white;
    width: 48px;
    height: 34px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    margin-right: 15px;
    box-shadow: 0 4px 10px rgba(255, 0, 0, 0.4);
}
.logo-text {
    font-size: 2.5rem;
    font-weight: 900;
    letter-spacing: -0.02em;
    color: #FFFFFF;
    margin: 0;
    line-height: 1;
}
.logo-subtext {
    font-weight: 300;
    color: #AAAAAA;
    margin-left: 10px;
    font-size: 1.8rem;
}

/* Data source badge */
.badge-live   { background: linear-gradient(90deg, #CC0000, #FF0000); color:#FFFFFF; padding:4px 12px; border-radius:4px; font-size:0.75rem; font-weight:700; letter-spacing:0.05em; animation: pulseGlow 2s infinite; }
.badge-synth  { background: linear-gradient(90deg, #FF8C00, #FFA500); color:#FFFFFF; padding:4px 12px; border-radius:4px; font-size:0.75rem; font-weight:700; }
.badge-cache  { background:#212121; color:#AAAAAA; border:1px solid #3D3D3D; padding:4px 12px; border-radius:4px; font-size:0.75rem; font-weight:600; }

/* Divider */
hr { border-color: rgba(255,255,255,0.05) !important; margin: 2rem 0 !important; }

/* Streamlit table */
.dataframe th { background: #212121 !important; color: #FFFFFF !important; font-weight: 600 !important; }
.dataframe td { background: #141414 !important; border-bottom: 1px solid #2A2A2A !important; }
.dataframe { border-radius: 8px; overflow: hidden; border: 1px solid #333 !important; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# Plotly theme helper
# ──────────────────────────────────────────────────────────────────────────────
PLOT_BG    = "rgba(0,0,0,0)"
PAPER_BG   = "rgba(0,0,0,0)"
GRID_COLOR = "#3d3d3d"
FONT_COLOR = "#F1F1F1"

def apply_theme(fig: go.Figure, height: int = 400) -> go.Figure:
    fig.update_layout(
        plot_bgcolor=PLOT_BG,
        paper_bgcolor=PAPER_BG,
        font=dict(color=FONT_COLOR, family="Roboto"),
        height=height,
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(
            bgcolor="rgba(33,33,33,0.8)",
            bordercolor="#3d3d3d",
            borderwidth=1,
        ),
    )
    fig.update_xaxes(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR)
    fig.update_yaxes(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR)
    return fig

RED_SEQ  = px.colors.sequential.Reds
YT_PALETTE = ["#FF0000", "#CC0000", "#990000", "#FF4D4D", "#FF9999", "#FFFFFF", "#AAAAAA"]

# ──────────────────────────────────────────────────────────────────────────────
# Load data (cached for performance)
# ──────────────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def get_data():
    return load_data()

with st.spinner("🔄 Loading YouTube Trending data…"):
    df_raw, source, is_live = get_data()

# ──────────────────────────────────────────────────────────────────────────────
# Sidebar
# ──────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## <i class='fa-solid fa-sliders' style='color:#FF0000;'></i> Controls", unsafe_allow_html=True)
    st.markdown("---")

    # Data source badge
    if source == "kaggle":
        st.markdown('<span class="badge-live"><i class="fa-solid fa-satellite-dish"></i> LIVE (Kaggle)</span>', unsafe_allow_html=True)
    elif source == "cache":
        st.markdown('<span class="badge-cache"><i class="fa-solid fa-database"></i> CACHED</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="badge-synth"><i class="fa-solid fa-flask"></i> SYNTHETIC</span>', unsafe_allow_html=True)

    st.caption(f"Last updated: {datetime.now().strftime('%d %b %Y, %H:%M')}")

    st.markdown("---")

    # Region filter (Continents now)
    all_regions = sorted(df_raw["region"].dropna().unique().tolist())
    sel_regions = st.multiselect(
        "🌍 Global Region",
        options=all_regions,
        default=all_regions,
    )
    
    # Country filter
    all_countries = sorted(df_raw["country_code"].dropna().unique().tolist())
    sel_countries = st.multiselect(
        "🏳️ Country Code",
        options=all_countries,
        default=all_countries,
    )

    # Category filter
    all_cats = sorted(df_raw["category_name"].dropna().unique().tolist())
    sel_cats = st.multiselect(
        "🏷️ Video Category",
        options=all_cats,
        default=all_cats,
    )

    # Date range
    min_date = df_raw["trending_date"].min()
    max_date = df_raw["trending_date"].max()
    if pd.notna(min_date) and pd.notna(max_date):
        date_range = st.date_input(
            "📅 Trending Date Range",
            value=(min_date.date(), max_date.date()),
            min_value=min_date.date(),
            max_value=max_date.date(),
        )
    else:
        date_range = None

    # Top N for charts
    top_n = st.slider("🏆 Top Chart Size", min_value=5, max_value=30, value=10)

    st.markdown("---")
    st.markdown("**Dataset:** YouTube Trending 2025")
    if not is_live:
        st.info("💡 Add `~/.kaggle/kaggle.json` for live data from Kaggle.", icon="🔑")

# ──────────────────────────────────────────────────────────────────────────────
# Apply filters
# ──────────────────────────────────────────────────────────────────────────────
df = df_raw.copy()
if sel_regions:
    df = df[df["region"].isin(sel_regions)]
if sel_countries:
    df = df[df["country_code"].isin(sel_countries)]
if sel_cats:
    df = df[df["category_name"].isin(sel_cats)]
if date_range and len(date_range) == 2:
    df = df[
        (df["trending_date"] >= pd.Timestamp(date_range[0])) &
        (df["trending_date"] <= pd.Timestamp(date_range[1]))
    ]

# ──────────────────────────────────────────────────────────────────────────────
# Header (Custom Logo)
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="logo-container">
    <div class="logo-icon"><i class="fa-solid fa-play"></i></div>
    <h1 class="logo-text">YouTube <span class="logo-subtext">Analytics 2025</span></h1>
</div>
<p style="color: #AAAAAA; font-size: 1.1rem; margin-top: 0;">Real-time intelligence on trending videos — updated daily via Kaggle.</p>
""", unsafe_allow_html=True)
st.markdown("---")

# ──────────────────────────────────────────────────────────────────────────────
# KPI cards
# ──────────────────────────────────────────────────────────────────────────────
def fmt(n: float, unit: str = "") -> str:
    if n >= 1_000_000_000:
        return f"{n/1_000_000_000:.1f}B{unit}"
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M{unit}"
    if n >= 1_000:
        return f"{n/1_000:.1f}K{unit}"
    return f"{n:.0f}{unit}"

total_videos   = len(df)
avg_views      = df["views"].mean() if total_videos else 0
avg_likes      = df["likes"].mean() if total_videos else 0
avg_engagement = df["engagement_rate"].mean() * 100 if total_videos else 0
total_views    = df["views"].sum()

c1, c2, c3, c4, c5 = st.columns(5)
for col, val, label, delta, icon in [
    (c1, f"{total_videos:,}",          "Trending Videos", "in selected filters", "fa-fire"),
    (c2, fmt(total_views),             "Total Views",     "across all videos", "fa-eye"),
    (c3, fmt(avg_views),               "Avg Views/Vid",   "per trending entry", "fa-chart-line"),
    (c4, fmt(avg_likes),               "Avg Likes/Vid",   "engagement signal", "fa-thumbs-up"),
    (c5, f"{avg_engagement:.2f}%",     "Engagement Rate", "(likes+comments)/views", "fa-heart"),
]:
    col.markdown(
        f'<div class="kpi-wrapper">'
        f'<div class="kpi-card">'
        f'<i class="fa-solid {icon} kpi-icon"></i>'
        f'<div class="kpi-value">{val}</div>'
        f'<div class="kpi-label">{label}</div>'
        f'<div class="kpi-delta">{delta}</div>'
        f'</div></div>',
        unsafe_allow_html=True,
    )

st.markdown("")

# ──────────────────────────────────────────────────────────────────────────────
# Row 1 — Top Videos  |  Category Breakdown
# ──────────────────────────────────────────────────────────────────────────────
col_a, col_b = st.columns([3, 2])

with col_a:
    st.markdown('<div class="section-title">🏆 Top Videos by Views</div>', unsafe_allow_html=True)
    top_df = (
        df.groupby(["title", "channel_title"], as_index=False)
          .agg(views=("views", "max"), likes=("likes", "max"))
          .sort_values("views", ascending=False)
          .head(top_n)
    )
    top_df["label"] = top_df["title"].str[:45] + "…"

    fig_top = px.bar(
        top_df, x="views", y="label",
        orientation="h",
        color="views",
        color_continuous_scale=RED_SEQ,
        labels={"views": "Views", "label": ""},
        hover_data={"channel_title": True, "likes": True, "label": False},
    )
    fig_top.update_coloraxes(showscale=False)
    fig_top.update_yaxes(categoryorder="total ascending")
    st.plotly_chart(apply_theme(fig_top, 440), use_container_width=True)

with col_b:
    st.markdown('<div class="section-title">🏷️ Category Distribution</div>', unsafe_allow_html=True)
    cat_df = df.groupby("category_name", as_index=False)["views"].sum().sort_values("views", ascending=False)
    fig_pie = px.pie(
        cat_df, values="views", names="category_name",
        hole=0.55,
        color_discrete_sequence=YT_PALETTE,
    )
    fig_pie.update_traces(textposition="inside", textinfo="percent+label")
    fig_pie.update_layout(showlegend=False)
    st.plotly_chart(apply_theme(fig_pie, 440), use_container_width=True)

# ──────────────────────────────────────────────────────────────────────────────
# Row 2 — Engagement Scatter  |  Daily Trending Volume
# ──────────────────────────────────────────────────────────────────────────────
col_c, col_d = st.columns(2)

with col_c:
    st.markdown('<div class="section-title">💬 Views vs Likes (Engagement)</div>', unsafe_allow_html=True)
    scatter_df = df.sample(min(2000, len(df)), random_state=0) if len(df) > 2000 else df
    fig_scatter = px.scatter(
        scatter_df, x="views", y="likes",
        color="category_name",
        size="comment_count",
        size_max=20,
        hover_name="title",
        log_x=True, log_y=True,
        color_discrete_sequence=YT_PALETTE,
        labels={"views": "Views (log)", "likes": "Likes (log)", "category_name": "Category"},
        opacity=0.75,
    )
    st.plotly_chart(apply_theme(fig_scatter, 420), use_container_width=True)

with col_d:
    st.markdown('<div class="section-title">📈 Daily Trending Volume</div>', unsafe_allow_html=True)
    _daily = df.dropna(subset=["trending_date"]).copy()
    _daily["date"] = _daily["trending_date"].dt.date
    daily_df = (
        _daily.groupby("date")
              .agg(count=("video_id", "count"))
              .reset_index()
    )
    fig_line = px.area(
        daily_df, x="date", y="count",
        labels={"date": "Date", "count": "Trending Videos"},
        color_discrete_sequence=["#FF0000"],
        line_shape="spline",
    )
    fig_line.update_traces(
        fill="tozeroy",
        fillcolor="rgba(255,0,0,0.2)",
        line=dict(color="#FF4D4D", width=2),
    )
    st.plotly_chart(apply_theme(fig_line, 420), use_container_width=True)

# ──────────────────────────────────────────────────────────────────────────────
# Row 3 — Region Heatmap  |  Top Channels
# ──────────────────────────────────────────────────────────────────────────────
col_e, col_f = st.columns(2)

with col_e:
    st.markdown('<div class="section-title">🌍 Views by Region</div>', unsafe_allow_html=True)
    region_df = (
        df.groupby("region", as_index=False)["views"]
          .sum()
          .sort_values("views", ascending=False)
    )
    fig_region = px.bar(
        region_df, x="region", y="views",
        color="views",
        color_continuous_scale=RED_SEQ,
        labels={"region": "Region", "views": "Total Views"},
    )
    fig_region.update_coloraxes(showscale=False)
    st.plotly_chart(apply_theme(fig_region, 380), use_container_width=True)

with col_f:
    st.markdown('<div class="section-title">📺 Top Channels by Trending Videos</div>', unsafe_allow_html=True)
    chan_df = (
        df.groupby("channel_title", as_index=False)
          .agg(count=("video_id", "count"), total_views=("views", "sum"))
          .sort_values("count", ascending=False)
          .head(top_n)
    )
    fig_chan = px.bar(
        chan_df, x="count", y="channel_title",
        orientation="h",
        color="total_views",
        color_continuous_scale=RED_SEQ,
        labels={"count": "Trending Count", "channel_title": ""},
    )
    fig_chan.update_coloraxes(showscale=False)
    fig_chan.update_yaxes(categoryorder="total ascending")
    st.plotly_chart(apply_theme(fig_chan, 380), use_container_width=True)

# ──────────────────────────────────────────────────────────────────────────────
# Row 4 — Engagement Rate by Category (box plot)
# ──────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">📊 Engagement Rate Distribution by Category</div>', unsafe_allow_html=True)
fig_box = px.box(
    df[df["engagement_rate"] < df["engagement_rate"].quantile(0.99)],
    x="category_name",
    y="engagement_rate",
    color="category_name",
    color_discrete_sequence=YT_PALETTE,
    labels={"engagement_rate": "Engagement Rate", "category_name": ""},
)
fig_box.update_layout(showlegend=False)
st.plotly_chart(apply_theme(fig_box, 380), use_container_width=True)

# ──────────────────────────────────────────────────────────────────────────────
# Raw Data Table
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown('<div class="section-title">📋 Raw Data Explorer</div>', unsafe_allow_html=True)

display_cols = [c for c in [
    "title", "channel_title", "category_name", "region",
    "trending_date", "views", "likes", "comment_count", "engagement_rate",
] if c in df.columns]

search_term = st.text_input("🔍 Search by title or channel", placeholder="e.g. MrBeast, TechGuru…")
table_df = df[display_cols].copy()
if search_term:
    mask = (
        table_df.get("title", pd.Series(dtype=str)).str.contains(search_term, case=False, na=False) |
        table_df.get("channel_title", pd.Series(dtype=str)).str.contains(search_term, case=False, na=False)
    )
    table_df = table_df[mask]

table_df["trending_date"] = table_df["trending_date"].dt.strftime("%Y-%m-%d")
st.dataframe(
    table_df.sort_values("views", ascending=False).reset_index(drop=True),
    use_container_width=True,
    height=400,
)

st.download_button(
    label="⬇️  Download filtered data as CSV",
    data=table_df.to_csv(index=False).encode("utf-8"),
    file_name="youtube_trending_filtered.csv",
    mime="text/csv",
)

# ──────────────────────────────────────────────────────────────────────────────
# Footer
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption(
    "Data source: [YouTube Trending Videos 2025](https://www.kaggle.com/datasets/sebastianbesinski/youtube-trending-videos-2025-updated-daily) · "
    "Built with Streamlit & Plotly · Refreshes daily"
)

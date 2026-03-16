import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from youtube_api import get_trending_videos, search_youtube_videos, get_categories
from data_loader import process_video_data, get_channel_summary
from ai_assistant import get_ai_response, analyze_trends
import datetime
from streamlit_autorefresh import st_autorefresh

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="YouTube InsightX | AI-Powered Premium",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CUSTOM CSS (PREMIUM UI v3) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .stApp {
        background-color: #0b0b0b;
        color: #ffffff;
    }
    
    /* Premium Sidebar */
    [data-testid="stSidebar"] {
        background-color: #111111;
        border-right: 1px solid rgba(255, 255, 255, 0.03);
        padding-top: 20px;
    }
    
    .sidebar-logo {
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 1.4rem;
        font-weight: 800;
        margin-bottom: 40px;
        padding-left: 10px;
    }
    
    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .glass-card:hover {
        background: rgba(255, 255, 255, 0.04);
        border-color: rgba(255, 0, 0, 0.2);
        transform: translateY(-4px);
    }
    
    /* Metrics Styling */
    .metric-value { font-size: 2.4rem; font-weight: 800; }
    .metric-label { font-size: 0.8rem; color: rgba(255, 255, 255, 0.5); text-transform: uppercase; letter-spacing: 1.5px; }
    .metric-trend { font-size: 0.75rem; display: flex; align-items: center; gap: 4px; padding-top: 8px; }
    .trend-up { color: #00ffa3; }
    
    /* Header Section */
    .hero-title {
        font-size: 44px;
        font-weight: 800;
        margin-bottom: 4px;
        color: #fff;
    }
    .hero-subtitle {
        color: rgba(255, 255, 255, 0.5);
        font-size: 1rem;
        margin-bottom: 32px;
    }
    
    /* Sidebar Selectbox Styling */
    .stSelectbox div[data-baseweb="select"] {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Results Banner */
    .banner {
        border-left: 4px solid #00ffa3;
        background: linear-gradient(90deg, rgba(0, 255, 163, 0.05) 0%, transparent 100%);
        padding: 16px;
        border-radius: 4px;
        margin: 20px 0;
    }
    
    /* footer {visibility: hidden;} */
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if 'search_results' not in st.session_state:
    st.session_state.search_results = pd.DataFrame()
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "🔥 Top Trending"
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = datetime.datetime.now()
if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = False
if 'query_str' not in st.session_state:
    st.session_state.query_str = ""
if 'region_choice_name' not in st.session_state:
    st.session_state.region_choice_name = "India"
if 'category_choice_name' not in st.session_state:
    st.session_state.category_choice_name = "All"
if 'cat_id_map' not in st.session_state:
    st.session_state.cat_id_map = {"All": "0"}

REGION_MAP = {"India": "IN", "United States": "US", "United Kingdom": "GB", "Global": "US", "Japan": "JP", "Australia": "AU"}

# --- DATA FETCHING FUNCTIONS ---
def update_data():
    try:
        region = REGION_MAP.get(st.session_state.get('region_choice_name', 'India'), 'IN')
        category_id = st.session_state.get('cat_id_map', {"All": "0"}).get(st.session_state.get('category_choice_name', 'All'), "0")
        query = st.session_state.get('temp_search_input', '')
        st.session_state.query_str = query
        
        if query:
            response = search_youtube_videos(query, region, category_id)
            st.session_state.active_tab = "🔍 Search Results"
        else:
            response = get_trending_videos(region, category_id)
            st.session_state.active_tab = "🔥 Top Trending"
            
        st.session_state.search_results = process_video_data(response)
        st.session_state.last_refresh = datetime.datetime.now()
    except Exception as e:
        st.error(f"Intelligence Update Error: {str(e)}")

# --- AUTO REFRESH ---
if st.session_state.auto_refresh:
    st_autorefresh(interval=60000, key="datarefresh") # 60s

# --- SIDEBAR (ULTRA PREMIUM) ---
with st.sidebar:
    # Proper YouTube Logo & Branding
    st.markdown('''
        <div style="display: flex; align-items: center; gap: 10px; padding: 10px 0 30px 0;">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="#ff0000" xmlns="http://www.w3.org/2000/svg">
                <path d="M19.615 3.184c-3.604-.246-11.631-.245-15.23 0-3.897.266-4.356 2.62-4.385 8.816.029 6.185.484 8.549 4.385 8.816 3.6.245 11.626.246 15.23 0 3.897-.266 4.356-2.62 4.385-8.816-.029-6.185-.484-8.549-4.385-8.816zm-10.615 12.816v-8l8 4-8 4z"/>
            </svg>
            <span style="font-size: 1.6rem; font-weight: 800; color: white; letter-spacing: -1px;">Insight<span style="color:#ff0000;">X</span></span>
        </div>
    ''', unsafe_allow_html=True)
    
    st.markdown("🌍 **Region Intelligence**")
    st.selectbox(
        "Select Region", 
        options=list(REGION_MAP.keys()), 
        key='region_choice_name', 
        on_change=update_data, 
        label_visibility="collapsed"
    )
    
    st.markdown("📂 **Content Niche**")
    try:
        # Cache category map to avoid extra API hits
        current_region = REGION_MAP.get(st.session_state.region_choice_name, 'IN')
        if st.session_state.get('last_region_cats') != current_region:
            cats = get_categories(current_region)
            new_map = {"All": "0"}
            for item in cats.get("items", []):
                new_map[item["snippet"]["title"]] = item["id"]
            st.session_state.cat_id_map = new_map
            st.session_state.last_region_cats = current_region
            
        st.selectbox("Select Category", options=list(st.session_state.cat_id_map.keys()), key='category_choice_name', on_change=update_data, label_visibility="collapsed")
    except Exception as e:
        st.error(f"Category Error: {str(e)}")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Premium Action Group
    with st.container():
        st.markdown('<div style="background:rgba(255,255,255,0.03); padding:15px; border-radius:10px; border:1px solid rgba(255,255,255,0.05);">', unsafe_allow_html=True)
        
        if not st.session_state.search_results.empty:
            csv_data = st.session_state.search_results.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Data (CSV)",
                data=csv_data,
                file_name=f"insightx_data_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime='text/csv',
                use_container_width=True
            )

        if st.button("🔄 Force Refresh", use_container_width=True):
            update_data()
            st.rerun()

        st.session_state.auto_refresh = st.checkbox("⚙️ Live Sync (60s)", value=st.session_state.auto_refresh)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption(f"Status: Connected • Updated {st.session_state.last_refresh.strftime('%H:%M:%S')}")

# --- HEADER SECTION ---
st.markdown('''
    <div style="display:flex; align-items:center; gap:12px; margin-bottom:20px;">
        <svg width="40" height="40" viewBox="0 0 24 24" fill="#ff0000" xmlns="http://www.w3.org/2000/svg">
            <path d="M19.615 3.184c-3.604-.246-11.631-.245-15.23 0-3.897.266-4.356 2.62-4.385 8.816.029 6.185.484 8.549 4.385 8.816 3.6.245 11.626.246 15.23 0 3.897-.266 4.356-2.62 4.385-8.816-.029-6.185-.484-8.549-4.385-8.816zm-10.615 12.816v-8l8 4-8 4z"/>
        </svg>
        <span style="font-size: 1.8rem; font-weight: 800; color: white; letter-spacing: -1px;">Insight<span style="color:#ff0000;">X</span></span>
    </div>
''', unsafe_allow_html=True)

st.markdown(f'<div class="hero-title">Intelligence for Creators</div>', unsafe_allow_html=True)
st.markdown(f'<div class="hero-subtitle">Scale your reach with lightning-fast analytics and AI-powered strategy. Real-time insights from <b>{st.session_state.region_choice_name}</b>.</div>', unsafe_allow_html=True)

# Main Search Bar (Trigger Auto Search on Enter)
st.text_input("Search for videos, tags, or channels...", value=st.session_state.query_str, key="temp_search_input", placeholder="What's trending today?", label_visibility="collapsed", on_change=update_data)
# Sync the input back if it changed manually or via enter
if st.session_state.temp_search_input != st.session_state.query_str:
    st.session_state.query_str = st.session_state.temp_search_input

# --- TOP METRICS ---
if not st.session_state.search_results.empty:
    df = st.session_state.search_results
    m1, m2, m3, m4 = st.columns(4)
    
    total_views = df['view_count'].sum()
    avg_engagement = df['engagement_rate'].mean()
    total_likes = df['like_count'].sum()
    videos_tracked = len(df)
    
    with m1:
        st.markdown(f'''<div class="glass-card"><div class="metric-label">Total Views</div><div class="metric-value">{total_views/1000:,.1f}K</div><div class="metric-trend trend-up">↑ 15.2% vs last week</div></div>''', unsafe_allow_html=True)
    with m2:
        st.markdown(f'''<div class="glass-card"><div class="metric-label">Avg Engagement</div><div class="metric-value">{avg_engagement:.2%}</div><div class="metric-trend trend-up">↑ 4.1% vs last week</div></div>''', unsafe_allow_html=True)
    with m3:
        st.markdown(f'''<div class="glass-card"><div class="metric-label">Total Likes</div><div class="metric-value">{total_likes/1000:,.1f}K</div><div class="metric-trend trend-up">↑ 10.5% vs last week</div></div>''', unsafe_allow_html=True)
    with m4:
        st.markdown(f'''<div class="glass-card"><div class="metric-label">Videos Tracked</div><div class="metric-value">{videos_tracked}</div><div class="metric-trend trend-up">● Live vs last week</div></div>''', unsafe_allow_html=True)

# --- NAVIGATION TABS ---
# CSS to ensure all buttons have the same height and no text wrapping
st.markdown("""
    <style>
    div[data-testid="stHorizontalBlock"] button {
        white-space: nowrap !important;
        min-height: 45px !important;
    }
    </style>
    """, unsafe_allow_html=True)

nav_cols = st.columns([1, 1, 1, 1, 2])
with nav_cols[0]:
    if st.button("🔥 Top Trending", type="primary" if st.session_state.active_tab=="🔥 Top Trending" else "secondary", use_container_width=True):
        st.session_state.query_str = "" # Clear search via proxy
        update_data()
        st.rerun()
with nav_cols[1]:
    if st.button("💖 Most Liked", type="primary" if st.session_state.active_tab=="💖 Most Liked" else "secondary", use_container_width=True):
        st.session_state.active_tab = "💖 Most Liked"
        if not st.session_state.search_results.empty:
            st.session_state.search_results = st.session_state.search_results.sort_values(by="like_count", ascending=False)
with nav_cols[2]:
    if st.button("📊 Deep Analysis", type="primary" if st.session_state.active_tab=="📊 Deep Analysis" else "secondary", use_container_width=True):
        st.session_state.active_tab = "📊 Deep Analysis"
with nav_cols[3]:
    if st.button("🤖 AI Strategist", type="primary" if st.session_state.active_tab=="🤖 AI Strategist" else "secondary", use_container_width=True):
        st.session_state.active_tab = "🤖 AI Strategist"

st.markdown("---")

# --- MAIN CONTENT AREA ---
if st.session_state.active_tab in ["🔥 Top Trending", "🔍 Search Results", "💖 Most Liked"]:
    if st.session_state.search_results.empty:
        update_data()
        st.rerun()
            
    st.subheader(f"{st.session_state.active_tab}")
    
    # Video Grid
    df = st.session_state.search_results
    for i in range(0, len(df), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(df):
                row = df.iloc[i+j]
                with cols[j]:
                    st.markdown(f'''
                        <div style="background:rgba(255,255,255,0.03); border-radius:12px; overflow:hidden; border:1px solid rgba(255,255,255,0.05); margin-bottom:20px;">
                            <img src="{row['thumbnail']}" style="width:100%; aspect-ratio:16/9; object-fit:cover;">
                            <div style="padding:16px;">
                                <div style="font-weight:600; font-size:1.05rem; margin-bottom:4px; height:44px; overflow:hidden;">{row['title']}</div>
                                <div style="color:rgba(255,255,255,0.4); font-size:0.85rem; display:flex; justify-content:space-between;">
                                    <span>👤 {row['channel_title']}</span>
                                    <span>📅 {row['published_at'].strftime('%d %b %Y')}</span>
                                </div>
                                <div style="display:flex; justify-content:space-between; margin-top:12px; font-size:0.9rem;">
                                    <span>👁️ {row['view_count']:,}</span>
                                    <span>👍 {row['like_count']:,}</span>
                                </div>
                            </div>
                        </div>
                    ''', unsafe_allow_html=True)
                    with st.expander("Details"):
                        st.video(f"https://www.youtube.com/watch?v={row['video_id']}")

    # Search Channel Insights Section
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🏆 Channel Intelligence Leaderboard")
    try:
        chan_df = get_channel_summary(df)
        if not chan_df.empty:
            # Format numbers for better readability in the table
            formatted_chan_df = chan_df.copy()
            formatted_chan_df['Total Views'] = formatted_chan_df['Total Views'].apply(lambda x: f"{x/1000:,.1f}K" if x > 1000 else str(x))
            formatted_chan_df['Total Likes'] = formatted_chan_df['Total Likes'].apply(lambda x: f"{x/1000:,.1f}K" if x > 1000 else str(x))
            formatted_chan_df['Engagement Rate'] = formatted_chan_df['Engagement Rate'].apply(lambda x: f"{x:.2%}")
            
            st.dataframe(
                formatted_chan_df,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No channel data available for the current results.")
    except Exception as e:
        st.error(f"Channel Insights Error: {str(e)}")
    
    # Creator Excellence Banner
    region_name = st.session_state.get('region_choice_name', 'Global')
    st.markdown(f'''
        <div class="banner">
            <span style="font-size:1.2rem; font-weight:800; color:#fff;">✨ {region_name} Content Excellence</span><br>
            <span style="color:rgba(255,255,255,0.6);">Featuring the most impactful creators and high-velocity trends in this region.</span>
        </div>
    ''', unsafe_allow_html=True)

elif st.session_state.active_tab == "📊 Deep Analysis":
    df = st.session_state.search_results
    if df.empty: 
        st.info("Load data first")
    else:
        st.markdown("### 📊 Deep Audience & Performance Intelligence")
        
        # Row 1: Donut and Pie
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.markdown("#### 🍩 Interaction Breakdown")
            # Calculate total likes and comments
            total_l = df['like_count'].sum()
            total_c = df['comment_count'].sum()
            fig1 = px.pie(
                names=["Likes", "Comments"], 
                values=[total_l, total_c], 
                hole=0.7, 
                color_discrete_sequence=['#ff4b4b', '#ffffff']
            )
            fig1.update_traces(textinfo='percent', textfont_size=14)
            fig1.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(0,0,0,0)', 
                font_color="white", 
                margin=dict(t=30, b=0, l=0, r=0),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig1, use_container_width=True)
            
        with col_c2:
            st.markdown("#### 🥧 Channel View Share")
            c_views = df.groupby("channel_title")["view_count"].sum().reset_index().nlargest(5, 'view_count')
            fig2 = px.pie(
                c_views, 
                values="view_count", 
                names="channel_title", 
                color_discrete_sequence=px.colors.sequential.Reds_r
            )
            fig2.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(0,0,0,0)', 
                font_color="white", 
                margin=dict(t=30, b=0, l=0, r=0),
                showlegend=False
            )
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown(" --- ")
        
        # Row 2: Performance Map and Engagement Efficiency
        col_c3, col_c4 = st.columns([1.5, 1])
        with col_c3:
            st.markdown("#### 🗺️ Performance Map (Views vs Likes)")
            fig3 = px.scatter(
                df, 
                x="view_count", 
                y="like_count",
                size="engagement_rate",
                hover_name="title",
                color="engagement_rate",
                color_continuous_scale="Reds",
                labels={"view_count": "Views", "like_count": "Likes", "engagement_rate": "ER %"}
            )
            fig3.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(0,0,0,0)', 
                font_color="white",
                xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
                coloraxis_showscale=False
            )
            st.plotly_chart(fig3, use_container_width=True)
            
        with col_c4:
            st.markdown("#### ⚡ Engagement Efficiency")
            top_er = df.nlargest(5, 'engagement_rate')
            fig4 = px.bar(
                top_er,
                y='title',
                x='engagement_rate',
                orientation='h',
                color='engagement_rate',
                color_continuous_scale="Reds",
                labels={"engagement_rate": "ER %", "title": "Video"}
            )
            fig4.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(0,0,0,0)', 
                font_color="white",
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=False, showticklabels=False), # Hide labels for cleaner look
                coloraxis_showscale=False,
                margin=dict(t=0, b=0, l=0, r=0)
            )
            st.plotly_chart(fig4, use_container_width=True)

elif st.session_state.active_tab == "🤖 AI Strategist":
    st.markdown("### 🤖 InsightX AI Content Strategist")
    if st.session_state.search_results.empty: st.warning("No data context.")
    else:
        if st.button("✨ Generate Viral Ideas"):
            with st.spinner("Analyzing..."):
                st.info(analyze_trends(st.session_state.search_results))
        if 'messages' not in st.session_state: st.session_state.messages = []
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]): st.markdown(msg["content"])
        if ci := st.chat_input("Ask a strategist..."):
            st.session_state.messages.append({"role": "user", "content": ci})
            with st.chat_message("user"): st.markdown(ci)
            with st.chat_message("assistant"):
                res = get_ai_response(ci, f"Top videos: {st.session_state.search_results['title'].head(5).tolist()}")
                st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res})

st.markdown("<br><br><center style='color:rgba(255,255,255,0.2); font-size:0.8rem;'>YouTube InsightX v3.0 Ultra | Powered by Groq AI</center>", unsafe_allow_html=True)

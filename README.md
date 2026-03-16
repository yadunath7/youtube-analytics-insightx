# YouTube Trending Videos 2025 — Analytics Dashboard

An interactive, production-ready analytics dashboard for YouTube Trending Videos 2025, updated daily.

## ✨ Features

| Feature | Details |
|---------|---------|
| 🎨 Dark theme | Premium dark UI with gradient design |
| 📊 7 Interactive Charts | Top Videos, Category Donut, Engagement Scatter, Daily Volume, Region Bar, Top Channels, Engagement Box Plot |
| 🃏 KPI Cards | Total Videos · Total Views · Avg Views · Avg Likes · Avg Engagement Rate |
| 🌍 Filters | Region · Category · Date Range · Top N |
| 🔍 Search | Real-time title/channel search |
| ⬇️ Export | Download filtered data as CSV |
| 🔄 Daily Refresh | Auto-refreshes Kaggle data every 24 hours |

## 🚀 Quick Start

```bash
cd /Users/yadunath/youtube_analytics
source venv/bin/activate
streamlit run app.py
```

The dashboard opens at **http://localhost:8501**.

## 📡 Live Data (Optional)

1. Go to https://www.kaggle.com/settings → **Create New Token** → download `kaggle.json`
2. Place it at `~/.kaggle/kaggle.json`
3. Restart the dashboard — it will pull live data automatically!

## 🗓️ Daily Auto-Update via Cron

```bash
# Add to crontab: updates data every day at 6am
0 6 * * * bash /Users/yadunath/youtube_analytics/update_data.sh >> /tmp/yt_update.log 2>&1
```

## 📁 Project Structure

```
youtube_analytics/
├── app.py              ← Streamlit dashboard (main entry point)
├── data_loader.py      ← Kaggle API + synthetic data fallback
├── update_data.sh      ← Manual data refresh script
├── requirements.txt    ← Python dependencies
├── .streamlit/
│   └── config.toml     ← Dark theme configuration
└── data/
    └── youtube_trending.csv  ← Cached dataset (auto-generated)
```

## 📦 Dataset

- **Source:** [YouTube Trending Videos 2025](https://www.kaggle.com/datasets/sebastianbesinski/youtube-trending-videos-2025-updated-daily)
- **Updated:** Daily by Kaggle author
- **Schema:** `video_id`, `title`, `channel_title`, `category`, `views`, `likes`, `dislikes`, `comment_count`, `trending_date`, `region`, `tags`

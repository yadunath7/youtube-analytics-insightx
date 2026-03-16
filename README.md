# YouTube InsightX – AI Powered YouTube Analytics Dashboard

YouTube InsightX is a premium, real-time analytics platform designed for creators and data analysts. It leverages the YouTube Data API v3 for live data fetching and Groq AI for generating intelligent content strategies.

## 🚀 Features

- **Real-time Data Fetching**: Get the latest trending videos or search by keyword across different regions and categories.
- **Premium Dark UI**: A sleek, modern dashboard inspired by YouTube Studio with glassmorphism effects.
- **Advanced Analytics**:
  - **Interaction Breakdown**: Donut chart showing Likes vs. Comments.
  - **Channel View Share**: Pie chart of view distribution among top channels.
  - **Performance Map**: Scatter plot correlating views, likes, and engagement.
  - **Engagement Efficiency**: Visualizing the most engaging content.
- **AI Content Strategist**: A built-in chatbot powered by Groq (LLaMA 3) that provides viral content ideas and trend analysis.
- **CSV Data Export**: Download your filtered results for offline analysis.
- **Embedded Player**: Watch videos directly within the dashboard.

## 🛠️ Tech Stack

- **Python**: Core logic.
- **Streamlit**: Web framework.
- **Pandas & NumPy**: Data manipulation.
- **Plotly**: Interactive visualizations.
- **Groq AI**: Intelligent content strategy generation.
- **YouTube Data API v3**: Live video metrics.

## 📦 Installation & Setup

1. **Clone the project**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure API Keys**:
   Create a `.env` file in the root directory (or use the provided one) and add your keys:
   ```env
   YOUTUBE_API_KEY=YOUR_YOUTUBE_API_KEY
   GROQ_API_KEY=YOUR_GROQ_API_KEY
   ```
4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

## 📊 Engagement Rate Formula
$Engagement Rate = \frac{Likes + Comments}{Views}$

---
Developed for Data Analytics Subject.

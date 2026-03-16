import pandas as pd
import numpy as np

def process_video_data(api_response):
    """Transform YouTube API response into a structured Pandas DataFrame."""
    items = api_response.get("items", [])
    if not items:
        return pd.DataFrame()
    
    data = []
    for item in items:
        snippet = item.get("snippet", {})
        stats = item.get("statistics", {})
        
        video_id = item.get("id")
        if isinstance(video_id, dict):
            video_id = video_id.get("videoId")
            
        video_data = {
            "video_id": video_id,
            "title": snippet.get("title"),
            "channel_title": snippet.get("channelTitle"),
            "channel_id": snippet.get("channelId"),
            "published_at": pd.to_datetime(snippet.get("publishedAt")),
            "description": snippet.get("description"),
            "thumbnail": snippet.get("thumbnails", {}).get("high", {}).get("url"),
            "view_count": int(stats.get("viewCount", 0)),
            "like_count": int(stats.get("likeCount", 0)),
            "comment_count": int(stats.get("commentCount", 0)),
            "category_id": snippet.get("categoryId")
        }
        
        # Calculate Engagement Rate: (likes + comments) / views
        if video_data["view_count"] > 0:
            video_data["engagement_rate"] = (video_data["like_count"] + video_data["comment_count"]) / video_data["view_count"]
        else:
            video_data["engagement_rate"] = 0.0
            
        data.append(video_data)
        
    df = pd.DataFrame(data)
    return df

def get_channel_summary(df):
    """Aggregate metrics by channel."""
    if df.empty:
        return pd.DataFrame()
    
    summary = df.groupby("channel_title").agg({
        "view_count": "sum",
        "like_count": "sum",
        "comment_count": "sum",
        "video_id": "count"
    }).reset_index()
    
    summary.rename(columns={
        "view_count": "Total Views",
        "like_count": "Total Likes",
        "comment_count": "Total Comments",
        "video_id": "Search Results Count",
        "channel_title": "Channel Name"
    }, inplace=True)
    
    # Recalculate Engagement Rate for the channel summary
    summary["Engagement Rate"] = (summary["Total Likes"] + summary["Total Comments"]) / summary["Total Views"]
    summary["Engagement Rate"] = summary["Engagement Rate"].fillna(0)
    
    return summary

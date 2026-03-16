import requests
import os
from dotenv import load_dotenv

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
BASE_URL = "https://www.googleapis.com/youtube/v3"

def get_trending_videos(region_code="US", video_category_id="0", max_results=20):
    """Fetch trending videos based on region and category."""
    url = f"{BASE_URL}/videos"
    params = {
        "part": "snippet,statistics,contentDetails",
        "chart": "mostPopular",
        "regionCode": region_code,
        "maxResults": max_results,
        "key": YOUTUBE_API_KEY
    }
    if video_category_id != "0":
        params["videoCategoryId"] = video_category_id
        
    response = requests.get(url, params=params)
    return response.json()

def search_youtube_videos(query, region_code="US", video_category_id="0", max_results=20):
    """Search for videos based on keyword, region, and category."""
    search_url = f"{BASE_URL}/search"
    search_params = {
        "part": "snippet",
        "q": query,
        "regionCode": region_code,
        "type": "video",
        "maxResults": max_results,
        "key": YOUTUBE_API_KEY
    }
    if video_category_id != "0":
        search_params["videoCategoryId"] = video_category_id
        
    search_response = requests.get(search_url, params=search_params).json()
    
    video_ids = [item["id"]["videoId"] for item in search_response.get("items", [])]
    if not video_ids:
        return {"items": []}
        
    # Search doesn't give statistics, so we need to call /videos
    return get_video_details(",".join(video_ids))

def get_video_details(video_ids):
    """Fetch detailed statistics for a list of video IDs."""
    url = f"{BASE_URL}/videos"
    params = {
        "part": "snippet,statistics,contentDetails",
        "id": video_ids,
        "key": YOUTUBE_API_KEY
    }
    response = requests.get(url, params=params)
    return response.json()

def get_categories(region_code="US"):
    """Fetch video categories for a specific region."""
    url = f"{BASE_URL}/videoCategories"
    params = {
        "part": "snippet",
        "regionCode": region_code,
        "key": YOUTUBE_API_KEY
    }
    response = requests.get(url, params=params)
    return response.json()

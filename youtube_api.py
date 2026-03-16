import googleapiclient.discovery
import googleapiclient.errors
import pandas as pd
from datetime import datetime

class YouTubeAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.youtube = googleapiclient.discovery.build(
            "youtube", "v3", developerKey=api_key
        )
        self.categories = {
            "All": None,
            "Music": "10",
            "Gaming": "20",
            "Film & Animation": "1",
            "Sports": "17",
            "Entertainment": "24",
            "News & Politics": "25",
            "How-to & Style": "26",
            "Education": "27",
            "Science & Technology": "28",
            "People & Blogs": "22",
            "Comedy": "23",
            "Travel & Events": "19"
        }

    def get_trending_videos(self, region_code="IN", category_id=None, max_results=20):
        """Fetch trending videos for a specific region and category."""
        try:
            params = {
                "part": "snippet,contentDetails,statistics",
                "chart": "mostPopular",
                "regionCode": region_code,
                "maxResults": max_results
            }
            if category_id:
                params["videoCategoryId"] = category_id
            
            request = self.youtube.videos().list(**params)
            response = request.execute()
            
            videos = []
            for item in response.get("items", []):
                videos.append({
                    "video_id": item["id"],
                    "title": item["snippet"]["title"],
                    "channel_title": item["snippet"]["channelTitle"],
                    "category_id": item["snippet"]["categoryId"],
                    "published_at": item["snippet"]["publishedAt"],
                    "trending_date": datetime.now().strftime("%Y-%m-%d"),
                    "views": int(item["statistics"].get("viewCount", 0)),
                    "likes": int(item["statistics"].get("likeCount", 0)),
                    "comment_count": int(item["statistics"].get("commentCount", 0)),
                    "thumbnail_link": item["snippet"]["thumbnails"]["high"]["url"],
                    "country_code": region_code
                })
            return pd.DataFrame(videos)
        except Exception as e:
            print(f"Error fetching trending videos: {e}")
            return pd.DataFrame()

    def get_video_comments(self, video_id, max_results=5):
        """Fetch top comments for a specific video."""
        try:
            request = self.youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=max_results,
                order="relevance"
            )
            response = request.execute()
            
            comments = []
            for item in response.get("items", []):
                comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                comments.append(comment)
            return comments
        except Exception as e:
            # Some videos have comments disabled
            return ["Comments are disabled for this video."]

    def search_videos(self, query, region_code="IN", max_results=10):
        """Search for videos based on a query."""
        try:
            request = self.youtube.search().list(
                part="snippet",
                q=query,
                regionCode=region_code,
                maxResults=max_results,
                type="video"
            )
            response = request.execute()
            
            video_ids = [item["id"]["videoId"] for item in response.get("items", [])]
            
            # Fetch full details for these videos
            if video_ids:
                details_request = self.youtube.videos().list(
                    part="snippet,statistics",
                    id=",".join(video_ids)
                )
                details_response = details_request.execute()
                
                videos = []
                for item in details_response.get("items", []):
                    videos.append({
                        "video_id": item["id"],
                        "title": item["snippet"]["title"],
                        "channel_title": item["snippet"]["channelTitle"],
                        "category_id": item["snippet"]["categoryId"],
                        "published_at": item["snippet"]["publishedAt"],
                        "trending_date": datetime.now().strftime("%Y-%m-%d"),
                        "views": int(item["statistics"].get("viewCount", 0)),
                        "likes": int(item["statistics"].get("likeCount", 0)),
                        "comment_count": int(item["statistics"].get("commentCount", 0)),
                        "thumbnail_link": item["snippet"]["thumbnails"]["high"]["url"],
                        "country_code": region_code
                    })
                return pd.DataFrame(videos)
            return pd.DataFrame()
        except Exception as e:
            print(f"Error searching videos: {e}")
            return pd.DataFrame()

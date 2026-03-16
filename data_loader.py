"""
data_loader.py
--------------
Handles all data acquisition for the YouTube Trending Videos 2025 dashboard.

Priority order:
  1. Try Kaggle API download (if ~/.kaggle/kaggle.json or env vars present)
  2. Fall back to realistic synthetic data with the same schema

Caching: Downloaded CSV is cached in ./data/ and refreshed only if older than 24 hours.
"""

import os
import json
import random
import hashlib
import logging
from pathlib import Path
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────────────────────────
# Config
# ──────────────────────────────────────────────────────────────────────────────
DATA_DIR        = Path(__file__).parent / "data"
CACHE_FILE      = DATA_DIR / "youtube_trending.csv"
KAGGLE_DATASET  = "sebastianbesinski/youtube-trending-videos-2025-updated-daily"
CACHE_MAX_AGE_H = 24   # hours before re-downloading


# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────
def _cache_is_fresh() -> bool:
    """Return True if cached CSV exists and is younger than CACHE_MAX_AGE_H."""
    if not CACHE_FILE.exists():
        return False
    age = datetime.now() - datetime.fromtimestamp(CACHE_FILE.stat().st_mtime)
    return age < timedelta(hours=CACHE_MAX_AGE_H)


def _kaggle_credentials_available() -> bool:
    """Check for kaggle.json or env-variable based auth."""
    kaggle_json = Path.home() / ".kaggle" / "kaggle.json"
    if kaggle_json.exists():
        return True
    return bool(os.getenv("KAGGLE_USERNAME") and os.getenv("KAGGLE_KEY"))


def _download_from_kaggle() -> bool:
    """Attempt to download the dataset via the Kaggle API. Returns True on success."""
    try:
        import kaggle
        from kaggle import api as kaggle_api

        kaggle_api.authenticate()
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        logger.info("Downloading dataset from Kaggle…")
        kaggle_api.dataset_download_files(KAGGLE_DATASET, path=str(DATA_DIR), unzip=True)
        logger.info("Download complete.")
        # Rename the first CSV found to our canonical cache name
        csvs = list(DATA_DIR.glob("*.csv"))
        if csvs and csvs[0] != CACHE_FILE:
            csvs[0].rename(CACHE_FILE)
        return CACHE_FILE.exists()
    except Exception as exc:
        logger.warning(f"Kaggle download failed: {exc}")
        return False


# ──────────────────────────────────────────────────────────────────────────────
# Synthetic data generator
# ──────────────────────────────────────────────────────────────────────────────
CATEGORIES = {
    "1":  "Film & Animation",
    "2":  "Autos & Vehicles",
    "10": "Music",
    "15": "Pets & Animals",
    "17": "Sports",
    "19": "Travel & Events",
    "20": "Gaming",
    "22": "People & Blogs",
    "23": "Comedy",
    "24": "Entertainment",
    "25": "News & Politics",
    "26": "How-to & Style",
    "27": "Education",
    "28": "Science & Technology",
    "29": "Nonprofits & Activism",
}

REGIONS = ["US", "GB", "IN", "CA", "AU", "DE", "FR", "JP", "BR", "MX"]

CHANNEL_TEMPLATES = [
    "TechGuru", "MrBeast", "NatGeo Wild", "CNN", "ESPN", "Tasty", "MKBHD",
    "Vox", "Kurzgesagt", "PewDiePie", "Veritasium", "LegalEagle", "Wendover",
    "ColdFusion", "SciShow", "MinutePhysics", "TED", "Bloomberg", "Vice",
]

VIDEO_TITLE_PREFIXES = [
    "I Tried", "We Built", "The Truth About", "Why Everyone is Talking About",
    "Unboxing the", "How to Master", "Top 10", "Reacting to", "Inside the World of",
    "The Dark Side of", "Behind the Scenes:", "Breaking Down", "World Record",
]

VIDEO_TITLE_SUBJECTS = [
    "A.I. in 2025", "the New iPhone", "Space Tourism", "Electric Cars", "Fast Food Hacks",
    "a Remote Island", "the World's Hardest Game", "Crypto Crashes", "a $1 vs $1M Hotel",
    "Hollywood Secrets", "the Internet's Biggest Mystery", "Climate Change Solutions",
    "Learning to Code in 24 Hours", "the Richest Person's Routine", "Viral TikTok Trends",
]

rng = np.random.default_rng(42)


def _make_video_id(n: int) -> str:
    return hashlib.md5(str(n).encode()).hexdigest()[:11]


def _generate_synthetic_data(n_rows: int = 5000) -> pd.DataFrame:
    """Generate a realistic synthetic YouTube trending dataset."""
    logger.info(f"Generating synthetic dataset with {n_rows} rows…")

    start_date = datetime(2025, 1, 1)
    end_date   = datetime(2026, 1, 1)
    date_range = (end_date - start_date).days

    rows = []
    for i in range(n_rows):
        category_id   = random.choice(list(CATEGORIES.keys()))
        trending_date = start_date + timedelta(days=int(rng.integers(0, date_range)))
        publish_offset = rng.integers(1, 365)
        publish_time  = trending_date - timedelta(days=int(publish_offset))

        # Correlated engagement stats
        views         = int(rng.lognormal(mean=14.5, sigma=1.5))
        likes         = int(views * rng.uniform(0.02, 0.15))
        dislikes      = int(likes  * rng.uniform(0.005, 0.05))
        comments      = int(views  * rng.uniform(0.001, 0.03))

        title_prefix  = random.choice(VIDEO_TITLE_PREFIXES)
        title_subject = random.choice(VIDEO_TITLE_SUBJECTS)
        title         = f"{title_prefix} {title_subject}"
        channel       = random.choice(CHANNEL_TEMPLATES) + f" {rng.integers(1, 10)}"
        region        = random.choice(REGIONS)
        tags          = "|".join(rng.choice(VIDEO_TITLE_SUBJECTS, size=3, replace=False).tolist())

        rows.append({
            "video_id":       _make_video_id(i),
            "title":          title,
            "channel_title":  channel,
            "category_id":    category_id,
            "category_name":  CATEGORIES[category_id],
            "publish_time":   publish_time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            "trending_date":  trending_date.strftime("%Y-%m-%d"),
            "tags":           tags,
            "views":          views,
            "likes":          likes,
            "dislikes":       dislikes,
            "comment_count":  comments,
            "country_code":   region,
            "thumbnail_link": f"https://i.ytimg.com/vi/{_make_video_id(i)}/maxresdefault.jpg",
            "trending_comments": json.dumps([
                f"This {title_subject} is amazing!",
                f"Can't believe they {title_prefix.lower()} this...",
                "Finally a high quality upload!",
                "First! Just kidding, but great video.",
                f"Love from {region}!",
                "Who else is here from the trending page?",
                "This needs more views."
            ][:int(rng.integers(2, 6))])
        })

    df = pd.DataFrame(rows)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(CACHE_FILE, index=False)
    logger.info("Synthetic dataset saved to cache.")
    return df


# ──────────────────────────────────────────────────────────────────────────────
# Public API
# ──────────────────────────────────────────────────────────────────────────────
def load_data() -> tuple[pd.DataFrame, str, bool]:
    """
    Load YouTube trending data.

    Returns
    -------
    df          : pd.DataFrame
    source      : str  — 'kaggle' | 'cache' | 'synthetic'
    is_live     : bool — True if data comes from Kaggle
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # ── 1. Serve from cache if fresh ──
    if _cache_is_fresh():
        logger.info("Serving from fresh cache.")
        df = pd.read_csv(CACHE_FILE)
        return _post_process(df), "cache", True

    # ── 2. Try Kaggle download ──
    if _kaggle_credentials_available():
        success = _download_from_kaggle()
        if success:
            df = pd.read_csv(CACHE_FILE)
            return _post_process(df), "kaggle", True

    # ── 3. Synthetic fallback ──
    df = _generate_synthetic_data()
    return _post_process(df), "synthetic", False


def _post_process(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and enrich the raw DataFrame — handles both real Kaggle and synthetic schemas."""
    # Normalise column names
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # ── Canonicalize real Kaggle dataset column names → internal schema ──
    rename_map = {
        "channel":      "channel_title",
        "country":      "country_code",
        "comments":     "comment_count",
        "published_at": "publish_time",
        "fetch_date":   "trending_date",
        "region":       "country_code" # Fallback for already processed synthetic data
    }
    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

    # Ensure required columns exist
    required = ["video_id", "title", "channel_title", "views", "likes",
                "comment_count", "trending_date", "country_code", 
                "thumbnail_link", "trending_comments"]
    for col in required:
        if col not in df.columns:
            df[col] = None

    # Type coercion
    for num_col in ["views", "likes", "dislikes", "comment_count"]:
        if num_col in df.columns:
            df[num_col] = pd.to_numeric(df[num_col], errors="coerce").fillna(0).astype(int)

    df["trending_date"] = pd.to_datetime(df["trending_date"], errors="coerce")

    # Derived metrics
    df["engagement_rate"] = (
        (df["likes"] + df.get("comment_count", 0)) / df["views"].replace(0, np.nan)
    ).fillna(0).round(4)

    # Category name mapping (in case only category_id is present)
    if "category_name" not in df.columns:
        if "category_id" in df.columns:
            df["category_id"] = df["category_id"].astype(str)
            df["category_name"] = df["category_id"].map(CATEGORIES).fillna("Unknown")
        else:
            df["category_name"] = "Unknown"

    # Fill missing country
    if "country_code" not in df.columns:
        df["country_code"] = "Unknown"
    df["country_code"] = df["country_code"].fillna("Unknown")
    
    # Derive Global Region from Country Code
    region_mapping = {
        "US": "North America", "CA": "North America", "MX": "North America", "PR": "North America",
        "GB": "Europe", "DE": "Europe", "FR": "Europe", "IT": "Europe", "ES": "Europe", "RU": "Europe",
        "IN": "Asia", "JP": "Asia", "KR": "Asia", "ID": "Asia", "TH": "Asia", "PH": "Asia", "SA": "Middle East", "AE": "Middle East",
        "BR": "South America", "AR": "South America", "CO": "South America", "CL": "South America",
        "AU": "Oceania", "NZ": "Oceania",
        "ZA": "Africa", "EG": "Africa", "NG": "Africa", "KE": "Africa"
    }
    df["region"] = df["country_code"].map(region_mapping).fillna("Other")

    return df


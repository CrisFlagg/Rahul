import os
import sys
import csv
import datetime
from pathlib import Path
from typing import List, Dict, Optional

import pandas as pd
import requests

try:
    from huggingface_hub import snapshot_download
except ImportError:
    snapshot_download = None

# Optional: Google Trends (no API key required)
try:
    from pytrends.request import TrendReq
except ImportError:
    TrendReq = None


DATA_DIR = Path("data")
SONICS_DIR = DATA_DIR / "sonics"
FIGURES_DIR = Path("figures")

YOUTUBE_MONTHLY_OUT = DATA_DIR / "youtube_ai_music_monthly.csv"
DEEZER_POINTS_OUT = DATA_DIR / "deezer_ai_daily_uploads.csv"
GOOGLE_TRENDS_OUT = DATA_DIR / "google_trends_ai_music.csv"


def ensure_dirs():
    DATA_DIR.mkdir(exist_ok=True)
    SONICS_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(exist_ok=True)


def download_sonics_dataset(local_dir: Path) -> Dict[str, Path]:
    """
    Download SONICS dataset metadata (fake_songs.csv, real_songs.csv) from Hugging Face.

    Returns dict of paths.
    """
    if snapshot_download is None:
        print("huggingface_hub is not installed. Please `pip install huggingface_hub` and rerun.")
        return {}

    print("Downloading SONICS dataset from Hugging Face...")
    cache_dir = snapshot_download(
        repo_id="awsaf49/sonics",
        repo_type="dataset",
        local_dir=str(local_dir),
        ignore_patterns=["*.mp3", "*.wav", "*.flac"]  # metadata only
    )

    # Find CSVs
    fake_csv = None
    real_csv = None
    for root, _, files in os.walk(cache_dir):
        for f in files:
            if f == "fake_songs.csv":
                fake_csv = Path(root) / f
            elif f == "real_songs.csv":
                real_csv = Path(root) / f

    out_paths = {}
    if fake_csv:
        dest = local_dir / "fake_songs.csv"
        if Path(fake_csv) != dest:
            pd.read_csv(fake_csv).to_csv(dest, index=False)
        out_paths["fake_songs"] = dest
        print(f"Saved: {dest}")
    else:
        print("fake_songs.csv not found in SONICS dataset")

    if real_csv:
        dest = local_dir / "real_songs.csv"
        if Path(real_csv) != dest:
            pd.read_csv(real_csv).to_csv(dest, index=False)
        out_paths["real_songs"] = dest
        print(f"Saved: {dest}")
    else:
        print("real_songs.csv not found in SONICS dataset")

    return out_paths


def aggregate_sonics_counts(fake_csv: Optional[Path], real_csv: Optional[Path]) -> None:
    """
    Produce simple aggregates from SONICS metadata (not time series).
    - Counts by source for fake songs (Suno/Udio)
    - Counts by label category ('full fake', 'half fake', 'mostly fake')
    - Real songs count by year (if present)
    Save CSVs under SONICS_DIR.
    """
    if fake_csv and fake_csv.exists():
        df_fake = pd.read_csv(fake_csv)
        cols = df_fake.columns.tolist()
        counts_by_source = df_fake.groupby("source").size().reset_index(name="count")
        counts_by_source.to_csv(SONICS_DIR / "fake_counts_by_source.csv", index=False)
        print(f"SONICS aggregates: {SONICS_DIR / 'fake_counts_by_source.csv'}")

        if "label" in cols:
            counts_by_label = df_fake.groupby("label").size().reset_index(name="count")
            counts_by_label.to_csv(SONICS_DIR / "fake_counts_by_label.csv", index=False)
            print(f"SONICS aggregates: {SONICS_DIR / 'fake_counts_by_label.csv'}")

    if real_csv and real_csv.exists():
        df_real = pd.read_csv(real_csv)
        if "year" in df_real.columns:
            counts_by_year = df_real.groupby("year").size().reset_index(name="count")
            counts_by_year.to_csv(SONICS_DIR / "real_counts_by_year.csv", index=False)
            print(f"SONICS aggregates: {SONICS_DIR / 'real_counts_by_year.csv'}")


def month_range(start_date: datetime.date, end_date: datetime.date) -> List[datetime.date]:
    months = []
    cur = datetime.date(start_date.year, start_date.month, 1)
    last = datetime.date(end_date.year, end_date.month, 1)
    while cur <= last:
        months.append(cur)
        # increment month
        if cur.month == 12:
            cur = datetime.date(cur.year + 1, 1, 1)
        else:
            cur = datetime.date(cur.year, cur.month + 1, 1)
    return months


def youtube_search_count(api_key: str, query: str, published_after: str, published_before: str) -> int:
    """
    Use YouTube Search API to count videos for a query in a time window.
    This is a heuristic; results can be noisy and may include non-music videos.
    """
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "key": api_key,
        "q": query,
        "part": "snippet",
        "type": "video",
        "order": "date",
        "maxResults": 50,
        "publishedAfter": published_after,
        "publishedBefore": published_before,
    }
    total = 0
    next_page_token = None
    attempts = 0
    while True:
        if next_page_token:
            params["pageToken"] = next_page_token
        resp = requests.get(url, params=params, timeout=30)
        if resp.status_code != 200:
            # Stop on error
            break
        data = resp.json()
        items = data.get("items", [])
        total += len(items)
        next_page_token = data.get("nextPageToken")
        attempts += 1
        if not next_page_token or attempts > 10:
            # cap pagination to avoid API quota blow-up
            break
    return total


def collect_youtube_monthly(api_key: str,
                            start_date: datetime.date,
                            end_date: datetime.date,
                            queries: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Collect rough monthly counts of AI music-related videos on YouTube.
    Queries default to common AI-music terms and platform names.
    """
    if queries is None:
        queries = [
            "AI generated music",
            "AI music",
            "Suno AI",
            "Udio AI",
            "Boomy AI music",
        ]

    months = month_range(start_date, end_date)
    rows = []
    print("Collecting YouTube monthly counts (heuristic)...")
    for m in months:
        if m.month == 12:
            next_m = datetime.date(m.year + 1, 1, 1)
        else:
            next_m = datetime.date(m.year, m.month + 1, 1)
        published_after = m.isoformat() + "T00:00:00Z"
        published_before = next_m.isoformat() + "T00:00:00Z"

        count_sum = 0
        for q in queries:
            c = youtube_search_count(api_key, q, published_after, published_before)
            count_sum += c

        rows.append({"month": m.isoformat(), "youtube_ai_music_count": count_sum})

        print(f"{m.isoformat()}: {count_sum}")

    df = pd.DataFrame(rows)
    df.to_csv(YOUTUBE_MONTHLY_OUT, index=False)
    print(f"Saved YouTube monthly counts: {YOUTUBE_MONTHLY_OUT}")
    return df


def save_deezer_points() -> pd.DataFrame:
    """
    Save known Deezer datapoints reported in industry press (MBW):
    - Jan 2025: ~10k daily fully AI-generated tracks uploaded
    - Apr 2025: ~20k daily
    - Sep 2025: ~30k daily (28% of daily deliveries)
    """
    points = [
        {"date": "2025-01-15", "daily_ai_uploads": 10000},
        {"date": "2025-04-15", "daily_ai_uploads": 20000},
        {"date": "2025-09-11", "daily_ai_uploads": 30000},
    ]
    df = pd.DataFrame(points)
    df.to_csv(DEEZER_POINTS_OUT, index=False)
    print(f"Saved Deezer timeline points: {DEEZER_POINTS_OUT}")
    return df


def collect_google_trends(start_date: datetime.date,
                          end_date: datetime.date,
                          queries: Optional[List[str]] = None,
                          geo: str = "") -> Optional[pd.DataFrame]:
    """
    Collect monthly Google Trends interest for AI-music-related queries.
    No API key required. Returns a DataFrame with month and interest columns.

    geo: empty string for worldwide, or country code like 'US'.
    """
    if TrendReq is None:
        print("pytrends is not installed. Please `pip install pytrends` to enable Google Trends collection.")
        return None

    if queries is None:
        queries = ["AI generated music", "AI music", "Suno", "Udio", "Boomy"]

    # Google Trends returns weekly data; resample to monthly averages.
    pytrends = TrendReq(hl="en-US", tz=360)
    pytrends.build_payload(kw_list=queries, timeframe=f"{start_date.strftime('%Y-%m-%d')} {end_date.strftime('%Y-%m-%d')}", geo=geo)
    df = pytrends.interest_over_time()
    if df.empty:
        print("Google Trends returned empty data.")
        return None

    df = df.drop(columns=[c for c in ["isPartial"] if c in df.columns])
    # Resample monthly average
    df_monthly = df.resample("MS").mean().reset_index()
    df_monthly = df_monthly.rename(columns={"date": "month"})
    df_monthly.to_csv(GOOGLE_TRENDS_OUT, index=False)
    print(f"Saved Google Trends data: {GOOGLE_TRENDS_OUT}")
    return df_monthly


def main():
    ensure_dirs()

    # 1) Download SONICS metadata and aggregate simple counts
    paths = download_sonics_dataset(SONICS_DIR)
    aggregate_sonics_counts(paths.get("fake_songs"), paths.get("real_songs"))

    # 2) Optional: Collect YouTube monthly counts (requires YOUTUBE_API_KEY env var)
    api_key = os.getenv("YOUTUBE_API_KEY", "")
    if api_key:
        # collect from Jan 2023 to current month
        start = datetime.date(2023, 1, 1)
        end = datetime.date.today().replace(day=1)
        collect_youtube_monthly(api_key, start, end)
    else:
        print("YOUTUBE_API_KEY not set; skipping YouTube monthly counts.")

    # 3) Save Deezer timeline points
    save_deezer_points()

    # 4) Collect Google Trends monthly interest (no API key required)
    trends_start = datetime.date(2023, 1, 1)
    trends_end = datetime.date.today().replace(day=1)
    collect_google_trends(trends_start, trends_end, queries=None, geo="")

    print("Done.")


if __name__ == "__main__":
    main()
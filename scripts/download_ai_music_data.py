"""
download_ai_music_data.py

Purpose:
- Fetch AI music-related metadata from open sources.
- Produce simple aggregates and time-series inputs for visualization.
- Do all of this using pandas DataFrames, with step-by-step comments
  so you can learn how DataFrames work along the way.

What you'll learn here:
- How to create folders with pathlib.
- How to read CSV files into pandas DataFrames (pd.read_csv).
- How to inspect and transform DataFrames (groupby, resample).
- How to write DataFrames back to disk (to_csv).
- How to collect Google Trends data without any API key (pytrends).
- How to save "known points" (Deezer press-reported figures) as a CSV.

Dependencies to install (one-time):
    pip install pandas requests huggingface_hub pytrends

You do NOT need any API keys to run this end-to-end. YouTube is optional
and will be skipped if you don't set YOUTUBE_API_KEY.

Tip: Think of a pandas DataFrame as an in-memory spreadsheet:
- rows = observations (e.g., songs)
- columns = fields/attributes (e.g., source, label, year)
- You can slice, filter, group, and aggregate like you would in a pivot table.
"""

import os
import datetime
from pathlib import Path
from typing import List, Dict, Optional

# pandas is the main library we use for tabular data.
# It provides the DataFrame object (a 2D table with labeled axes).
import pandas as pd

import requests

# huggingface_hub lets us download the SONICS dataset metadata without manual steps.
try:
    from huggingface_hub import snapshot_download
except ImportError:
    snapshot_download = None

# pytrends is a simple wrapper around Google Trends. No API key needed.
try:
    from pytrends.request import TrendReq
except ImportError:
    TrendReq = None


# Define a few folders we will use. Path objects are convenient and cross-platform.
DATA_DIR = Path("data")
SONICS_DIR = DATA_DIR / "sonics"
FIGURES_DIR = Path("figures")

# Where we'll save our CSV outputs
YOUTUBE_MONTHLY_OUT = DATA_DIR / "youtube_ai_music_monthly.csv"
DEEZER_POINTS_OUT = DATA_DIR / "deezer_ai_daily_uploads.csv"
GOOGLE_TRENDS_OUT = DATA_DIR / "google_trends_ai_music.csv"


def ensure_dirs():
    """
    Create folders if they don't exist.

    This doesn't involve DataFrames; it's just preparing the filesystem so
    our scripts can save files in the expected locations.

    - DATA_DIR: top-level data folder
    - SONICS_DIR: subfolder specifically for SONICS metadata/aggregates
    - FIGURES_DIR: used by the visualization script
    """
    DATA_DIR.mkdir(exist_ok=True)
    SONICS_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(exist_ok=True)


def download_sonics_dataset(local_dir: Path) -> Dict[str, Path]:
    """
    Download SONICS dataset metadata (fake_songs.csv, real_songs.csv) from Hugging Face.

    Returns a dict of output file paths.

    DataFrame concepts in this function:
    - pd.read_csv("path") -> loads a CSV file into a DataFrame.
    - df.to_csv("path", index=False) -> writes a DataFrame back to CSV.

    We only download metadata CSVs here (not audio files).
    """
    if snapshot_download is None:
        print("huggingface_hub is not installed. Please `pip install huggingface_hub` and rerun.")
        return {}

    print("Downloading SONICS dataset from Hugging Face...")
    # snapshot_download returns the local cache directory where files were stored
    cache_dir = snapshot_download(
        repo_id="awsaf49/sonics",
        repo_type="dataset",
        local_dir=str(local_dir),  # put a copy under our 'data/sonics' folder
        ignore_patterns=["*.mp3", "*.wav", "*.flac"]  # metadata only
    )

    # Find the metadata CSVs in the downloaded cache directory
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
        # Read the CSV -> DataFrame (loads rows and columns into memory)
        df_fake = pd.read_csv(fake_csv)
        # Write the DataFrame to our target location (persist to disk)
        dest = local_dir / "fake_songs.csv"
        df_fake.to_csv(dest, index=False)
        out_paths["fake_songs"] = dest
        print(f"Saved: {dest} (rows={len(df_fake)}, columns={list(df_fake.columns)})")
    else:
        print("fake_songs.csv not found in SONICS dataset")

    if real_csv:
        df_real = pd.read_csv(real_csv)
        dest = local_dir / "real_songs.csv"
        df_real.to_csv(dest, index=False)
        out_paths["real_songs"] = dest
        print(f"Saved: {dest} (rows={len(df_real)}, columns={list(df_real.columns)})")
    else:
        print("real_songs.csv not found in SONICS dataset")

    return out_paths


def aggregate_sonics_counts(fake_csv: Optional[Path], real_csv: Optional[Path]) -> None:
    """
    Produce simple aggregates from SONICS metadata and save them as CSVs.

    DataFrame concepts demonstrated:
    - df.columns -> lists column names.
    - df.groupby("col").size().reset_index(name="count") -> "pivot table"-like group-by,
      resulting in a new DataFrame with counts for each unique value in a column.

    We compute:
      1) Counts by 'source' for fake songs (which platform: Suno/Udio).
      2) Counts by 'label' ('full fake', 'half fake', 'mostly fake').
      3) Real songs count by 'year' (if present).

    Why reset_index(name="count")?
    - groupby(...).size() returns a Series (1D labeled array).
    - reset_index(name="count") turns it back into a 2D DataFrame with explicit column names.
    """
    if fake_csv and fake_csv.exists():
        df_fake = pd.read_csv(fake_csv)
        # Look at the columns in this DataFrame (metadata fields available)
        cols = df_fake.columns.tolist()
        print("SONICS fake_songs.csv columns:", cols)

        # Group by 'source' and count rows in each group.
        # Example: source == "Suno" vs "Udio"
        counts_by_source = df_fake.groupby("source").size().reset_index(name="count")
        counts_by_source.to_csv(SONICS_DIR / "fake_counts_by_source.csv", index=False)
        print(f"SONICS aggregates: {SONICS_DIR / 'fake_counts_by_source.csv'}")

        # If a 'label' column exists, group by that too.
        # Example labels in SONICS: "full fake", "half fake", "mostly fake"
        if "label" in cols:
            counts_by_label = df_fake.groupby("label").size().reset_index(name="count")
            counts_by_label.to_csv(SONICS_DIR / "fake_counts_by_label.csv", index=False)
            print(f"SONICS aggregates: {SONICS_DIR / 'fake_counts_by_label.csv'}")
        else:
            print("No 'label' column found in fake_songs.csv; skipping label aggregate.")

    if real_csv and real_csv.exists():
        df_real = pd.read_csv(real_csv)
        print("SONICS real_songs.csv columns:", df_real.columns.tolist())
        # If a 'year' column exists, count songs per year (simple trend proxy)
        if "year" in df_real.columns:
            counts_by_year = df_real.groupby("year").size().reset_index(name="count")
            counts_by_year.to_csv(SONICS_DIR / "real_counts_by_year.csv", index=False)
            print(f"SONICS aggregates: {SONICS_DIR / 'real_counts_by_year.csv'}")
        else:
            print("No 'year' column found in real_songs.csv; skipping year aggregate.")


def month_range(start_date: datetime.date, end_date: datetime.date) -> List[datetime.date]:
    """
    Utility to generate a list of month-start dates between start_date and end_date, inclusive.

    Not a pandas concept—just handy for building monthly series when we need
    to iterate month by month (e.g., API calls or rolling aggregations).
    """
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
    This is a heuristic and OPTIONAL section. If you don't set YOUTUBE_API_KEY
    we'll skip YouTube entirely.

    This function does NOT involve pandas—it's a simple REST API call.
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
    OPTIONAL: Collect rough monthly counts of AI music-related videos on YouTube.

    DataFrame concepts:
    - Build up a list of dicts (rows), then convert to DataFrame with pd.DataFrame(rows).
    - Save to CSV with df.to_csv("path").

    NOTE: This is only called if you set YOUTUBE_API_KEY in your environment.
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
        # compute next month start
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

        # Build one row (dict) per month
        rows.append({"month": m.isoformat(), "youtube_ai_music_count": count_sum})
        print(f"{m.isoformat()}: {count_sum}")

    # Convert rows -> DataFrame (DataFrame constructor maps dict keys to columns)
    df = pd.DataFrame(rows)

    # Write to CSV (index=False means don't write row numbers)
    df.to_csv(YOUTUBE_MONTHLY_OUT, index=False)
    print(f"Saved YouTube monthly counts: {YOUTUBE_MONTHLY_OUT}")
    return df


def save_deezer_points() -> pd.DataFrame:
    """
    Save known Deezer datapoints reported in industry press (MBW) as a CSV.

    DataFrame concepts:
    - pd.DataFrame(list_of_dicts) -> create a DataFrame from Python data.
    - df.to_csv(path) -> persist to disk.

    Points:
      - Jan 2025: ~10k daily fully AI-generated tracks uploaded
      - Apr 2025: ~20k daily
      - Sep 2025: ~30k daily (28% of daily deliveries)

    Why store these points?
    - They act as a simple time series we can visualize even without direct API access.
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

    DataFrame concepts:
    - interest_over_time() returns a DataFrame with a DateTimeIndex (dates are the index, not a column).
    - df.resample("MS").mean() resamples weekly -> monthly start ("MS") by averaging values in each month.
    - df.reset_index() turns the index into a normal 'date' column (so we can save it easily).
    - df.rename(columns={"date": "month"}) renames for clarity.
    - df.to_csv("path") writes the result to disk.

    geo: empty string for worldwide, or country code like 'US'.

    Note: Google Trends values are normalized (0–100) and represent relative interest,
    not absolute counts of uploads or streams.
    """
    if TrendReq is None:
        print("pytrends is not installed. Please `pip install pytrends` to enable Google Trends collection.")
        return None

    if queries is None:
        queries = ["AI generated music", "AI music", "Suno", "Udio", "Boomy"]

    # Initialize pytrends and request interest over time.
    pytrends = TrendReq(hl="en-US", tz=360)  # tz=360 means UTC+6 for request time; not critical here.
    timeframe = f"{start_date.strftime('%Y-%m-%d')} {end_date.strftime('%Y-%m-%d')}"
    pytrends.build_payload(kw_list=queries, timeframe=timeframe, geo=geo)

    # This returns weekly data by default (DateTimeIndex + one column per query)
    df = pytrends.interest_over_time()

    if df.empty:
        print("Google Trends returned empty data.")
        return None

    # The 'isPartial' column (if present) indicates ongoing weeks; it's not needed for our plots.
    df = df.drop(columns=[c for c in ["isPartial"] if c in df.columns])

    # Resample weekly -> monthly start, taking the average per month.
    # 'MS' == Month Start. Other options include 'M' (Month End), etc.
    df_monthly = df.resample("MS").mean().reset_index()

    # Rename the 'date' column to 'month' for clarity (fits the time-series pattern in our repo)
    df_monthly = df_monthly.rename(columns={"date": "month"})

    # Save the monthly time series to CSV
    df_monthly.to_csv(GOOGLE_TRENDS_OUT, index=False)
    print(f"Saved Google Trends data: {GOOGLE_TRENDS_OUT} (rows={len(df_monthly)})")
    return df_monthly


def main():
    """
    Orchestrates the whole download + aggregation workflow.

    Reading this function should give you a step-by-step sense of what's happening:
      1) Create necessary folders.
      2) Download SONICS metadata and save basic aggregates using DataFrames.
      3) Optionally collect YouTube monthly counts (skipped if no API key).
      4) Save Deezer timeline points (press-reported figures).
      5) Collect Google Trends monthly interest without any API key.

    After this runs, check the 'data' folder for CSVs and then run:
        python scripts/visualize_ai_music_usage.py
    to create charts from the CSVs.
    """
    ensure_dirs()

    # 1) Download SONICS metadata and aggregate simple counts
    paths = download_sonics_dataset(SONICS_DIR)
    aggregate_sonics_counts(paths.get("fake_songs"), paths.get("real_songs"))

    # 2) OPTIONAL: Collect YouTube monthly counts (requires YOUTUBE_API_KEY env var).
    # If you don't set the API key, we skip this step entirely.
    api_key = os.getenv("YOUTUBE_API_KEY", "")
    if api_key:
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

    print("All done. Next: run scripts/visualize_ai_music_usage.py to produce charts.")


if __name__ == "__main__":
    main()
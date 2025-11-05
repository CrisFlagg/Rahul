"""
visualize_ai_music_usage.py

Purpose:
- Turn the CSV files produced by the downloader into clear charts.
- Explain, with comments, how pandas DataFrames flow into matplotlib plots.

What you'll learn here:
- How to load a CSV into a DataFrame (pd.read_csv).
- How to convert string dates into actual datetime objects (pd.to_datetime).
- How to sort by time and plot a time series.
- How to create simple bar charts from grouped counts.
- How to plot multiple series on one chart (Google Trends queries).
- Why we call plt.tight_layout() and how saving figures works.

Run after:
    python scripts/download_ai_music_data.py

Tip: matplotlib is the plotting library we use here.
- plt.figure() creates a new plotting canvas (width x height in inches).
- plt.plot() draws a line (we pass x and y from DataFrame columns).
- plt.savefig() writes the image file to disk; plt.close() frees memory.
"""

import datetime
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


DATA_DIR = Path("data")
SONICS_DIR = DATA_DIR / "sonics"
FIGURES_DIR = Path("figures")


def ensure_dirs():
    """
    Make sure the figures folder exists before saving charts.

    Path.mkdir(exist_ok=True) will create the folder if it doesn't exist and
    silently continue if it does — so it's safe to call every run.
    """
    FIGURES_DIR.mkdir(exist_ok=True)


def plot_youtube_monthly(csv_path: Path) -> Path:
    """
    Plot monthly counts of AI-music-related YouTube videos (if collected).

    DataFrame concepts:
    - pd.read_csv(path) -> load CSV into a DataFrame.
    - pd.to_datetime(df["month"]) -> convert strings like "2024-01-01" to datetime objects.
    - df.sort_values("month") -> ensure the time series is in chronological order.
    - We pass DataFrame columns directly to matplotlib to build the chart.

    Chart decisions:
    - marker="o" shows a dot for each monthly point (better readability).
    - linewidth=2 makes the line more visible.
    - grid(True, linestyle="--", alpha=0.5) adds a faint grid to aid reading values.
    """
    if not csv_path.exists():
        print(f"Missing YouTube monthly data: {csv_path}")
        return Path()

    # Load CSV -> DataFrame with columns ['month', 'youtube_ai_music_count']
    df = pd.read_csv(csv_path)

    # Convert 'month' strings to datetime so matplotlib treats them as dates on the x-axis
    df["month"] = pd.to_datetime(df["month"])

    # Sort rows by month ascending (earliest -> latest)
    df = df.sort_values("month")

    # Plot the time series
    plt.figure(figsize=(10, 5))
    plt.plot(df["month"], df["youtube_ai_music_count"], marker="o", linewidth=2, color="#1f77b4")
    plt.title("YouTube AI-Music Related Uploads (Heuristic) per Month")
    plt.xlabel("Month")
    plt.ylabel("Video count (sum of queries)")
    plt.grid(True, linestyle="--", alpha=0.5)

    # tight_layout() reduces extra whitespace and prevents label cutoff
    out = FIGURES_DIR / "youtube_ai_music_usage.png"
    plt.tight_layout()
    plt.savefig(out)
    plt.close()
    print(f"Saved: {out}")
    return out


def plot_deezer_points(csv_path: Path) -> Path:
    """
    Plot the Deezer daily AI-upload points (press-reported figures).

    DataFrame concepts:
    - pd.read_csv(path)
    - pd.to_datetime(df["date"])
    - df.sort_values("date")
    - iterating through rows (df.iterrows()) to annotate specific values

    Annotation explains exact values next to each point so viewers
    can read the chart without hovering.
    """
    if not csv_path.exists():
        print(f"Missing Deezer points: {csv_path}")
        return Path()

    df = pd.read_csv(csv_path)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    plt.figure(figsize=(8, 4))
    plt.plot(df["date"], df["daily_ai_uploads"], marker="o", linestyle="-", color="#ff7f0e")

    # Annotate each point with its value
    for _, row in df.iterrows():
        plt.annotate(f"{row['daily_ai_uploads']}", (row["date"], row["daily_ai_uploads"]),
                     textcoords="offset points", xytext=(0, 8), ha="center", fontsize=9)

    plt.title("Deezer Daily Fully AI-Generated Track Uploads (Reported Points)")
    plt.xlabel("Date")
    plt.ylabel("Daily uploads (count)")
    plt.grid(True, linestyle="--", alpha=0.5)
    out = FIGURES_DIR / "deezer_ai_daily_uploads.png"
    plt.tight_layout()
    plt.savefig(out)
    plt.close()
    print(f"Saved: {out}")
    return out


def plot_sonics_bars(by_source_csv: Path, by_label_csv: Path) -> Path:
    """
    Plot simple bar charts from SONICS aggregates.

    DataFrame concepts:
    - df = pd.read_csv(path) -> DataFrame with columns like ['source', 'count'].
    - axes[0].bar(x_values, y_values) -> bar chart of counts per category.

    Why two subplots?
    - We visualize "by source" (Suno/Udio) and "by label" side by side to compare.
    """
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    plotted = False

    # Left chart: counts by source (Suno/Udio)
    if by_source_csv.exists():
        df_src = pd.read_csv(by_source_csv)
        axes[0].bar(df_src["source"], df_src["count"], color="#2ca02c")
        axes[0].set_title("SONICS: Fake Songs by Source")
        axes[0].set_xlabel("Source")
        axes[0].set_ylabel("Count")
        plotted = True
    else:
        # When a file is missing, we turn this subplot into a simple message
        axes[0].text(0.5, 0.5, "Missing counts_by_source", ha="center", va="center")
        axes[0].axis("off")

    # Right chart: counts by label (full/half/mostly fake)
    if by_label_csv.exists():
        df_lbl = pd.read_csv(by_label_csv)
        axes[1].bar(df_lbl["label"], df_lbl["count"], color="#d62728")
        axes[1].set_title("SONICS: Fake Songs by Label")
        axes[1].set_xlabel("Label")
        axes[1].set_ylabel("Count")
        axes[1].tick_params(axis='x', rotation=20)  # rotate x labels so they don't overlap
        plotted = True
    else:
        axes[1].text(0.5, 0.5, "Missing counts_by_label", ha="center", va="center")
        axes[1].axis("off")

    out = FIGURES_DIR / "sonics_aggregates.png"
    if plotted:
        plt.tight_layout()
        plt.savefig(out)
        print(f"Saved: {out}")
    plt.close()
    return out if plotted else Path()


def plot_google_trends(csv_path: Path) -> Path:
    """
    Plot Google Trends monthly interest for AI-music related queries.
    Multiple series on one chart.

    DataFrame concepts:
    - df.columns contains both 'month' and one column per query (e.g., 'Suno', 'Udio').
    - We loop through each query column and plot it as a separate line.

    Design note:
    - Plotting all series together lets you compare relative interest over time.
    """
    if not csv_path.exists():
        print(f"Missing Google Trends data: {csv_path}")
        return Path()

    df = pd.read_csv(csv_path)
    if "month" not in df.columns:
        print("Google Trends data malformed: no 'month' column.")
        return Path()

    # Ensure 'month' is a datetime so matplotlib formats the axis nicely
    df["month"] = pd.to_datetime(df["month"])
    df = df.sort_values("month")

    # Determine query columns (all non-month numeric columns)
    query_cols = [c for c in df.columns if c != "month"]
    if not query_cols:
        print("Google Trends data malformed: no query columns found.")
        return Path()

    plt.figure(figsize=(10, 5))
    for c in query_cols:
        plt.plot(df["month"], df[c], label=c, linewidth=2)
    plt.title("Google Trends: Interest Over Time for AI-Music Queries")
    plt.xlabel("Month")
    plt.ylabel("Interest (0-100)")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    out = FIGURES_DIR / "google_trends_ai_music.png"
    plt.tight_layout()
    plt.savefig(out)
    plt.close()
    print(f"Saved: {out}")
    return out


def main():
    """
    Drive the visualization pipeline:
      - If YouTube monthly data exists, plot it.
      - Plot Deezer reported points.
      - Plot SONICS aggregates (bars).
      - Plot Google Trends multi-series.

    After running, check the 'figures' folder for:
      - youtube_ai_music_usage.png (if data exists)
      - deezer_ai_daily_uploads.png
      - sonics_aggregates.png
      - google_trends_ai_music.png
    """
    ensure_dirs()
    # YouTube plot (optional, only if data exists)
    plot_youtube_monthly(DATA_DIR / "youtube_ai_music_monthly.csv")
    # Deezer timeline (press-reported points)
    plot_deezer_points(DATA_DIR / "deezer_ai_daily_uploads.csv")
    # SONICS aggregates
    plot_sonics_bars(SONICS_DIR / "fake_counts_by_source.csv",
                     SONICS_DIR / "fake_counts_by_label.csv")
    # Google Trends (no API key required)
    plot_google_trends(DATA_DIR / "google_trends_ai_music.csv")
    print("Done.")


if __name__ == "__main__":
    main()
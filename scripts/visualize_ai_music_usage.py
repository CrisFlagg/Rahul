import datetime
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


DATA_DIR = Path("data")
SONICS_DIR = DATA_DIR / "sonics"
FIGURES_DIR = Path("figures")


def ensure_dirs():
    FIGURES_DIR.mkdir(exist_ok=True)


def plot_youtube_monthly(csv_path: Path) -> Path:
    if not csv_path.exists():
        print(f"Missing YouTube monthly data: {csv_path}")
        return Path()

    df = pd.read_csv(csv_path)
    df["month"] = pd.to_datetime(df["month"])
    df = df.sort_values("month")

    plt.figure(figsize=(10, 5))
    plt.plot(df["month"], df["youtube_ai_music_count"], marker="o", linewidth=2, color="#1f77b4")
    plt.title("YouTube AI-Music Related Uploads (Heuristic) per Month")
    plt.xlabel("Month")
    plt.ylabel("Video count (sum of queries)")
    plt.grid(True, linestyle="--", alpha=0.5)
    out = FIGURES_DIR / "youtube_ai_music_usage.png"
    plt.tight_layout()
    plt.savefig(out)
    plt.close()
    print(f"Saved: {out}")
    return out


def plot_deezer_points(csv_path: Path) -> Path:
    if not csv_path.exists():
        print(f"Missing Deezer points: {csv_path}")
        return Path()

    df = pd.read_csv(csv_path)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    plt.figure(figsize=(8, 4))
    plt.plot(df["date"], df["daily_ai_uploads"], marker="o", linestyle="-", color="#ff7f0e")
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
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    plotted = False

    if by_source_csv.exists():
        df_src = pd.read_csv(by_source_csv)
        axes[0].bar(df_src["source"], df_src["count"], color="#2ca02c")
        axes[0].set_title("SONICS: Fake Songs by Source")
        axes[0].set_xlabel("Source")
        axes[0].set_ylabel("Count")
        plotted = True
    else:
        axes[0].text(0.5, 0.5, "Missing counts_by_source", ha="center", va="center")
        axes[0].axis("off")

    if by_label_csv.exists():
        df_lbl = pd.read_csv(by_label_csv)
        axes[1].bar(df_lbl["label"], df_lbl["count"], color="#d62728")
        axes[1].set_title("SONICS: Fake Songs by Label")
        axes[1].set_xlabel("Label")
        axes[1].set_ylabel("Count")
        axes[1].tick_params(axis='x', rotation=20)
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


def main():
    ensure_dirs()
    yt_out = plot_youtube_monthly(DATA_DIR / "youtube_ai_music_monthly.csv")
    deezer_out = plot_deezer_points(DATA_DIR / "deezer_ai_daily_uploads.csv")
    sonics_out = plot_sonics_bars(SONICS_DIR / "fake_counts_by_source.csv",
                                  SONICS_DIR / "fake_counts_by_label.csv")
    print("Done.")


if __name__ == "__main__":
    main()
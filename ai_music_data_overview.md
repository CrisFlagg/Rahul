# AI-Generated Music: Platform Use Signals and Research Datasets (2025 Overview)

This file summarizes two things:
1) Data about AI-generated music currently in use on major platforms (signals and adoption).
2) Datasets that let you analyze AI music and usage patterns.

— Informational, not legal advice. Sources are linked; platform stats are typically press-reported or policy notes rather than open datasets.

## 1) AI music currently in use (platform signals and adoption)

- Deezer
  - 28% of daily track deliveries are fully AI-generated (~30,000/day, Sept 2025). Up to 70% of plays for those tracks detected as fraudulent; ~0.5% of total streams are AI-generated, according to Deezer. Deezer tags 100% AI-generated content and excludes it from recommendations/editorial playlists.
  - Source: Music Business Worldwide coverage
    - https://www.musicbusinessworldwide.com/nearly-a-third-of-all-tracks-uploaded-to-deezer-are-now-fully-ai-generated-says-platform/

- Spotify
  - Publicly reported crackdowns on “spammy” uploads and artificial streaming; notable 2023 takedown involving Boomy uploads. Open, per-track AI labels are not publicly exposed via an official dataset.
  - Indicative press:
    - https://www.musicbusinessworldwide.com/spotify-has-deleted-75m-spammy-tracks-as-it-unveils-new-ai-music-policies/

- YouTube
  - Requires creators to disclose realistic synthetic content (including synthetic voices); expanding AI-content labels and moving toward provenance (C2PA) metadata. Not an open dataset, but disclosure signals exist and may be accessible via the Data API.
  - Policy: https://blog.youtube/news-and-events/disclosing-ai-generated-content/

- TikTok and Luminate
  - Impact reports show TikTok’s strong role in discovery and streaming saves via “Add to Music App.” No open dataset specifying the AI-generated share of music uploads/engagement.
  - Report: https://newsroom.tiktok.com/en-us/tiktok-and-luminate-release-latest-music-impact-report

- Creator adoption (survey-based)
  - GEMA/SACEM: 35% of surveyed members used AI in their work in 2024; 51% among under-35s. Useful for creator-side adoption metrics.
  - Report PDF: https://www.gema.de/documents/d/guest/gema-sacem-goldmedia-ai-and-music-pdf

Note: There is no public, cross-platform dataset that quantifies AI-generated track share on Spotify/YouTube/TikTok at scale. Most platform telemetry is reported via press, policy notes, or paywalled analytics (Chartmetric, Luminate).

## 2) Datasets for analyzing AI music

- SONICS: Synthetic Or Not — Identifying Counterfeit Songs
  - Focus: End-to-end detection of synthetic songs (vocals + backing), primarily from Suno and Udio; ~97k songs total with ~49k synthetic.
  - Fields: title, duration, source (Suno/Udio), generation algorithm, genre/mood/topic, lyrics features, label (“full/half/mostly fake”), train/val/test splits. Real songs are referenced via YouTube IDs (download separately).
  - Access:
    - Paper: https://arxiv.org/abs/2408.14080
    - Hugging Face dataset: https://huggingface.co/datasets/awsaf49/sonics
    - Kaggle dataset: https://www.kaggle.com/datasets/awsaf49/sonics-dataset
    - Code/models: https://github.com/awsaf49/sonics

- AIMS Prompts (KTH): Text-conditioned AI music usage on Suno/Udio
  - Focus: How users use AI-music platforms (prompts, tags, lyrics, replaced artist tags), 101,953 songs (May–Oct 2024), plus interactive visualizations.
  - Access:
    - Paper (HTML): https://arxiv.org/html/2509.11824v1
    - Code + URL lists: https://github.com/mister-magpie/aims_prompts
    - Interactive viz: https://mister-magpie.github.io/aims_prompts/
  - Note: Authors share URL lists rather than raw metadata/audio due to IP concerns.

- SunoCaps: AI-generated tracks with emotion and prompt-alignment annotations
  - Focus: 256 Suno-generated songs created from MusicCaps prompts; annotated for emotion and prompt alignment (useful for evaluation of alignment and affect).
  - Access:
    - Kaggle: https://www.kaggle.com/datasets/miguelcivit/sunocaps
    - Paper (Data in Brief): https://doi.org/10.1016/j.dib.2024.110743

- Support datasets often used in AI music analysis (not AI-specific usage)
  - MusicCaps: human-written captions for 5k+ audio clips (used to condition generation/evaluation)
    - https://www.kaggle.com/datasets/googleai/musiccaps
  - Spotify track datasets on Kaggle: audio features, popularity metrics for large catalogs (not AI-tagged, but useful for trend analysis/feature modeling)
    - Example: https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset

## How to study “usage” on specific platforms with data today

- Combine SONICS and AIMS Prompts to analyze:
  - Growth patterns by source (Suno vs Udio), metadata distributions (genre/mood/topic), prompt/tag practices, and variations over time.

- Sample platform-level signals
  - YouTube: Use the Data API to collect videos with AI-disclosure labels and filter to music category (metadata only; may be incomplete).
  - Spotify: Identify known AI “artists” and catalogs via API (e.g., Aventhis, Blow Records) to estimate reach; not comprehensive but useful signals.
  - Deezer: Track public statements/press and, if possible, establish a research partnership to access aggregated AI-tag stats.

## Next steps (optional)

- Compile a unified CSV/Parquet combining:
  - SONICS metadata
  - AIMS Prompts URL list with normalized fields (prompt/lyrics/tags)
  - SunoCaps annotations for alignment/emotion
- Enrich with platform metrics via public APIs (YouTube/Spotify) where allowed, and document lawful access/TOS compliance.
- Produce notebooks for usage analysis (prompt trends, genre/mood distributions, suspected impersonation tags, time series).

— Last updated: November 2025.
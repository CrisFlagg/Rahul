# Tutorial: Install Python, set up a virtual environment, and use Jupyter Notebooks on macOS

This guide is for first-time users. It will walk you through:
- Installing Homebrew (macOS package manager)
- Installing Python 3
- Creating and using a virtual environment
- Installing Jupyter (Notebook or Lab)
- Opening and running the tutorial notebooks in this repo
- Optional: setting your YouTube API key for the YouTube notebook
- Troubleshooting and alternatives

Prerequisites: A Mac running macOS 11+ (Big Sur or newer). You’ll use the Terminal app (found in Applications > Utilities > Terminal).


## 1) Install Homebrew (recommended)

Homebrew makes it easy to install developer tools on macOS.

- Open Terminal and run:

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

- When it finishes, follow any on-screen instructions to add Homebrew to your PATH. On Apple silicon (M1/M2/M3), you’ll likely need to add this line to your shell profile (zsh is default on macOS):

```
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

- Verify Homebrew:

```
brew --version
```

If you see a version number, Homebrew is installed.


## 2) Install Python 3 with Homebrew

- In Terminal:

```
brew update
brew install python
```

- Verify Python:

```
python3 --version
which python3
```

You should see a Python 3.x version and a path under `/opt/homebrew/bin/python3` (Apple silicon) or `/usr/local/bin/python3` (Intel).


## 3) Create a project folder and a virtual environment

A virtual environment keeps your project’s Python packages separate from your system Python.

- In Terminal, go to your project (the folder with this repo):

```
cd /path/to/your/project
```

- Create a virtual environment named `.venv`:

```
python3 -m venv .venv
```

This creates a `.venv` folder containing an isolated Python + pip.

- Activate the virtual environment:

```
source .venv/bin/activate
```

You should see your shell prompt change, for example to:

```
(.venv) yourname@Mac ~ %
```

- Upgrade pip (good practice):

```
pip install --upgrade pip
```

Note: When the venv is active, `python` and `pip` refer to the venv versions. To exit the venv later, run `deactivate`.


## 4) Install Jupyter and required libraries

We’ll install Jupyter Lab (modern UI) and the libraries used by these notebooks.

- With your venv activated:

```
pip install jupyterlab notebook pandas matplotlib requests huggingface_hub pytrends
```

This installs:
- jupyterlab and notebook: Jupyter interfaces
- pandas: DataFrames (tabular data)
- matplotlib: plotting
- requests: web requests
- huggingface_hub: dataset download
- pytrends: Google Trends access


## 5) Launch Jupyter Lab and open the tutorials

- Start Jupyter Lab from your project root:

```
jupyter lab
```

This opens Jupyter Lab in your default browser. If it doesn’t, Terminal will show a URL (something like http://localhost:8888/lab); copy-paste it into your browser.

- In the Jupyter file browser (left pane), navigate to the `notebooks/` folder:
  - `ai_music_tutorial.ipynb` — no-API tutorial (SONICS, Google Trends, Deezer points)
  - `youtube_ai_music_tutorial.ipynb` — optional YouTube API tutorial

- Click a notebook to open it, then run cells top-to-bottom:
  - Use the “Run” ▶ button or press Shift+Enter to run the current cell.
  - If the notebook asks for permissions or “Trust this notebook”, confirm.


## 6) Optional: Using Jupyter Notebook (classic UI)

If you prefer the classic interface:

```
jupyter notebook
```

Then open the notebooks under the `notebooks/` folder and run them the same way.


## 7) Optional: Set your YouTube API key (for the YouTube tutorial)

The `youtube_ai_music_tutorial.ipynb` notebook needs a YouTube Data API key. You can set it either before launching Jupyter or inside the notebook.

- In Terminal (zsh on macOS):

```
export YOUTUBE_API_KEY=your_key_here
```

- Then launch Jupyter Lab:

```
jupyter lab
```

- Alternatively, when the notebook prompts for the API key, paste it there.

Tip: To make the key persistent, add the `export` line to your `~/.zshrc`:
```
echo 'export YOUTUBE_API_KEY=your_key_here' >> ~/.zshrc
source ~/.zshrc
```


## 8) Running scripts without notebooks (optional)

You can also run the Python scripts in `scripts/` from Terminal.

- With the virtual environment activated:

```
python scripts/download_ai_music_data.py
python scripts/visualize_ai_music_usage.py
```

Outputs:
- Data CSVs in `data/` and `data/sonics/`
- Figures in `figures/`

Note: The download script will skip YouTube unless `YOUTUBE_API_KEY` is set. It always collects Google Trends (no API key) and saves Deezer timeline points.


## 9) Troubleshooting

- “command not found: brew”
  - Homebrew didn’t install correctly or isn’t in PATH. Re-run the install command and the PATH setup:
    ```
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
    eval "$(/opt/homebrew/bin/brew shellenv)"
    ```

- “command not found: python3”
  - Run `brew install python` and verify `python3 --version`.

- “venv activation didn’t change my prompt”
  - Make sure you’re in the project folder, then run:
    ```
    source .venv/bin/activate
    ```
  - If it still doesn’t show, try:
    ```
    echo $PATH
    which python
    which pip
    ```
    Verify they point inside `.venv/bin/`.

- Jupyter doesn’t open a browser
  - Terminal prints a local URL like http://localhost:8888/lab. Copy-paste it into Safari/Chrome.

- “Permission denied” or “Xcode command line tools missing”
  - Run:
    ```
    xcode-select --install
    ```
    This installs essential build tools Apple requires for some packages.

- “pip installs to the wrong location”
  - Ensure the venv is active (prompt shows `(.venv)`).
  - Use `which pip` to confirm it points to `.venv/bin/pip`.

- Notebook says “Untrusted” or won’t run cells
  - Use the “Trust” button in Jupyter Labs or open the Command Palette (⇧⌘P) and search “Trust Notebook”.

- Google Trends returns empty data
  - Try running later; Trends can throttle. Ensure you have internet and correct timeframe.


## 10) Alternatives (optional)

- Anaconda (conda)
  - Anaconda is an all-in-one Python distribution popular for data science.
  - Download from https://www.anaconda.com and install.
  - Create an environment:
    ```
    conda create -n aimusic python=3.11
    conda activate aimusic
    conda install jupyterlab pandas matplotlib requests
    pip install huggingface_hub pytrends
    jupyter lab
    ```

- Visual Studio Code
  - VS Code can open notebooks directly with the Python extension.
  - Install VS Code, the Python extension, and ensure your virtual environment is selected.


## 11) Quick recap (what you’ll do most often)

- Activate your virtual environment:
  ```
  cd /path/to/your/project
  source .venv/bin/activate
  ```

- Start Jupyter Lab:
  ```
  jupyter lab
  ```

- Open `notebooks/ai_music_tutorial.ipynb`, run cells top-to-bottom.

- For YouTube tutorial:
  ```
  export YOUTUBE_API_KEY=your_key_here
  jupyter lab
  ```
  Open `notebooks/youtube_ai_music_tutorial.ipynb` and run cells.

You’re set. If you’d like a short video walkthrough tailored to your setup, I can add one next.
# Tutorial: Install Python, set up a virtual environment, and use Jupyter Notebooks on macOS

This guide is written for first-time users. It explains not just what to do, but why. By the end you’ll be able to:
- Install Python 3 on macOS
- Create and use a virtual environment (an isolated Python workspace)
- Install Jupyter (Lab and Notebook)
- Open and run the tutorial notebooks in this repo
- Optionally configure a YouTube API key for the YouTube tutorial
- Troubleshoot the most common issues

You will use the Terminal app (Applications > Utilities > Terminal). Terminal is where we type commands for the computer to run.


## 0) Before you start: keyboard, shell, and paths

- macOS uses the zsh shell by default (it’s fine if you don’t know what that means yet).
- View which shell you’re using:
  ```
  echo $SHELL
  ```
  Typical output: `/bin/zsh`. That’s zsh.

- “PATH” is a list of folders your shell searches for programs (like `python3` or `jupyter`).
  ```
  echo $PATH
  ```
  We’ll add Homebrew to PATH so `brew`, `python3`, and `jupyter` are easy to run.

- To see your current folder (directory):
  ```
  pwd
  ```
  To list files in the folder:
  ```
  ls
  ```


## 1) Install Homebrew (recommended)

Homebrew is a package manager for macOS. It makes installing developer tools (like Python) simple.

- Open Terminal and run:
  ```
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  ```

- When it finishes, add Homebrew to your PATH (Apple silicon Macs use `/opt/homebrew`):
  ```
  echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
  eval "$(/opt/homebrew/bin/brew shellenv)"
  ```
  If you’re on Intel (older Macs), Homebrew usually lives at `/usr/local`. The installer prints instructions—follow those.

- Verify Homebrew:
  ```
  brew --version
  ```
  If you see a version number, Homebrew is installed.


### Alternative: Install Python without Homebrew

If you prefer not to use Homebrew, you can install Python from python.org:

- Download the latest macOS installer: https://www.python.org/downloads/macos/
- Run the installer and follow prompts
- Verify:
  ```
  python3 --version
  which python3
  ```
  The path may be under `/Library/Frameworks/...` or `/usr/local/bin/python3`. Both are fine.

We’ll continue with the Homebrew route below, as it’s commonly used.


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
  You should see `Python 3.x.y` and a path like `/opt/homebrew/bin/python3` (Apple silicon) or `/usr/local/bin/python3` (Intel).


## 3) Create a project folder and a virtual environment

A virtual environment (venv) is an isolated Python workspace. It keeps your project’s packages separate, avoiding conflicts.

- In Terminal, go to your project (the folder with this repo). Example:
  ```
  cd /path/to/your/project
  ```
  Tip: In Finder, right-click your project folder > “Copy (as) Pathname”, then paste into Terminal after `cd `.

- Create a virtual environment named `.venv`:
  ```
  python3 -m venv .venv
  ```
  This creates a folder `.venv` containing an isolated Python and pip.

- Activate the virtual environment:
  ```
  source .venv/bin/activate
  ```
  Your prompt should change to show `(.venv)` like:
  ```
  (.venv) yourname@Mac project %
  ```

- Upgrade pip (recommended):
  ```
  pip install --upgrade pip
  ```

- Deactivate later (when you’re done):
  ```
  deactivate
  ```

Why venv? Different projects often need different versions of packages. venv keeps each project clean and self-contained.


### Optional: Make your venv a selectable Jupyter kernel

This helps ensure notebooks run with the correct Python:

- Install ipykernel in your venv:
  ```
  pip install ipykernel
  ```

- Register the venv as a Jupyter kernel:
  ```
  python -m ipykernel install --user --name aimusic-venv --display-name "Python (aimusic)"
  ```
  In Jupyter, you can select the kernel “Python (aimusic)” for notebooks in this repo (Kernel > Change Kernel).


## 4) Install Jupyter and required libraries

We’ll install Jupyter Lab (modern UI) and the libraries used by these notebooks.

- With your venv activated:
  ```
  pip install jupyterlab notebook pandas matplotlib requests huggingface_hub pytrends
  ```

What these do:
- jupyterlab + notebook: Notebook interfaces
- pandas: Tabular data (DataFrames)
- matplotlib: Plotting
- requests: HTTP requests
- huggingface_hub: Download datasets/models from Hugging Face
- pytrends: Google Trends interface (no API key required)


## 5) Launch Jupyter Lab and open the tutorials

- Start Jupyter Lab from your project root:
  ```
  jupyter lab
  ```
  It opens Jupyter in your default browser. If it doesn’t, Terminal shows a URL (e.g., http://localhost:8888/lab). Copy-paste it into Safari or Chrome.

- In the Jupyter file browser (left pane), navigate to the `notebooks/` folder:
  - `ai_music_tutorial.ipynb` — no-API tutorial (SONICS, Google Trends, Deezer points)
  - `youtube_ai_music_tutorial.ipynb` — optional YouTube API tutorial

- Click a notebook to open it. Run cells from top to bottom:
  - Run button ▶ or Shift+Enter runs the selected cell
  - Kernel busy indicator (top-right) shows when code is running
  - To stop a long-running cell: Kernel > Interrupt
  - To fully restart: Kernel > Restart Kernel

- “Trust” prompt:
  - If Jupyter asks you to trust the notebook, click Trust so it can run code and display outputs.


### Optional: Use Jupyter Notebook (classic UI)

If you prefer the classic interface:
```
jupyter notebook
```
Then open the notebooks under `notebooks/` and run them the same way.


## 6) Optional: Set your YouTube API key (for the YouTube tutorial)

The YouTube tutorial uses the YouTube Data API v3 to count monthly uploads matching AI-music queries (heuristic). You can either set the key in your shell before launching Jupyter, or paste it when the notebook prompts you.

- Set the key in your shell (zsh):
  ```
  export YOUTUBE_API_KEY=your_key_here
  jupyter lab
  ```
- Or paste the key when the notebook prompts you.

To make it persistent across Terminal sessions:
```
echo 'export YOUTUBE_API_KEY=your_key_here' >> ~/.zshrc
source ~/.zshrc
```

### How to obtain a YouTube Data API key (step-by-step)

1) Sign in to Google Cloud Console
   - Go to https://console.cloud.google.com/ and sign in with your Google account.

2) Create a new project (or select an existing one)
   - Click the project dropdown at the top left and choose “New Project.”
   - Give it a name (e.g., “ai-music-tutorial”), then click Create.
   - Make sure the new project is selected (visible at the top bar).

3) Enable the YouTube Data API v3 for your project
   - In the left sidebar, go to “APIs & Services” > “Library.”
   - Search for “YouTube Data API v3.”
   - Click it, then click “Enable.”

4) Create API credentials (API key)
   - Go to “APIs & Services” > “Credentials.”
   - Click “Create Credentials” > “API key.”
   - A new API key string will appear. Copy it.

5) Restrict your API key (recommended for security)
   - In “Credentials,” click your new API key to edit it.
   - Under “Application restrictions,” choose:
     - “IP addresses” (best for scripts run from known networks), or
     - “HTTP referrers (web sites)” if you’ll call the API from a browser.
     - Leave “None” only for testing; do not commit an unrestricted key to Git.
   - Under “API restrictions,” choose “Restrict key,” then select “YouTube Data API v3.”
   - Click “Save.”

6) Add the key to your environment (do not commit to Git)
   - Temporarily for the current Terminal session:
     ```
     export YOUTUBE_API_KEY=your_key_here
     ```
   - Persistently for every Terminal session (zsh):
     ```
     echo 'export YOUTUBE_API_KEY=your_key_here' >> ~/.zshrc
     source ~/.zshrc
     ```
   - Alternatively, set it in your shell profile or use a local .env file (not committed).

7) Quotas, billing, and usage
   - Most basic API usage is free within default quotas.
   - You can view quota usage under “APIs & Services” > “Dashboard” or “Quotas.”
   - If you hit quotas, reduce the number of queries or pagination depth.
   - Official docs: https://developers.google.com/youtube/v3/getting-started

8) Regenerate or delete your key
   - If your key is exposed or you want to rotate it, go to “APIs & Services” > “Credentials,” select the key, and choose “Regenerate key” or “Delete.”
   - Update your environment variable with the new key.

Security tips:
- Treat API keys like passwords—do not post or commit them publicly.
- Use application and API restrictions to limit abuse.
- Rotate keys periodically and monitor usage.

Note: The main pipeline runs without YouTube (it will skip that part if the key isn’t set). The Google Trends + SONICS + Deezer steps work with no API keys.


## 7) Running the scripts directly (optional)

You can run the Python scripts in `scripts/` from Terminal.

- With the venv activated:
  ```
  python scripts/download_ai_music_data.py
  python scripts/visualize_ai_music_usage.py
  ```

Outputs:
- Data CSVs in `data/` and `data/sonics/`
- Figures in `figures/`

The download script:
- Always collects Google Trends (no API key) and saves Deezer points
- Skips YouTube unless `YOUTUBE_API_KEY` is set


## 8) Saving and sharing your environment (requirements.txt)

To record exactly which packages and versions you used:
```
pip freeze > requirements.txt
```
To recreate the same environment later (or on another machine):
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```


## 9) Troubleshooting and common pitfalls

- “command not found: brew”
  - Homebrew isn’t installed or PATH isn’t set. Re-run the installer and PATH setup:
    ```
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
    eval "$(/opt/homebrew/bin/brew shellenv)"
    ```

- “command not found: python3”
  - Install Python (`brew install python`) or use python.org installer. Verify:
    ```
    python3 --version
    which python3
    ```

- venv activation didn’t change my prompt
  - Ensure you’re in the project folder, then:
    ```
    source .venv/bin/activate
    ```
  - Check which Python and pip you’re using:
    ```
    which python
    which pip
    ```
    They should point inside `.venv/bin/`.

- Jupyter doesn’t open a browser
  - Terminal prints a local URL (http://localhost:8888/lab). Copy-paste into Safari/Chrome.

- “Permission denied” or “Xcode command line tools missing”
  - Install Apple’s command line tools:
    ```
    xcode-select --install
    ```

- pip installs to the wrong location
  - Activate venv first (`source .venv/bin/activate`)
  - Confirm `which pip` points to `.venv/bin/pip`

- Notebook says “Untrusted” or won’t run
  - Use the “Trust” button in Jupyter Lab, or Command Palette (⇧⌘P) > “Trust Notebook”

- Google Trends returned empty data
  - Trends can throttle or temporarily return no data. Try again later. Ensure timeframe is valid and you have a network connection.

- Wrong kernel in Jupyter
  - If you registered your venv kernel (`ipykernel install`), select it via Kernel > Change Kernel (“Python (aimusic)” or similar).
  - Otherwise, make sure your venv is active when launching `jupyter lab` so it uses the right Python.


## 10) Alternatives (optional)

- Anaconda (conda)
  - Anaconda is a popular all-in-one data science distribution.
  - Install from https://www.anaconda.com
  - Create and use an environment:
    ```
    conda create -n aimusic python=3.11
    conda activate aimusic
    conda install jupyterlab pandas matplotlib requests
    pip install huggingface_hub pytrends
    jupyter lab
    ```

- Visual Studio Code
  - VS Code can open notebooks directly with the Python extension.
  - Install VS Code, the Python extension, then:
    - Open your project folder
    - Select the `.venv` interpreter in the bottom right status bar
    - Open `notebooks/*.ipynb` and run cells


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

- For the YouTube tutorial:
  ```
  export YOUTUBE_API_KEY=your_key_here
  jupyter lab
  ```
  Open `notebooks/youtube_ai_music_tutorial.ipynb` and run cells.

You’re set. If you’d like a short video walkthrough tailored to your setup, I can add one next. For any step above, feel free to ask for clarification—I’m happy to expand further.
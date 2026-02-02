# TRP 1 Challenge — Step-by-Step Task List

Use this checklist to tackle the challenge in small, manageable steps. Check off each box as you complete it.

---

## Part 1: Environment Setup & API Configuration (~30 min)

### 1.1 Clone & install

- [ ] **1.1.1** Navigate to project root: `cd` into the repo (e.g. `trp1-ai-artist` or `ai-content`).
- [ ] **1.1.2** Install dependencies: run `uv sync` **or** `pip install -e .`.
- [ ] **1.1.3** Confirm no install errors; note any and add to your troubleshooting log.

### 1.2 Get at least one API key

- [ ] **1.2.1** Choose provider(s): **Google Gemini** and/or **AIMLAPI** (Kling not required).
- [ ] **1.2.2** **If using Google:** go to [Google AI Studio](https://aistudio.google.com/) → get API key.
- [ ] **1.2.3** **If using AIMLAPI:** go to [AIMLAPI.com](https://aimlapi.com/) → sign up → get API key.
- [ ] **1.2.4** Save key(s) somewhere safe (you will put them in `.env` next).

### 1.3 Configure environment

- [ ] **1.3.1** In project root, create a file named `.env` (if it doesn’t exist).
- [ ] **1.3.2** Add lines (replace with your real keys):
  ```env
  GEMINI_API_KEY=your_google_api_key_here
  AIMLAPI_KEY=your_aimlapi_key_here
  ```
- [ ] **1.3.3** Add `.env` to `.gitignore` if not already there — **do not commit keys**.

### 1.4 Verify installation

- [ ] **1.4.1** Run: `uv run ai-content --help` — CLI help should appear.
- [ ] **1.4.2** Run: `uv run ai-content list-providers` — list of providers should appear.
- [ ] **1.4.3** Run: `uv run ai-content list-presets` — list of presets should appear.
- [ ] **1.4.4** If any command fails, note the error and fix (path, env, package name) before continuing.

---

## Part 2: Codebase Exploration (~45 min)

### 2.1 Create exploration folder

- [ ] **2.1.1** Create folder: `exploration/` in project root.
- [ ] **2.1.2** You will put `ARCHITECTURE.md`, `PROVIDERS.md`, and `PRESETS.md` here.

### 2.2 Package structure (for ARCHITECTURE.md)

- [ ] **2.2.1** List contents of `src/ai_content/`: core, config, providers, presets, pipelines, cli, etc.
- [ ] **2.2.2** Note how providers are organized (e.g. `providers/google/`, `providers/aimlapi/`, `providers/kling/`).
- [ ] **2.2.3** Open `pipelines/` and note: base, music, video, full — what each does.
- [ ] **2.2.4** Write a short “Package structure” section in `exploration/ARCHITECTURE.md`.

### 2.3 Provider capabilities (for PROVIDERS.md)

- [ ] **2.3.1** **Music:** List providers (e.g. Lyria, MiniMax). Note: BPM, duration, vocals, lyrics support.
- [ ] **2.3.2** **Video:** List providers (e.g. Veo, Kling). Note which support image-to-video.
- [ ] **2.3.3** Identify which provider supports vocals/lyrics (e.g. MiniMax via AIMLAPI).
- [ ] **2.3.4** Summarize in `exploration/PROVIDERS.md` (table or bullets).

### 2.4 Preset system (for PRESETS.md)

- [ ] **2.4.1** Inspect `src/ai_content/presets/music.py` — list presets with BPM and mood.
- [ ] **2.4.2** Inspect `src/ai_content/presets/video.py` — list presets with aspect ratios.
- [ ] **2.4.3** Find how to add a new preset (e.g. register in preset module / registry).
- [ ] **2.4.4** Write `exploration/PRESETS.md` with the catalog and “how to add a preset”.

### 2.5 CLI commands

- [ ] **2.5.1** Run `uv run ai-content --help` and list all top-level commands.
- [ ] **2.5.2** Run `uv run ai-content music --help` — note options (style, prompt, provider, duration, bpm, lyrics, etc.).
- [ ] **2.5.3** Run `uv run ai-content video --help` — note options (style, prompt, provider, duration, aspect, etc.).
- [ ] **2.5.4** Optionally add a “CLI reference” subsection to `exploration/ARCHITECTURE.md` or a small `exploration/CLI.md`.

### 2.6 Finalize exploration docs

- [ ] **2.6.1** Ensure `exploration/ARCHITECTURE.md` describes structure and pipeline purpose.
- [ ] **2.6.2** Ensure `exploration/PROVIDERS.md` and `exploration/PRESETS.md` are complete and readable.

---

## Part 3: Content Generation (~60 min)

### 3.1 Instrumental music

- [ ] **3.1.1** Pick a preset (e.g. jazz): `uv run ai-content music --style jazz --provider lyria --duration 30`.
- [ ] **3.1.2** Note output path and filename; confirm the file exists and plays.
- [ ] **3.1.3** (Optional) Try another style or custom prompt: `uv run ai-content music --prompt "..." --provider lyria --duration 30`.
- [ ] **3.1.4** Save the exact command and prompt for SUBMISSION.md — this is **audio file #1**.

### 3.2 Second audio (different style or provider)

- [ ] **3.2.1** Generate a second track (different preset or provider): e.g. different `--style` or `--provider minimax` if you have AIMLAPI.
- [ ] **3.2.2** Confirm file is created — this is **audio file #2**.

### 3.3 Music with vocals (optional, if AIMLAPI)

- [ ] **3.3.1** Create a `.txt` lyrics file (e.g. `my_lyrics.txt`) with plain text lyrics.
- [ ] **3.3.2** Run: `uv run ai-content music --prompt "Your style prompt" --provider minimax --lyrics path/to/my_lyrics.txt`.
- [ ] **3.3.3** Note any errors; if it works, keep this as an extra artifact.

### 3.4 Video

- [ ] **3.4.1** Generate video: e.g. `uv run ai-content video --style nature --provider veo --duration 5`.
- [ ] **3.4.2** Note output path; confirm the video file exists and plays — this is **video file #1**.
- [ ] **3.4.3** Save command and prompt for SUBMISSION.md.

### 3.5 Bonus: music video (FFmpeg)

- [ ] **3.5.1** Install FFmpeg if needed; ensure it’s on PATH.
- [ ] **3.5.2** Pick one generated video and one generated audio.
- [ ] **3.5.3** Run:  
  `ffmpeg -i video.mp4 -i music.wav -c:v copy -c:a aac -shortest output.mp4`  
  (replace filenames with your actual paths.)
- [ ] **3.5.4** Confirm `output.mp4` plays correctly — this is your **combined music video**.

### 3.6 Generation log

- [ ] **3.6.1** List all commands you ran, prompts used, and which file each produced.
- [ ] **3.6.2** Note file sizes and durations; you’ll paste this into SUBMISSION.md later.

---

## Part 4: YouTube Upload & Submission (~45 min)

### 4.1 Upload to YouTube

- [ ] **4.1.1** Choose your best content (e.g. one music track and/or the music video).
- [ ] **4.1.2** Upload to YouTube (unlisted is fine).
- [ ] **4.1.3** Title format: `[TRP1] Your Name - Content Description`.
- [ ] **4.1.4** In description include: prompt, provider, preset, and any creative decisions.

### 4.2 Create SUBMISSION.md

Create `SUBMISSION.md` in project root with these sections:

- [ ] **4.2.1** **Environment setup** — Which APIs you configured; setup issues and how you resolved them.
- [ ] **4.2.2** **Codebase understanding** — Short architecture description/diagram; provider system; pipeline orchestration.
- [ ] **4.2.3** **Generation log** — Commands, prompts, results (screenshots, file sizes, durations).
- [ ] **4.2.4** **Challenges & solutions** — What failed at first; how you troubleshooted; workarounds.
- [ ] **4.2.5** **Insights & learnings** — Surprises, possible improvements, comparison to other AI tools.
- [ ] **4.2.6** **Links** — YouTube video link(s); GitHub repo with exploration artifacts.

### 4.3 Final checklist (from challenge)

- [ ] `.env` configured and **not** committed.
- [ ] `exploration/ARCHITECTURE.md` done.
- [ ] `exploration/PROVIDERS.md` done.
- [ ] `exploration/PRESETS.md` done.
- [ ] At least 2 generated audio files.
- [ ] At least 1 generated video file.
- [ ] `SUBMISSION.md` complete.
- [ ] YouTube link(s) in submission.
- [ ] GitHub repo link with all artifacts.

---

## Quick reference

| Part   | Time  | Main outcome |
|--------|-------|----------------|
| Part 1 | ~30 m | Working env, API keys, `uv run ai-content` works |
| Part 2 | ~45 m | `exploration/ARCHITECTURE.md`, `PROVIDERS.md`, `PRESETS.md` |
| Part 3 | ~60 m | ≥2 audio, ≥1 video, (optional) music video |
| Part 4 | ~45 m | YouTube upload, `SUBMISSION.md`, links |

**CLI reminder:** Use `uv run ai-content` (or `pip run ai-content` / global `ai-content` if installed that way). Replace `ai-content` with your actual CLI name if different in your repo.

Good luck. Work through the steps in order; if stuck, document the issue and try the next small step.

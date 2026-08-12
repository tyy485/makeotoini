# 🎵 makeotoini — UTAU OTO.ini Smart Generator

> Drag your audio folder in, generate oto.ini with one click. Supports auto-transcoding, silence detection, batch alias processing, multilingual voicebank, character.txt generation, breath file auto-identification, and preview confirmation.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux%20%7C%20Android-lightgrey)](https://github.com/tyy485/makeotoini)

---

## 📖 Table of Contents

- [✨ Features](#-features)
- [📦 Installation & Running](#-installation--running)
- [🚀 Usage Guide](#-usage-guide)
- [🛠️ Configuration Options](#️-configuration-options)
- [📁 Output Example](#-output-example)
- [📁 Project Structure](#-project-structure)
- [❓ FAQ](#-faq)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [💬 Credits](#-credits)

---

## ✨ Features

- 🎯 **One-click generation** — Scan .wav files, auto-estimate parameters, output standard oto.ini
- 🔄 **Auto-transcoding** — Convert MP3 / FLAC / M4A / OGG etc. to .wav automatically (requires FFmpeg), with retry mechanism
- 📦 **Zero dependencies** — Uses only Python standard library; no `pip install` needed
- 🧹 **Abnormal filename cleaning** — Remove invisible characters to avoid UTAU errors
- 🏷️ **Batch alias processing** — Add/remove prefixes/suffixes, delete character ranges – 6 modes available, supports removing all matches
- 🔇 **Silence detection** — Automatically locate offset to reduce breath-cut errors
- 🌬️ **Breath file auto-identification** — Automatically detects files named with `br`/`br_数字`/`呼`/`吸`/`breathe`/`breath`, assigns aliases with custom template (supports `x` placeholder for numbering)
- 🔧 **Romaji auto-fix** — Correct common labels like `short`/`long`/`vowel` to standard Romaji (supports Japanese Kana and Korean Hangul)
- 🌍 **Multilingual voicebank support** — Choose from 日本語 / 中文 / 한국어 / English
- 🌐 **Bilingual UI** — Interface supports Chinese/English toggle
- 📋 **character.txt generation** — Interactive generation of voicebank info file with name, version, website, icon (auto-scans directory images)
- 👁️ **Preview confirmation mode** — Preview oto.ini configuration before generation, confirm before writing to file
- 🛡️ **Smart error handling** — Common errors with solutions, auto-retry on conversion failure, auto-switch to UTF-8 on encoding error
- 🌍 **Cross-platform** — Works on Windows / macOS / Linux / Termux (Android)
- 🔤 **Encoding options** — Choose Shift-JIS / GB2312 / UTF-8 as needed

---

## 📦 Installation & Running

### 🪟 Windows Users

#### 1. Install Python (if not already)
- Visit [python.org/downloads](https://www.python.org/downloads/)
- Download the latest Python (click the yellow Download button)
- **During installation, make sure to check `Add Python to PATH`** (very important!)
- Click `Next` to complete installation

#### 2. Verify Python is installed
Open Command Prompt (`Win+R` → type `cmd` → Enter), then run:
```bash
python --version
```
If you see `Python 3.x.x`, it's installed correctly.

#### 3. Install FFmpeg (only needed for transcoding MP3/FLAC etc.)
> 💡 If all your audio files are `.wav`, **you can skip this step**

- Download the Windows version from [ffmpeg.org/download.html](https://ffmpeg.org/download.html)
- Extract to `C:\ffmpeg`
- Add `C:\ffmpeg\bin` to your system PATH:
  1. Right-click "This PC" → "Properties" → "Advanced system settings"
  2. Click "Environment Variables" → find `Path` under "System variables" → double-click
  3. Click "New" → enter `C:\ffmpeg\bin` → OK

#### 4. Download this tool
- Click the green `Code` button (top-right) → `Download ZIP`
- Extract to where you want (e.g., `D:\oto_voice\`)

#### 5. Run
Type `cmd` in the folder address bar and press Enter, then run:
```bash
python make_oto.py
```

#### 6. If you see `python is not recognized as an internal or external command`
Python was not added to PATH. **Reinstall Python and check `Add Python to PATH`**.

---

### 🍎 macOS Users

#### 1. Install Python (if not already)
```bash
# Using Homebrew (recommended)
brew install python

# Or download the installer from python.org
```

#### 2. Verify Python is installed
```bash
python3 --version
```
If you see `Python 3.x.x`, it's ready.

#### 3. Install FFmpeg (for transcoding)
```bash
brew install ffmpeg
```

#### 4. Clone this tool
```bash
git clone https://github.com/tyy485/makeotoini.git
cd makeotoini
```

#### 5. Run
```bash
python3 make_oto.py
```

> 💡 On macOS, always use `python3` because the system-built Python is Python 2 (deprecated).

---

### 🐧 Linux Users

#### 1. Install Python (if not already)
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3

# Fedora
sudo dnf install python3

# Arch
sudo pacman -S python
```

#### 2. Verify Python is installed
```bash
python3 --version
```

#### 3. Install FFmpeg (for transcoding)
```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# Fedora
sudo dnf install ffmpeg

# Arch
sudo pacman -S ffmpeg
```

#### 4. Clone this tool
```bash
git clone https://github.com/tyy485/makeotoini.git
cd makeotoini
```

#### 5. Run
```bash
python3 make_oto.py
```

#### 6. Optional: Make it a global command (run `makeotoini` from anywhere)
```bash
chmod +x make_oto.py
sudo ln -s $(pwd)/make_oto.py /usr/local/bin/makeotoini
makeotoini   # Now you can run it from any directory!
```

---

### 📱 Termux (Android) Users

> Run Python on your phone to generate oto.ini – great for when you don't have a computer.

#### 1. Install Termux
- Download Termux from F-Droid (**not** from Google Play – it's outdated)
- Open Termux

#### 2. Install Python and FFmpeg
```bash
pkg update
pkg install python ffmpeg
```

#### 3. Clone this tool
```bash
git clone https://github.com/tyy485/makeotoini.git
cd makeotoini
```

#### 4. Run
```bash
python make_oto.py
```

> 💡 Audio files on your phone are usually in `/sdcard/`. In Termux, you can access them via `~/storage/shared/`.

---

## 🚀 Usage Guide

### Quick Start

1. Place your audio files (.wav / .mp3 / .flac etc.) in a folder
2. Run `python make_oto.py` (or `python3` on macOS/Linux)
3. Follow the prompts to select UI language, voicebank language, encoding, processing mode, breath alias template, alias rules, character.txt generation, etc.
4. Preview the oto.ini configuration, confirm, and it will be generated
5. The generated `oto.ini` and `character.txt` (if enabled) will appear in the same folder

### 📋 Complete Interactive Flow Example

```
============================================================
🌐 请选择工具界面语言 / Select UI language
============================================================
  1. 中文
  2. English
============================================================
请输入语言序号 / Enter language number (1/2): 2
✅ Selected: English

============================================================
🎵 OTO.ini Smart Generator v4.0 (with Audio Conversion)
============================================================

Generator loading…
Generator loaded, loading encoding selector…
Loading your good mood…

Detecting your software…
💻 竟然是CMD，来吧，进我的生成器

============================================================
🌍 Select voicebank language
============================================================
  1. 日本語 (Japanese)
  2. 中文 (Chinese)
  3. 한국어 (Korean)
  4. English
============================================================
Enter language number (1/2/3/4): 1
✅ Japanese

============================================================
📝 Select your oto encoding
============================================================
  1. GB 2312
  2. Shift-JIS
============================================================
Enter encoding number: 2
✅ Shift-JIS encoding

============================================================
🧹 Abnormal filename handling mode
============================================================
  1. Ask one by one (for small batches)
  2. Auto clean all
  3. Skip all
============================================================
Select mode (1/2/3): 2
✅ Auto clean all

============================================================
📦 Converted file handling mode
============================================================
  1. Keep converted wav files permanently
  2. Temporary conversion, delete after generating oto
============================================================
Select mode (1/2): 2
✅ Temporary conversion mode

============================================================
🔄 Conversion mode
============================================================
  1. Force reconvert (overwrite existing wav)
  2. Reuse existing wav (faster)
============================================================
Select mode (1/2): 2
✅ Reuse existing wav

============================================================
📂 Scan mode
============================================================
  1. Recursive scan subfolders
  2. Scan current directory only
============================================================
Select mode (1/2): 1
✅ Recursive scan

============================================================
🎚️  Silence detection sensitivity
============================================================
  1. Low (0.02) - for loud recordings
  2. Medium (0.01) - for normal recordings [default]
  3. High (0.005) - for quiet recordings
  4. Manual input (0.001-0.1)
============================================================
Select sensitivity (1/2/3/4): 2
✅ Medium sensitivity (threshold: 0.01)

============================================================
🌬️  Breath alias template
============================================================
💡 Use x as placeholder for number, e.g.: breath_x → breath_1, breath_2...
   Examples: breath_x, br{x}, b{x}, breath, br, b
============================================================
Enter breath alias template (default: breath): breath_x
✅ Breath alias template: breath_x

============================================================
🏷️  Alias custom mode
============================================================
  1. No alias processing (use filename directly)
  2. Add prefix (e.g.: x_)
  3. Remove prefix (e.g.: remove x_)
  4. Remove suffix (e.g.: remove _x)
  5. Add suffix (e.g.: _x)
  6. Remove character range (e.g.: remove 1st-3rd chars)
============================================================
Select alias mode (1/2/3/4/5/6): 1
✅ No alias processing

============================================================
🔧 Romaji auto fix
============================================================
  1. Enable auto fix (replace short/long with correct romaji)
  2. Disable auto fix
============================================================
Select (1/2): 1✅ Enabled: Romaji auto fix

============================================================
📋 character.txt generation
============================================================
  1. Enable character.txt and icon support
  2. Disable (do not generate)
============================================================
Select (1/2): 1
✅ Enabled: Generate character info file

Enter singer name (name): Hatsune Miku
✅ Singer name: Hatsune Miku

Enter version (version, leave blank to skip): 1.0
✅ Version: 1.0

Enter website (web, leave blank to skip): https://example.com
✅ Website: https://example.com

============================================================
📷 Voicebank icon selection
============================================================
Place icon file in voicebank directory, or enter full path
Found 2 image files:
   1. icon.png
   2. avatar.jpg
Select number (1-2): 1
✅ Selected icon: icon.png

✅ FFmpeg ready, supports auto audio conversion

📁 Default directory: D:\oto_voice

📂 Scanning: D:\oto_voice
📊 Found 52 files
------------------------------------------------------------
🔍 Scanning: 52/52
✅ Scan complete: found 52 wav files

🔧 Processing 52 wav files
------------------------------------------------------------

[1/52] Processing: あ_i.wav
✅ Processed: あ_i.wav (alias: i, duration: 1200ms, silence: 120ms, offset: 120ms)

[2/52] Processing: br1.wav
   🌬️  Breath file: br1.wav -> alias: breath_1
✅ Processed: br1.wav (alias: breath_1, duration: 300ms, silence: 0ms, offset: 0ms)

[3/52] Processing: br2.wav
   🌬️  Breath file: br2.wav -> alias: breath_2
✅ Processed: br2.wav (alias: breath_2, duration: 280ms, silence: 0ms, offset: 0ms)

[4/52] Processing: か_ka.wav
✅ Processed: か_ka.wav (alias: ka, duration: 950ms, silence: 80ms, offset: 80ms)

... (similar for remaining files)

============================================================
📋 Preview oto.ini configuration
============================================================
📊 52 entries
------------------------------------------------------------
  1. あ_i.wav                      → i                    offset: 120 consonant:  80 cutoff: 400 pre: 100 overlap:  60
  2. br1.wav                       → breath_1             offset:   0 consonant:   0 cutoff: 300 pre:   0 overlap:   0
  3. br2.wav                       → breath_2             offset:   0 consonant:   0 cutoff: 280 pre:   0 overlap:   0
  4. か_ka.wav                      → ka                   offset:  80 consonant:  60 cutoff: 350 pre:  80 overlap:  40
  ... (more entries)
------------------------------------------------------------
Confirm to generate oto.ini? (Y/N): Y

✅ oto.ini generated: D:\oto_voice\oto.ini
📊 52 entries
🔤 Encoding: shift-jis

✅ character.txt generated: D:\oto_voice\character.txt

============================================================
✨ Generation complete!
📁 oto.ini location: D:\oto_voice\oto.ini
📋 character.txt location: D:\oto_voice\character.txt
💡 Place this file with audio files in the same directory for UTAU
============================================================
```

### Folder Structure Suggestion

```
your_voice_folder/
├── あ_i.wav
├── い_u.wav
├── か_ka.wav
├── br1.wav         ← Breath file (auto-detected)
├── br2.wav         ← Breath file (auto-detected)
├── icon.png        ← Voicebank icon (auto-scanned)
├── make_oto.py     ← Place the tool here
├── oto.ini         ← Generated automatically
└── character.txt   ← Generated automatically (if enabled)
```

---

## 🛠️ Configuration Options

| Option | Description |
|--------|-------------|
| **UI Language** | Chinese / English – display language of the tool interface |
| **Voicebank Language** | 日本語 / 中文 / 한국어 / English – script recognition for Romaji auto-fix |
| **Encoding** | Shift-JIS (UTAU default) / GB2312 / UTF-8 – choose as needed |
| **Abnormal filename handling** | Ask one by one / Auto clean / Skip all – useful for filenames with invisible characters |
| **Conversion mode** | Keep permanently / Temporary (delete after generation to save space) |
| **Alias mode** | 6 modes: none / add prefix / remove prefix (supports removing all matches) / add suffix / remove suffix (supports removing all matches) / delete character range |
| **Silence sensitivity** | Low / Medium / High – choose lower sensitivity for recordings with background noise |
| **Breath alias template** | Custom alias format for breath files, supports `x` placeholder for auto-numbering (e.g., `breath_x` → `breath_1`, `breath_2`...) |
| **Scan mode** | Recursive scan (subfolders included) / Current directory only |
| **Romaji auto-fix** | Automatically corrects labels like `short`/`long`/`vowel` to standard Romaji, supports Japanese Kana and Korean Hangul |
| **character.txt generation** | Interactive generation of voicebank info file with name, version, website, icon |
| **Preview confirmation** | Preview all configurations before generation, confirm before writing to file |

---

## 📁 Output Example

### oto.ini
```ini
[#VERSION]
VERSION=100

あ_i.wav=i,0,120,400,100,60
い_u.wav=u,0,110,380,90,50
か_ka.wav=ka,80,60,350,80,40
br1.wav=breath_1,0,0,300,0,0
br2.wav=breath_2,0,0,280,0,0
```

Parameter meanings (left to right):
- `Alias` – The name shown in UTAU
- `offset` – Milliseconds skipped from the beginning (silence)
- `consonant` – Consonant duration (breath: 0)
- `blank` – Blank section duration (breath: entire duration)
- `preutterance` – Pre-utterance time (breath: 0)
- `overlap` – Crossfade time (breath: 0)

### character.txt
```ini
name=Hatsune Miku
version=1.0
web=https://example.com
image=icon.png
```

---

## 📁 Project Structure

```
makeotoini/
├── make_oto.py      # Main program – run this
├── README.md
├── README_EN.md
└── LICENSE
```

---

## ❓ FAQ

**Q: It says FFmpeg not found?**  
A: If all your audio files are `.wav`, you **don't need FFmpeg at all** – just run the tool. If you need to convert MP3/FLAC etc., please install FFmpeg following the instructions above.

**Q: Can it handle Chinese filenames?**  
A: Yes, but we recommend using English/Japanese/Korean/Romaji naming instead – UTAU has limited support for Chinese, and there's a higher risk of garbled output.

**Q: Do I need to manually adjust the generated parameters?**  
A: The tool generates "workable" parameters – they'll produce sound immediately. For perfect quality, tuners can fine-tune them later.

**Q: Does it support batch processing of subfolders?**  
A: Yes! Select "Recursive scan" when prompted.

**Q: Can this tool be used with UTAU-Synth?**  
A: Yes, the oto.ini format is universal.

**Q: Why does my oto.ini show garbled text when I open it?**  
A: You chose the wrong encoding. UTAU defaults to Shift-JIS – open the file with an editor that supports that encoding (e.g. Notepad++).

**Q: What does Romaji auto-fix do?**  
A: When filenames contain non-standard labels like `short`, `long`, `vowel`, the tool automatically corrects them to standard forms like `q`, `-`, etc., so UTAU can recognise them correctly. Currently supports Japanese Kana (Hiragana/Katakana) and Korean Hangul.

**Q: What's the difference between UI language and voicebank language?**  
A: UI language controls the display language of the tool itself (Chinese or English). Voicebank language controls which script the Romaji auto-fix feature recognizes (Japanese Kana or Korean Hangul).

**Q: How does the breath alias template work?**  
A: Enter a template containing `x`, and the tool will auto-number. For example, `breath_x` → `breath_1`, `breath_2`... If you don't include `x`, all breaths will use the same alias – the tool will warn you but let you proceed.

**Q: What is the preview mode for?**  
A: Before generating oto.ini, the tool displays a table of all configurations for you to review. Confirm before writing to file, avoiding mistakes that would require manual fixing later.

**Q: What does "remove all matching" mean for prefix/suffix deletion?**  
A: When removing prefixes/suffixes, the tool asks whether to remove all matches. Choose Y to loop until no match remains (e.g., `test_test_test` with `test_` becomes empty), choose N to remove only the first match.

**Q: What is character.txt for?**  
A: It's the voicebank info file for UTAU, displaying singer name, version, website, and icon. Some UTAU front-end tools (like UTAU-Synth's voicebank list) read this file.

**Q: Will conversion retry on failure?**  
A: Yes. The tool automatically retries up to 2 times, and gives clear feedback if it still fails.

**Q: What happens on encoding errors?**  
A: The tool automatically switches to UTF-8 and regenerates, no manual intervention needed.

---

## 🤝 Contributing

Issues, PRs, and forks are all welcome!

If you have good ideas, feel free to reach out.

---

## 📄 License

MIT © [tyy485](https://github.com/tyy485)

**Fully open source – use it freely, modify it, sell it, do whatever you like.**  
If you find it useful, a ⭐ Star would mean a lot!

---

## 💬 Credits

- The UTAU community – all tuners and voicebank creators
- Everyone who suggested features and helped with testing

---

**Happy Tuning! 🎶**
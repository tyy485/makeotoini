# 🎵 makeotoini — UTAU OTO.ini Smart Generator

> One-click oto.ini generation with auto-transcoding, silence detection, batch alias processing, multilingual voicebank, character.txt, health check, bulk offset adjustment, smart pre-white, vowel protection, frq generation, volume normalization, encrypted config, progress recovery, and recording mode.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux%20%7C%20Android-lightgrey)](https://github.com/tyy485/makeotoini)

---

## 📖 Table of Contents

- [✨ Features](#-features)
- [📦 Installation & Running](#-installation--running)
- [🚀 Usage Guide](#-usage-guide)
- [🎙️ Recording Mode](#️-recording-mode)
- [🛠️ Configuration Options](#️-configuration-options)
- [📁 Output Example](#-output-example)
- [📁 Project Structure](#-project-structure)
- [❓ FAQ](#-faq)
- [📄 License](#-license)

---

## ✨ Features

- 🎯 **One-click generation** — Scan .wav files, auto-estimate parameters, output standard oto.ini
- 🔄 **Auto-transcoding** — MP3 / FLAC / M4A / OGG → .wav (with retry)
- 📦 **Zero dependencies** — Python standard library only
- 🧹 **Abnormal filename cleaning** — Remove invisible characters
- 🏷️ **Batch alias processing** — Add/remove prefixes/suffixes, delete ranges, keep kana/romaji (Japanese), keep Hangul/romanization (Korean)
- 🔇 **Silence detection** — Auto-locate offset
- 🌬️ **Breath file detection** — Auto-detect `br`/`呼`/`吸`/`breathe`/`breath` files, custom alias template with `x` placeholder
- 🔧 **Romaji auto-fix** — Fix `short`/`long`/`vowel` labels (Japanese Kana & Korean Hangul)
- 🎯 **Smart Pre-White** — Auto-detect breath at start of recording, include in offset
- 🔊 **Vowel Protection** — Prevent consonants from swallowing vowels
- 📈 **Pure Python frq generation** — Autocorrelation-based frq generation, no wavtool required
- 🎚️ **Volume normalization** — Normalize all audio using FFmpeg loudnorm
- 🏥 **Health Check** — Scan voicebank for missing phonemes (Japanese 50-sounds, Chinese Pinyin, Korean Hangul, English phonemes)
- 🎚️ **Bulk Offset Adjustment** — Adjust all phoneme offsets at once (fix "rush/drag" issues)
- 📋 **character.txt generation** — Interactive voicebank info file with name, version, website, icon
- 👁️ **Preview confirmation** — Preview before writing
- 🛡️ **Smart error handling** — Auto-solutions, retry on conversion fail, auto UTF-8 fallback
- 📂 **Encrypted config (.moic)** — Import/export encrypted config, tamper-proof, shareable
- 🔄 **Progress save & recovery** — Auto-save on interruption, resume on next run
- 📖 **Story mode** — Built-in + online stories for entertainment during long runs
- 🎙️ **Recording mode** — Double Enter triggers recording (macOS/Linux/Termux)
- 📝 **Log export** — Export run logs after generation for troubleshooting
- 🌍 **Cross-platform** — Windows / macOS / Linux / Termux(Android)
- 🔤 **Encoding options** — Shift-JIS / GB2312 / EUC-KR / UTF-8 / Smart encoding

---

## 📦 Installation & Running

### 🪟 Windows Users

#### 1. Install Python
- Visit [python.org/downloads](https://www.python.org/downloads/)
- Download the latest Python
- **Check `Add Python to PATH` during installation**
- Complete installation

#### 2. Verify Python
Open Command Prompt (`Win+R` → `cmd` → Enter):
```bash
python --version
```
Should show `Python 3.x.x`.

#### 3. Install FFmpeg (for transcoding)
> 💡 Skip if all your audio files are `.wav`

- Download from [ffmpeg.org/download.html](https://ffmpeg.org/download.html)
- Extract to `C:\ffmpeg`
- Add `C:\ffmpeg\bin` to system PATH

#### 4. Download this tool
- Click green `Code` → `Download ZIP`
- Extract to your preferred location

#### 5. Run
```bash
python make_oto.py
```

---

### 🍎 macOS Users

```bash
# Install Python (if not already)
brew install python

# Install FFmpeg (optional)
brew install ffmpeg

# Clone and run
git clone https://github.com/tyy485/makeotoini.git
cd makeotoini
python3 make_oto.py
```

> 💡 Use `python3` on macOS.

---

### 🐧 Linux Users

```bash
# Install Python (if not already)
# Ubuntu/Debian
sudo apt update && sudo apt install python3

# Fedora
sudo dnf install python3

# Arch
sudo pacman -S python

# Install FFmpeg (optional)
sudo apt install ffmpeg   # Ubuntu/Debian

# Clone and run
git clone https://github.com/tyy485/makeotoini.git
cd makeotoini
python3 make_oto.py
```

---

### 📱 Termux (Android) Users

#### 1. Install Termux
- Open https://github.com/termux/termux-app/
- Scroll down to **Releases** and click the latest version
- In the Assets section, download the `.apk` file matching your device's processor architecture:
  - Most phones use `arm64-v8a` – download the corresponding `termux-app_vXXX.apk`
  - If unsure about your architecture, download the `universal` version
- For users in China, if GitHub downloads are slow, prepend the download link with:
  ```
  https://ghproxy.net/ + original_download_link
  ```
  Example:
  ```
  https://ghproxy.net/https://github.com/termux/termux-app/releases/download/v0.118.3/termux-app_v0.118.3+apt-android-7-github-debug_universal.apk
  ```
- Install the downloaded APK file
- If the system shows "Installation from unknown sources blocked", go to system settings and allow the current file manager or browser to install apps
- Open Termux and wait for automatic initialization to complete

#### 2. Install required packages
Open Termux terminal:

```
~ $ pkg update
~ $ pkg install git python ffmpeg
```

> 💡 `pkg` and `apt` work the same. `pkg update` refreshes the package list. `pkg install` installs all three packages at once.

**For recording support**, also install:
```
~ $ pkg install termux-api
```

#### 3. Clone this tool
```
~ $ git clone https://github.com/tyy485/makeotoini.git
~ $ cd makeotoini
```

#### 4. Run
```
~ $ python make_oto.py
```

> 💡 Audio files on Android are usually in `/sdcard/`. In Termux, access via `~/storage/shared/`.

---

## 🚀 Usage Guide

### Quick Start

1. Place your audio files (.wav / .mp3 / .flac / etc.) in a folder
2. Run `python make_oto.py` (`python3` on macOS/Linux)
3. Follow prompts to select UI language, voicebank language, encoding, alias rules, advanced options (Smart Pre-White, Vowel Protection, Health Check, etc.)
4. Preview configuration, confirm, and generate
5. `oto.ini`, `character.txt` (if enabled), and frq files (if enabled) will appear in the same directory

### Configuration Options Overview

| Step | Option | Description |
|------|--------|-------------|
| 1 | UI Language | Chinese / English |
| 2 | Voicebank Language | 日本語 / 中文 / 한국어 / English / Constructed |
| 3 | Encoding | GB2312 / Shift-JIS / UTF-8 / EUC-KR / Smart |
| 4 | Abnormal filename handling | Ask / Auto / Skip |
| 5 | Conversion mode | Keep / Temporary |
| 6 | Conversion mode | Force / Reuse |
| 7 | Scan mode | Recursive / Current only |
| 8 | Silence sensitivity | Low / Medium / High / Manual |
| 9 | Bulk offset adjustment | Positive = delay, negative = advance (ms) |
| 10 | Breath alias template | Supports `x` placeholder |
| 11 | Alias mode | 8 modes (Japanese/Korean specific) |
| 12 | Romaji auto-fix | Enable / Disable |
| 13 | Smart Pre-White | Enable / Disable |
| 14 | Vowel Protection | Enable / Disable |
| 15 | frq generation | Generate / Skip |
| 16 | Volume normalization | Enable / Disable (needs FFmpeg) |
| 17 | Health Check | Run / Skip |
| 18 | character.txt | Generate / Skip |

All options support Enter for default values.

---

## 🎙️ Recording Mode

Press Enter twice (empty input) during any prompt to trigger recording mode.

- **macOS**: Uses built-in `afrecord`
- **Linux**: Uses built-in `arecord`
- **Termux**: Uses `termux-microphone-record` (requires `pkg install termux-api`)
- **Windows**: Not supported, prompts to use Audacity or online tools

Recordings are saved to the current voicebank directory as `recording_timestamp.wav`.

---

## 🛠️ Configuration Options

| Option | Description |
|--------|-------------|
| **UI Language** | Chinese / English |
| **Voicebank Language** | 日本語 / 中文 / 한국어 / English / Constructed |
| **Encoding** | Shift-JIS / GB2312 / EUC-KR / UTF-8 / Smart |
| **Abnormal filename handling** | Ask / Auto / Skip |
| **Conversion mode** | Keep / Temporary |
| **Alias mode** | 8 modes: none / add prefix / remove prefix (all matches) / remove suffix (all matches) / add suffix / slice / keep kana/romaji (Japanese) / keep Hangul/romanization (Korean) |
| **Silence sensitivity** | Low / Medium / High / Manual (Constructed defaults to 0.1) |
| **Bulk Offset Adjustment** | Adjust all offsets at once (positive=delay, negative=advance) |
| **Breath alias template** | Custom template with `x` placeholder |
| **Smart Pre-White** | Auto-detect breath at start of recording |
| **Vowel Protection** | Prevent consonants from overpowering vowels |
| **frq generation** | Pure Python autocorrelation, no wavtool required |
| **Volume normalization** | Normalize all audio using FFmpeg |
| **Health Check** | Scan for missing phonemes |
| **character.txt generation** | Interactive voicebank info file |
| **Preview confirmation** | Preview before writing |
| **Encrypted config** | `.moic` format, tamper-proof, shareable |
| **Progress recovery** | Auto-save on interruption |
| **Story mode** | Built-in + online stories |
| **Recording mode** | Double Enter triggers recording |
| **Log export** | Export run logs |

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
```

### character.txt
```ini
name=Hatsune Miku
version=1.0
web=https://example.com
image=icon.png
```

### .makeotoini_config.moic
Encrypted config file, import/export via the tool.

---

## 📁 Project Structure

```
makeotoini/
├── make_oto.py      # Main program
├── README.md
├── README_EN.md
├── LICENSE
└── doc/
    ├── ERROR_CODES_zh.md
    └── ERROR_CODES_en.md
```

---

## ❓ FAQ

**Q: FFmpeg not found?**  
A: Skip if all files are `.wav`. Otherwise install FFmpeg.

**Q: How to generate frq?**  
A: Version 4.1 uses pure Python autocorrelation, no wavtool needed.

**Q: What languages does Health Check support?**  
A: Japanese 50-sounds, Chinese Pinyin, Korean Hangul, English phonemes.

**Q: What's Bulk Offset Adjustment for?**  
A: Fix "rush/drag" issues by adjusting all offsets at once.

**Q: How does the config system work?**  
A: The tool auto-detects `.makeotoini_config.moic` in the current directory. Import to reuse settings or share with others.

**Q: How to trigger recording mode?**  
A: Press Enter twice (empty input) during any prompt.

**Q: Which platforms support recording?**  
A: macOS (afrecord), Linux (arecord), Termux (termux-microphone-record, requires termux-api). Windows is not supported and will prompt to use other tools.

**Q: What is progress recovery?**  
A: If interrupted (Ctrl+C or crash), progress is auto-saved to `~/.makeprogress/`. Next run will ask if you want to continue.

**Q: How to export logs?**  
A: During exit, select "Export log" from the end menu.

**Q: What is EUC-KR?**  
A: A common encoding for Korean. Use EUC-KR or Smart encoding for Korean voicebanks.

**Q: What is Constructed Language mode?**  
A: When voicebank language is set to "Constructed / Unknown", silence threshold is automatically set to 0.1, suitable for voicebanks with waveforms that differ significantly from human speech.

---

## 🤝 Contributing

Issues, PRs, and forks welcome!

---

## 📄 License

MIT © [tyy485](https://github.com/tyy485)

**Fully open source – use it freely, modify it, sell it, do whatever you like.**  
If you find it useful, a ⭐ Star would mean a lot!

---

**Happy Tuning! 🎶**
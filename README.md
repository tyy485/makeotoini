# 🎵 makeotoini — UTAU OTO.ini 智能生成器

> 一键生成 oto.ini，支持自动转码、静音检测、别名处理、多语言音源、健康检查、批量偏移、智能前白、元音保护、frq 生成、音量归一化、加密配置文件、进度恢复、录音辅助。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux%20%7C%20Android-lightgrey)](https://github.com/tyy485/makeotoini)

---

## 📖 目录

- [✨ 特性](#-特性)
- [📦 安装与运行](#-安装与运行)
- [🚀 使用指南](#-使用指南)
- [🎙️ 录音模式](#️-录音模式)
- [🛠️ 配置选项详解](#️-配置选项详解)
- [📁 输出示例](#-输出示例)
- [📁 项目结构](#-项目结构)
- [❓ 常见问题](#-常见问题)
- [📄 许可证](#-许可证)

---

## ✨ 特性

- 🎯 **一键生成** — 扫描 wav 文件，自动估算参数，输出标准 oto.ini
- 🔄 **自动转码** — 支持 MP3 / FLAC / M4A / OGG 等格式 → 自动转 wav（含重试机制）
- 📦 **零依赖** — 只用 Python 标准库，不用 `pip install` 任何东西
- 🧹 **异常文件名清洗** — 剔除不可见字符，避免 UTAU 报错
- 🏷️ **别名批量处理** — 加/删前缀后缀、删除字符范围、保留假名/罗马音（日文）、保留谚文/罗马音（韩文）
- 🔇 **静音检测** — 自动定位 offset，减少呼吸声误切
- 🌬️ **呼吸声智能识别** — 自动识别 `br`/`br_数字`/`呼`/`吸`/`breathe`/`breath` 格式，支持自定义别名模板（如 `breath_x` 自动编号）
- 🔧 **罗马音自动修复** — 将 `short`/`long`/`vowel` 等标注修正为标准罗马音（支持日文假名和韩文谚文）
- 🎯 **智能前白留空（Smart Pre-White）** — 自动检测录音开头的呼吸声，算进 offset，让发音更自然
- 🔊 **元音保护** — 防止辅音过长盖过元音（俗称“吞元音”）
- 📈 **纯 Python frq 生成** — 自相关法生成 frq 文件，UTAU 音高更自然，无需安装 wavtool
- 🎚️ **统一音量（归一化）** — 使用 FFmpeg 将所有音频统一到相同音量
- 🏥 **音源健康检查** — 扫描音源目录，检查是否缺音（支持日语五十音、中文拼音、韩文谚文、英文音素）
- 🎚️ **批量偏移调整** — 整体微调所有音素的 offset，解决“抢拍/拖拍”
- 📋 **character.txt 生成** — 交互式生成声库信息文件，支持歌手名、版本、网站、图标
- 👁️ **预览确认模式** — 生成前预览配置，确认后再写入
- 🛡️ **智能错误处理** — 常见错误自动给出解决方案，转码失败自动重试，编码错误自动切换 UTF-8
- 📂 **加密配置文件（.moic）** — 导入/导出加密配置，防篡改，可分享
- 🔄 **进度保存与恢复** — 中断后自动保存，下次运行可继续
- 📖 **故事库** — 内置故事 + 联网下载，生成文件多时可以听故事解闷
- 🎙️ **录音模式** — 连续按两次回车触发，直接录音到音源目录（支持 macOS/Linux/Termux）
- 📝 **日志导出** — 生成后可选导出运行日志，方便排查问题
- 🌍 **跨平台** — Windows / macOS / Linux / Termux(Android) 全支持
- 🔤 **编码可选** — Shift-JIS / GB2312 / EUC-KR / UTF-8 / 智能编码，按需选择

---

## 📦 安装与运行

### 🪟 Windows 用户

#### 1. 安装 Python（如果没有）
- 访问 [python.org/downloads](https://www.python.org/downloads/)
- 下载最新版 Python（点黄色的 Download 按钮）
- **安装时务必勾选 `Add Python to PATH`**（这步非常重要！）
- 一路点 `Next` 完成安装

#### 2. 验证 Python 是否装好
打开命令行（`Win+R` → 输入 `cmd` → 回车），输入：
```bash
python --version
```
如果显示 `Python 3.x.x` 就说明装好了。

#### 3. 安装 FFmpeg（如需转码 MP3/FLAC 等格式）
> 💡 如果您的音频全是 `.wav` 格式，**可以跳过这一步**

- 下载 [ffmpeg.org/download.html](https://ffmpeg.org/download.html) 里的 Windows 版本
- 解压到 `C:\ffmpeg`
- 把 `C:\ffmpeg\bin` 添加到系统 PATH：
  1. 右键「此电脑」→「属性」→「高级系统设置」
  2. 点击「环境变量」→ 在「系统变量」中找到 `Path` → 双击
  3. 点击「新建」→ 输入 `C:\ffmpeg\bin` → 确定

#### 4. 下载本工具
- 点击右上角绿色的 `Code` → `Download ZIP`
- 解压到您想放的位置（比如 `D:\oto音源\`）

#### 5. 运行
在文件夹地址栏输入 `cmd` 然后按回车，输入：
```bash
python make_oto.py
```

#### 6. 如果报错 `python 不是内部或外部命令`
说明 Python 没加 PATH，**重装 Python 并勾选 `Add Python to PATH`** 即可。

---

### 🍎 macOS 用户

#### 1. 安装 Python（如果没有）
```bash
# 用 Homebrew 安装（推荐）
brew install python

# 或者从 python.org 下载安装包
```

#### 2. 验证 Python 是否装好
```bash
python3 --version
```
如果显示 `Python 3.x.x` 就说明装好了。

#### 3. 安装 FFmpeg（如需转码）
```bash
brew install ffmpeg
```

#### 4. 克隆本工具
```bash
git clone https://github.com/tyy485/makeotoini.git
cd makeotoini
```

#### 5. 运行
```bash
python3 make_oto.py
```

> 💡 macOS 要用 `python3` 而不是 `python`，因为系统自带的 Python 2 已经过时了

---

### 🐧 Linux 用户

#### 1. 安装 Python（如果没有）
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3

# Fedora
sudo dnf install python3

# Arch
sudo pacman -S python
```

#### 2. 验证 Python 是否装好
```bash
python3 --version
```

#### 3. 安装 FFmpeg（如需转码）
```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# Fedora
sudo dnf install ffmpeg

# Arch
sudo pacman -S ffmpeg
```

#### 4. 克隆本工具
```bash
git clone https://github.com/tyy485/makeotoini.git
cd makeotoini
```

#### 5. 运行
```bash
python3 make_oto.py
```

#### 6. 可选：做成全局命令（以后直接敲 `makeotoini` 就能跑）
```bash
chmod +x make_oto.py
sudo ln -s $(pwd)/make_oto.py /usr/local/bin/makeotoini
makeotoini   # 以后再任何目录都能直接用了！
```

---

### 📱 Termux (Android) 用户

> 在手机上跑 Python 生成 oto.ini，适合没电脑时应急使用

#### 1. 安装 Termux
- 打开 https://github.com/termux/termux-app/
- 往下翻找到 **Releases**，点击进入最新版本
- 在 Assets 区域，根据手机处理器架构下载对应的 `.apk` 文件：
  - 大部分手机是 `arm64-v8a`，下载 `termux-app_vXXX.apk` 即可
  - 如果不确定架构，下载 `universal` 版本
- 国内用户如果 GitHub 下载慢，可复制下载链接到：
  ```
  https://ghproxy.net/ + 原始下载链接
  ```
  例如：
  ```
  https://ghproxy.net/https://github.com/termux/termux-app/releases/download/v0.118.3/termux-app_v0.118.3+apt-android-7-github-debug_universal.apk
  ```
  如果你不想手动拼接链接，可以安装「GitHub 加速」插件，在插件里填上 `ghproxy.net`，插件会自动拼接加速链接。
- 安装下载好的 APK 文件
- 如果系统提示「禁止安装未知来源应用」，请前往系统设置允许当前文件管理器或浏览器安装应用
- 打开 Termux，等待自动初始化完成

#### 2. 安装必要软件包
打开 Termux 终端，你会看到类似这样的提示符：

```
~ $
```

先更新软件源：

```
~ $ pkg update
```

然后一次性安装 `git`、`python`、`ffmpeg` 三个包：

```
~ $ pkg install git python ffmpeg
```

> 💡 `pkg` 和 `apt` 效果一样，用哪个都行。`pkg update` 保证源是最新的，`pkg install` 一次性装好三个包，省得后续再补。

**如需使用录音功能**，还需要安装 `termux-api`：
```
~ $ pkg install termux-api
```

#### 3. 克隆本工具
```
~ $ git clone https://github.com/tyy485/makeotoini.git
~ $ cd makeotoini
```

#### 4. 运行
```
~ $ python make_oto.py
```

> 💡 手机上的音频文件放在 `/sdcard/` 目录下，Termux 里用 `~/storage/shared/` 可以访问

---

## 🚀 使用指南

### 快速开始

1. 将您的音频文件（.wav / .mp3 / .flac 等）放入一个文件夹
2. 运行 `python make_oto.py`（macOS/Linux 用 `python3`）
3. 按提示选择界面语言、音源语言、编码、处理模式、别名规则、高级选项（智能前白、元音保护、健康检查等）
4. 预览配置，确认后生成
5. 生成的 `oto.ini`、`character.txt`（如启用）、frq 文件（如启用）会在同一目录下

### 配置选项速览

程序启动后会依次询问以下配置项（括号内为默认值）：

| 步骤 | 选项 | 说明 |
|------|------|------|
| 1 | 界面语言 | 中文 / English |
| 2 | 音源语言 | 日本語 / 中文 / 한국어 / English / 人造语言 |
| 3 | 编码格式 | GB2312 / Shift-JIS / UTF-8 / EUC-KR / 智能编码 |
| 4 | 异常文件名处理 | 逐个询问 / 全部自动清洗 / 全部跳过 |
| 5 | 转换文件处理 | 永久保留 / 临时转换（生成后删除） |
| 6 | 转换模式 | 强制重新转换 / 复用已有 wav |
| 7 | 扫描模式 | 递归扫描 / 仅当前目录 |
| 8 | 静音检测灵敏度 | 低 / 中 / 高 / 手动 |
| 9 | 批量偏移调整 | 正数后移，负数前移（毫秒） |
| 10 | 呼吸声别名模板 | 支持 `x` 占位符自动编号 |
| 11 | 别名模式 | 8 种（含日文/韩文专用模式） |
| 12 | 罗马音自动修复 | 启用 / 禁用 |
| 13 | 智能前白留空 | 启用 / 禁用 |
| 14 | 元音保护 | 启用 / 禁用 |
| 15 | frq 生成 | 生成 / 不生成 |
| 16 | 统一音量 | 启用 / 禁用（需 FFmpeg） |
| 17 | 健康检查 | 运行 / 跳过 |
| 18 | character.txt | 生成 / 不生成 |

所有选项都支持在提示时直接回车使用默认值，全程无需记忆。

---

## 🎙️ 录音模式

运行过程中连续按两次回车（输入空行），会进入录音模式。

- **macOS**：使用系统自带的 `afrecord`
- **Linux**：使用系统自带的 `arecord`
- **Termux**：使用 `termux-microphone-record`（需要先安装 `pkg install termux-api`）
- **Windows**：暂不支持系统录音，会引导你使用 Audacity 或在线录音工具

录音文件会自动保存到当前音源目录，格式为 `recording_时间戳.wav`。

---

## 🛠️ 配置选项详解

| 选项 | 说明 |
|------|------|
| **界面语言** | 中文 / English，工具界面的显示语言 |
| **音源语言** | 日本語 / 中文 / 한국어 / English / 人造语言，影响编码和健康检查 |
| **编码格式** | Shift-JIS / GB2312 / EUC-KR / UTF-8 / 智能编码，智能编码根据语言自动匹配 |
| **异常文件名处理** | 逐个询问 / 自动清洗 / 全部跳过 |
| **转换模式** | 永久保留 / 临时转换（生成后删除 wav） |
| **别名模式** | 8 种：不加 / 加前缀 / 删前缀（支持删除所有匹配）/ 加后缀 / 删后缀（支持删除所有匹配）/ 删除字符范围 / 保留假名/保留罗马音（日文）/ 保留谚文/保留罗马音（韩文） |
| **静音灵敏度** | 低/中/高/手动（人造语言默认阈值为 0.1） |
| **批量偏移调整** | 整体微调所有音素的 offset（正数后移，负数前移） |
| **呼吸声别名模板** | 自定义呼吸声别名格式，支持 `x` 占位符自动编号 |
| **智能前白留空** | 自动检测录音开头呼吸声，算进 offset |
| **元音保护** | 防止辅音过长盖过元音 |
| **frq 生成** | 纯 Python 自相关法生成 frq，无需 wavtool |
| **统一音量** | 使用 FFmpeg 归一化所有音频音量 |
| **健康检查** | 扫描音源，输出缺音报告（含假名/谚文读音） |
| **character.txt 生成** | 交互式生成声库信息文件 |
| **预览确认** | 生成前预览配置，确认后再写入 |
| **加密配置文件** | `.moic` 格式，防篡改，可分享 |
| **进度恢复** | 中断后自动保存，下次运行可继续 |
| **故事库** | 内置故事 + 联网下载，解闷用 |
| **录音模式** | 连续按两次回车触发，直接录音到音源目录 |
| **日志导出** | 生成后可选导出运行日志 |

---

## 📁 输出示例

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
name=初音未来
version=1.0
web=https://example.com
image=icon.png
```

### .makeotoini_config.moic
加密配置文件，无法直接查看，用本工具导出和导入。

---

## 📁 项目结构

```
makeotoini/
├── make_oto.py      # 主程序，直接运行这个
├── README.md
├── README_EN.md
├── LICENSE
└── doc/
    ├── ERROR_CODES_zh.md
    └── ERROR_CODES_en.md
```

---

## ❓ 常见问题

**Q: 提示找不到 FFmpeg？**  
A: 如果全是 `.wav` 格式，完全不需要 FFmpeg。否则按教程安装。

**Q: frq 怎么生成？**  
A: 4.1 开始使用纯 Python 自相关法生成 frq，无需额外安装 wavtool。

**Q: 健康检查支持哪些语言？**  
A: 日语五十音、中文拼音、韩文谚文、英文音素。

**Q: 批量偏移调整有什么用？**  
A: 如果整首歌听起来“抢拍”或“拖拍”，可以整体调整 offset，不用手动改几百条。

**Q: 配置文件怎么用？**  
A: 运行时会自动检测当前目录的 `.makeotoini_config.moic`，选择导入即可复用所有设置，也可以分享给他人。

**Q: 录音模式怎么触发？**  
A: 在任意输入提示处连续按两次回车（输入空行），即可进入录音模式。

**Q: 录音支持哪些平台？**  
A: macOS（afrecord）、Linux（arecord）、Termux（termux-microphone-record，需安装 termux-api）。Windows 暂不支持，会引导使用其他工具。

**Q: 进度保存有什么用？**  
A: 如果中途中断（如 Ctrl+C 或断电），进度会自动保存到 `~/.makeprogress/`。下次运行会询问是否继续。

**Q: 日志怎么导出？**  
A: 生成结束后，在结束菜单中选择“导出配置文件”即可导出 `.moic` 加密配置。日志导出在退出时选择“导出日志”。

**Q: EUC-KR 是什么？**  
A: 韩文常用的编码格式。如果音源语言选择韩文，建议使用 EUC-KR 或智能编码。

**Q: 人造语言模式是什么？**  
A: 当音源语言选择“人造语言 / 未知语言”时，静音检测阈值自动调整为 0.1，适合波形特征与人类语音差异较大的音源。

---

## 🤝 贡献

欢迎提 Issue、PR、Fork！

---

## 📄 许可证

MIT © [tyy485](https://github.com/tyy485)

**完全开源，随便用，随便改，随便商用。**  
如果你觉得好用，点个 ⭐ Star 就是对我最大的支持！

---

**Happy Tuning! 🎶**
# 🎵 makeotoini — UTAU OTO.ini 智能生成器

> 把音频文件夹拖进来，一键生成 oto.ini，支持自动转码 + 静音检测 + 别名批量处理 + 罗马音自动修复

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux%20%7C%20Android-lightgrey)](https://github.com/new/makeotoini)

---

## 📖 目录

- [✨ 特性](#-特性)
- [📦 安装与运行](#-安装与运行)
  - [🪟 Windows 用户](#-windows-用户)
  - [🍎 macOS 用户](#-macos-用户)
  - [🐧 Linux 用户](#-linux-用户)
  - [📱 Termux (Android) 用户](#-termux-android-用户)
- [🚀 使用指南](#-使用指南)
- [🛠️ 配置选项详解](#️-配置选项详解)
- [📁 输出示例](#-输出示例)
- [📁 项目结构](#-项目结构)
- [❓ 常见问题](#-常见问题)
- [🤝 贡献](#-贡献)
- [📄 许可证](#-许可证)
- [💬 鸣谢](#-鸣谢)

---

## ✨ 特性

- 🎯 **一键生成** — 扫描 wav 文件，自动估算参数，输出标准 oto.ini
- 🔄 **自动转码** — 支持 MP3 / FLAC / M4A / OGG 等格式 → 自动转 wav（需 FFmpeg）
- 📦 **零依赖** — 只用 Python 标准库，不用 `pip install` 任何东西
- 🧹 **异常文件名清洗** — 剔除不可见字符，避免 UTAU 报错
- 🏷️ **别名批量处理** — 加/删前缀后缀、删除指定字符范围，六种模式任选
- 🔇 **静音检测** — 自动定位 offset，减少呼吸声误切
- 🔧 **罗马音自动修复** — 将 `short`/`long`/`vowel` 等常见标注自动修正为标准罗马音
- 🌍 **跨平台** — Windows / macOS / Linux / Termux(Android) 全支持
- 🔤 **编码可选** — Shift-JIS / GB2312 / UTF-8，按需输出

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
git clone https://github.com/new/makeotoini.git
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
git clone https://github.com/new/makeotoini.git
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
- 从 F-Droid 下载 Termux（**不要从 Google Play 下，版本太旧**）
- 打开 Termux

#### 2. 安装 Python 和 FFmpeg
```bash
pkg update
pkg install python ffmpeg
```

#### 3. 克隆本工具
```bash
git clone https://github.com/new/makeotoini.git
cd makeotoini
```

#### 4. 运行
```bash
python make_oto.py
```

> 💡 手机上的音频文件放在 `/sdcard/` 目录下，Termux 里用 `~/storage/shared/` 可以访问

---

## 🚀 使用指南

### 快速开始

1. 将您的音频文件（.wav / .mp3 / .flac 等）放入一个文件夹
2. 运行 `python make_oto.py`（macOS/Linux 用 `python3`）
3. 按提示选择编码、处理模式、别名规则
4. 生成的 `oto.ini` 会在同一目录下

### 交互流程示例

```
🎵 OTO.ini 智能生成器 v3.6

📝 请选择你的oto编码
  1. GB 2312
  2. Shift-JIS
  3. UTF-8

🧹 异常文件名处理模式
  1. 逐个询问
  2. 全部自动清洗
  3. 全部跳过

📦 转换文件处理模式
  1. 永久保留转换的wav文件
  2. 临时转换，生成oto后删除

🔄 转换模式
  1. 强制重新转换
  2. 复用已有wav

📂 扫描模式
  1. 递归扫描子文件夹
  2. 仅扫描当前目录

🎚️ 静音检测灵敏度
  1. 低灵敏度 (0.02)
  2. 中灵敏度 (0.01) [默认]
  3. 高灵敏度 (0.005)
  4. 手动输入阈值

🏷️ 别名自定义模式
  1. 不使用别名处理
  2. 批量添加前缀
  3. 批量删除前缀
  4. 批量删除后缀
  5. 批量添加后缀
  6. 删除指定字符范围

🔧 罗马音自动修复
  1. 启用自动修复
  2. 禁用自动修复
```

按提示一步步操作即可，**全程中文交互**，不需要任何编程知识。

### 目录结构建议

```
你的音源文件夹/
├── あ_i.wav
├── い_u.wav
├── か_ka.wav
├── make_oto.py   ← 把本工具放进来（或放在任意位置，运行时指定路径）
└── oto.ini       ← 生成后自动出现在这里
```

---

## 🛠️ 配置选项详解

| 选项 | 说明 |
|------|------|
| **编码格式** | Shift-JIS（UTAU 默认）/ GB2312 / UTF-8，按需选择 |
| **异常文件名处理** | 逐个询问 / 自动清洗 / 全部跳过，遇到乱码文件名时很有用 |
| **转换模式** | 永久保留 / 临时转换（生成 oto 后自动删除 wav，省空间） |
| **别名模式** | 6 种：不加 / 加前缀 / 删前缀 / 加后缀 / 删后缀 / 删除指定字符范围 |
| **静音灵敏度** | 低/中/高三档可调，录音底噪大的选低灵敏度 |
| **扫描模式** | 递归扫描子文件夹 / 仅扫描当前目录 |
| **罗马音自动修复** | 将 `short`/`long`/`vowel` 等常见标注自动修正为标准罗马音，避免 UTAU 识别错误 |

---

## 📁 输出示例

```ini
[#VERSION]
VERSION=100

あ_i.wav=i,0,362,844,482,241
い_u.wav=u,0,334,780,445,222
か_ka.wav=ka,0,362,844,482,241
き_ki.wav=ki,0,348,812,464,232
く_ku.wav=ku,0,320,747,427,213
```

参数含义（从左到右）：
- `别名` — UTAU 里显示的名称
- `offset` — 从开头跳过多少毫秒（静音段）
- `consonant` — 辅音长度
- `blank` — 空白段长度
- `preutterance` — 提前发声时间
- `overlap` — 交叉淡入淡出时间

---

## 📁 项目结构

```
makeotoini/
├── make_oto.py      # 主程序，直接运行这个
├── README.md
└── LICENSE
```

---

## ❓ 常见问题

**Q: 提示找不到 FFmpeg？**  
A: 如果您的音频全是 `.wav` 格式，**完全不需要 FFmpeg**，直接运行即可。如果需要转 MP3/FLAC 等格式，请按上面教程安装 FFmpeg。

**Q: 能处理中文文件名吗？**  
A: 可以，但建议用英文/日文/拼音命名，因为 UTAU 对中文支持有限，乱码风险更低。

**Q: 生成的参数需要手动调吗？**  
A: 工具提供的是“可用”参数，能直接出声。追求完美音质的调教师可以在此基础上微调。

**Q: 支持批量处理子文件夹吗？**  
A: 支持！运行时选择“递归扫描子文件夹”即可。

**Q: 这个工具能用在 UTAU-Synth 上吗？**  
A: 可以，oto.ini 格式通用。

**Q: 为什么我的 oto.ini 打开是乱码？**  
A: 因为编码选错了。UTAU 默认用 Shift-JIS，请用支持该编码的编辑器打开（如 Notepad++）。

**Q: 罗马音自动修复是做什么的？**  
A: 当文件名中含有 `short`、`long`、`vowel` 等非标准罗马音标注时，工具会自动将其修正为 `q`、`-` 等标准形式，避免 UTAU 无法识别。

---

## 🤝 贡献

欢迎提 Issue、PR、Fork 自己改！

如果你有好的想法，也欢迎直接联系我。

---

## 📄 许可证

MIT © [new](https://github.com/tyy485)

**完全开源，随便用，随便改，随便商用。**  
如果你觉得好用，点个 ⭐ Star 就是对我最大的支持！

---

## 💬 鸣谢

- UTAU 社区的所有调教师和音源制作者
- 所有提建议、帮忙测试的朋友们

---

**Happy Tuning! 🎶**
import os
import glob
import wave
import re
import sys
import subprocess
import tempfile
import platform
import shutil
import atexit
import time
from pathlib import Path

VERSION = "3.6"

class OtoGenerator:
    def __init__(self, wav_dir=None, output_path='oto.ini'):
        self.wav_dir = wav_dir
        self.output_path = output_path
        self.notes = []
        self.abnormal_files = []
        self.converted_files = []
        self.skipped_files = []
        self.temp_wav_files = []
        self.ffmpeg_available = None
        self.ffprobe_available = None
        self.encoding = 'shift-jis'
        self.clean_mode = 'ask'
        self.temp_mode = False
        self.silence_threshold = 0.01
        self.running = True
        self.cleanup_done = False
        self.force_reconvert = False
        self.recursive_scan = True
        self.alias_start = 0
        self.alias_end = 0
        self.alias_mode = 'none'
        self.alias_prefix = ''
        self.alias_suffix = ''
        self.fix_romaji = False
        
        self.kana_to_romaji = {
            'あ': 'a', 'い': 'i', 'う': 'u', 'え': 'e', 'お': 'o',
            'か': 'ka', 'き': 'ki', 'く': 'ku', 'け': 'ke', 'こ': 'ko',
            'さ': 'sa', 'し': 'shi', 'す': 'su', 'せ': 'se', 'そ': 'so',
            'た': 'ta', 'ち': 'chi', 'つ': 'tsu', 'て': 'te', 'と': 'to',
            'な': 'na', 'に': 'ni', 'ぬ': 'nu', 'ね': 'ne', 'の': 'no',
            'は': 'ha', 'ひ': 'hi', 'ふ': 'fu', 'へ': 'he', 'ほ': 'ho',
            'ま': 'ma', 'み': 'mi', 'む': 'mu', 'め': 'me', 'も': 'mo',
            'や': 'ya', 'ゆ': 'yu', 'よ': 'yo',
            'ら': 'ra', 'り': 'ri', 'る': 'ru', 'れ': 're', 'ろ': 'ro',
            'わ': 'wa', 'を': 'wo', 'ん': 'n',
            'が': 'ga', 'ぎ': 'gi', 'ぐ': 'gu', 'げ': 'ge', 'ご': 'go',
            'ざ': 'za', 'じ': 'ji', 'ず': 'zu', 'ぜ': 'ze', 'ぞ': 'zo',
            'だ': 'da', 'ぢ': 'ji', 'づ': 'zu', 'で': 'de', 'ど': 'do',
            'ば': 'ba', 'び': 'bi', 'ぶ': 'bu', 'べ': 'be', 'ぼ': 'bo',
            'ぱ': 'pa', 'ぴ': 'pi', 'ぷ': 'pu', 'ぺ': 'pe', 'ぽ': 'po',
            'きゃ': 'kya', 'きゅ': 'kyu', 'きょ': 'kyo',
            'しゃ': 'sha', 'しゅ': 'shu', 'しょ': 'sho',
            'ちゃ': 'cha', 'ちゅ': 'chu', 'ちょ': 'cho',
            'にゃ': 'nya', 'にゅ': 'nyu', 'にょ': 'nyo',
            'ひゃ': 'hya', 'ひゅ': 'hyu', 'ひょ': 'hyo',
            'みゃ': 'mya', 'みゅ': 'myu', 'みょ': 'myo',
            'りゃ': 'rya', 'りゅ': 'ryu', 'りょ': 'ryo',
            'ぎゃ': 'gya', 'ぎゅ': 'gyu', 'ぎょ': 'gyo',
            'じゃ': 'ja', 'じゅ': 'ju', 'じょ': 'jo',
            'びゃ': 'bya', 'びゅ': 'byu', 'びょ': 'byo',
            'ぴゃ': 'pya', 'ぴゅ': 'pyu', 'ぴょ': 'pyo',
            'ぁ': 'a', 'ぃ': 'i', 'ぅ': 'u', 'ぇ': 'e', 'ぉ': 'o',
            'っ': 'q',
            'ー': '-'
        }
        
        self.romaji_fix_map = {
            'short': 'q',
            'long': '-',
            'vowel': '',
            'sokuon': 'q',
            'chouon': '-',
            'hatsuon': 'n',
            'small': ''
        }
        
    def emergency_cleanup(self):
        if self.cleanup_done:
            return
        if self.temp_mode and self.temp_wav_files:
            for wav_path in self.temp_wav_files:
                try:
                    if os.path.exists(wav_path):
                        os.remove(wav_path)
                except:
                    pass
        self.cleanup_done = True
    
    def check_ffmpeg(self):
        if self.ffmpeg_available is not None:
            return self.ffmpeg_available
            
        try:
            result = subprocess.run(
                ['ffmpeg', '-version'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=2
            )
            self.ffmpeg_available = (result.returncode == 0)
        except:
            self.ffmpeg_available = False
            
        if not self.ffmpeg_available:
            print("⚠️  未找到FFmpeg，音频转换功能不可用")
            print("💡 请安装FFmpeg: https://ffmpeg.org/download.html")
        
        return self.ffmpeg_available
    
    def check_ffprobe(self):
        if self.ffprobe_available is not None:
            return self.ffprobe_available
            
        try:
            result = subprocess.run(
                ['ffprobe', '-version'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=2
            )
            self.ffprobe_available = (result.returncode == 0)
        except:
            self.ffprobe_available = False
        
        return self.ffprobe_available
    
    def detect_platform(self):
        system = platform.system()
        
        if system == 'Darwin':
            print("🍎 还用苹果电脑，这么有钱")
        elif system == 'Linux':
            if 'ANDROID_ROOT' in os.environ or 'TERMUX_VERSION' in os.environ:
                print("📱 Termux？这玩意可是安卓神器")
            else:
                print("🐧 我去，居然是神级系统")
        elif system == 'Windows':
            if 'TERM' in os.environ or 'ANSICON' in os.environ:
                print("🖥️  检测到高级终端")
            else:
                print("💻 竟然是CMD，来吧，进我的生成器")
        else:
            print(f"🖥️  检测到系统: {system}")
        
        return system
    
    def select_encoding(self):
        print("\n" + "="*60)
        print("📝 请选择你的oto编码")
        print("="*60)
        print("  1. GB 2312")
        print("  2. Shift-JIS")
        print("="*60)
        
        while True:
            choice = input("\n请输入编码序号: ").strip()
            
            if choice == '1' or choice.lower() == 'gb2312' or choice.lower() == 'gb 2312':
                self.encoding = 'gb2312'
                print(f"✅ 已选择: GB 2312 编码")
                return
            elif choice == '2' or choice.lower() == 'shift-jis' or choice.lower() == 'shiftjis':
                self.encoding = 'shift-jis'
                print(f"✅ 已选择: Shift-JIS 编码")
                return
            elif choice.lower() == 'unicode' or choice.lower() == 'utf-8' or choice.lower() == 'utf8':
                self.encoding = 'utf-8'
                print(f"✅ 已选择: UTF-8 编码")
                return
            else:
                print("❌ 无效选择，请输入 1 或 2")
                continue
    
    def select_clean_mode(self):
        print("\n" + "="*60)
        print("🧹 异常文件名处理模式")
        print("="*60)
        print("  1. 逐个询问 (适合少量文件)")
        print("  2. 全部自动清洗")
        print("  3. 全部跳过")
        print("="*60)
        
        while True:
            choice = input("\n请选择处理模式 (1/2/3): ").strip()
            
            if choice == '1':
                self.clean_mode = 'ask'
                print("✅ 已选择: 逐个询问模式")
                return
            elif choice == '2':
                self.clean_mode = 'auto'
                print("✅ 已选择: 全部自动清洗")
                return
            elif choice == '3':
                self.clean_mode = 'skip'
                print("✅ 已选择: 全部跳过")
                return
            else:
                print("❌ 无效选择，请输入 1、2 或 3")
                continue
    
    def select_temp_mode(self):
        print("\n" + "="*60)
        print("📦 转换文件处理模式")
        print("="*60)
        print("  1. 永久保留转换的wav文件")
        print("  2. 临时转换，生成oto后删除")
        print("="*60)
        
        while True:
            choice = input("\n请选择处理模式 (1/2): ").strip()
            
            if choice == '1':
                self.temp_mode = False
                print("✅ 已选择: 永久保留wav文件")
                return
            elif choice == '2':
                self.temp_mode = True
                print("✅ 已选择: 临时转换模式")
                return
            else:
                print("❌ 无效选择，请输入 1 或 2")
                continue
    
    def select_reconvert_mode(self):
        print("\n" + "="*60)
        print("🔄 转换模式")
        print("="*60)
        print("  1. 强制重新转换 (覆盖已有wav)")
        print("  2. 复用已有wav (加快速度)")
        print("="*60)
        
        while True:
            choice = input("\n请选择转换模式 (1/2): ").strip()
            
            if choice == '1':
                self.force_reconvert = True
                print("✅ 已选择: 强制重新转换")
                return
            elif choice == '2':
                self.force_reconvert = False
                print("✅ 已选择: 复用已有wav")
                return
            else:
                print("❌ 无效选择，请输入 1 或 2")
                continue
    
    def select_scan_mode(self):
        print("\n" + "="*60)
        print("📂 扫描模式")
        print("="*60)
        print("  1. 递归扫描子文件夹")
        print("  2. 仅扫描当前目录")
        print("="*60)
        
        while True:
            choice = input("\n请选择扫描模式 (1/2): ").strip()
            
            if choice == '1':
                self.recursive_scan = True
                print("✅ 已选择: 递归扫描")
                return
            elif choice == '2':
                self.recursive_scan = False
                print("✅ 已选择: 仅扫描当前目录")
                return
            else:
                print("❌ 无效选择，请输入 1 或 2")
                continue
    
    def select_silence_threshold(self):
        print("\n" + "="*60)
        print("🎚️  静音检测灵敏度")
        print("="*60)
        print("  1. 低灵敏度 (0.02) - 适合响亮的录音")
        print("  2. 中灵敏度 (0.01) - 适合普通录音 [默认]")
        print("  3. 高灵敏度 (0.005) - 适合小声录音")
        print("  4. 手动输入阈值 (0.001-0.1)")
        print("="*60)
        
        while True:
            choice = input("\n请选择灵敏度 (1/2/3/4): ").strip()
            
            if choice == '1':
                self.silence_threshold = 0.02
                print(f"✅ 已选择: 低灵敏度 (阈值: {self.silence_threshold})")
                return
            elif choice == '2':
                self.silence_threshold = 0.01
                print(f"✅ 已选择: 中灵敏度 (阈值: {self.silence_threshold})")
                return
            elif choice == '3':
                self.silence_threshold = 0.005
                print(f"✅ 已选择: 高灵敏度 (阈值: {self.silence_threshold})")
                return
            elif choice == '4':
                while True:
                    try:
                        threshold = float(input("请输入阈值 (0.001-0.1): ").strip())
                        if 0.001 <= threshold <= 0.1:
                            self.silence_threshold = threshold
                            print(f"✅ 已设置阈值: {self.silence_threshold}")
                            return
                        else:
                            print("❌ 阈值必须在 0.001 到 0.1 之间")
                    except ValueError:
                        print("❌ 请输入有效的数字")
            else:
                print("❌ 无效选择，请输入 1、2、3 或 4")
                continue
    
    def select_alias_mode(self):
        print("\n" + "="*60)
        print("🏷️  别名 (Alias) 自定义模式")
        print("="*60)
        print("  1. 不使用别名处理 (直接用文件名)")
        print("  2. 批量添加前缀 (如: x_)")
        print("  3. 批量删除前缀 (如: 删除 x_)")
        print("  4. 批量删除后缀 (如: 删除 _x)")
        print("  5. 批量添加后缀 (如: _x)")
        print("  6. 删除指定字符范围 (如: 删除第1-3个字符)")
        print("="*60)
        
        while True:
            choice = input("\n请选择别名模式 (1/2/3/4/5/6): ").strip()
            
            if choice == '1':
                self.alias_mode = 'none'
                print("✅ 已选择: 不使用别名处理")
                return
            elif choice == '2':
                self.alias_mode = 'add_prefix'
                prefix = input("请输入要添加的前缀: ").strip()
                self.alias_prefix = prefix
                print(f"✅ 已选择: 批量添加前缀 '{prefix}'")
                return
            elif choice == '3':
                self.alias_mode = 'remove_prefix'
                prefix = input("请输入要删除的前缀: ").strip()
                self.alias_prefix = prefix
                print(f"✅ 已选择: 批量删除前缀 '{prefix}'")
                return
            elif choice == '4':
                self.alias_mode = 'remove_suffix'
                suffix = input("请输入要删除的后缀: ").strip()
                self.alias_suffix = suffix
                print(f"✅ 已选择: 批量删除后缀 '{suffix}'")
                return
            elif choice == '5':
                self.alias_mode = 'add_suffix'
                suffix = input("请输入要添加的后缀: ").strip()
                self.alias_suffix = suffix
                print(f"✅ 已选择: 批量添加后缀 '{suffix}'")
                return
            elif choice == '6':
                self.alias_mode = 'slice'
                print("\n💡 提示: 字符位置从1开始计数，如文件名 'abcde'")
                print("   删除 1-3 得到 'de'")
                print("   删除 3-5 得到 'ab'")
                print("   删除 2-4 得到 'ae'")
                
                while True:
                    try:
                        start = input("请输入起始字符位置: ").strip()
                        end = input("请输入结束字符位置: ").strip()
                        
                        start_int = int(start)
                        end_int = int(end)
                        
                        if start_int < 1 or end_int < 1:
                            print("❌ 起始和结束位置必须 >= 1")
                            continue
                        if start_int > end_int:
                            print("❌ 起始位置不能大于结束位置")
                            continue
                        
                        self.alias_start = start_int - 1
                        self.alias_end = end_int
                        print(f"✅ 已选择: 删除第 {start} 到第 {end} 个字符")
                        return
                    except ValueError:
                        print("❌ 请输入有效的数字")
                        continue
            else:
                print("❌ 无效选择，请输入 1、2、3、4、5 或 6")
                continue
    
    def select_romaji_fix(self):
        print("\n" + "="*60)
        print("🔧 罗马音自动修复")
        print("="*60)
        print("  1. 启用自动修复 (将short/long等替换为正确罗马音)")
        print("  2. 禁用自动修复")
        print("="*60)
        
        while True:
            choice = input("\n请选择 (1/2): ").strip()
            
            if choice == '1':
                self.fix_romaji = True
                print("✅ 已启用: 罗马音自动修复")
                return
            elif choice == '2':
                self.fix_romaji = False
                print("✅ 已禁用: 罗马音自动修复")
                return
            else:
                print("❌ 无效选择，请输入 1 或 2")
                continue
    
    def extract_kana(self, text):
        kana_pattern = re.compile(
            r'[\u3040-\u309f\u30a0-\u30ff\u31f0-\u31ff]'
        )
        return ''.join(kana_pattern.findall(text))
    
    def kana_to_romaji_str(self, kana):
        result = ''
        i = 0
        while i < len(kana):
            if i + 1 < len(kana):
                pair = kana[i:i+2]
                if pair in self.kana_to_romaji:
                    result += self.kana_to_romaji[pair]
                    i += 2
                    continue
            char = kana[i]
            if char in self.kana_to_romaji:
                result += self.kana_to_romaji[char]
            else:
                result += char
            i += 1
        return result
    
    def fix_romaji_in_filename(self, filename):
        if not self.fix_romaji:
            return filename
        
        base_name = os.path.splitext(filename)[0]
        ext = os.path.splitext(filename)[1]
        
        kana = self.extract_kana(base_name)
        if not kana:
            return filename
        
        correct_romaji = self.kana_to_romaji_str(kana)
        
        lower_name = base_name.lower()
        for wrong, correct in self.romaji_fix_map.items():
            if wrong in lower_name:
                if correct:
                    pattern = re.compile(wrong, re.IGNORECASE)
                    base_name = pattern.sub(correct, base_name, count=1)
                else:
                    pattern = re.compile(wrong, re.IGNORECASE)
                    base_name = pattern.sub('', base_name, count=1)
        
        if '_' in base_name:
            parts = base_name.split('_')
            for i, part in enumerate(parts):
                if part.lower() in self.romaji_fix_map:
                    fix = self.romaji_fix_map[part.lower()]
                    if fix:
                        parts[i] = fix
                    else:
                        parts.pop(i)
                        break
            base_name = '_'.join(parts)
        
        if '_' in base_name:
            parts = base_name.split('_')
            for i, part in enumerate(parts):
                kana_in_part = self.extract_kana(part)
                if kana_in_part:
                    correct_part = self.kana_to_romaji_str(kana_in_part)
                    if part.lower() != correct_part.lower():
                        fixed = False
                        for wrong, correct in self.romaji_fix_map.items():
                            if wrong in part.lower():
                                if correct:
                                    parts[i] = correct_part + '_' + correct
                                else:
                                    parts[i] = correct_part
                                fixed = True
                                break
                        if not fixed:
                            if '_' in part:
                                subparts = part.split('_')
                                if any(w in subparts[-1].lower() for w in self.romaji_fix_map):
                                    for wrong, correct in self.romaji_fix_map.items():
                                        if wrong in subparts[-1].lower():
                                            if correct:
                                                subparts[-1] = correct
                                            else:
                                                subparts.pop()
                                            break
                                    parts[i] = '_'.join(subparts)
        
        new_name = base_name + ext
        
        if new_name != filename:
            print(f"   🔧 修复罗马音: {filename} -> {new_name}")
        
        return new_name
    
    def apply_alias(self, filename):
        base_name = os.path.splitext(filename)[0]
        
        if self.fix_romaji:
            base_name = self.fix_romaji_in_filename(base_name)
        
        if self.alias_mode == 'none':
            return base_name
        
        elif self.alias_mode == 'add_prefix':
            return self.alias_prefix + base_name
        
        elif self.alias_mode == 'remove_prefix':
            if base_name.startswith(self.alias_prefix):
                return base_name[len(self.alias_prefix):]
            return base_name
        
        elif self.alias_mode == 'remove_suffix':
            if base_name.endswith(self.alias_suffix):
                return base_name[:-len(self.alias_suffix)]
            return base_name
        
        elif self.alias_mode == 'add_suffix':
            return base_name + self.alias_suffix
        
        elif self.alias_mode == 'slice':
            if len(base_name) < self.alias_end:
                return base_name
            return base_name[:self.alias_start] + base_name[self.alias_end:]
        
        return base_name
    
    def is_audio_file(self, filepath):
        audio_extensions = {
            '.mp3', '.flac', '.m4a', '.aac', '.ogg', '.wma', 
            '.aiff', '.aif', '.opus', '.wav', '.pcm', '.mp4',
            '.m4p', '.m4b', '.m4r', '.3gp', '.amr', '.awb'
        }
        
        ext = os.path.splitext(filepath)[1].lower()
        if ext in audio_extensions:
            return True
        
        try:
            with open(filepath, 'rb') as f:
                header = f.read(12)
                magic_bytes = {
                    b'ID3': True,
                    b'fLaC': True,
                    b'ftyp': True,
                    b'OggS': True,
                    b'RIFF': True,
                    b'FORM': True,
                    b'MThd': True,
                }
                for magic in magic_bytes:
                    if header[:len(magic)] == magic:
                        return True
        except:
            pass
        
        return False
    
    def is_wav_file(self, filepath):
        ext = os.path.splitext(filepath)[1].lower()
        if ext != '.wav':
            return False
        
        try:
            with open(filepath, 'rb') as f:
                header = f.read(12)
                return header[:4] == b'RIFF' and header[8:12] == b'WAVE'
        except:
            return False
    
    def detect_silence(self, wav_path):
        try:
            with wave.open(wav_path, 'rb') as wf:
                frames = wf.getnframes()
                rate = wf.getframerate()
                sampwidth = wf.getsampwidth()
                
                if sampwidth == 1:
                    max_val = 127
                    offset = 128
                elif sampwidth == 2:
                    max_val = 32768
                    offset = 0
                else:
                    return 0
                
                chunk_size = min(1024, frames)
                silent_samples = 0
                max_amplitude = 0
                scan_duration = min(rate // 10, frames)
                
                for _ in range(0, scan_duration, chunk_size):
                    data = wf.readframes(chunk_size)
                    if not data:
                        break
                    
                    samples = []
                    for i in range(0, len(data), sampwidth):
                        if sampwidth == 1:
                            sample = data[i] - offset
                        elif sampwidth == 2:
                            sample = int.from_bytes(data[i:i+2], 'little', signed=True)
                        else:
                            break
                        samples.append(sample)
                    
                    if len(samples) == 0:
                        break
                    
                    rms = (sum(s**2 for s in samples) / len(samples)) ** 0.5
                    normalized_rms = rms / max_val
                    max_amplitude = max(max_amplitude, normalized_rms)
                    
                    if normalized_rms > self.silence_threshold:
                        break
                    
                    silent_samples += len(samples)
                
                if max_amplitude < self.silence_threshold * 2:
                    return 0
                
                return int(silent_samples / rate * 1000)
        except:
            return 0
    
    def convert_to_wav(self, audio_path):
        if not self.check_ffmpeg():
            return None
        
        base_name = os.path.splitext(audio_path)[0]
        wav_path = base_name + '.wav'
        
        if not self.force_reconvert and os.path.exists(wav_path) and self.is_wav_file(wav_path):
            if os.path.getmtime(wav_path) >= os.path.getmtime(audio_path):
                return wav_path
        
        try:
            print(f"🔄 转换中: {os.path.basename(audio_path)} -> {os.path.basename(wav_path)}")
            
            cmd = [
                'ffmpeg',
                '-i', audio_path,
                '-ar', '44100',
                '-ac', '1',
                '-sample_fmt', 's16',
                '-y',
                wav_path
            ]
            
            result = subprocess.run(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=30
            )
            
            if result.returncode == 0 and os.path.exists(wav_path) and self.is_wav_file(wav_path):
                self.converted_files.append(audio_path)
                if self.temp_mode:
                    self.temp_wav_files.append(wav_path)
                print(f"✅ 转换成功: {os.path.basename(wav_path)}")
                return wav_path
            else:
                print(f"❌ 转换失败: {os.path.basename(audio_path)}")
                return None
                
        except subprocess.TimeoutExpired:
            print(f"⏰ 转换超时: {os.path.basename(audio_path)}")
            return None
        except Exception as e:
            print(f"❌ 转换出错 {os.path.basename(audio_path)}: {e}")
            return None
    
    def scan_audio_files(self, directory):
        all_files = []
        
        if self.recursive_scan:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    all_files.append(os.path.join(root, file))
        else:
            for file in os.listdir(directory):
                filepath = os.path.join(directory, file)
                if os.path.isfile(filepath):
                    all_files.append(filepath)
        
        all_files.sort(key=lambda x: os.path.basename(x))
        
        wav_files = []
        
        print(f"\n📂 扫描目录: {directory}")
        print(f"📊 共发现 {len(all_files)} 个文件")
        print("-"*60)
        
        for idx, filepath in enumerate(all_files, 1):
            filename = os.path.basename(filepath)
            
            progress_msg = f"🔍 扫描进度: {idx}/{len(all_files)}"
            print(f"{progress_msg:<50}", end='\r')
            
            if not self.is_audio_file(filepath):
                self.skipped_files.append(filepath)
                continue
            
            if self.is_wav_file(filepath):
                wav_files.append(filepath)
                continue
            
            print(f"\n🎵 发现非wav音频: {filename}")
            wav_path = self.convert_to_wav(filepath)
            
            if wav_path and os.path.exists(wav_path):
                wav_files.append(wav_path)
                if wav_path != filepath:
                    print(f"   💡 已生成: {os.path.basename(wav_path)}")
            else:
                print(f"   ⚠️  跳过文件: {filename} (转换失败)")
                self.skipped_files.append(filepath)
        
        print(f"\n✅ 扫描完成: 找到 {len(wav_files)} 个wav文件")
        if self.converted_files:
            print(f"   🔄 转换了 {len(self.converted_files)} 个文件为wav")
        if self.skipped_files:
            print(f"   ⏭️  跳过了 {len(self.skipped_files)} 个非音频文件")
        
        return wav_files
    
    def detect_abnormal_chars(self, filename):
        abnormal_pattern = re.compile(
            r'[\x00-\x1f\x7f-\x9f]'
            r'|[\u200b-\u200f\u2028-\u202f\u2060-\u206f]'
            r'|[\ufeff]'
            r'|[\u00ad\u034f\u180e]'
        )
        return bool(abnormal_pattern.search(filename))
    
    def clean_filename(self, filename):
        abnormal_pattern = re.compile(
            r'[\x00-\x1f\x7f-\x9f]'
            r'|[\u200b-\u200f\u2028-\u202f\u2060-\u206f]'
            r'|[\ufeff]'
            r'|[\u00ad\u034f\u180e]'
        )
        return abnormal_pattern.sub('', filename)
    
    def get_unique_filename(self, directory, base_name, extension):
        counter = 1
        new_name = base_name + extension
        new_path = os.path.join(directory, new_name)
        
        while os.path.exists(new_path):
            name_parts = base_name.rsplit('_', 1)
            if len(name_parts) > 1 and name_parts[1].isdigit():
                base_name = name_parts[0]
                counter = int(name_parts[1]) + 1
            else:
                counter += 1
            new_name = f"{base_name}_{counter}{extension}"
            new_path = os.path.join(directory, new_name)
        
        return new_name, new_path
    
    def get_wav_duration(self, wav_path):
        try:
            with wave.open(wav_path, 'rb') as wf:
                frames = wf.getnframes()
                rate = wf.getframerate()
                return int(frames / rate * 1000)
        except:
            if self.check_ffprobe():
                try:
                    result = subprocess.run(
                        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                         '-of', 'default=noprint_wrappers=1:nokey=1', wav_path],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.DEVNULL,
                        timeout=5
                    )
                    if result.returncode == 0 and result.stdout:
                        duration = float(result.stdout.decode().strip())
                        return int(duration * 1000)
                except:
                    pass
            
            print(f"⚠️  无法读取时长: {os.path.basename(wav_path)}")
            return 500
    
    def estimate_oto_params(self, wav_path):
        duration = self.get_wav_duration(wav_path)
        silence = self.detect_silence(wav_path)
        
        effective_duration = duration - silence
        
        if effective_duration < 200:
            params = {
                'offset': silence,
                'consonant': max(20, int(effective_duration * 0.15)),
                'cutoff': max(50, int(effective_duration * 0.5)),
                'preutterance': max(30, int(effective_duration * 0.2)),
                'overlap': max(20, int(effective_duration * 0.1))
            }
        elif effective_duration < 500:
            params = {
                'offset': silence,
                'consonant': max(50, int(effective_duration * 0.2)),
                'cutoff': max(100, int(effective_duration * 0.4)),
                'preutterance': max(60, int(effective_duration * 0.25)),
                'overlap': max(30, int(effective_duration * 0.12))
            }
        else:
            params = {
                'offset': silence,
                'consonant': max(80, int(effective_duration * 0.15)),
                'cutoff': max(150, int(effective_duration * 0.35)),
                'preutterance': max(80, int(effective_duration * 0.2)),
                'overlap': max(40, int(effective_duration * 0.1))
            }
        
        params['consonant'] = min(params['consonant'], effective_duration // 2)
        params['cutoff'] = min(params['cutoff'], effective_duration)
        params['preutterance'] = min(params['preutterance'], effective_duration // 2)
        params['overlap'] = min(params['overlap'], effective_duration // 4)
        
        return params
    
    def interactive_path_selection(self):
        print("\n" + "="*60)
        print("🔍 未找到音频文件")
        print("="*60)
        print("请选择操作:")
        print("  1. 输入音频文件夹路径（相对或绝对路径）")
        print("  2. 将本程序移动到音频文件夹所在目录")
        print("  3. 退出程序")
        print("="*60)
        print("💡 提示: 支持以下音频格式自动转wav")
        print("   MP3, FLAC, M4A, AAC, OGG, WMA, AIFF, OPUS 等")
        print("="*60)
        
        while True:
            print("\n💡 提示: 你可以拖拽文件夹到命令行窗口，或直接输入路径")
            user_input = input("📁 请输入文件夹路径: ").strip()
            
            user_input = user_input.strip('"\'')
            
            if user_input.lower() in ['exit', 'quit', 'q', '3']:
                print("👋 程序退出")
                sys.exit(0)
            
            if self.is_valid_directory(user_input):
                audio_files = self.scan_audio_files(user_input)
                if audio_files:
                    return user_input, audio_files
                else:
                    print(f"❌ 目录 '{user_input}' 下没有可用的音频文件")
                    print("💡 请检查目录是否包含支持的音频格式")
                    continue
            else:
                print(f"❌ 无效路径: '{user_input}'")
                print("💡 请确保路径正确且目录存在")
                continue
    
    def is_valid_directory(self, path):
        try:
            return os.path.isdir(path) and os.path.exists(path)
        except:
            return False
    
    def process_files(self, wav_files):
        if not wav_files:
            print("❌ 没有可用的wav文件！")
            return False
        
        print(f"\n🔧 开始处理 {len(wav_files)} 个wav文件")
        print("-"*60)
        
        for idx, wav_path in enumerate(wav_files, 1):
            filename = os.path.basename(wav_path)
            
            print(f"\n[{idx}/{len(wav_files)}] 处理: {filename}")
            
            if self.detect_abnormal_chars(filename):
                self.abnormal_files.append(filename)
                
                if self.clean_mode == 'ask':
                    print(f"⚠️  检测到异常字符: {filename}")
                    while True:
                        choice = input("输入 Y 剔除异常字符，输入 N 跳过此文件 (Y/N): ").strip().upper()
                        if choice == 'Y':
                            new_filename = self.clean_filename(filename)
                            if new_filename:
                                new_name, new_path = self.get_unique_filename(
                                    os.path.dirname(wav_path),
                                    os.path.splitext(new_filename)[0],
                                    os.path.splitext(wav_path)[1]
                                )
                                try:
                                    os.rename(wav_path, new_path)
                                    print(f"✅ 已重命名: {filename} -> {new_name}")
                                    filename = new_name
                                    wav_path = new_path
                                except Exception as e:
                                    print(f"❌ 重命名失败: {e}")
                                    continue
                            else:
                                print("❌ 清洗后文件名为空，跳过此文件")
                                continue
                            break
                        elif choice == 'N':
                            print(f"⏭️  跳过文件: {filename}")
                            break
                        else:
                            print("❌ 无效输入，请输入 Y 或 N")
                            continue
                elif self.clean_mode == 'auto':
                    new_filename = self.clean_filename(filename)
                    if new_filename and new_filename != filename:
                        new_name, new_path = self.get_unique_filename(
                            os.path.dirname(wav_path),
                            os.path.splitext(new_filename)[0],
                            os.path.splitext(wav_path)[1]
                        )
                        try:
                            os.rename(wav_path, new_path)
                            print(f"✅ 自动清洗: {filename} -> {new_name}")
                            filename = new_name
                            wav_path = new_path
                        except Exception as e:
                            print(f"❌ 清洗失败: {e}")
                    elif not new_filename:
                        print(f"⚠️  清洗后文件名为空，跳过: {filename}")
                        continue
                else:
                    print(f"⏭️  跳过异常文件: {filename}")
                    continue
            
            params = self.estimate_oto_params(wav_path)
            alias = self.apply_alias(filename)
            
            self.notes.append({
                'filename': filename,
                'alias': alias,
                **params
            })
            
            duration = self.get_wav_duration(wav_path)
            silence = self.detect_silence(wav_path)
            print(f"✅ 已处理: {filename} (别名: {alias}, 时长: {duration}ms, 静音: {silence}ms, offset: {params['offset']}ms)")
        
        return True
    
    def generate_oto(self):
        if not self.notes:
            print("❌ 没有有效数据可生成")
            return False
        
        try:
            with open(self.output_path, 'w', encoding=self.encoding) as f:
                f.write('[#VERSION]\n')
                f.write('VERSION=100\n\n')
                
                for note in self.notes:
                    line = (f"{note['filename']}={note['alias']},"
                            f"{note['offset']},{note['consonant']},"
                            f"{note['cutoff']},{note['preutterance']},"
                            f"{note['overlap']}\n")
                    f.write(line)
            
            print(f"\n✅ oto.ini 已生成: {os.path.abspath(self.output_path)}")
            print(f"📊 共 {len(self.notes)} 条配置")
            print(f"🔤 编码格式: {self.encoding}")
            return True
        except Exception as e:
            print(f"❌ 生成失败: {e}")
            return False
    
    def cleanup_temp_files(self):
        if self.cleanup_done:
            return
        if self.temp_mode and self.temp_wav_files:
            print(f"\n🧹 清理临时wav文件...")
            for wav_path in self.temp_wav_files:
                try:
                    if os.path.exists(wav_path):
                        os.remove(wav_path)
                        print(f"   ✅ 删除: {os.path.basename(wav_path)}")
                except Exception as e:
                    print(f"   ❌ 删除失败: {os.path.basename(wav_path)} - {e}")
        self.cleanup_done = True
    
    def run(self):
        try:
            print("="*60)
            print(f"🎵 OTO.ini 智能生成器 v{VERSION} (带音频转换)")
            print("="*60)
            
            print("\n生成器正在加载…")
            print("生成器加载完成，正在加载编码选择器…")
            print("正在加载你的好心情…")
            
            print("正在检测你使用的软件…")
            self.detect_platform()
            
            self.select_encoding()
            self.select_clean_mode()
            self.select_temp_mode()
            self.select_reconvert_mode()
            self.select_scan_mode()
            self.select_silence_threshold()
            self.select_alias_mode()
            self.select_romaji_fix()
            
            self.check_ffmpeg()
            self.check_ffprobe()
            
            if self.ffmpeg_available:
                print("✅ FFmpeg 已就绪，支持自动转换音频格式")
            else:
                print("⚠️  FFmpeg 未安装，只支持wav格式")
                print("💡 建议安装FFmpeg以支持更多音频格式")
            
            if not self.ffprobe_available:
                print("⚠️  ffprobe 未安装，时长读取可能回退到500ms")
            
            if self.wav_dir is None:
                self.wav_dir = os.getcwd()
            
            print(f"\n📁 默认目录: {os.path.abspath(self.wav_dir)}")
            
            audio_files = self.scan_audio_files(self.wav_dir)
            
            if not audio_files:
                self.wav_dir, audio_files = self.interactive_path_selection()
            else:
                print(f"\n💡 当前目录找到 {len(audio_files)} 个可用音频文件")
                print("   如果想处理其他目录，可以输入新路径")
                print("   直接按回车继续使用当前目录")
                print("   输入 'q' 退出程序")
                
                user_input = input("\n📁 请输入新路径（或按回车继续）: ").strip()
                
                if user_input.lower() in ['q', 'quit', 'exit']:
                    print("👋 程序退出")
                    sys.exit(0)
                
                if user_input:
                    user_input = user_input.strip('"\'')
                    if self.is_valid_directory(user_input):
                        new_audio = self.scan_audio_files(user_input)
                        if new_audio:
                            self.wav_dir = user_input
                            audio_files = new_audio
                            print(f"✅ 切换到新目录: {self.wav_dir}")
                        else:
                            print(f"⚠️  目录 '{user_input}' 下没有音频文件，继续使用当前目录")
                    else:
                        print(f"⚠️  无效路径，继续使用当前目录")
            
            print("\n" + "="*60)
            print(f"📁 处理目录: {os.path.abspath(self.wav_dir)}")
            print("="*60)
            
            if not self.process_files(audio_files):
                return False
            
            if self.abnormal_files:
                print(f"\n⚠️  共有 {len(self.abnormal_files)} 个文件包含异常字符")
                print("   请检查这些文件是否处理成功:")
                for f in self.abnormal_files:
                    print(f"   - {f}")
            
            if self.converted_files:
                print(f"\n🔄 共转换了 {len(self.converted_files)} 个音频文件为wav:")
                for f in self.converted_files:
                    print(f"   - {os.path.basename(f)}")
            
            if self.skipped_files:
                print(f"\n⏭️  跳过了 {len(self.skipped_files)} 个非音频文件")
            
            self.output_path = os.path.join(self.wav_dir, 'oto.ini')
            self.generate_oto()
            
            self.cleanup_temp_files()
            
            print("\n" + "="*60)
            print("✨ 生成完成！")
            print(f"📁 oto.ini 位置: {os.path.abspath(self.output_path)}")
            print("💡 请将此文件与音频文件放在同一目录下供UTAU使用")
            print("="*60)
            return True
        finally:
            self.running = False
            self.emergency_cleanup()

if __name__ == '__main__':
    try:
        generator = OtoGenerator()
        generator.run()
        
        print("\n按回车键退出...")
        input()
    except KeyboardInterrupt:
        print("\n\n👋 程序被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 程序出错: {e}")
        import traceback
        traceback.print_exc()
        input("按回车键退出...")
        sys.exit(1)
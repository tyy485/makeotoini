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

VERSION = "3.7"

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
        self.language = 'japanese'
        self.ui_language = 'zh'
        
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
        
        self.hangul_to_roman = {
            '가': 'ga', '나': 'na', '다': 'da', '라': 'ra', '마': 'ma',
            '바': 'ba', '사': 'sa', '아': 'a', '자': 'ja', '차': 'cha',
            '카': 'ka', '타': 'ta', '파': 'pa', '하': 'ha',
            '거': 'geo', '너': 'neo', '더': 'deo', '러': 'reo', '머': 'meo',
            '버': 'beo', '서': 'seo', '어': 'eo', '저': 'jeo', '처': 'cheo',
            '커': 'keo', '터': 'teo', '퍼': 'peo', '허': 'heo',
            '고': 'go', '노': 'no', '도': 'do', '로': 'ro', '모': 'mo',
            '보': 'bo', '소': 'so', '오': 'o', '조': 'jo', '초': 'cho',
            '코': 'ko', '토': 'to', '포': 'po', '호': 'ho',
            '구': 'gu', '누': 'nu', '두': 'du', '루': 'ru', '무': 'mu',
            '부': 'bu', '수': 'su', '우': 'u', '주': 'ju', '추': 'chu',
            '쿠': 'ku', '투': 'tu', '푸': 'pu', '후': 'hu',
            '그': 'geu', '느': 'neu', '드': 'deu', '르': 'reu', '므': 'meu',
            '브': 'beu', '스': 'seu', '으': 'eu', '즈': 'jeu', '츠': 'cheu',
            '크': 'keu', '트': 'teu', '프': 'peu', '흐': 'heu',
            '기': 'gi', '니': 'ni', '디': 'di', '리': 'ri', '미': 'mi',
            '비': 'bi', '시': 'si', '이': 'i', '지': 'ji', '치': 'chi',
            '키': 'ki', '티': 'ti', '피': 'pi', '히': 'hi',
            '깨': 'ggae', '껴': 'ggyeo', '꼬': 'ggo', '뀌': 'ggwi', '끼': 'ggi',
            '째': 'jjae', '쪄': 'jjyeo', '쬬': 'jjyo', '쭈': 'jju', '찌': 'jji'
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
        
        self.ui_texts = {
            'zh': {
                'title': '🎵 OTO.ini 智能生成器 v{version} (带音频转换)',
                'loading': '生成器正在加载…',
                'loading_done': '生成器加载完成，正在加载编码选择器…',
                'loading_mood': '正在加载你的好心情…',
                'detecting': '正在检测你使用的软件…',
                'language_select': '🌍 请选择音源语言',
                'language_jp': '1. 日本語 (Japanese)',
                'language_zh': '2. 中文 (Chinese)',
                'language_ko': '3. 한국어 (Korean)',
                'language_en': '4. English',
                'lang_choice': '请输入语言序号 (1/2/3/4): ',
                'lang_jp': '日本語',
                'lang_zh': '中文',
                'lang_ko': '한국어',
                'lang_en': 'English',
                'ui_language_select': '🌐 请选择工具界面语言',
                'ui_zh': '1. 中文',
                'ui_en': '2. English',
                'ui_choice': '请输入语言序号 (1/2): ',
                'ui_zh_done': '中文',
                'ui_en_done': 'English',
                'encoding_select': '📝 请选择你的oto编码',
                'encoding_gb': '1. GB 2312',
                'encoding_sjis': '2. Shift-JIS',
                'encoding_choice': '请输入编码序号: ',
                'encoding_gb_done': 'GB 2312 编码',
                'encoding_sjis_done': 'Shift-JIS 编码',
                'encoding_utf8': 'UTF-8 编码',
                'clean_select': '🧹 异常文件名处理模式',
                'clean_ask': '1. 逐个询问 (适合少量文件)',
                'clean_auto': '2. 全部自动清洗',
                'clean_skip': '3. 全部跳过',
                'clean_choice': '请选择处理模式 (1/2/3): ',
                'clean_ask_done': '逐个询问模式',
                'clean_auto_done': '全部自动清洗',
                'clean_skip_done': '全部跳过',
                'temp_select': '📦 转换文件处理模式',
                'temp_keep': '1. 永久保留转换的wav文件',
                'temp_temp': '2. 临时转换，生成oto后删除',
                'temp_choice': '请选择处理模式 (1/2): ',
                'temp_keep_done': '永久保留wav文件',
                'temp_temp_done': '临时转换模式',
                'reconvert_select': '🔄 转换模式',
                'reconvert_force': '1. 强制重新转换 (覆盖已有wav)',
                'reconvert_reuse': '2. 复用已有wav (加快速度)',
                'reconvert_choice': '请选择转换模式 (1/2): ',
                'reconvert_force_done': '强制重新转换',
                'reconvert_reuse_done': '复用已有wav',
                'scan_select': '📂 扫描模式',
                'scan_recursive': '1. 递归扫描子文件夹',
                'scan_current': '2. 仅扫描当前目录',
                'scan_choice': '请选择扫描模式 (1/2): ',
                'scan_recursive_done': '递归扫描',
                'scan_current_done': '仅扫描当前目录',
                'silence_select': '🎚️  静音检测灵敏度',
                'silence_low': '1. 低灵敏度 (0.02) - 适合响亮的录音',
                'silence_medium': '2. 中灵敏度 (0.01) - 适合普通录音 [默认]',
                'silence_high': '3. 高灵敏度 (0.005) - 适合小声录音',
                'silence_manual': '4. 手动输入阈值 (0.001-0.1)',
                'silence_choice': '请选择灵敏度 (1/2/3/4): ',
                'silence_low_done': '低灵敏度 (阈值: {threshold})',
                'silence_medium_done': '中灵敏度 (阈值: {threshold})',
                'silence_high_done': '高灵敏度 (阈值: {threshold})',
                'silence_manual_input': '请输入阈值 (0.001-0.1): ',
                'silence_manual_done': '已设置阈值: {threshold}',
                'alias_select': '🏷️  别名 (Alias) 自定义模式',
                'alias_none': '1. 不使用别名处理 (直接用文件名)',
                'alias_add_prefix': '2. 批量添加前缀 (如: x_)',
                'alias_remove_prefix': '3. 批量删除前缀 (如: 删除 x_)',
                'alias_remove_suffix': '4. 批量删除后缀 (如: 删除 _x)',
                'alias_add_suffix': '5. 批量添加后缀 (如: _x)',
                'alias_slice': '6. 删除指定字符范围 (如: 删除第1-3个字符)',
                'alias_choice': '请选择别名模式 (1/2/3/4/5/6): ',
                'alias_none_done': '不使用别名处理',
                'alias_add_prefix_done': '批量添加前缀 \'{prefix}\'',
                'alias_remove_prefix_done': '批量删除前缀 \'{prefix}\'',
                'alias_remove_suffix_done': '批量删除后缀 \'{suffix}\'',
                'alias_add_suffix_done': '批量添加后缀 \'{suffix}\'',
                'alias_prefix_input': '请输入要添加的前缀: ',
                'alias_prefix_remove_input': '请输入要删除的前缀: ',
                'alias_suffix_remove_input': '请输入要删除的后缀: ',
                'alias_suffix_input': '请输入要添加的后缀: ',
                'alias_slice_hint': '\n💡 提示: 字符位置从1开始计数，如文件名 \'abcde\'\n   删除 1-3 得到 \'de\'\n   删除 3-5 得到 \'ab\'\n   删除 2-4 得到 \'ae\'',
                'alias_slice_start': '请输入起始字符位置: ',
                'alias_slice_end': '请输入结束字符位置: ',
                'alias_slice_done': '删除第 {start} 到第 {end} 个字符',
                'romaji_fix_select': '🔧 罗马音自动修复',
                'romaji_fix_enable': '1. 启用自动修复 (将short/long等替换为正确罗马音)',
                'romaji_fix_disable': '2. 禁用自动修复',
                'romaji_fix_choice': '请选择 (1/2): ',
                'romaji_fix_enabled': '已启用: 罗马音自动修复',
                'romaji_fix_disabled': '已禁用: 罗马音自动修复',
                'romaji_fix_skip': 'ℹ️  当前语言不支持罗马音修复，已自动禁用',
                'ffmpeg_ready': '✅ FFmpeg 已就绪，支持自动转换音频格式',
                'ffmpeg_missing': '⚠️  FFmpeg 未安装，只支持wav格式',
                'ffmpeg_hint': '💡 建议安装FFmpeg以支持更多音频格式',
                'ffprobe_missing': '⚠️  ffprobe 未安装，时长读取可能回退到500ms',
                'default_dir': '📁 默认目录: {path}',
                'scanning': '📂 扫描目录: {directory}',
                'scan_files': '📊 共发现 {count} 个文件',
                'scan_progress': '🔍 扫描进度: {current}/{total}',
                'scan_found_audio': '🎵 发现非wav音频: {filename}',
                'convert_success': '✅ 转换成功: {filename}',
                'convert_fail': '❌ 转换失败: {filename}',
                'convert_skip': '⚠️  跳过文件: {filename} (转换失败)',
                'converted_generated': '💡 已生成: {filename}',
                'scan_complete': '✅ 扫描完成: 找到 {count} 个wav文件',
                'converted_count': '   🔄 转换了 {count} 个文件为wav',
                'skipped_count': '   ⏭️  跳过了 {count} 个非音频文件',
                'processing_start': '🔧 开始处理 {count} 个wav文件',
                'processing_file': '[{idx}/{total}] 处理: {filename}',
                'abnormal_detected': '⚠️  检测到异常字符: {filename}',
                'abnormal_choice': '输入 Y 剔除异常字符，输入 N 跳过此文件 (Y/N): ',
                'abnormal_renamed': '✅ 已重命名: {old} -> {new}',
                'abnormal_rename_fail': '❌ 重命名失败: {error}',
                'abnormal_empty': '❌ 清洗后文件名为空，跳过此文件',
                'abnormal_skip': '⏭️  跳过文件: {filename}',
                'abnormal_invalid': '❌ 无效输入，请输入 Y 或 N',
                'abnormal_auto_clean': '✅ 自动清洗: {old} -> {new}',
                'abnormal_auto_fail': '❌ 清洗失败: {error}',
                'abnormal_auto_empty': '⚠️  清洗后文件名为空，跳过: {filename}',
                'abnormal_skip_all': '⏭️  跳过异常文件: {filename}',
                'processed': '✅ 已处理: {filename} (别名: {alias}, 时长: {duration}ms, 静音: {silence}ms, offset: {offset}ms)',
                'romaji_fix': '   🔧 修复罗马音: {old} -> {new}',
                'no_wav': '❌ 没有可用的wav文件！',
                'generate_success': '✅ oto.ini 已生成: {path}',
                'generate_count': '📊 共 {count} 条配置',
                'generate_encoding': '🔤 编码格式: {encoding}',
                'generate_fail': '❌ 生成失败: {error}',
                'cleanup_temp': '🧹 清理临时wav文件...',
                'cleanup_deleted': '   ✅ 删除: {filename}',
                'cleanup_fail': '   ❌ 删除失败: {filename} - {error}',
                'abnormal_summary': '\n⚠️  共有 {count} 个文件包含异常字符',
                'abnormal_summary_list': '   请检查这些文件是否处理成功:',
                'converted_summary': '\n🔄 共转换了 {count} 个音频文件为wav:',
                'skipped_summary': '\n⏭️  跳过了 {count} 个非音频文件',
                'complete': '\n✨ 生成完成！',
                'complete_path': '📁 oto.ini 位置: {path}',
                'complete_hint': '💡 请将此文件与音频文件放在同一目录下供UTAU使用',
                'dir_found': '📁 默认目录: {path}',
                'dir_current': '\n💡 当前目录找到 {count} 个可用音频文件',
                'dir_hint': '   如果想处理其他目录，可以输入新路径\n   直接按回车继续使用当前目录\n   输入 \'q\' 退出程序',
                'dir_input': '\n📁 请输入新路径（或按回车继续）: ',
                'dir_switched': '✅ 切换到新目录: {path}',
                'dir_no_audio': '⚠️  目录 \'{path}\' 下没有音频文件，继续使用当前目录',
                'dir_invalid': '⚠️  无效路径，继续使用当前目录',
                'dir_processing': '\n📁 处理目录: {path}',
                'exit': '👋 程序退出',
                'invalid_choice': '❌ 无效选择，请输入 {range}',
                'invalid_number': '❌ 请输入有效的数字',
                'invalid_range': '❌ 起始位置不能大于结束位置',
                'invalid_min': '❌ 起始和结束位置必须 >= 1',
                'threshold_range': '❌ 阈值必须在 0.001 到 0.1 之间',
                'no_audio_found': '🔍 未找到音频文件',
                'no_audio_menu': '请选择操作:\n  1. 输入音频文件夹路径（相对或绝对路径）\n  2. 将本程序移动到音频文件夹所在目录\n  3. 退出程序',
                'no_audio_hint': '💡 提示: 支持以下音频格式自动转wav\n   MP3, FLAC, M4A, AAC, OGG, WMA, AIFF, OPUS 等',
                'no_audio_input': '📁 请输入文件夹路径: ',
                'no_audio_error': '❌ 目录 \'{path}\' 下没有可用的音频文件',
                'no_audio_check': '💡 请检查目录是否包含支持的音频格式',
                'path_invalid': '❌ 无效路径: \'{path}\'',
                'path_hint': '💡 请确保路径正确且目录存在',
                'drag_hint': '💡 提示: 你可以拖拽文件夹到命令行窗口，或直接输入路径',
            },
            'en': {
                'title': '🎵 OTO.ini Smart Generator v{version} (with Audio Conversion)',
                'loading': 'Generator loading…',
                'loading_done': 'Generator loaded, loading encoding selector…',
                'loading_mood': 'Loading your good mood…',
                'detecting': 'Detecting your software…',
                'language_select': '🌍 Select voicebank language',
                'language_jp': '1. 日本語 (Japanese)',
                'language_zh': '2. 中文 (Chinese)',
                'language_ko': '3. 한국어 (Korean)',
                'language_en': '4. English',
                'lang_choice': 'Enter language number (1/2/3/4): ',
                'lang_jp': 'Japanese',
                'lang_zh': 'Chinese',
                'lang_ko': 'Korean',
                'lang_en': 'English',
                'ui_language_select': '🌐 Select UI language',
                'ui_zh': '1. 中文',
                'ui_en': '2. English',
                'ui_choice': 'Enter language number (1/2): ',
                'ui_zh_done': 'Chinese',
                'ui_en_done': 'English',
                'encoding_select': '📝 Select your oto encoding',
                'encoding_gb': '1. GB 2312',
                'encoding_sjis': '2. Shift-JIS',
                'encoding_choice': 'Enter encoding number: ',
                'encoding_gb_done': 'GB 2312 encoding',
                'encoding_sjis_done': 'Shift-JIS encoding',
                'encoding_utf8': 'UTF-8 encoding',
                'clean_select': '🧹 Abnormal filename handling mode',
                'clean_ask': '1. Ask one by one (for small batches)',
                'clean_auto': '2. Auto clean all',
                'clean_skip': '3. Skip all',
                'clean_choice': 'Select mode (1/2/3): ',
                'clean_ask_done': 'Ask one by one mode',
                'clean_auto_done': 'Auto clean all',
                'clean_skip_done': 'Skip all',
                'temp_select': '📦 Converted file handling mode',
                'temp_keep': '1. Keep converted wav files permanently',
                'temp_temp': '2. Temporary conversion, delete after generating oto',
                'temp_choice': 'Select mode (1/2): ',
                'temp_keep_done': 'Keep wav files permanently',
                'temp_temp_done': 'Temporary conversion mode',
                'reconvert_select': '🔄 Conversion mode',
                'reconvert_force': '1. Force reconvert (overwrite existing wav)',
                'reconvert_reuse': '2. Reuse existing wav (faster)',
                'reconvert_choice': 'Select mode (1/2): ',
                'reconvert_force_done': 'Force reconvert',
                'reconvert_reuse_done': 'Reuse existing wav',
                'scan_select': '📂 Scan mode',
                'scan_recursive': '1. Recursive scan subfolders',
                'scan_current': '2. Scan current directory only',
                'scan_choice': 'Select mode (1/2): ',
                'scan_recursive_done': 'Recursive scan',
                'scan_current_done': 'Current directory only',
                'silence_select': '🎚️  Silence detection sensitivity',
                'silence_low': '1. Low (0.02) - for loud recordings',
                'silence_medium': '2. Medium (0.01) - for normal recordings [default]',
                'silence_high': '3. High (0.005) - for quiet recordings',
                'silence_manual': '4. Manual input (0.001-0.1)',
                'silence_choice': 'Select sensitivity (1/2/3/4): ',
                'silence_low_done': 'Low sensitivity (threshold: {threshold})',
                'silence_medium_done': 'Medium sensitivity (threshold: {threshold})',
                'silence_high_done': 'High sensitivity (threshold: {threshold})',
                'silence_manual_input': 'Enter threshold (0.001-0.1): ',
                'silence_manual_done': 'Threshold set: {threshold}',
                'alias_select': '🏷️  Alias custom mode',
                'alias_none': '1. No alias processing (use filename directly)',
                'alias_add_prefix': '2. Add prefix (e.g.: x_)',
                'alias_remove_prefix': '3. Remove prefix (e.g.: remove x_)',
                'alias_remove_suffix': '4. Remove suffix (e.g.: remove _x)',
                'alias_add_suffix': '5. Add suffix (e.g.: _x)',
                'alias_slice': '6. Remove character range (e.g.: remove 1st-3rd chars)',
                'alias_choice': 'Select alias mode (1/2/3/4/5/6): ',
                'alias_none_done': 'No alias processing',
                'alias_add_prefix_done': 'Add prefix \'{prefix}\'',
                'alias_remove_prefix_done': 'Remove prefix \'{prefix}\'',
                'alias_remove_suffix_done': 'Remove suffix \'{suffix}\'',
                'alias_add_suffix_done': 'Add suffix \'{suffix}\'',
                'alias_prefix_input': 'Enter prefix to add: ',
                'alias_prefix_remove_input': 'Enter prefix to remove: ',
                'alias_suffix_remove_input': 'Enter suffix to remove: ',
                'alias_suffix_input': 'Enter suffix to add: ',
                'alias_slice_hint': '\n💡 Tip: Character positions start from 1, e.g. filename \'abcde\'\n   Remove 1-3 gives \'de\'\n   Remove 3-5 gives \'ab\'\n   Remove 2-4 gives \'ae\'',
                'alias_slice_start': 'Enter start position: ',
                'alias_slice_end': 'Enter end position: ',
                'alias_slice_done': 'Remove from {start} to {end}',
                'romaji_fix_select': '🔧 Romaji auto fix',
                'romaji_fix_enable': '1. Enable auto fix (replace short/long with correct romaji)',
                'romaji_fix_disable': '2. Disable auto fix',
                'romaji_fix_choice': 'Select (1/2): ',
                'romaji_fix_enabled': 'Enabled: Romaji auto fix',
                'romaji_fix_disabled': 'Disabled: Romaji auto fix',
                'romaji_fix_skip': 'ℹ️  Current language does not support romaji fix, disabled automatically',
                'ffmpeg_ready': '✅ FFmpeg ready, supports auto audio conversion',
                'ffmpeg_missing': '⚠️  FFmpeg not installed, only wav format supported',
                'ffmpeg_hint': '💡 Install FFmpeg for more audio formats',
                'ffprobe_missing': '⚠️  ffprobe not installed, duration may fallback to 500ms',
                'default_dir': '📁 Default directory: {path}',
                'scanning': '📂 Scanning: {directory}',
                'scan_files': '📊 Found {count} files',
                'scan_progress': '🔍 Scanning: {current}/{total}',
                'scan_found_audio': '🎵 Found non-wav audio: {filename}',
                'convert_success': '✅ Converted: {filename}',
                'convert_fail': '❌ Conversion failed: {filename}',
                'convert_skip': '⚠️  Skipped: {filename} (conversion failed)',
                'converted_generated': '💡 Generated: {filename}',
                'scan_complete': '✅ Scan complete: found {count} wav files',
                'converted_count': '   🔄 Converted {count} files to wav',
                'skipped_count': '   ⏭️  Skipped {count} non-audio files',
                'processing_start': '🔧 Processing {count} wav files',
                'processing_file': '[{idx}/{total}] Processing: {filename}',
                'abnormal_detected': '⚠️  Abnormal characters detected: {filename}',
                'abnormal_choice': 'Enter Y to remove characters, N to skip (Y/N): ',
                'abnormal_renamed': '✅ Renamed: {old} -> {new}',
                'abnormal_rename_fail': '❌ Rename failed: {error}',
                'abnormal_empty': '❌ Filename empty after cleaning, skipped',
                'abnormal_skip': '⏭️  Skipped: {filename}',
                'abnormal_invalid': '❌ Invalid input, enter Y or N',
                'abnormal_auto_clean': '✅ Auto cleaned: {old} -> {new}',
                'abnormal_auto_fail': '❌ Cleaning failed: {error}',
                'abnormal_auto_empty': '⚠️  Empty filename after cleaning, skipped: {filename}',
                'abnormal_skip_all': '⏭️  Skipped abnormal file: {filename}',
                'processed': '✅ Processed: {filename} (alias: {alias}, duration: {duration}ms, silence: {silence}ms, offset: {offset}ms)',
                'romaji_fix': '   🔧 Fixed romaji: {old} -> {new}',
                'no_wav': '❌ No wav files available!',
                'generate_success': '✅ oto.ini generated: {path}',
                'generate_count': '📊 {count} entries',
                'generate_encoding': '🔤 Encoding: {encoding}',
                'generate_fail': '❌ Generation failed: {error}',
                'cleanup_temp': '🧹 Cleaning temporary wav files...',
                'cleanup_deleted': '   ✅ Deleted: {filename}',
                'cleanup_fail': '   ❌ Delete failed: {filename} - {error}',
                'abnormal_summary': '\n⚠️  {count} files contain abnormal characters',
                'abnormal_summary_list': '   Check these files:',
                'converted_summary': '\n🔄 Converted {count} audio files to wav:',
                'skipped_summary': '\n⏭️  Skipped {count} non-audio files',
                'complete': '\n✨ Generation complete!',
                'complete_path': '📁 oto.ini location: {path}',
                'complete_hint': '💡 Place this file with audio files in the same directory for UTAU',
                'dir_found': '📁 Default directory: {path}',
                'dir_current': '\n💡 Found {count} audio files in current directory',
                'dir_hint': '   Enter new path to process other directory\n   Press Enter to continue with current directory\n   Enter \'q\' to exit',
                'dir_input': '\n📁 Enter new path (or press Enter to continue): ',
                'dir_switched': '✅ Switched to: {path}',
                'dir_no_audio': '⚠️  No audio files in \'{path}\', continuing with current directory',
                'dir_invalid': '⚠️  Invalid path, continuing with current directory',
                'dir_processing': '\n📁 Processing: {path}',
                'exit': '👋 Exiting',
                'invalid_choice': '❌ Invalid choice, enter {range}',
                'invalid_number': '❌ Enter a valid number',
                'invalid_range': '❌ Start position cannot be greater than end position',
                'invalid_min': '❌ Start and end positions must be >= 1',
                'threshold_range': '❌ Threshold must be between 0.001 and 0.1',
                'no_audio_found': '🔍 No audio files found',
                'no_audio_menu': 'Select action:\n  1. Enter audio folder path\n  2. Move program to audio folder directory\n  3. Exit',
                'no_audio_hint': '💡 Supports auto conversion from: MP3, FLAC, M4A, AAC, OGG, WMA, AIFF, OPUS etc.',
                'no_audio_input': '📁 Enter folder path: ',
                'no_audio_error': '❌ No audio files in \'{path}\'',
                'no_audio_check': '💡 Check if directory contains supported audio formats',
                'path_invalid': '❌ Invalid path: \'{path}\'',
                'path_hint': '💡 Make sure the path is correct and directory exists',
                'drag_hint': '💡 Drag folder to command window, or enter path directly',
            }
        }
        
    def t(self, key, **kwargs):
        text = self.ui_texts[self.ui_language].get(key, key)
        if kwargs:
            return text.format(**kwargs)
        return text
        
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
            print(self.t('ffmpeg_missing'))
            print(self.t('ffmpeg_hint'))
        
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
    
    def select_ui_language(self):
        print("\n" + "="*60)
        print(self.t('ui_language_select'))
        print("="*60)
        print(self.t('ui_zh'))
        print(self.t('ui_en'))
        print("="*60)
        
        while True:
            choice = input(self.t('ui_choice')).strip()
            
            if choice == '1' or choice.lower() in ['zh', '中文']:
                self.ui_language = 'zh'
                print(f"✅ {self.t('ui_zh_done')}")
                return
            elif choice == '2' or choice.lower() in ['en', 'english']:
                self.ui_language = 'en'
                print(f"✅ {self.t('ui_en_done')}")
                return
            else:
                print(self.t('invalid_choice', range='1 或 2'))
                continue
    
    def select_language(self):
        print("\n" + "="*60)
        print(self.t('language_select'))
        print("="*60)
        print(self.t('language_jp'))
        print(self.t('language_zh'))
        print(self.t('language_ko'))
        print(self.t('language_en'))
        print("="*60)
        
        while True:
            choice = input(self.t('lang_choice')).strip()
            
            if choice == '1' or choice.lower() in ['japanese', 'ja', '日', '日本']:
                self.language = 'japanese'
                print(f"✅ {self.t('lang_jp')}")
                return
            elif choice == '2' or choice.lower() in ['chinese', 'zh', '中', '中文']:
                self.language = 'chinese'
                print(f"✅ {self.t('lang_zh')}")
                return
            elif choice == '3' or choice.lower() in ['korean', 'ko', '한', '한국']:
                self.language = 'korean'
                print(f"✅ {self.t('lang_ko')}")
                return
            elif choice == '4' or choice.lower() in ['english', 'en', '英']:
                self.language = 'english'
                print(f"✅ {self.t('lang_en')}")
                return
            else:
                print(self.t('invalid_choice', range='1、2、3 或 4'))
                continue
    
    def select_encoding(self):
        print("\n" + "="*60)
        print(self.t('encoding_select'))
        print("="*60)
        print(self.t('encoding_gb'))
        print(self.t('encoding_sjis'))
        print("="*60)
        
        while True:
            choice = input(self.t('encoding_choice')).strip()
            
            if choice == '1' or choice.lower() == 'gb2312' or choice.lower() == 'gb 2312':
                self.encoding = 'gb2312'
                print(f"✅ {self.t('encoding_gb_done')}")
                return
            elif choice == '2' or choice.lower() == 'shift-jis' or choice.lower() == 'shiftjis':
                self.encoding = 'shift-jis'
                print(f"✅ {self.t('encoding_sjis_done')}")
                return
            elif choice.lower() == 'unicode' or choice.lower() == 'utf-8' or choice.lower() == 'utf8':
                self.encoding = 'utf-8'
                print(f"✅ {self.t('encoding_utf8')}")
                return
            else:
                print(self.t('invalid_choice', range='1 或 2'))
                continue
    
    def select_clean_mode(self):
        print("\n" + "="*60)
        print(self.t('clean_select'))
        print("="*60)
        print(self.t('clean_ask'))
        print(self.t('clean_auto'))
        print(self.t('clean_skip'))
        print("="*60)
        
        while True:
            choice = input(self.t('clean_choice')).strip()
            
            if choice == '1':
                self.clean_mode = 'ask'
                print(f"✅ {self.t('clean_ask_done')}")
                return
            elif choice == '2':
                self.clean_mode = 'auto'
                print(f"✅ {self.t('clean_auto_done')}")
                return
            elif choice == '3':
                self.clean_mode = 'skip'
                print(f"✅ {self.t('clean_skip_done')}")
                return
            else:
                print(self.t('invalid_choice', range='1、2 或 3'))
                continue
    
    def select_temp_mode(self):
        print("\n" + "="*60)
        print(self.t('temp_select'))
        print("="*60)
        print(self.t('temp_keep'))
        print(self.t('temp_temp'))
        print("="*60)
        
        while True:
            choice = input(self.t('temp_choice')).strip()
            
            if choice == '1':
                self.temp_mode = False
                print(f"✅ {self.t('temp_keep_done')}")
                return
            elif choice == '2':
                self.temp_mode = True
                print(f"✅ {self.t('temp_temp_done')}")
                return
            else:
                print(self.t('invalid_choice', range='1 或 2'))
                continue
    
    def select_reconvert_mode(self):
        print("\n" + "="*60)
        print(self.t('reconvert_select'))
        print("="*60)
        print(self.t('reconvert_force'))
        print(self.t('reconvert_reuse'))
        print("="*60)
        
        while True:
            choice = input(self.t('reconvert_choice')).strip()
            
            if choice == '1':
                self.force_reconvert = True
                print(f"✅ {self.t('reconvert_force_done')}")
                return
            elif choice == '2':
                self.force_reconvert = False
                print(f"✅ {self.t('reconvert_reuse_done')}")
                return
            else:
                print(self.t('invalid_choice', range='1 或 2'))
                continue
    
    def select_scan_mode(self):
        print("\n" + "="*60)
        print(self.t('scan_select'))
        print("="*60)
        print(self.t('scan_recursive'))
        print(self.t('scan_current'))
        print("="*60)
        
        while True:
            choice = input(self.t('scan_choice')).strip()
            
            if choice == '1':
                self.recursive_scan = True
                print(f"✅ {self.t('scan_recursive_done')}")
                return
            elif choice == '2':
                self.recursive_scan = False
                print(f"✅ {self.t('scan_current_done')}")
                return
            else:
                print(self.t('invalid_choice', range='1 或 2'))
                continue
    
    def select_silence_threshold(self):
        print("\n" + "="*60)
        print(self.t('silence_select'))
        print("="*60)
        print(self.t('silence_low'))
        print(self.t('silence_medium'))
        print(self.t('silence_high'))
        print(self.t('silence_manual'))
        print("="*60)
        
        while True:
            choice = input(self.t('silence_choice')).strip()
            
            if choice == '1':
                self.silence_threshold = 0.02
                print(f"✅ {self.t('silence_low_done', threshold=self.silence_threshold)}")
                return
            elif choice == '2':
                self.silence_threshold = 0.01
                print(f"✅ {self.t('silence_medium_done', threshold=self.silence_threshold)}")
                return
            elif choice == '3':
                self.silence_threshold = 0.005
                print(f"✅ {self.t('silence_high_done', threshold=self.silence_threshold)}")
                return
            elif choice == '4':
                while True:
                    try:
                        threshold = float(input(self.t('silence_manual_input')).strip())
                        if 0.001 <= threshold <= 0.1:
                            self.silence_threshold = threshold
                            print(f"✅ {self.t('silence_manual_done', threshold=self.silence_threshold)}")
                            return
                        else:
                            print(self.t('threshold_range'))
                    except ValueError:
                        print(self.t('invalid_number'))
            else:
                print(self.t('invalid_choice', range='1、2、3 或 4'))
                continue
    
    def select_alias_mode(self):
        print("\n" + "="*60)
        print(self.t('alias_select'))
        print("="*60)
        print(self.t('alias_none'))
        print(self.t('alias_add_prefix'))
        print(self.t('alias_remove_prefix'))
        print(self.t('alias_remove_suffix'))
        print(self.t('alias_add_suffix'))
        print(self.t('alias_slice'))
        print("="*60)
        
        while True:
            choice = input(self.t('alias_choice')).strip()
            
            if choice == '1':
                self.alias_mode = 'none'
                print(f"✅ {self.t('alias_none_done')}")
                return
            elif choice == '2':
                self.alias_mode = 'add_prefix'
                prefix = input(self.t('alias_prefix_input')).strip()
                self.alias_prefix = prefix
                print(f"✅ {self.t('alias_add_prefix_done', prefix=prefix)}")
                return
            elif choice == '3':
                self.alias_mode = 'remove_prefix'
                prefix = input(self.t('alias_prefix_remove_input')).strip()
                self.alias_prefix = prefix
                print(f"✅ {self.t('alias_remove_prefix_done', prefix=prefix)}")
                return
            elif choice == '4':
                self.alias_mode = 'remove_suffix'
                suffix = input(self.t('alias_suffix_remove_input')).strip()
                self.alias_suffix = suffix
                print(f"✅ {self.t('alias_remove_suffix_done', suffix=suffix)}")
                return
            elif choice == '5':
                self.alias_mode = 'add_suffix'
                suffix = input(self.t('alias_suffix_input')).strip()
                self.alias_suffix = suffix
                print(f"✅ {self.t('alias_add_suffix_done', suffix=suffix)}")
                return
            elif choice == '6':
                self.alias_mode = 'slice'
                print(self.t('alias_slice_hint'))
                
                while True:
                    try:
                        start = input(self.t('alias_slice_start')).strip()
                        end = input(self.t('alias_slice_end')).strip()
                        
                        start_int = int(start)
                        end_int = int(end)
                        
                        if start_int < 1 or end_int < 1:
                            print(self.t('invalid_min'))
                            continue
                        if start_int > end_int:
                            print(self.t('invalid_range'))
                            continue
                        
                        self.alias_start = start_int - 1
                        self.alias_end = end_int
                        print(f"✅ {self.t('alias_slice_done', start=start, end=end)}")
                        return
                    except ValueError:
                        print(self.t('invalid_number'))
                        continue
            else:
                print(self.t('invalid_choice', range='1、2、3、4、5 或 6'))
                continue
    
    def select_romaji_fix(self):
        if self.language in ['japanese', 'korean']:
            print("\n" + "="*60)
            print(self.t('romaji_fix_select'))
            print("="*60)
            print(self.t('romaji_fix_enable'))
            print(self.t('romaji_fix_disable'))
            print("="*60)
            
            while True:
                choice = input(self.t('romaji_fix_choice')).strip()
                
                if choice == '1':
                    self.fix_romaji = True
                    print(f"✅ {self.t('romaji_fix_enabled')}")
                    return
                elif choice == '2':
                    self.fix_romaji = False
                    print(f"✅ {self.t('romaji_fix_disabled')}")
                    return
                else:
                    print(self.t('invalid_choice', range='1 或 2'))
                    continue
        else:
            self.fix_romaji = False
            print(self.t('romaji_fix_skip'))
    
    def extract_kana(self, text):
        kana_pattern = re.compile(
            r'[\u3040-\u309f\u30a0-\u30ff\u31f0-\u31ff]'
        )
        return ''.join(kana_pattern.findall(text))
    
    def extract_hangul(self, text):
        hangul_pattern = re.compile(
            r'[\uac00-\ud7af\u1100-\u11ff\u3130-\u318f]'
        )
        return ''.join(hangul_pattern.findall(text))
    
    def extract_chinese(self, text):
        chinese_pattern = re.compile(
            r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]'
        )
        return ''.join(chinese_pattern.findall(text))
    
    def extract_english(self, text):
        english_pattern = re.compile(r'[a-zA-Z]')
        return ''.join(english_pattern.findall(text))
    
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
    
    def hangul_to_roman_str(self, hangul):
        result = ''
        for char in hangul:
            if char in self.hangul_to_roman:
                result += self.hangul_to_roman[char]
            else:
                result += char
        return result
    
    def fix_romaji_in_filename(self, filename):
        if not self.fix_romaji:
            return filename
        
        base_name = os.path.splitext(filename)[0]
        ext = os.path.splitext(filename)[1]
        
        if self.language == 'japanese':
            script = self.extract_kana(base_name)
            if not script:
                return filename
            correct_romaji = self.kana_to_romaji_str(script)
        elif self.language == 'korean':
            script = self.extract_hangul(base_name)
            if not script:
                return filename
            correct_romaji = self.hangul_to_roman_str(script)
        else:
            return filename
        
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
                if self.language == 'japanese':
                    script_in_part = self.extract_kana(part)
                elif self.language == 'korean':
                    script_in_part = self.extract_hangul(part)
                else:
                    script_in_part = ''
                
                if script_in_part:
                    if self.language == 'japanese':
                        correct_part = self.kana_to_romaji_str(script_in_part)
                    elif self.language == 'korean':
                        correct_part = self.hangul_to_roman_str(script_in_part)
                    else:
                        correct_part = part
                    
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
            print(self.t('romaji_fix', old=filename, new=new_name))
        
        return new_name
    
    def apply_alias(self, filename):
        base_name = os.path.splitext(filename)[0]
        
        if self.fix_romaji and self.language in ['japanese', 'korean']:
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
            print(self.t('scan_found_audio', filename=os.path.basename(audio_path)))
            
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
                print(self.t('convert_success', filename=os.path.basename(wav_path)))
                return wav_path
            else:
                print(self.t('convert_fail', filename=os.path.basename(audio_path)))
                return None
                
        except subprocess.TimeoutExpired:
            print(self.t('convert_fail', filename=os.path.basename(audio_path)) + " (timeout)")
            return None
        except Exception as e:
            print(self.t('convert_fail', filename=os.path.basename(audio_path)) + f" ({e})")
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
        
        print(f"\n{self.t('scanning', directory=directory)}")
        print(self.t('scan_files', count=len(all_files)))
        print("-"*60)
        
        for idx, filepath in enumerate(all_files, 1):
            filename = os.path.basename(filepath)
            
            progress_msg = self.t('scan_progress', current=idx, total=len(all_files))
            print(f"{progress_msg:<50}", end='\r')
            
            if not self.is_audio_file(filepath):
                self.skipped_files.append(filepath)
                continue
            
            if self.is_wav_file(filepath):
                wav_files.append(filepath)
                continue
            
            wav_path = self.convert_to_wav(filepath)
            
            if wav_path and os.path.exists(wav_path):
                wav_files.append(wav_path)
                if wav_path != filepath:
                    print(self.t('converted_generated', filename=os.path.basename(wav_path)))
            else:
                print(self.t('convert_skip', filename=filename))
                self.skipped_files.append(filepath)
        
        print(f"\n{self.t('scan_complete', count=len(wav_files))}")
        if self.converted_files:
            print(self.t('converted_count', count=len(self.converted_files)))
        if self.skipped_files:
            print(self.t('skipped_count', count=len(self.skipped_files)))
        
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
            
            print(self.t('generate_fail', error=f"无法读取时长: {os.path.basename(wav_path)}"))
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
        print(self.t('no_audio_found'))
        print("="*60)
        print(self.t('no_audio_menu'))
        print("="*60)
        print(self.t('no_audio_hint'))
        print("="*60)
        
        while True:
            print(self.t('drag_hint'))
            user_input = input(self.t('no_audio_input')).strip()
            
            user_input = user_input.strip('"\'')
            
            if user_input.lower() in ['exit', 'quit', 'q', '3']:
                print(self.t('exit'))
                sys.exit(0)
            
            if self.is_valid_directory(user_input):
                audio_files = self.scan_audio_files(user_input)
                if audio_files:
                    return user_input, audio_files
                else:
                    print(self.t('no_audio_error', path=user_input))
                    print(self.t('no_audio_check'))
                    continue
            else:
                print(self.t('path_invalid', path=user_input))
                print(self.t('path_hint'))
                continue
    
    def is_valid_directory(self, path):
        try:
            return os.path.isdir(path) and os.path.exists(path)
        except:
            return False
    
    def process_files(self, wav_files):
        if not wav_files:
            print(self.t('no_wav'))
            return False
        
        print(f"\n{self.t('processing_start', count=len(wav_files))}")
        print("-"*60)
        
        for idx, wav_path in enumerate(wav_files, 1):
            filename = os.path.basename(wav_path)
            
            print(f"\n{self.t('processing_file', idx=idx, total=len(wav_files), filename=filename)}")
            
            if self.detect_abnormal_chars(filename):
                self.abnormal_files.append(filename)
                
                if self.clean_mode == 'ask':
                    print(self.t('abnormal_detected', filename=filename))
                    while True:
                        choice = input(self.t('abnormal_choice')).strip().upper()
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
                                    print(self.t('abnormal_renamed', old=filename, new=new_name))
                                    filename = new_name
                                    wav_path = new_path
                                except Exception as e:
                                    print(self.t('abnormal_rename_fail', error=e))
                                    continue
                            else:
                                print(self.t('abnormal_empty'))
                                continue
                            break
                        elif choice == 'N':
                            print(self.t('abnormal_skip', filename=filename))
                            break
                        else:
                            print(self.t('abnormal_invalid'))
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
                            print(self.t('abnormal_auto_clean', old=filename, new=new_name))
                            filename = new_name
                            wav_path = new_path
                        except Exception as e:
                            print(self.t('abnormal_auto_fail', error=e))
                    elif not new_filename:
                        print(self.t('abnormal_auto_empty', filename=filename))
                        continue
                else:
                    print(self.t('abnormal_skip_all', filename=filename))
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
            print(self.t('processed', filename=filename, alias=alias, duration=duration, silence=silence, offset=params['offset']))
        
        return True
    
    def generate_oto(self):
        if not self.notes:
            print(self.t('generate_fail', error="没有有效数据"))
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
            
            print(f"\n{self.t('generate_success', path=os.path.abspath(self.output_path))}")
            print(self.t('generate_count', count=len(self.notes)))
            print(self.t('generate_encoding', encoding=self.encoding))
            return True
        except Exception as e:
            print(self.t('generate_fail', error=e))
            return False
    
    def cleanup_temp_files(self):
        if self.cleanup_done:
            return
        if self.temp_mode and self.temp_wav_files:
            print(f"\n{self.t('cleanup_temp')}")
            for wav_path in self.temp_wav_files:
                try:
                    if os.path.exists(wav_path):
                        os.remove(wav_path)
                        print(self.t('cleanup_deleted', filename=os.path.basename(wav_path)))
                except Exception as e:
                    print(self.t('cleanup_fail', filename=os.path.basename(wav_path), error=e))
        self.cleanup_done = True
    
    def run(self):
        try:
            print("="*60)
            print(self.t('title', version=VERSION))
            print("="*60)
            
            print(self.t('loading'))
            print(self.t('loading_done'))
            print(self.t('loading_mood'))
            
            self.select_ui_language()
            
            print(self.t('detecting'))
            self.detect_platform()
            
            self.select_language()
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
                print(self.t('ffmpeg_ready'))
            else:
                print(self.t('ffmpeg_missing'))
                print(self.t('ffmpeg_hint'))
            
            if not self.ffprobe_available:
                print(self.t('ffprobe_missing'))
            
            if self.wav_dir is None:
                self.wav_dir = os.getcwd()
            
            print(f"\n{self.t('dir_found', path=os.path.abspath(self.wav_dir))}")
            
            audio_files = self.scan_audio_files(self.wav_dir)
            
            if not audio_files:
                self.wav_dir, audio_files = self.interactive_path_selection()
            else:
                print(f"\n{self.t('dir_current', count=len(audio_files))}")
                print(self.t('dir_hint'))
                
                user_input = input(self.t('dir_input')).strip()
                
                if user_input.lower() in ['q', 'quit', 'exit']:
                    print(self.t('exit'))
                    sys.exit(0)
                
                if user_input:
                    user_input = user_input.strip('"\'')
                    if self.is_valid_directory(user_input):
                        new_audio = self.scan_audio_files(user_input)
                        if new_audio:
                            self.wav_dir = user_input
                            audio_files = new_audio
                            print(self.t('dir_switched', path=self.wav_dir))
                        else:
                            print(self.t('dir_no_audio', path=user_input))
                    else:
                        print(self.t('dir_invalid'))
            
            print(f"\n{self.t('dir_processing', path=os.path.abspath(self.wav_dir))}")
            print("="*60)
            
            if not self.process_files(audio_files):
                return False
            
            if self.abnormal_files:
                print(self.t('abnormal_summary', count=len(self.abnormal_files)))
                print(self.t('abnormal_summary_list'))
                for f in self.abnormal_files:
                    print(f"   - {f}")
            
            if self.converted_files:
                print(self.t('converted_summary', count=len(self.converted_files)))
                for f in self.converted_files:
                    print(f"   - {os.path.basename(f)}")
            
            if self.skipped_files:
                print(self.t('skipped_summary', count=len(self.skipped_files)))
            
            self.output_path = os.path.join(self.wav_dir, 'oto.ini')
            self.generate_oto()
            
            self.cleanup_temp_files()
            
            print("\n" + "="*60)
            print(self.t('complete'))
            print(self.t('complete_path', path=os.path.abspath(self.output_path)))
            print(self.t('complete_hint'))
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
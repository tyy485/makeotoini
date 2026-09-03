import os
import sys
import re
import wave
import json
import time
import glob
import shutil
import random
import atexit
import signal
import platform
import tempfile
import subprocess
import urllib.request
import urllib.parse
import webbrowser
import zipfile
import struct
import hashlib
import base64
from pathlib import Path

VERSION = "4.1"
START_TIME = time.time()

EGGS = [
    "🐧 我去，居然是神级系统",
    "🍎 还用苹果电脑，这么有钱",
    "💻 竟然是CMD，来吧，进我的生成器",
    "🎵 你正在生成声库，伟大的调教师！",
    "🦄 这个世界需要更多的 UTAU 音源",
    "☕ 喝杯咖啡，等待生成...",
    "🐱 猫猫在帮你生成 oto.ini",
    "🎤 唱首歌吧，调教师！",
    "✨ 这可能是你做过最棒的音源",
    "🔥 燃起来了！生成中...",
    "💡 提示：多备份，少熬夜",
    "🎹 你已经是个成熟的调教师了",
    "🎶 音高修正？那是下一版本的事",
    "📦 零依赖，说到做到",
    "🚀 生成速度太快，就像火箭",
]

STORIES_ZH = [
    "从前有座小镇，镇西边巷尾，藏着一间不起眼的钟表铺。铺子木门斑驳，玻璃橱窗蒙着一层薄灰，里面摆满大大小小旧时钟。守店的是一位白发老人，大家都叫他老钟伯。镇上所有人都知道，老钟伯修钟表手艺顶尖，却唯独不肯校准自己店里墙上那座老挂钟。这座钟每天都会慢上三分钟，年年如此。有人上门修表时总会打趣，劝他顺手把自家钟调准。老钟伯只是淡淡一笑，擦干净手里的齿轮，并不解释缘由。早年间小镇节奏缓慢，没人在意这三分钟。后来新城扩建，街道上车流越来越密，行人步履匆匆。上班族攥着手表一路狂奔，学生背着书包埋头赶路，每个人都拼命追赶时间。大家渐渐习惯分秒必争，走路要快，吃饭要快，连说话都赶着节奏。不少人路过钟表铺，看见墙上走慢的时钟，总觉得别扭，还有人私下议论老钟伯太过懒散，连时钟都懒得调。老钟伯听见流言，依旧日复一日坐在木桌前，拆开老旧钟表，打磨生锈的齿轮。三年之后，小镇启动旧城改造，整条老街纳入拆迁范围。拆迁通知贴出来那天，老街居民心里五味杂陈。老钟伯接到搬迁通知，收拾铺子里物件。搬迁前最后一个傍晚，他拿出螺丝刀，缓缓拧动挂钟旋钮，把走慢多年的时钟调得分秒不差。第二天老街街坊路过，发现时钟准时走动，反倒心里空落落的。一位常来修表的少年忍不住问他，为什么偏偏等到要搬走，才把钟调准。老钟伯坐在门槛上，望着天边晚霞慢慢说道：从前我把钟调慢三分钟，不是我不会修。我是想让路过这里的人，多留片刻喘口气。赶路的人可以停下脚步看看落日，放学的孩子可以蹲下来观察墙角蚂蚁，买菜的老人不必慌慌张张往家赶。如今老街马上拆了，这份慢时光留不住，时钟自然不必再慢。没过多久，老钟表铺被拆除。新建的宽阔马路车流不息，街边全是崭新商铺。再也没有一座故意走慢三分钟的挂钟，留在巷口等候行人。镇上居民偶尔想起老钟伯的话，才猛然发觉，生活里最珍贵的，恰恰是被大家忽略的片刻空闲。",

    "小城有个年轻作曲人，名叫阿远。他一心想写出完美乐曲，每次写谱都把音符填得满满当当，小节之间不留一点空隙。他总觉得，空白就是缺憾，一段曲子只有密密麻麻铺满音符，才算饱满好听。有一年，市里举办原创音乐比赛，阿远熬了整整半个月，日夜打磨一首乐曲。每一段旋律反复修改，每一个小节全部写满音符，整首曲子没有一处停顿留白。他满怀期待上交乐谱，满心以为能拿到名次。比赛结果公布，阿远名落孙山。评委给他写下评语：音符堆砌太满，听的时候让人喘不过气，缺少呼吸感。阿远心里不服气，回家一遍遍播放曲子，越听越烦躁。他不甘心失败，打算重新写一首，这次他准备把旋律编得更加繁复。某天傍晚，阿远去郊外散步，路过一间老琴房。屋内传来缓慢柔和的钢琴曲。琴声偶尔停下，安静持续一两秒，旋律才缓缓继续。短暂的空白没有打断音乐，反而让接下来的旋律更加动人。他站在窗外静静听完一曲，忽然恍然大悟。回到家中，阿远拿出乐谱，删掉大量细碎音符，刻意在段落之间留出长短不一的空白。有些停顿只有半秒，有些足足两秒。刚开始修改，他心里总觉得空荡荡，忍不住想把空白填上音符。他强迫自己忍住冲动，反复弹奏调整停顿时长。半年后第二次音乐比赛，阿远带着修改后的作品参赛。乐曲响起，舒缓的旋律搭配恰到好处的留白，听众跟着节奏慢慢放松。演奏结束，台下掌声久久不停，他顺利拿下一等奖。后来阿远常跟身边学音乐的年轻人说起这件事。音乐不代表把所有空间填满，短暂的空白不是浪费，而是给旋律喘息的机会。人生也是一样，不必时时刻刻把日程排满，适当停下脚步，才能看清前方的路。",

    "市中心老图书馆三楼角落，立着一本翻得破烂的厚字典。封皮早已磨损褪色，书页边角卷成波浪，不少页面沾着深浅不一的茶渍。管理员张叔在这里工作二十多年，每天整理书架，唯独这本字典一直放在老位置。他慢慢发现一个奇怪现象：每天都有不同读者，悄悄翻开字典里写着遗憾的那一页。有人站在书架前沉默许久，轻轻摩挲书页；有人指尖划过文字，悄悄叹一口气，随后默默合上字典离开。张叔很好奇，这一页究竟藏着什么魔力。他抽空翻开查看，字典上印刷字迹普通，没有特别批注，看不出异样。一个雨夜，图书馆快要闭馆，外面大雨滂沱。馆内只剩零星读者。张叔收拾书架时，看见一只灰扑扑的小老鼠，顺着书架缝隙爬到字典上。小老鼠细细啃咬遗憾两个字的书页边角，啃出细碎残缺的缺口。张叔下意识想拿起扫把驱赶，手抬到半空停住。他静静站在一旁，看着小老鼠慢悠悠啃完，钻进书架缝隙消失不见。从那天起，遗憾两个字不再完整。之后读者再来翻这一页，看见残缺的字迹，神情慢慢发生变化。从前很多人盯着这两个字陷入悲伤，纠结过往做错的选择。如今看着缺角的文字，不少人忽然释怀。有人说，遗憾本就不会完整。过去做错的事、错过的人，不可能重新圆满。与其死死攥住遗憾不肯放下，不如坦然接受它残缺的模样。这本旧字典依旧摆在角落，日复一日接待前来翻阅的读者。残缺的两个字，悄悄解开无数人心底长久的心结。",

    "森林深处住着一只灰松鼠，名叫松松。它是整片森林的专属邮差。每天天刚蒙蒙亮，松松就背起鼓鼓囊囊的帆布邮包，穿梭在林间小路，给小动物们派送信件。春天山路泥泞，雨水打湿路面，泥土沾满脚掌；夏天烈日当头，树叶缝隙漏下滚烫阳光，汗水浸透皮毛；秋天落叶铺满小路，脚下打滑容易摔跤；冬天寒风呼啸，雪花落在身上冻得发抖。无论天气好坏，松松从来没有迟到过。森林里小动物都很喜欢这位邮差。小兔子会塞给他一根胡萝卜，小刺猬送上几颗野果，啄木鸟偶尔会在它赶路时，提醒前方树枝松动。日复一日，松松送了三年信件。慢慢它开始疲惫。每天重复走相同路线，翻相同山坡，跨过同一条小溪。有时候它心里会冒出念头：每天送信好像没有意义。有一天，松松收到一封特殊信件。收信地址是森林最偏僻的山洞，收件者是独居多年的老鼹鼠。信封上字迹歪歪扭扭，寄信人是远方鼹鼠的小孙女。山路格外难走，后半段几乎没有成型小路，荆棘不断刮到松松后背。它走了整整一个下午，才找到山洞。老鼹鼠常年独自居住，很少收到信件。拆开信封看见孙女的字迹，浑浊眼睛慢慢湿润。它拿出珍藏多年的坚果，执意要送给松松。回家路上，夕阳洒遍森林，松松忽然明白自己工作的意义。它送出去的不只是一张张信纸，还有思念、牵挂与期盼。往后的日子，松松继续奔走林间。哪怕路途辛苦，它再也没有觉得枯燥。每一封薄薄的信件，都藏着一份温暖，等待它亲手送到主人手上。"
]

STORIES_EN = [
    "There was an old clockmaker living at the end of a quiet alley in a small town. His shop had a worn wooden door and dusty glass windows filled with clocks of all sizes. Everyone called him Old Clock. The whole town knew he was the best clockmaker around, but he never bothered to fix the old clock on his own wall. That clock ran three minutes slow every single day, year after year. Customers would joke about it when they brought in their watches, telling him to fix his own clock. Old Clock would just smile, wipe his gears clean, and never explain why. Back in the day, nobody cared about three minutes. Then the town grew. New roads, more cars, people rushing everywhere. Office workers ran to catch trains, students walked with their heads down, everyone was chasing time. Soon people started to notice the slow clock in the shop window. Some whispered that Old Clock was lazy. Old Clock heard the gossip but kept sitting at his wooden bench, taking apart old clocks and polishing rusty gears. Three years later, the old street was scheduled for demolition. When the notice went up, the neighborhood fell quiet. Old Clock packed up his tools. On the last evening before moving, he took out a screwdriver and slowly turned the dial, setting the old clock to the exact right time for the first time in years. The next morning, neighbors walked by and saw the clock ticking perfectly. It felt strange. A young boy who often came to get his watch fixed asked Old Clock why he only fixed it now. Old Clock sat on the doorstep and watched the sunset. He said, I set it slow on purpose, not because I couldn't fix it. I wanted people passing by to stop for a moment. To catch their breath. To watch the sunset. To let children squat down and watch ants. To let old folks not rush home. Now the street is being torn down. That slow time can't stay, so there's no need for the clock to run slow anymore. The shop was torn down soon after. A wide road took its place with shiny new stores. No more slow clock waiting at the corner. Sometimes the townspeople would remember Old Clock's words and realize that the most precious thing in life was the spare moments they used to ignore.",

    "In a small city lived a young composer named Yuan. He was determined to write the perfect song. Every time he wrote music, he filled every bar with notes, leaving no space at all between measures. He thought that empty space was a flaw. To him, a great melody had to be packed tight with notes. One year the city held an original music competition. Yuan worked for two weeks straight, polishing his piece day and night. He revised every phrase, stuffed every bar full, leaving no rests anywhere. He submitted his score with high hopes, sure he would place. When the results came out, Yuan didn't even rank. The judges wrote back: Too many notes. It suffocates the listener. No room to breathe. Yuan was frustrated. He played his piece over and over at home, getting more upset each time. He decided to write something even more complex. One evening, he took a walk outside the city and passed by an old piano room. A soft piano piece was playing from inside. The melody would pause occasionally, falling silent for a second or two before continuing. Those short silences didn't break the music. They made the melody feel even more moving. He stood outside and listened quietly until the piece finished. Then it clicked. Back home, he pulled out his score and started cutting notes. He removed clusters of small notes and deliberately left empty space between sections. Some rests lasted half a second, others two full seconds. At first it felt wrong. He kept wanting to fill those gaps. But he forced himself to hold back, adjusting each pause carefully. Six months later, Yuan entered the competition again with his revised piece. The melody was gentle and spacious, with rests that let the audience breathe. When the music ended, the applause didn't stop. He took first place. Later, Yuan would tell young musicians he taught that music isn't about filling every space. The rests aren't wasted. They give the melody room to breathe. Life is the same. You don't have to fill every hour. Sometimes you need to stop and see where you're going.",

    "At the back corner of the third floor in the old city library stood a worn-out dictionary. Its cover was faded and frayed, pages curled at the edges, spotted with tea stains of all shades. Uncle Zhang had worked there for over twenty years. He shelved books every day, but he always left that dictionary in the same spot. He started noticing something strange. Different readers would come each day and quietly flip to the page with the word regret printed on it. Some would stand in silence, gently rubbing the page. Others would trace the text with their fingers, sigh softly, and close the book before walking away. Uncle Zhang grew curious. What was so special about that page? He checked the dictionary himself. The printing was ordinary. No markings, no handwriting, nothing out of place. One rainy evening near closing time, with only a few readers left inside, Uncle Zhang was tidying the shelves when he noticed a small gray mouse crawling up the bookcase. The mouse squeezed through a gap and climbed onto the dictionary. It started nibbling at the corner of the page where regret was written. Uncle Zhang raised his broom, ready to shoo it away, but stopped midair. He stood still and watched the mouse chew slowly, leaving tiny ragged gaps in the paper. When it finished, the mouse crept away through the shelf crack and disappeared. After that, the word regret was never quite whole again. Readers who came to that page looked different. Before, many of them would linger, caught up in past mistakes and choices they couldn't undo. Now, seeing those torn edges, some of them seemed to let go. Someone said that regret is never meant to be complete. The things you did wrong, the people you lost, you can't make them whole again. Instead of holding onto regret forever, maybe it's better to accept it as it is, broken and incomplete. That dictionary still sits in the corner, day after day, welcoming those who come to find it. Those two imperfect letters quietly untied knots that had stayed in people's hearts for years.",

    "Deep in the forest lived a gray squirrel named Song. He was the forest mailman. Every morning at dawn, he would sling a bulging canvas bag over his shoulder and dash through the forest paths, delivering letters to all the little animals. Spring paths were muddy, rain soaked the ground and dirt stuck to his paws. Summer sun blazed through the leaves, sweat soaked through his fur. Autumn leaves covered the trails, making each step slippery. Winter winds howled, snowflakes landed on his back and made him shiver. No matter the weather, Song never arrived late. The forest animals loved their mailman. Little rabbits would hand him carrots. Hedgehogs gave him wild berries. Woodpeckers would warn him when a branch ahead was loose. Day after day, Song delivered mail for three years. Slowly, he started to feel tired. He walked the same trails, climbed the same slopes, crossed the same stream every single day. Sometimes he wondered: What's the point of carrying letters all day? One day, Song received a special letter. The address was a cave at the edge of the forest, the home of an old mole who lived alone. The handwriting was wobbly. It was from the mole's granddaughter, far away. The path to the cave was rough. There was barely any trail near the end, and thorns kept scratching Song's back. It took him all afternoon to reach the cave. The old mole rarely got mail. When he tore open the envelope and saw his granddaughter's handwriting, his cloudy eyes grew wet. He took out nuts he had saved for years and insisted on giving them to Song. On the way home, the sunset cast golden light across the forest. Song finally understood what his work meant. He wasn't just delivering paper. He was carrying longing, care, and hope. From then on, Song kept walking through the forest. Even when the work was hard, he never found it dull again. Every thin envelope held a quiet warmth, waiting for him to carry it to the right hands."
]

def signal_handler(sig, frame):
    print("\n" + "=" * 60)
    print("⚠️  检测到中断信号")
    print("=" * 60)
    print("  你按了 CTRL+C，想跑？")
    print("  退出后所有参数丢失，得从头再来。")
    print("=" * 60)
    print("  1. 走，不干了")
    print("  2. 算了，继续")
    print("=" * 60)

    while True:
        choice = input("请选择 1 或 2: ").strip()
        if choice == '1':
            print("\n👋 溜了溜了，下次见！")
            sys.exit(0)
        elif choice == '2':
            print("\n✅ 这就对了，接着干。")
            return
        else:
            print("❌ 这都能输错？只能选 1 或 2")

signal.signal(signal.SIGINT, signal_handler)

class ErrorHandler:
    def __init__(self, ui_language='zh'):
        self.ui_language = ui_language
        self.errors = {
            'zh': {
                'dir_not_found': {'msg': '❌ 找不到文件夹：{path}', 'solution': '💡 检查路径对不对，或者重新选一个文件夹'},
                'no_permission': {'msg': '❌ 没有权限读取文件夹：{path}', 'solution': '💡 换个文件夹试试，或者给这个文件夹开权限'},
                'no_audio': {'msg': '❌ 这个文件夹里没有音频文件', 'solution': '💡 确认音频放在这里了，支持 wav/mp3/flac/m4a/ogg'},
                'wav_corrupt': {'msg': '❌ WAV 文件损坏：{filename}', 'solution': '💡 重新录一下，或者用其他软件转成 wav'},
                'ffmpeg_missing': {'msg': '❌ 没装 FFmpeg，转不了格式', 'solution': '💡 如果全是 wav 格式就不用管，否则去 ffmpeg.org 下载安装'},
                'ffmpeg_timeout': {'msg': '❌ 转码超时：{filename}', 'solution': '💡 音频太大了，试试剪短一点，或者重新运行一次'},
                'encoding_error': {'msg': '❌ 有生僻字符写不进文件', 'solution': '💡 自动换成 UTF-8 重新生成'},
                'user_cancel': {'msg': '👋 用户取消了', 'solution': '💡 重新运行程序再来一次'},
                'unknown': {'msg': '❌ 出事了，但我不说是啥事', 'solution': '💡 重新运行试试，还不行就把截图发给我'},
                'no_data': {'msg': '❌ 没数据预览啥？先扫文件啊', 'solution': '💡 先扫描音频文件再预览'},
                'abnormal_empty': {'msg': '❌ 清洗后文件名为空', 'solution': '💡 重命名文件，去掉不可见字符'},
                'rename_fail': {'msg': '❌ 重命名失败了，文件被占用了？', 'solution': '💡 检查文件是否被占用，或者手动重命名'},
                'ffprobe_missing': {'msg': '⚠️ 没装 ffprobe，时长可能读不准', 'solution': '💡 部分 WAV 可能读不到时长，建议安装 ffprobe'}
            },
            'en': {
                'dir_not_found': {'msg': '❌ Folder not found: {path}', 'solution': '💡 Check the path, or pick another folder'},
                'no_permission': {'msg': '❌ Can\'t read that. Permissions? Or maybe it\'s haunted.', 'solution': '💡 Try another folder, or grant permission'},
                'no_audio': {'msg': '❌ Zero audio files. You sure they\'re in there?', 'solution': '💡 Make sure audio files are there (wav/mp3/flac/m4a/ogg)'},
                'wav_corrupt': {'msg': '❌ This WAV is cooked. Re-record it.', 'solution': '💡 Re-record it, or convert it again'},
                'ffmpeg_missing': {'msg': '❌ FFmpeg? Nope. Can\'t convert without it.', 'solution': '💡 If all you got is wavs, carry on. Otherwise install FFmpeg'},
                'ffmpeg_timeout': {'msg': '❌ Timeout. How big is this file anyway?', 'solution': '💡 Try a shorter audio file, or run again'},
                'encoding_error': {'msg': '❌ Cannot write special characters', 'solution': '💡 Auto-switched to UTF-8, try again'},
                'user_cancel': {'msg': '👋 Cancelled by user', 'solution': '💡 Run again when you are ready'},
                'unknown': {'msg': '❌ Uh oh. Something broke. No idea what.', 'solution': '💡 Try again, if it still fails, send me a screenshot'},
                'no_data': {'msg': '❌ Nothing to preview. Scan some files first.', 'solution': '💡 Scan audio files first'},
                'abnormal_empty': {'msg': '❌ Filename empty after cleaning', 'solution': '💡 Rename the file, remove invisible characters'},
                'rename_fail': {'msg': '❌ Can\'t rename. File is busy or you don\'t own it.', 'solution': '💡 Check if file is in use, or rename manually'},
                'ffprobe_missing': {'msg': '⚠️ ffprobe? Missing. Duration might be a lie.', 'solution': '💡 Some WAV files may not read duration, install ffprobe'}
            }
        }

    def set_language(self, ui_language):
        self.ui_language = ui_language

    def get(self, error_key, **kwargs):
        lang = self.ui_language
        err_data = self.errors.get(lang, {}).get(error_key, self.errors['zh']['unknown'])
        msg = err_data['msg'].format(**kwargs)
        sol = err_data['solution'].format(**kwargs)
        return msg + "\n" + sol

    def get_msg(self, error_key, **kwargs):
        lang = self.ui_language
        err_data = self.errors.get(lang, {}).get(error_key, self.errors['zh']['unknown'])
        return err_data['msg'].format(**kwargs)

    def get_solution(self, error_key, **kwargs):
        lang = self.ui_language
        err_data = self.errors.get(lang, {}).get(error_key, self.errors['zh']['unknown'])
        return err_data['solution'].format(**kwargs)


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
        self.silence_scan_duration = 100
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
        self.generate_character = False
        self.character_name = ''
        self.character_version = ''
        self.character_web = ''
        self.character_image = ''
        self.breath_alias_template = 'breath'
        self.breath_counter = 0
        self.breath_has_placeholder = False
        self.breath_warned = False
        self.remove_all_prefix = False
        self.remove_all_suffix = False
        self.offset_adjust = 0
        self.health_check = False
        self.smart_prewhite = True
        self.vowel_protection = True
        self.generate_frq = False
        self.normalize_volume = False
        self.fast_mode = False
        self.stories_loaded = False
        self.stories = []
        self.current_story = None
        self.err = ErrorHandler(self.ui_language)
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
        self.standard_japanese = [
            'あ', 'い', 'う', 'え', 'お',
            'か', 'き', 'く', 'け', 'こ',
            'さ', 'し', 'す', 'せ', 'そ',
            'た', 'ち', 'つ', 'て', 'と',
            'な', 'に', 'ぬ', 'ね', 'の',
            'は', 'ひ', 'ふ', 'へ', 'ほ',
            'ま', 'み', 'む', 'め', 'も',
            'や', 'ゆ', 'よ',
            'ら', 'り', 'る', 'れ', 'ろ',
            'わ', 'を', 'ん',
            'が', 'ぎ', 'ぐ', 'げ', 'ご',
            'ざ', 'じ', 'ず', 'ぜ', 'ぞ',
            'だ', 'ぢ', 'づ', 'で', 'ど',
            'ば', 'び', 'ぶ', 'べ', 'ぼ',
            'ぱ', 'ぴ', 'ぷ', 'ぺ', 'ぽ',
            'きゃ', 'きゅ', 'きょ',
            'しゃ', 'しゅ', 'しょ',
            'ちゃ', 'ちゅ', 'ちょ',
            'にゃ', 'にゅ', 'にょ',
            'ひゃ', 'ひゅ', 'ひょ',
            'みゃ', 'みゅ', 'みょ',
            'りゃ', 'りゅ', 'りょ',
            'ぎゃ', 'ぎゅ', 'ぎょ',
            'じゃ', 'じゅ', 'じょ',
            'びゃ', 'びゅ', 'びょ',
            'ぴゃ', 'ぴゅ', 'ぴょ'
        ]
        self.standard_chinese = [
            'a', 'o', 'e', 'i', 'u', 'ü',
            'ai', 'ei', 'ui', 'ao', 'ou', 'iu',
            'ie', 'üe', 'er', 'an', 'en', 'in',
            'un', 'ün', 'ang', 'eng', 'ing', 'ong',
            'b', 'p', 'm', 'f', 'd', 't',
            'n', 'l', 'g', 'k', 'h', 'j',
            'q', 'x', 'zh', 'ch', 'sh', 'r',
            'z', 'c', 's', 'y', 'w'
        ]
        self.standard_korean = [
            '가', '나', '다', '라', '마', '바',
            '사', '아', '자', '차', '카', '타',
            '파', '하', '거', '너', '더', '러',
            '머', '버', '서', '어', '저', '처',
            '커', '터', '퍼', '허', '고', '노',
            '도', '로', '모', '보', '소', '오',
            '조', '초', '코', '토', '포', '호',
            '구', '누', '두', '루', '무', '부',
            '수', '우', '주', '추', '쿠', '투',
            '푸', '후', '그', '느', '드', '르',
            '므', '브', '스', '으', '즈', '츠',
            '크', '트', '프', '흐', '기', '니',
            '디', '리', '미', '비', '시', '이',
            '지', '치', '키', '티', '피', '히'
        ]
        self.standard_english = [
            'a', 'b', 'c', 'd', 'e', 'f', 'g',
            'h', 'i', 'j', 'k', 'l', 'm', 'n',
            'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z',
            'aa', 'ae', 'ah', 'aw', 'ay',
            'b', 'ch', 'd', 'dh', 'eh', 'er',
            'ey', 'f', 'g', 'hh', 'ih', 'iy',
            'jh', 'k', 'l', 'm', 'n', 'ng',
            'ow', 'oy', 'p', 'r', 's', 'sh',
            't', 'th', 'uh', 'uw', 'v', 'w',
            'y', 'z', 'zh'
        ]
        self.ui_texts = {
            'zh': {
                'title': '🎵 OTO.ini 智能生成器 v{version}',
                'loading': '生成器正在加载…别急',
                'loading_done': '加载完了，正在给你整编码选择器',
                'loading_mood': '正在加载你的好心情…这玩意儿比较耗资源',
                'detecting': '正在偷看你用啥软件…',
                'ui_language_select': '🌐 选个语言吧，后面就不让你换了',
                'ui_zh': '1. 中文',
                'ui_en': '2. English',
                'ui_choice': '输入 1 或 2，别输错了：',
                'ui_zh_done': '中文',
                'ui_en_done': 'English',
                'config_detect': '📂 配置文件检测',
                'config_found': '已在当前目录发现配置文件: {path}',
                'config_found_hint': '是否引用此文件？',
                'config_use': '1. 是，立即导入',
                'config_manual': '2. 否，手动指定路径',
                'config_choice': '请选择 1 或 2: ',
                'config_imported': '✅ 已导入配置文件',
                'config_import_hint': '📁 请输入配置文件路径: ',
                'config_not_found': '当前目录未发现配置文件',
                'config_import_option': '1. 导入配置文件（手动指定路径）',
                'config_skip': '2. 跳过，重新配置',
                'config_skip_choice': '请选择 1 或 2: ',
                'config_invalid': '❌ 文件不存在或格式无效，是否重新输入？(1. 重新输入 2. 跳过): ',
                'config_retry': '📁 请重新输入配置文件路径: ',
                'config_skip_confirm': '⏭️ 跳过配置文件',
                'config_warning_no_id': '⚠️ 警告：文件没有防伪标识 (ismakeoto: yes)',
                'config_force': '1. 强制导入',
                'config_reselect': '2. 重新选择',
                'config_force_choice': '请选择 1 或 2: ',
                'config_force_import': '🔄 正在尝试导入...',
                'config_import_success': '✅ 导入成功',
                'config_missing_version': '⚠️ 版本号缺失！配置也缺失！你这是两大缺失吗？快把剩下那点补完。',
                'config_missing_fill': '💡 将使用当前程序版本 ({version}) 作为配置版本，缺失的配置项将按默认值补全。',
                'config_version_old': '⚠️ 检测到配置文件版本 ({old}) 与当前版本 ({new}) 不一致',
                'config_version_new': '以下选项为新版本新增，请自行配置：',
                'config_version_continue': '其他已配置项将按配置文件导入。',
                'config_lang_select': '🌍 请选择音源语言',
                'config_lang_jp': '1. 日本語 (Japanese)',
                'config_lang_zh': '2. 中文 (Chinese)',
                'config_lang_ko': '3. 한국어 (Korean)',
                'config_lang_en': '4. English',
                'config_lang_special': '5. 人造语言 / 未知语言',
                'config_lang_choice': '请输入语言序号 (1/2/3/4/5): ',
                'config_lang_jp_done': '日本語',
                'config_lang_zh_done': '中文',
                'config_lang_ko_done': '한국어',
                'config_lang_en_done': 'English',
                'config_lang_special_done': '人造语言 / 未知语言',
                'special_threshold_warn': '🔧 检测到人造语言，启用逆天阈值检测器',
                'special_threshold_apply': '📊 阈值范围已调整为 0.01 ~ 0.5',
                'encoding_select': '📝 请选择你的oto编码',
                'encoding_gb': '1. GB 2312',
                'encoding_sjis': '2. Shift-JIS',
                'encoding_utf8': '3. UTF-8',
                'encoding_euckr': '4. EUC-KR',
                'encoding_smart': '5. 智能编码（根据音源语言自动匹配）',
                'encoding_choice': '请输入编码序号: ',
                'encoding_gb_done': 'GB 2312 编码',
                'encoding_sjis_done': 'Shift-JIS 编码',
                'encoding_utf8_done': 'UTF-8 编码',
                'encoding_euckr_done': 'EUC-KR 编码',
                'encoding_smart_done': '智能编码',
                'encoding_smart_info': '💡 根据当前音源语言自动匹配编码: {encoding}',
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
                'offset_adjust_select': '🎚️  批量偏移调整',
                'offset_adjust_hint': '调整所有音素的 offset（正数=整体后移，负数=整体前移）\n单位：毫秒（ms）\n例如：输入 10 → 整体往后移 10ms\n输入 -5 → 整体往前移 5ms\n输入 0 → 不调整',
                'offset_adjust_input': '请输入偏移值 (ms，正数后移，负数前移，默认 0): ',
                'offset_adjust_done_positive': '✅ 所有音素整体后移 {value}ms',
                'offset_adjust_done_negative': '✅ 所有音素整体前移 {value}ms',
                'offset_adjust_done_zero': '✅ 不调整 offset',
                'breath_alias_select': '🌬️  呼吸声别名模板',
                'breath_alias_hint': '使用 x 作为序号占位符，例如: breath_x → breath_1, breath_2...',
                'breath_alias_examples': '示例: breath_x, br{x}, b{x}, breath, br, b',
                'breath_alias_input': '请输入呼吸声别名模板 (默认: breath): ',
                'breath_alias_done': '呼吸声别名模板: {template}',
                'breath_alias_warning': '⚠️  呼吸声别名模板中没有序号占位符 (x)，所有呼吸声将使用相同别名',
                'breath_alias_warning2': '⚠️  第二次警告：呼吸声别名模板仍然没有 x，所有呼吸声将使用相同别名',
                'alias_select': '🏷️  别名 (Alias) 自定义模式',
                'alias_none': '1. 不使用别名处理 (直接用文件名)',
                'alias_add_prefix': '2. 批量添加前缀 (如: x_)',
                'alias_remove_prefix': '3. 批量删除前缀 (如: 删除 x_)',
                'alias_remove_suffix': '4. 批量删除后缀 (如: 删除 _x)',
                'alias_add_suffix': '5. 批量添加后缀 (如: _x)',
                'alias_slice': '6. 删除指定字符范围 (如: 删除第1-3个字符)',
                'alias_keep_kana': '7. 删除罗马音并保留假名 (仅日文)',
                'alias_keep_romaji': '8. 删除假名并保留罗马音 (仅日文)',
                'alias_keep_hangul': '7. 删除罗马音并保留谚文 (仅韩文)',
                'alias_keep_roman': '8. 删除谚文并保留罗马音 (仅韩文)',
                'alias_choice': '请选择别名模式 (1/2/3/4/5/6/7/8): ',
                'alias_none_done': '不使用别名处理',
                'alias_add_prefix_done': '批量添加前缀 \'{prefix}\'',
                'alias_remove_prefix_done': '批量删除前缀 \'{prefix}\'',
                'alias_remove_suffix_done': '批量删除后缀 \'{suffix}\'',
                'alias_add_suffix_done': '批量添加后缀 \'{suffix}\'',
                'alias_keep_kana_done': '删除罗马音并保留假名',
                'alias_keep_romaji_done': '删除假名并保留罗马音',
                'alias_prefix_input': '请输入要添加的前缀: ',
                'alias_prefix_remove_input': '请输入要删除的前缀: ',
                'alias_suffix_remove_input': '请输入要删除的后缀: ',
                'alias_suffix_input': '请输入要添加的后缀: ',
                'alias_slice_hint': '\n💡 提示: 字符位置从1开始计数，如文件名 \'abcde\'\n   删除 1-3 得到 \'de\'\n   删除 3-5 得到 \'ab\'\n   删除 2-4 得到 \'ae\'',
                'alias_slice_start': '请输入起始字符位置: ',
                'alias_slice_end': '请输入结束字符位置: ',
                'alias_slice_done': '删除第 {start} 到第 {end} 个字符',
                'alias_slice_warning': '⚠️  文件名长度 ({length}) 小于结束位置 ({end})，切片将不生效',
                'alias_remove_all_prefix': '是否删除所有匹配的前缀？(Y/N，默认N只删一次): ',
                'alias_remove_all_suffix': '是否删除所有匹配的后缀？(Y/N，默认N只删一次): ',
                'romaji_fix_select': '🔧 罗马音自动修复',
                'romaji_fix_enable': '1. 启用自动修复 (将short/long等替换为正确罗马音)',
                'romaji_fix_disable': '2. 禁用自动修复',
                'romaji_fix_choice': '请选择 (1/2): ',
                'romaji_fix_enabled': '已启用: 罗马音自动修复',
                'romaji_fix_disabled': '已禁用: 罗马音自动修复',
                'romaji_fix_skip': '当前语言不支持罗马音修复，已自动禁用',
                'smart_prewhite_select': '🎯 智能前白留空',
                'smart_prewhite_hint': '自动检测录音开头的呼吸声，算进 offset，让发音更自然。',
                'smart_prewhite_enable': '1. 启用智能前白留空 [推荐]',
                'smart_prewhite_disable': '2. 禁用（使用传统静音检测）',
                'smart_prewhite_choice': '请选择 (1/2，默认 1): ',
                'smart_prewhite_enabled': '✅ 已启用智能前白留空',
                'smart_prewhite_disabled': '✅ 已禁用智能前白留空',
                'vowel_protect_select': '🔊 元音保护',
                'vowel_protect_hint': '防止辅音过长盖过元音（俗称"吞元音"）。\n启用后，程序会自动为每个音素预留足够的元音空间。',
                'vowel_protect_enable': '1. 启用元音保护 [推荐]',
                'vowel_protect_disable': '2. 禁用元音保护',
                'vowel_protect_choice': '请选择 (1/2，默认 1): ',
                'vowel_protect_enabled': '✅ 已启用元音保护',
                'vowel_protect_disabled': '✅ 已禁用元音保护',
                'frq_select': '📈 frq 音高文件生成',
                'frq_hint': 'frq 文件让 UTAU 音高更自然，使用纯 Python 自相关法生成。',
                'frq_enable': '1. 生成 frq',
                'frq_disable': '2. 不生成',
                'frq_choice': '请选择 (1/2，默认 2): ',
                'frq_enabled': '✅ 将生成 frq',
                'frq_disabled': '✅ 不生成 frq',
                'normalize_select': '🎚️ 统一音量',
                'normalize_hint': '不同录音文件音量可能不一致，导致 UTAU 里听起来忽大忽小。\n使用 FFmpeg 将所有音频统一到相同的音量。',
                'normalize_enable': '1. 统一音量（使用 FFmpeg 归一化）',
                'normalize_disable': '2. 不统一',
                'normalize_choice': '请选择 (1/2，默认 2): ',
                'normalize_enabled': '✅ 将使用 FFmpeg 统一音量',
                'normalize_disabled': '✅ 不统一音量',
                'health_check_select': '🏥 音源健康检查',
                'health_check_hint': '扫描音源目录，检查是否缺音。\n支持检查：日语五十音、中文拼音、韩文谚文、英文音素。',
                'health_check_enable': '1. 运行健康检查',
                'health_check_disable': '2. 跳过健康检查',
                'health_check_choice': '请选择 (1/2，默认 2): ',
                'health_check_enabled': '✅ 已启用健康检查',
                'health_check_disabled': '⏭️  跳过健康检查',
                'health_check_title': '🏥 健康检查',
                'health_check_missing': '⚠️  缺少 {count} 个音素：',
                'health_check_complete': '✅ 所有标准音素齐全！',
                'health_check_continue': '是否继续生成 oto.ini？(1. 继续 2. 取消): ',
                'health_check_continue_yes': '✅ 继续生成',
                'health_check_continue_no': '❌ 用户取消生成',
                'character_select': '📋 声库信息文件 (character.txt) 生成',
                'character_enable': '1. 启用生成 character.txt 和图标支持',
                'character_disable': '2. 禁用 (不生成)',
                'character_choice': '请选择 (1/2): ',
                'character_enabled': '已启用: 生成声库信息文件',
                'character_disabled': '已禁用: 不生成声库信息文件',
                'character_name_input': '请输入歌手名称 (name): ',
                'character_name_done': '歌手名称: {name}',
                'character_version_input': '请输入版本号 (version，留空跳过): ',
                'character_version_done': '版本号: {version}',
                'character_web_input': '请输入网站 (web，留空跳过): ',
                'character_web_done': '网站: {web}',
                'character_image_input': '请输入图标文件名或路径 (留空跳过): ',
                'character_image_done': '已设置图标: {image}',
                'character_image_skip': '未设置图标',
                'oto_exists_title': '⚠️ 检测到 oto.ini 已存在',
                'oto_exists_hint': '你这不是已经有了吗？是要重写吗？重写的话，我帮你顺便把这文件删了。如果你不重写，是要补充库的话，很抱歉，我只提供 character.txt。',
                'oto_exists_choice': '请选择 1 或 2: ',
                'oto_exists_rewrite': '1. 重写——删掉旧 oto.ini，重新生成',
                'oto_exists_keep': '2. 不重写——保留旧 oto.ini，只生成 character.txt',
                'oto_exists_deleted': '✅ 已删除旧 oto.ini',
                'oto_exists_keep_confirm': '✅ 保留旧 oto.ini',
                'oto_exists_char_ask': '📋 是否需要生成 character.txt？\n  1. 生成\n  2. 不生成\n请选择 1 或 2: ',
                'oto_exists_char_generated': '✅ character.txt 已生成',
                'oto_exists_char_skip': '⏭️ 不生成 character.txt',
                'preview_title': '📋 预览 oto.ini 配置',
                'preview_count': '📊 共 {count} 条配置',
                'preview_more': '... 还有 {count} 条未显示',
                'preview_confirm': '是否确认生成 oto.ini？(Y/N): ',
                'preview_show': '{index:3}. {filename:30} → {alias:20} offset:{offset:4} consonant:{consonant:4} cutoff:{cutoff:4} pre:{preutterance:4} overlap:{overlap:4}',
                'ffmpeg_ready': '✅ FFmpeg 已就绪，支持自动转换音频格式',
                'ffmpeg_hint': '💡 建议安装FFmpeg以支持更多音频格式',
                'default_dir': '📁 默认目录: {path}',
                'scanning': '📂 扫描目录: {directory}',
                'scan_files': '📊 共发现 {count} 个文件',
                'scan_progress': '🔍 扫描进度: {current}/{total}',
                'scan_found_audio': '🎵 发现非wav音频: {filename}',
                'convert_success': '✅ 转换成功: {filename}',
                'converted_generated': '💡 已生成: {filename}',
                'scan_complete': '✅ 扫描完成: 找到 {count} 个wav文件',
                'converted_count': '   🔄 转换了 {count} 个文件为wav',
                'skipped_count': '   ⏭️  跳过了 {count} 个非音频文件',
                'processing_start': '🔧 开始处理 {count} 个wav文件',
                'processing_file': '[{idx}/{total}] 处理: {filename}',
                'abnormal_detected': '⚠️  检测到异常字符: {filename}',
                'abnormal_choice': '输入 Y 剔除异常字符，输入 N 跳过此文件 (Y/N): ',
                'abnormal_renamed': '✅ 已重命名: {old} -> {new}',
                'abnormal_skip': '⏭️  跳过文件: {filename}',
                'abnormal_invalid': '❌ 无效输入，请输入 Y 或 N',
                'abnormal_auto_clean': '✅ 自动清洗: {old} -> {new}',
                'abnormal_auto_empty': '⚠️  清洗后文件名为空，跳过: {filename}',
                'abnormal_skip_all': '⏭️  跳过异常文件: {filename}',
                'processed': '✅ 已处理: {filename} (别名: {alias}, 时长: {duration}ms, 静音: {silence}ms, offset: {offset}ms)',
                'breath_detected': '   🌬️  呼吸声文件: {filename} -> 别名: {alias}',
                'romaji_fix': '   🔧 修复罗马音: {old} -> {new}',
                'generate_success': '✅ oto.ini 已生成: {path}',
                'generate_count': '📊 共 {count} 条配置',
                'generate_encoding': '🔤 编码格式: {encoding}',
                'character_generated': '✅ character.txt 已生成: {path}',
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
                'dir_current': '\n💡 当前目录找到 {count} 个可用音频文件',
                'dir_hint': '   如果想处理其他目录，可以输入新路径\n   直接按回车继续使用当前目录\n   输入 \'q\' 退出程序',
                'dir_input': '\n📁 请输入新路径（或按回车继续）: ',
                'dir_switched': '✅ 切换到新目录: {path}',
                'dir_processing': '\n📁 处理目录: {path}',
                'exit': '👋 程序退出',
                'invalid_choice': '❌ 这都能输错？只能选 {range}',
                'invalid_number': '❌ 请输入有效的数字',
                'invalid_range': '❌ 起始位置不能大于结束位置',
                'invalid_min': '❌ 起始和结束位置必须 >= 1',
                'threshold_range': '❌ 阈值必须在 0.001 到 0.1 之间',
                'no_audio_found': '🔍 没找到音频文件，你确定放对地方了？',
                'no_audio_menu': '请选择操作:\n  1. 输入音频文件夹路径（相对或绝对路径）\n  2. 将本程序移动到音频文件夹所在目录\n  3. 退出程序',
                'no_audio_hint': '💡 提示: 支持以下音频格式自动转wav\n   MP3, FLAC, M4A, AAC, OGG, WMA, AIFF, OPUS 等',
                'no_audio_input': '📁 请输入文件夹路径: ',
                'path_invalid': '❌ 无效路径: \'{path}\'',
                'path_hint': '💡 检查一下路径，或者换个文件夹试试',
                'drag_hint': '💡 提示: 你可以拖拽文件夹到命令行窗口，或直接输入路径',
                'egg_random': '🎉 {egg}',
                'egg_project': '🎵 你发现了这个项目的名字！tyy485 敬上，感谢使用 ❤️',
                'egg_author': '👤 作者主页：https://github.com/tyy485',
                'egg_star': '⭐ 给项目点个 Star 吧！',
                'egg_cool': '是的，你也很酷！但如果想最酷，就把交互流程走完。',
                'egg_minecraft': '哎哟，想玩 MC，行，给你跳转过去了。',
                'egg_progress': '🎵 进度条卡住了？骗你的，继续。',
                'egg_scan': '🐱 你猜怎么着？这些文件里混进了一个猫叫，但我不会告诉你哪个。',
                'egg_startup': '🎉 恭喜触发隐藏彩蛋！你今天运气不错。',
                'end_menu_title': '🔗 相关链接',
                'end_menu_1': '1. 打开 OpenUTAU 官网',
                'end_menu_2': '2. 打开 UTAU 官网',
                'end_menu_3': '3. 打开项目 GitHub 主页',
                'end_menu_4': '4. 导出配置文件',
                'end_menu_5': '5. 退出程序',
                'end_menu_choice': '请选择 (1/2/3/4/5): ',
                'end_menu_open_success': '✅ 已打开 {name} 官网',
                'end_menu_open_fail': '❌ 无法自动打开浏览器',
                'end_menu_open_manual': '💡 请手动访问: {url}',
                'end_menu_linux_no_browser': '❌ 你没有安装图形化浏览器，请先安装',
                'end_menu_linux_install_hint': '💡 例如: sudo apt install firefox',
                'end_menu_android_manual': '📱 Android 设备请手动打开链接',
                'end_menu_press_enter': '按回车键继续...',
                'end_menu_config_exported': '📁 配置文件已保存: {path}',
                'end_menu_config_export_success': '✅ 导出成功！',
                'exit_goodbye': '👋 溜了溜了，下次见！',
                'time_elapsed': '⏱️ 总耗时: {seconds} 秒',
                'output_dir_select': '📂 输出位置选择',
                'output_dir_hint': 'oto.ini 将保存在哪里？',
                'output_dir_default': '1. 保存在音源目录（默认）',
                'output_dir_custom': '2. 自定义位置',
                'output_dir_choice': '请选择 1 或 2，默认 1: ',
                'output_dir_input': '📁 请输入保存目录路径: ',
                'output_dir_created': '✅ 目录已创建: {path}',
                'output_dir_not_exists': '⚠️ 目录不存在，是否创建？(1. 创建 2. 重新输入): ',
                'output_dir_invalid': '❌ 无效路径，请重新输入',
                'story_select': '📖 故事库',
                'story_hint': '如果你的文件比较多，想在生成时休闲一会，那你就从网上下点故事吧。',
                'story_download': '1. 从网上下载故事',
                'story_builtin': '2. 用内置故事库',
                'story_choice': '请选择 1 或 2: ',
                'story_downloading': '📡 正在联网下载故事...',
                'story_download_success': '✅ 下载成功！已获取 {count} 个新故事',
                'story_download_fail': '❌ 联网失败，请检查网络连接',
                'story_cache_hit': '📁 故事已保存到本地缓存',
                'story_fallback': '💡 自动切换至内置故事库（{count} 个故事）',
                'story_ready': '✅ 使用内置故事库（{count} 个故事）',
                'story_trigger': '我的妈，你这个文件也太多了！\n我先在后台给你生成，现在要不要听我讲个故事？',
                'story_trigger_choice': '请选择 1 或 2: ',
                'story_trigger_yes': '1. 听！快讲！',
                'story_trigger_no': '2. 不听了，干正事',
                'story_generating': '🎯 正在生成...',
                'story_export_hint': '💡 如果想把故事看完，最后扣个 6，我帮你把故事导出去。\n跑题了跑题了。',
                'story_exported': '📁 故事已导出: {path}',
                'story_export_prompt': '（输入 6 导出完整故事，按回车跳过）: ',
                'log_export_title': '📝 运行日志',
                'log_export_hint': '本次运行已结束。是否导出运行日志？\n日志可以帮助排查问题或记录本次操作。',
                'log_export_yes': '1. 导出日志',
                'log_export_no': '2. 不导出，直接退出',
                'log_export_choice': '请选择 1 或 2: ',
                'log_export_success': '📁 日志已保存: {path}',
                'log_export_press': '按回车键退出...',
                'error_output': '程序遇到了一个{level}错误！错误码:{code}，请前往GitHub查询文档来了解错误和解决方案！',
                'error_unknown': '程序遇到了一个未知错误！错误码:E???，以下为输出日志:',
                'error_log_fail': '无法生成错误日志，原因: {reason}',
                'termux_wake_hint': '你用的可能是 Termux。\n建议你先运行一下 termux-wake-lock，防止被安卓杀掉进程，\n尤其是文件多的情况下。',
                'termux_wake_ask': '你要终止程序并去运行吗？(y/n): ',
                'termux_wake_quit': '请运行以下命令后再重新运行本程序：\n   termux-wake-lock',
                'termux_wake_continue': '继续运行，不执行 termux-wake-lock\n⚠️ 如果进程被杀死，请重新运行并选择 y',
                'wave_read_fail': '文件格式异常，正在尝试自动修复...',
                'wave_fix_first': '第一次修复（标准转换）...',
                'wave_fix_second': '第一次修复失败，尝试兼容模式...',
                'wave_fix_second_desc': '第二次修复（兼容参数）...',
                'wave_fix_success': '✅ 修复成功，继续处理',
                'wave_fix_fail': '❌ 文件修复失败: {filename}',
                'wave_fix_skip': '已跳过此文件',
                'nonhuman_detect': '波形特征与人类语音存在差异。\n但有些正常音源如正弦波合成音源也具有类似特征。\n是否按正常音源处理？',
                'nonhuman_choice_1': '1. 是，按正常音源处理',
                'nonhuman_choice_2': '2. 否，启用非人类语模式',
                'nonhuman_choice_3': '3. 跳过此文件',
                'nonhuman_choice_prompt': '请选择 1/2/3: ',
                'cold_storage_title': '以下文件已被跳过：',
            },
            'en': {
                'title': '🎵 OTO.ini Smart Generator v{version}',
                'loading': 'Loading... don\'t hold your breath',
                'loading_done': 'Boom. Encoding selector loading...',
                'loading_mood': 'Downloading your good vibes... this might take a sec',
                'detecting': 'Snooping on your setup...',
                'ui_language_select': '🌐 Pick a language. No take-backs.',
                'ui_zh': '1. 中文',
                'ui_en': '2. English',
                'ui_choice': 'Type 1 or 2. Don\'t mess it up:',
                'ui_zh_done': 'Chinese',
                'ui_en_done': 'English',
                'config_detect': '📂 Config File Detection',
                'config_found': 'Found config file in current directory: {path}',
                'config_found_hint': 'Use this file?',
                'config_use': '1. Yes, import it',
                'config_manual': '2. No, pick a different file',
                'config_choice': 'Choose 1 or 2: ',
                'config_imported': '✅ Config imported',
                'config_import_hint': '📁 Enter config file path: ',
                'config_not_found': 'No config file found in current directory',
                'config_import_option': '1. Import config (manual path)',
                'config_skip': '2. Skip, configure manually',
                'config_skip_choice': 'Choose 1 or 2: ',
                'config_invalid': '❌ File not found or invalid format. Retry? (1. Retry 2. Skip): ',
                'config_retry': '📁 Enter config file path again: ',
                'config_skip_confirm': '⏭️ Skipping config file',
                'config_warning_no_id': '⚠️ Warning: File missing ismakeoto: yes tag',
                'config_force': '1. Force import',
                'config_reselect': '2. Pick another file',
                'config_force_choice': 'Choose 1 or 2: ',
                'config_force_import': '🔄 Attempting to import...',
                'config_import_success': '✅ Import successful',
                'config_missing_version': '⚠️ Missing version! Missing config items too! Fill in the rest.',
                'config_missing_fill': '💡 Using current version ({version}) as config version. Missing items filled with defaults.',
                'config_version_old': '⚠️ Config version ({old}) doesn\'t match current version ({new})',
                'config_version_new': 'New options added in this version:',
                'config_version_continue': 'Other settings will be imported from config file.',
                'config_lang_select': '🌍 Select voicebank language',
                'config_lang_jp': '1. 日本語 (Japanese)',
                'config_lang_zh': '2. 中文 (Chinese)',
                'config_lang_ko': '3. 한국어 (Korean)',
                'config_lang_en': '4. English',
                'config_lang_special': '5. Constructed / Unknown Language',
                'config_lang_choice': 'Enter language number (1/2/3/4/5): ',
                'config_lang_jp_done': 'Japanese',
                'config_lang_zh_done': 'Chinese',
                'config_lang_ko_done': 'Korean',
                'config_lang_en_done': 'English',
                'config_lang_special_done': 'Constructed / Unknown Language',
                'special_threshold_warn': '🔧 Constructed language detected, enabling special threshold mode',
                'special_threshold_apply': '📊 Threshold range adjusted to 0.01 ~ 0.5',
                'encoding_select': '📝 Select your oto encoding',
                'encoding_gb': '1. GB 2312',
                'encoding_sjis': '2. Shift-JIS',
                'encoding_utf8': '3. UTF-8',
                'encoding_euckr': '4. EUC-KR',
                'encoding_smart': '5. Smart encoding (auto-match based on voicebank language)',
                'encoding_choice': 'Enter encoding number: ',
                'encoding_gb_done': 'GB 2312 encoding',
                'encoding_sjis_done': 'Shift-JIS encoding',
                'encoding_utf8_done': 'UTF-8 encoding',
                'encoding_euckr_done': 'EUC-KR encoding',
                'encoding_smart_done': 'Smart encoding',
                'encoding_smart_info': '💡 Auto-matched encoding based on voicebank language: {encoding}',
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
                'silence_select': '🎚️ Silence detection sensitivity',
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
                'offset_adjust_select': '🎚️ Batch offset adjustment',
                'offset_adjust_hint': 'Adjust offset for all phonemes (positive=delay, negative=advance)\nUnit: milliseconds (ms)\nExample: 10 → delay all by 10ms\n-5 → advance all by 5ms\n0 → no adjustment',
                'offset_adjust_input': 'Enter offset in ms (positive=delay, negative=advance, default 0): ',
                'offset_adjust_done_positive': '✅ Delayed all phonemes by {value}ms',
                'offset_adjust_done_negative': '✅ Advanced all phonemes by {value}ms',
                'offset_adjust_done_zero': '✅ No offset adjustment',
                'breath_alias_select': '🌬️ Breath alias template',
                'breath_alias_hint': 'Use x as placeholder for number, e.g.: breath_x → breath_1, breath_2...',
                'breath_alias_examples': 'Examples: breath_x, br{x}, b{x}, breath, br, b',
                'breath_alias_input': 'Enter breath alias template (default: breath): ',
                'breath_alias_done': 'Breath alias template: {template}',
                'breath_alias_warning': '⚠️ No number placeholder (x) in breath alias template, all breaths will use same alias',
                'breath_alias_warning2': '⚠️ Second warning: Still no x in breath alias template, all breaths will use same alias',
                'alias_select': '🏷️ Alias custom mode',
                'alias_none': '1. No alias processing (use filename directly)',
                'alias_add_prefix': '2. Add prefix (e.g.: x_)',
                'alias_remove_prefix': '3. Remove prefix (e.g.: remove x_)',
                'alias_remove_suffix': '4. Remove suffix (e.g.: remove _x)',
                'alias_add_suffix': '5. Add suffix (e.g.: _x)',
                'alias_slice': '6. Remove character range (e.g.: remove 1st-3rd chars)',
                'alias_keep_kana': '7. Remove romaji, keep kana (Japanese only)',
                'alias_keep_romaji': '8. Remove kana, keep romaji (Japanese only)',
                'alias_keep_hangul': '7. Remove romanization, keep Hangul (Korean only)',
                'alias_keep_roman': '8. Remove Hangul, keep romanization (Korean only)',
                'alias_choice': 'Select alias mode (1/2/3/4/5/6/7/8): ',
                'alias_none_done': 'No alias processing',
                'alias_add_prefix_done': 'Add prefix \'{prefix}\'',
                'alias_remove_prefix_done': 'Remove prefix \'{prefix}\'',
                'alias_remove_suffix_done': 'Remove suffix \'{suffix}\'',
                'alias_add_suffix_done': 'Add suffix \'{suffix}\'',
                'alias_keep_kana_done': 'Keep kana, remove romaji',
                'alias_keep_romaji_done': 'Keep romaji, remove kana',
                'alias_prefix_input': 'Enter prefix to add: ',
                'alias_prefix_remove_input': 'Enter prefix to remove: ',
                'alias_suffix_remove_input': 'Enter suffix to remove: ',
                'alias_suffix_input': 'Enter suffix to add: ',
                'alias_slice_hint': '\n💡 Tip: Character positions start from 1, e.g. filename \'abcde\'\n   Remove 1-3 gives \'de\'\n   Remove 3-5 gives \'ab\'\n   Remove 2-4 gives \'ae\'',
                'alias_slice_start': 'Enter start position: ',
                'alias_slice_end': 'Enter end position: ',
                'alias_slice_done': 'Remove from {start} to {end}',
                'alias_slice_warning': '⚠️ Filename length ({length}) is less than end position ({end}), slice will not take effect',
                'alias_remove_all_prefix': 'Remove all matching prefixes? (Y/N, default N only remove once): ',
                'alias_remove_all_suffix': 'Remove all matching suffixes? (Y/N, default N only remove once): ',
                'romaji_fix_select': '🔧 Romaji auto fix',
                'romaji_fix_enable': '1. Enable auto fix (replace short/long with correct romaji)',
                'romaji_fix_disable': '2. Disable auto fix',
                'romaji_fix_choice': 'Select (1/2): ',
                'romaji_fix_enabled': 'Enabled: Romaji auto fix',
                'romaji_fix_disabled': 'Disabled: Romaji auto fix',
                'romaji_fix_skip': 'Current language does not support romaji fix, disabled automatically',
                'smart_prewhite_select': '🎯 Smart pre-white',
                'smart_prewhite_hint': 'Automatically detect breath at beginning of recording and include it in offset.',
                'smart_prewhite_enable': '1. Enable Smart Pre-White [Recommended]',
                'smart_prewhite_disable': '2. Disable (use traditional silence detection)',
                'smart_prewhite_choice': 'Select (1/2, default 1): ',
                'smart_prewhite_enabled': '✅ Smart Pre-White enabled',
                'smart_prewhite_disabled': '✅ Smart Pre-White disabled',
                'vowel_protect_select': '🔊 Vowel protection',
                'vowel_protect_hint': 'Prevents consonants from overpowering vowels ("swallowing vowels").',
                'vowel_protect_enable': '1. Enable Vowel Protection [Recommended]',
                'vowel_protect_disable': '2. Disable Vowel Protection',
                'vowel_protect_choice': 'Select (1/2, default 1): ',
                'vowel_protect_enabled': '✅ Vowel Protection enabled',
                'vowel_protect_disabled': '✅ Vowel Protection disabled',
                'frq_select': '📈 FRQ file generation',
                'frq_hint': 'FRQ files make UTAU pitch more natural, using pure Python autocorrelation.',
                'frq_enable': '1. Generate FRQ',
                'frq_disable': '2. Do not generate',
                'frq_choice': 'Select (1/2, default 2): ',
                'frq_enabled': '✅ Will generate FRQ',
                'frq_disabled': '✅ FRQ generation disabled',
                'normalize_select': '🎚️ Normalize volume',
                'normalize_hint': 'Different recordings may have inconsistent volume levels.\nUse FFmpeg to normalize all audio to the same volume.',
                'normalize_enable': '1. Normalize volume (using FFmpeg)',
                'normalize_disable': '2. Do not normalize',
                'normalize_choice': 'Select (1/2, default 2): ',
                'normalize_enabled': '✅ Will normalize volume using FFmpeg',
                'normalize_disabled': '✅ Volume normalization disabled',
                'health_check_select': '🏥 Voicebank health check',
                'health_check_hint': 'Scan voicebank directory and report missing phonemes.\nSupports: Japanese 50-sounds, Chinese Pinyin, Korean Hangul, English phonemes.',
                'health_check_enable': '1. Run Health Check',
                'health_check_disable': '2. Skip Health Check',
                'health_check_choice': 'Select (1/2, default 2): ',
                'health_check_enabled': '✅ Health Check enabled',
                'health_check_disabled': '⏭️ Skipping Health Check',
                'health_check_title': '🏥 Health Check',
                'health_check_missing': '⚠️ Missing {count} phonemes:',
                'health_check_complete': '✅ All standard phonemes present!',
                'health_check_continue': 'Continue generating oto.ini? (1. Continue 2. Cancel): ',
                'health_check_continue_yes': '✅ Continuing generation',
                'health_check_continue_no': '❌ Generation cancelled by user',
                'character_select': '📋 character.txt generation',
                'character_enable': '1. Enable character.txt and icon support',
                'character_disable': '2. Disable (do not generate)',
                'character_choice': 'Select (1/2): ',
                'character_enabled': 'Enabled: Generate character info file',
                'character_disabled': 'Disabled: Do not generate character info file',
                'character_name_input': 'Enter singer name (name): ',
                'character_name_done': 'Singer name: {name}',
                'character_version_input': 'Enter version (version, leave blank to skip): ',
                'character_version_done': 'Version: {version}',
                'character_web_input': 'Enter website (web, leave blank to skip): ',
                'character_web_done': 'Website: {web}',
                'character_image_input': 'Enter icon filename or path (leave blank to skip): ',
                'character_image_done': 'Icon set: {image}',
                'character_image_skip': 'No icon set',
                'oto_exists_title': '⚠️ oto.ini already exists',
                'oto_exists_hint': 'You already have one. Overwrite it? If you choose not to, I can only generate character.txt for you.',
                'oto_exists_choice': 'Choose 1 or 2: ',
                'oto_exists_rewrite': '1. Overwrite — delete old oto.ini, generate new one',
                'oto_exists_keep': '2. Keep — keep old oto.ini, only generate character.txt',
                'oto_exists_deleted': '✅ Old oto.ini deleted',
                'oto_exists_keep_confirm': '✅ Keeping old oto.ini',
                'oto_exists_char_ask': '📋 Generate character.txt?\n  1. Yes\n  2. No\nChoose 1 or 2: ',
                'oto_exists_char_generated': '✅ character.txt generated',
                'oto_exists_char_skip': '⏭️ Skipping character.txt',
                'preview_title': '📋 Preview oto.ini configuration',
                'preview_count': '📊 {count} entries',
                'preview_more': '... {count} more entries not shown',
                'preview_confirm': 'Ready to cook oto.ini? (Y/N): ',
                'preview_show': '{index:3}. {filename:30} → {alias:20} offset:{offset:4} consonant:{consonant:4} cutoff:{cutoff:4} pre:{preutterance:4} overlap:{overlap:4}',
                'ffmpeg_ready': '✅ FFmpeg ready, supports auto audio conversion',
                'ffmpeg_hint': '💡 Install FFmpeg for more audio formats',
                'default_dir': '📁 Default directory: {path}',
                'scanning': '📂 Scanning: {directory}',
                'scan_files': '📊 Found {count} files',
                'scan_progress': '🔍 Scanning: {current}/{total}',
                'scan_found_audio': '🎵 Found non-wav audio: {filename}',
                'convert_success': '✅ Converted: {filename}',
                'converted_generated': '💡 Generated: {filename}',
                'scan_complete': '✅ Scan complete: found {count} wav files',
                'converted_count': '   🔄 Converted {count} files to wav',
                'skipped_count': '   ⏭️ Skipped {count} non-audio files',
                'processing_start': '🔧 Processing {count} wav files',
                'processing_file': '[{idx}/{total}] Processing: {filename}',
                'abnormal_detected': '⚠️ Abnormal characters detected: {filename}',
                'abnormal_choice': 'Enter Y to remove characters, N to skip (Y/N): ',
                'abnormal_renamed': '✅ Renamed: {old} -> {new}',
                'abnormal_skip': '⏭️ Skipped: {filename}',
                'abnormal_invalid': '❌ Invalid input, enter Y or N',
                'abnormal_auto_clean': '✅ Auto cleaned: {old} -> {new}',
                'abnormal_auto_empty': '⚠️ Empty filename after cleaning, skipped: {filename}',
                'abnormal_skip_all': '⏭️ Skipped abnormal file: {filename}',
                'processed': '✅ Processed: {filename} (alias: {alias}, duration: {duration}ms, silence: {silence}ms, offset: {offset}ms)',
                'breath_detected': '   🌬️ Breath file: {filename} -> alias: {alias}',
                'romaji_fix': '   🔧 Fixed romaji: {old} -> {new}',
                'generate_success': '✅ oto.ini generated: {path}',
                'generate_count': '📊 {count} entries',
                'generate_encoding': '🔤 Encoding: {encoding}',
                'character_generated': '✅ character.txt generated: {path}',
                'cleanup_temp': '🧹 Cleaning temporary wav files...',
                'cleanup_deleted': '   ✅ Deleted: {filename}',
                'cleanup_fail': '   ❌ Delete failed: {filename} - {error}',
                'abnormal_summary': '\n⚠️ {count} files contain abnormal characters',
                'abnormal_summary_list': '   Check these files:',
                'converted_summary': '\n🔄 Converted {count} audio files to wav:',
                'skipped_summary': '\n⏭️ Skipped {count} non-audio files',
                'complete': '\n✨ Generation complete!',
                'complete_path': '📁 oto.ini location: {path}',
                'complete_hint': '💡 Place this file with audio files in the same directory for UTAU',
                'dir_current': '\n💡 Found {count} audio files in current directory',
                'dir_hint': '   Enter new path to process other directory\n   Press Enter to continue with current directory\n   Enter \'q\' to exit',
                'dir_input': '\n📁 Enter new path (or press Enter to continue): ',
                'dir_switched': '✅ Switched to: {path}',
                'dir_processing': '\n📁 Processing: {path}',
                'exit': '👋 Exiting',
                'invalid_choice': '❌ Bruh. Just {range}.',
                'invalid_number': '❌ Enter a valid number',
                'invalid_range': '❌ Start position cannot be greater than end position',
                'invalid_min': '❌ Start and end positions must be >= 1',
                'threshold_range': '❌ Threshold must be between 0.001 and 0.1',
                'no_audio_found': '🔍 No audio files found. You sure they\'re in there?',
                'no_audio_menu': 'Select action:\n  1. Enter audio folder path\n  2. Move program to audio folder directory\n  3. Exit',
                'no_audio_hint': '💡 Supports auto conversion from: MP3, FLAC, M4A, AAC, OGG, WMA, AIFF, OPUS etc.',
                'no_audio_input': '📁 Enter folder path: ',
                'path_invalid': '❌ Invalid path: \'{path}\'',
                'path_hint': '💡 Double-check the path. Or pick another folder.',
                'drag_hint': '💡 Drag folder to command window, or enter path directly',
                'egg_random': '🎉 {egg}',
                'egg_project': '🎵 You found the project name! tyy485 thanks you ❤️',
                'egg_author': '👤 Author: https://github.com/tyy485',
                'egg_star': '⭐ Star this repo!',
                'egg_cool': 'Yeah, you\'re cool too! But the coolest move is to finish the whole flow.',
                'egg_minecraft': 'Oh, want to play MC? There you go.',
                'egg_progress': '🎵 Progress stuck? Just kidding. Moving on.',
                'egg_scan': '🐱 Guess what? One of these files has a cat meow in it. Not telling which.',
                'egg_startup': '🎉 Congrats on finding the hidden easter egg! Lucky day.',
                'end_menu_title': '🔗 Related Links',
                'end_menu_1': '1. Open OpenUTAU website',
                'end_menu_2': '2. Open UTAU website',
                'end_menu_3': '3. Open GitHub repository',
                'end_menu_4': '4. Export config file',
                'end_menu_5': '5. Exit',
                'end_menu_choice': 'Select (1/2/3/4/5): ',
                'end_menu_open_success': '✅ Opened {name} website',
                'end_menu_open_fail': '❌ Cannot open browser automatically',
                'end_menu_open_manual': '💡 Please visit manually: {url}',
                'end_menu_linux_no_browser': '❌ No graphical browser installed',
                'end_menu_linux_install_hint': '💡 e.g.: sudo apt install firefox',
                'end_menu_android_manual': '📱 Android device, please open link manually',
                'end_menu_press_enter': 'Press Enter to continue...',
                'end_menu_config_exported': '📁 Config saved: {path}',
                'end_menu_config_export_success': '✅ Export successful!',
                'exit_goodbye': '👋 Gone. Catch you next time.',
                'time_elapsed': '⏱️ Total time: {seconds} seconds',
                'output_dir_select': '📂 Output location',
                'output_dir_hint': 'Where should oto.ini be saved?',
                'output_dir_default': '1. Save in voicebank directory (default)',
                'output_dir_custom': '2. Custom location',
                'output_dir_choice': 'Choose 1 or 2, default 1: ',
                'output_dir_input': '📁 Enter save directory path: ',
                'output_dir_created': '✅ Directory created: {path}',
                'output_dir_not_exists': '⚠️ Directory doesn\'t exist. Create it? (1. Create 2. Re-enter): ',
                'output_dir_invalid': '❌ Invalid path. Try again.',
                'story_select': '📖 Story Library',
                'story_hint': 'If you have a lot of files and want to chill during generation, grab some stories from the internet.',
                'story_download': '1. Download stories from the internet',
                'story_builtin': '2. Use built-in stories',
                'story_choice': 'Choose 1 or 2: ',
                'story_downloading': '📡 Downloading stories...',
                'story_download_success': '✅ Downloaded! Got {count} new stories',
                'story_download_fail': '❌ Network failed. Check your connection.',
                'story_cache_hit': '📁 Stories cached locally',
                'story_fallback': '💡 Switching to built-in stories ({count} stories)',
                'story_ready': '✅ Using built-in stories ({count} stories)',
                'story_trigger': 'Oh my gosh, that\'s a LOT of files!\nI\'ll generate in the background. Wanna hear a story?',
                'story_trigger_choice': 'Choose 1 or 2: ',
                'story_trigger_yes': '1. Yes! Tell me!',
                'story_trigger_no': '2. Nah, just work',
                'story_generating': '🎯 Generating...',
                'story_export_hint': '💡 If you want to finish the story, type 6 at the end and I\'ll export it for you.',
                'story_exported': '📁 Story exported: {path}',
                'story_export_prompt': '(Type 6 to export full story, press Enter to skip): ',
                'log_export_title': '📝 Run Log',
                'log_export_hint': 'This run has ended. Export run log?\nLogs can help with troubleshooting or tracking this session.',
                'log_export_yes': '1. Export log',
                'log_export_no': '2. No, exit directly',
                'log_export_choice': 'Choose 1 or 2: ',
                'log_export_success': '📁 Log saved: {path}',
                'log_export_press': 'Press Enter to exit...',
                'error_output': 'The program encountered a {level} error! Error code: {code}',
                'error_unknown': 'The program encountered an unknown error! Error code: E???',
                'error_log_fail': 'Failed to generate error log. Reason: {reason}',
                'termux_wake_hint': 'You are likely using Termux.\nIt is recommended to run termux-wake-lock to prevent Android from killing the process,\nespecially when processing many files.',
                'termux_wake_ask': 'Do you want to exit and run it now? (y/n): ',
                'termux_wake_quit': 'Please run the following command before running the program again:\n   termux-wake-lock',
                'termux_wake_continue': 'Continuing without termux-wake-lock\n⚠️ If the process gets killed, re-run and choose y',
                'wave_read_fail': 'File format error, attempting auto repair...',
                'wave_fix_first': 'First repair attempt (standard conversion)...',
                'wave_fix_second': 'First repair failed, trying compatibility mode...',
                'wave_fix_second_desc': 'Second repair attempt (compatibility mode)...',
                'wave_fix_success': '✅ Repair successful, continuing',
                'wave_fix_fail': '❌ File repair failed: {filename}',
                'wave_fix_skip': 'Skipped this file',
                'nonhuman_detect': 'Waveform characteristics differ from human speech.\nHowever, some normal voicebanks like sine-wave synthesized ones have similar characteristics.\nProcess as normal voicebank?',
                'nonhuman_choice_1': '1. Yes, process as normal',
                'nonhuman_choice_2': '2. No, enable non-human mode',
                'nonhuman_choice_3': '3. Skip this file',
                'nonhuman_choice_prompt': 'Choose 1/2/3: ',
                'cold_storage_title': 'The following files were skipped:',
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

    def open_url(self, url):
        system = platform.system()
        if system == 'Windows':
            try:
                os.startfile(url)
                return True
            except:
                pass
            try:
                chrome_paths = [
                    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                    r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
                ]
                for path in chrome_paths:
                    if os.path.exists(path):
                        subprocess.run([path, url], timeout=2)
                        return True
            except:
                pass
            try:
                webbrowser.open(url)
                return True
            except:
                pass
            print(self.t('end_menu_open_fail'))
            print(self.t('end_menu_open_manual', url=url))
            return False
        elif system == 'Darwin':
            try:
                subprocess.run(['open', url])
                return True
            except:
                try:
                    webbrowser.open(url)
                    return True
                except:
                    print(self.t('end_menu_open_fail'))
                    print(self.t('end_menu_open_manual', url=url))
                    return False
        elif system == 'Linux':
            if 'ANDROID_ROOT' in os.environ:
                print(self.t('end_menu_android_manual'))
                print("💡 " + url)
                return False
            browsers = ['xdg-open', 'firefox', 'google-chrome', 'chromium', 'opera']
            for browser in browsers:
                if shutil.which(browser):
                    try:
                        subprocess.run([browser, url], timeout=2)
                        return True
                    except:
                        continue
            try:
                webbrowser.open(url)
                return True
            except:
                pass
            print(self.t('end_menu_linux_no_browser'))
            print(self.t('end_menu_linux_install_hint'))
            print(self.t('end_menu_open_manual', url=url))
            return False
        else:
            print(self.t('end_menu_open_fail'))
            print(self.t('end_menu_open_manual', url=url))
            return False

    def show_egg_random(self):
        if self.fast_mode:
            return
        if random.random() < 0.01:
            egg = random.choice(EGGS)
            print(self.t('egg_random', egg=egg))

    def handle_egg_command(self, user_input):
        cmd = user_input.strip().lower()
        if cmd == 'makeotoini':
            print("\n" + self.t('egg_project'))
            self.open_url('https://github.com/tyy485/makeotoini')
            return True
        elif cmd == 'tyy485':
            print("\n" + self.t('egg_author'))
            self.open_url('https://github.com/tyy485')
            return True
        elif cmd == 'star':
            print("\n" + self.t('egg_star'))
            self.open_url('https://github.com/tyy485/makeotoini')
            return True
        elif cmd == 'cool':
            print("\n" + self.t('egg_cool'))
            return True
        elif cmd == 'minecraft':
            print("\n" + self.t('egg_minecraft'))
            self.open_url('https://minecraft.net')
            return True
        elif cmd == 'fast':
            self.fast_mode = True
            print("\n⚡ Fast mode enabled")
            return True
        elif cmd == 'q':
            return 'quit'
        return False

    def check_ffmpeg(self):
        if self.ffmpeg_available is not None:
            return self.ffmpeg_available
        try:
            result = subprocess.run(['ffmpeg', '-version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=2)
            self.ffmpeg_available = (result.returncode == 0)
        except:
            self.ffmpeg_available = False
        if not self.ffmpeg_available:
            print(self.err.get('ffmpeg_missing'))
        return self.ffmpeg_available

    def check_ffprobe(self):
        if self.ffprobe_available is not None:
            return self.ffprobe_available
        try:
            result = subprocess.run(['ffprobe', '-version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=2)
            self.ffprobe_available = (result.returncode == 0)
        except:
            self.ffprobe_available = False
        if not self.ffprobe_available:
            print(self.err.get('ffprobe_missing'))
        return self.ffprobe_available

    def detect_platform(self):
        system = platform.system()
        if system == 'Darwin':
            print("🍎 还用苹果电脑，这么有钱")
        elif system == 'Android':
            print("📱 Termux？这玩意可是安卓神器")
        elif system == 'Linux':
            print("🐧 我去，居然是神级系统")
        elif system == 'Windows':
            if 'TERM' in os.environ or 'ANSICON' in os.environ:
                print("🖥️  检测到高级终端")
            else:
                print("💻 竟然是CMD，来吧，进我的生成器")
        else:
            print("🖥️  检测到系统: {system}")
        return system

    def get_user_input(self, prompt):
        empty_count = 0
        while True:
            user_input = input(prompt).strip()
            if user_input == '':
                empty_count += 1
                if empty_count == 2:
                    self.enter_recording_mode()
                    empty_count = 0
                    continue
            else:
                empty_count = 0
            if self.handle_egg_command(user_input) == 'quit':
                self.save_progress_and_exit()
            if self.handle_egg_command(user_input):
                continue
            return user_input

    def enter_recording_mode(self):
        print("\n" + "=" * 60)
        print("🎙️  检测到空行，进入录音模式")
        print("=" * 60)
        print("  录音结束后自动保存到当前音源目录。")
        print("=" * 60)
        print("  1. 开始录音（5秒）")
        print("  2. 开始录音（10秒）")
        print("  3. 自定义时长")
        print("  4. 打开系统录音软件")
        print("  5. 取消")
        print("=" * 60)
        while True:
            choice = input("请选择 1/2/3/4/5: ").strip()
            if choice == '1':
                self.record_audio(5)
                break
            elif choice == '2':
                self.record_audio(10)
                break
            elif choice == '3':
                try:
                    duration = int(input("请输入录音时长（秒）: "))
                    self.record_audio(duration)
                    break
                except ValueError:
                    print("❌ 请输入有效的数字")
            elif choice == '4':
                self.open_recording_software()
                break
            elif choice == '5':
                print("⏭️  取消录音")
                break
            else:
                print("❌ 请输入 1/2/3/4/5")

    def record_audio(self, duration):
        system = platform.system()
        if system == 'Windows':
            print("⚠️  Windows 录音功能暂不支持，请使用 Audacity 或在线录音工具")
            self.open_recording_software()
            return
        elif system == 'Darwin':
            print("🎙️  正在录音... 使用 afrecord")
            cmd = f"afrecord -d {duration} recording_{int(time.time())}.wav"
            os.system(cmd)
            print("✅ 录音完成")
        elif system == 'Linux':
            if 'ANDROID_ROOT' in os.environ:
                print("🎙️  正在录音... 使用 termux-microphone-record")
                cmd = f"termux-microphone-record -d {duration} -f recording_{int(time.time())}.wav"
                os.system(cmd)
                print("✅ 录音完成")
            else:
                print("🎙️  正在录音... 使用 arecord")
                cmd = f"arecord -f cd -t wav -d {duration} recording_{int(time.time())}.wav"
                os.system(cmd)
                print("✅ 录音完成")
        else:
            print("❌ 不支持当前系统录音，请使用其他工具")

    def open_recording_software(self):
        print("🔗 打开在线录音工具...")
        self.open_url('https://online-voice-recorder.com')

    def save_progress_and_exit(self):
        print("\n" + "=" * 60)
        print("⚠️  是否保存当前进度？")
        print("  保存后下次可以继续。")
        print("=" * 60)
        print("  1. 保存并退出")
        print("  2. 直接退出")
        print("  3. 取消，继续运行")
        print("=" * 60)
        while True:
            choice = input("请选择 1/2/3: ").strip()
            if choice == '1':
                self.save_progress()
                print("\n👋 进度已保存，下次见！")
                sys.exit(0)
            elif choice == '2':
                print("\n👋 溜了溜了，下次见！")
                sys.exit(0)
            elif choice == '3':
                print("\n✅ 继续运行")
                return
            else:
                print("❌ 请输入 1/2/3")

    def save_progress(self):
        progress_dir = os.path.expanduser('~/.makeprogress')
        os.makedirs(progress_dir, exist_ok=True)
        progress_data = {
            'version': VERSION,
            'language': self.language,
            'encoding': self.encoding,
            'clean_mode': self.clean_mode,
            'temp_mode': self.temp_mode,
            'force_reconvert': self.force_reconvert,
            'recursive_scan': self.recursive_scan,
            'silence_threshold': self.silence_threshold,
            'offset_adjust': self.offset_adjust,
            'breath_alias_template': self.breath_alias_template,
            'alias_mode': self.alias_mode,
            'alias_prefix': self.alias_prefix,
            'alias_suffix': self.alias_suffix,
            'fix_romaji': self.fix_romaji,
            'smart_prewhite': self.smart_prewhite,
            'vowel_protection': self.vowel_protection,
            'generate_frq': self.generate_frq,
            'normalize_volume': self.normalize_volume,
            'health_check': self.health_check,
            'wav_dir': self.wav_dir,
            'notes': self.notes
        }
        with open(os.path.join(progress_dir, 'progress.json'), 'w', encoding='utf-8') as f:
            json.dump(progress_data, f, indent=2, ensure_ascii=False)
        with open(os.path.join(progress_dir, 'interrupted.flag'), 'w') as f:
            f.write('1')
        print("📁 进度已保存到 ~/.makeprogress/")

    def load_progress(self):
        progress_dir = os.path.expanduser('~/.makeprogress')
        flag_path = os.path.join(progress_dir, 'interrupted.flag')
        if not os.path.exists(flag_path):
            return None
        progress_path = os.path.join(progress_dir, 'progress.json')
        if not os.path.exists(progress_path):
            return None
        try:
            with open(progress_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except:
            return None

    def select_ui_language(self):
        print("\n" + "=" * 60)
        print(self.t('ui_language_select'))
        print("=" * 60)
        print(self.t('ui_zh'))
        print(self.t('ui_en'))
        print("=" * 60)
        while True:
            choice = input(self.t('ui_choice'))
            if choice == '1' or choice.lower() in ['zh', '中文']:
                self.ui_language = 'zh'
                self.err.set_language('zh')
                print("✅ " + self.t('ui_zh_done'))
                self.show_egg_random()
                return
            elif choice == '2' or choice.lower() in ['en', 'english']:
                self.ui_language = 'en'
                self.err.set_language('en')
                print("✅ " + self.t('ui_en_done'))
                self.show_egg_random()
                return
            else:
                print(self.t('invalid_choice', range='1 或 2'))

    def check_termux_wake_lock(self):
        if platform.system() != 'Android':
            return
        print("\n" + "=" * 60)
        print("📱 检测到 Android 系统")
        print("=" * 60)
        print(self.t('termux_wake_hint'))
        print("=" * 60)
        while True:
            choice = input(self.t('termux_wake_ask')).strip().lower()
            if choice == 'y':
                print("\n💡 " + self.t('termux_wake_quit'))
                print("\n👋 " + self.t('exit_goodbye'))
                sys.exit(0)
            elif choice == 'n':
                print("\n✅ " + self.t('termux_wake_continue'))
                return
            else:
                print("❌ 请输入 y 或 n")

    def load_moic(self, path):
        try:
            with zipfile.ZipFile(path, 'r') as zf:
                enc_data = zf.read('config.json.enc')
            key = base64.urlsafe_b64encode(hashlib.sha256(b'makeotoini_secret_key_2024').digest()[:32])
            cipher = None
            try:
                from cryptography.fernet import Fernet
                cipher = Fernet(key)
                data = cipher.decrypt(enc_data)
                config = json.loads(data.decode('utf-8'))
                return config
            except ImportError:
                import hashlib
                hash_obj = hashlib.sha256()
                hash_obj.update(b'makeotoini_secret_key_2024')
                key_bytes = hash_obj.digest()
                iv = enc_data[:16]
                encrypted = enc_data[16:]
                try:
                    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
                    from cryptography.hazmat.backends import default_backend
                    cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv), backend=default_backend())
                    decryptor = cipher.decryptor()
                    decrypted = decryptor.update(encrypted) + decryptor.finalize()
                    pad_len = decrypted[-1]
                    data = decrypted[:-pad_len]
                    config = json.loads(data.decode('utf-8'))
                    return config
                except:
                    return None
        except:
            return None

    def save_moic(self, path, config):
        data = json.dumps(config, ensure_ascii=False).encode('utf-8')
        key = base64.urlsafe_b64encode(hashlib.sha256(b'makeotoini_secret_key_2024').digest()[:32])
        try:
            from cryptography.fernet import Fernet
            cipher = Fernet(key)
            enc_data = cipher.encrypt(data)
        except ImportError:
            import hashlib
            from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
            from cryptography.hazmat.backends import default_backend
            hash_obj = hashlib.sha256()
            hash_obj.update(b'makeotoini_secret_key_2024')
            key_bytes = hash_obj.digest()
            iv = os.urandom(16)
            cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv), backend=default_backend())
            encryptor = cipher.encryptor()
            pad_len = 16 - (len(data) % 16)
            padded = data + bytes([pad_len] * pad_len)
            enc_data = iv + encryptor.update(padded) + encryptor.finalize()
        with zipfile.ZipFile(path, 'w') as zf:
            zf.writestr('config.json.enc', enc_data)

    def load_config(self):
        config_path = os.path.join(os.getcwd(), '.makeotoini_config.moic')
        if os.path.exists(config_path):
            print("\n" + "=" * 60)
            print(self.t('config_detect'))
            print("=" * 60)
            print(self.t('config_found', path=config_path))
            print(self.t('config_found_hint'))
            print("=" * 60)
            print(self.t('config_use'))
            print(self.t('config_manual'))
            print("=" * 60)
            while True:
                choice = self.get_user_input(self.t('config_choice'))
                if choice == '1':
                    return self.load_config_file(config_path)
                elif choice == '2':
                    return self.manual_config_import()
                else:
                    print(self.t('invalid_choice', range='1 或 2'))
        else:
            print("\n" + "=" * 60)
            print(self.t('config_detect'))
            print("=" * 60)
            print(self.t('config_not_found'))
            print("=" * 60)
            print(self.t('config_import_option'))
            print(self.t('config_skip'))
            print("=" * 60)
            while True:
                choice = self.get_user_input(self.t('config_skip_choice'))
                if choice == '1':
                    return self.manual_config_import()
                elif choice == '2':
                    print(self.t('config_skip_confirm'))
                    return False
                else:
                    print(self.t('invalid_choice', range='1 或 2'))

    def manual_config_import(self):
        while True:
            path = self.get_user_input(self.t('config_import_hint'))
            if not path:
                return False
            if path.endswith('.json'):
                print("❌ 不支持 JSON 格式配置文件")
                print("💡 请使用 .moic 格式（由本工具导出）")
                print("💡 如需迁移旧配置，请用本工具重新导出")
                return False
            if os.path.exists(path):
                return self.load_config_file(path)
            else:
                choice = self.get_user_input(self.t('config_invalid'))
                if choice == '1':
                    continue
                elif choice == '2':
                    print(self.t('config_skip_confirm'))
                    return False
                else:
                    print(self.t('invalid_choice', range='1 或 2'))

    def load_config_file(self, path):
        try:
            data = self.load_moic(path)
            if data is None:
                print("❌ 无法解密配置文件")
                return False
            if 'ismakeoto' in data and data['ismakeoto'] == 'yes':
                return self.apply_config(data)
            else:
                print("\n" + self.t('config_warning_no_id'))
                print("=" * 60)
                print(self.t('config_force'))
                print(self.t('config_reselect'))
                print("=" * 60)
                while True:
                    choice = self.get_user_input(self.t('config_force_choice'))
                    if choice == '1':
                        print(self.t('config_force_import'))
                        return self.apply_config(data, force=True)
                    elif choice == '2':
                        return self.manual_config_import()
                    else:
                        print(self.t('invalid_choice', range='1 或 2'))
        except:
            return False

    def apply_config(self, data, force=False):
        try:
            if 'version' in data:
                config_version = data['version']
                if config_version != VERSION:
                    new_options = []
                    if self.language == 'japanese':
                        new_options.append('删除罗马音并保留假名 / 删除假名并保留罗马音')
                    elif self.language == 'korean':
                        new_options.append('删除罗马音并保留谚文 / 删除谚文并保留罗马音')
                    if new_options:
                        print("\n" + self.t('config_version_old', old=config_version, new=VERSION))
                        print(self.t('config_version_new'))
                        for opt in new_options:
                            print("  - " + opt)
                        print(self.t('config_version_continue'))
            else:
                print("\n" + self.t('config_missing_version'))
                data['version'] = VERSION
                print(self.t('config_missing_fill', version=VERSION))

            if 'language' in data:
                self.language = data['language']
            if 'encoding' in data:
                self.encoding = data['encoding']
            if 'clean_mode' in data:
                self.clean_mode = data['clean_mode']
            if 'temp_mode' in data:
                self.temp_mode = data['temp_mode']
            if 'force_reconvert' in data:
                self.force_reconvert = data['force_reconvert']
            if 'recursive_scan' in data:
                self.recursive_scan = data['recursive_scan']
            if 'silence_threshold' in data:
                self.silence_threshold = data['silence_threshold']
            if 'offset_adjust' in data:
                self.offset_adjust = data['offset_adjust']
            if 'breath_alias_template' in data:
                self.breath_alias_template = data['breath_alias_template']
                if 'x' in self.breath_alias_template or '{x}' in self.breath_alias_template or '<x>' in self.breath_alias_template:
                    self.breath_has_placeholder = True
            if 'alias_mode' in data:
                self.alias_mode = data['alias_mode']
            if 'alias_prefix' in data:
                self.alias_prefix = data['alias_prefix']
            if 'alias_suffix' in data:
                self.alias_suffix = data['alias_suffix']
            if 'fix_romaji' in data:
                self.fix_romaji = data['fix_romaji']
            if 'smart_prewhite' in data:
                self.smart_prewhite = data['smart_prewhite']
            if 'vowel_protection' in data:
                self.vowel_protection = data['vowel_protection']
            if 'generate_frq' in data:
                self.generate_frq = data['generate_frq']
            if 'normalize_volume' in data:
                self.normalize_volume = data['normalize_volume']
            if 'health_check' in data:
                self.health_check = data['health_check']

            print(self.t('config_import_success'))
            input(self.t('end_menu_press_enter'))
            return True
        except:
            return False

    def select_language(self):
        print("\n" + "=" * 60)
        print(self.t('config_lang_select'))
        print("=" * 60)
        print(self.t('config_lang_jp'))
        print(self.t('config_lang_zh'))
        print(self.t('config_lang_ko'))
        print(self.t('config_lang_en'))
        print(self.t('config_lang_special'))
        print("=" * 60)
        while True:
            choice = self.get_user_input(self.t('config_lang_choice'))
            if choice == '1' or choice.lower() in ['japanese', 'ja', '日', '日本']:
                self.language = 'japanese'
                print("✅ " + self.t('config_lang_jp_done'))
                return
            elif choice == '2' or choice.lower() in ['chinese', 'zh', '中', '中文']:
                self.language = 'chinese'
                print("✅ " + self.t('config_lang_zh_done'))
                return
            elif choice == '3' or choice.lower() in ['korean', 'ko', '한', '한국']:
                self.language = 'korean'
                print("✅ " + self.t('config_lang_ko_done'))
                return
            elif choice == '4' or choice.lower() in ['english', 'en', '英']:
                self.language = 'english'
                print("✅ " + self.t('config_lang_en_done'))
                return
            elif choice == '5' or choice.lower() in ['special', 'constructed', 'unknown']:
                self.language = 'special'
                print("✅ " + self.t('config_lang_special_done'))
                print(self.t('special_threshold_warn'))
                print(self.t('special_threshold_apply'))
                self.silence_threshold = 0.1
                return
            else:
                print(self.t('invalid_choice', range='1、2、3、4 或 5'))

    def select_encoding(self):
        print("\n" + "=" * 60)
        print(self.t('encoding_select'))
        print("=" * 60)
        print(self.t('encoding_gb'))
        print(self.t('encoding_sjis'))
        print(self.t('encoding_utf8'))
        print(self.t('encoding_euckr'))
        print(self.t('encoding_smart'))
        print("=" * 60)
        while True:
            choice = self.get_user_input(self.t('encoding_choice'))
            if choice == '1' or choice.lower() == 'gb2312' or choice.lower() == 'gb 2312':
                self.encoding = 'gb2312'
                print("✅ " + self.t('encoding_gb_done'))
                return
            elif choice == '2' or choice.lower() == 'shift-jis' or choice.lower() == 'shiftjis':
                self.encoding = 'shift-jis'
                print("✅ " + self.t('encoding_sjis_done'))
                return
            elif choice == '3' or choice.lower() == 'utf-8' or choice.lower() == 'utf8':
                self.encoding = 'utf-8'
                print("✅ " + self.t('encoding_utf8_done'))
                return
            elif choice == '4' or choice.lower() == 'euc-kr' or choice.lower() == 'euckr':
                self.encoding = 'euc-kr'
                print("✅ " + self.t('encoding_euckr_done'))
                return
            elif choice == '5' or choice.lower() == 'smart':
                if self.language == 'japanese':
                    self.encoding = 'shift-jis'
                elif self.language == 'chinese':
                    self.encoding = 'gb2312'
                elif self.language == 'korean':
                    self.encoding = 'euc-kr'
                elif self.language == 'english':
                    self.encoding = 'utf-8'
                else:
                    self.encoding = 'utf-8'
                print("✅ " + self.t('encoding_smart_done'))
                print(self.t('encoding_smart_info', encoding=self.encoding))
                return
            else:
                print(self.t('invalid_choice', range='1、2、3、4 或 5'))

    def select_clean_mode(self):
        print("\n" + "=" * 60)
        print(self.t('clean_select'))
        print("=" * 60)
        print(self.t('clean_ask'))
        print(self.t('clean_auto'))
        print(self.t('clean_skip'))
        print("=" * 60)
        while True:
            choice = self.get_user_input(self.t('clean_choice'))
            if choice == '1':
                self.clean_mode = 'ask'
                print("✅ " + self.t('clean_ask_done'))
                return
            elif choice == '2':
                self.clean_mode = 'auto'
                print("✅ " + self.t('clean_auto_done'))
                return
            elif choice == '3':
                self.clean_mode = 'skip'
                print("✅ " + self.t('clean_skip_done'))
                return
            else:
                print(self.t('invalid_choice', range='1、2 或 3'))

    def select_temp_mode(self):
        print("\n" + "=" * 60)
        print(self.t('temp_select'))
        print("=" * 60)
        print(self.t('temp_keep'))
        print(self.t('temp_temp'))
        print("=" * 60)
        while True:
            choice = self.get_user_input(self.t('temp_choice'))
            if choice == '1':
                self.temp_mode = False
                print("✅ " + self.t('temp_keep_done'))
                return
            elif choice == '2':
                self.temp_mode = True
                print("✅ " + self.t('temp_temp_done'))
                return
            else:
                print(self.t('invalid_choice', range='1 或 2'))

    def select_reconvert_mode(self):
        print("\n" + "=" * 60)
        print(self.t('reconvert_select'))
        print("=" * 60)
        print(self.t('reconvert_force'))
        print(self.t('reconvert_reuse'))
        print("=" * 60)
        while True:
            choice = self.get_user_input(self.t('reconvert_choice'))
            if choice == '1':
                self.force_reconvert = True
                print("✅ " + self.t('reconvert_force_done'))
                return
            elif choice == '2':
                self.force_reconvert = False
                print("✅ " + self.t('reconvert_reuse_done'))
                return
            else:
                print(self.t('invalid_choice', range='1 或 2'))

    def select_scan_mode(self):
        print("\n" + "=" * 60)
        print(self.t('scan_select'))
        print("=" * 60)
        print(self.t('scan_recursive'))
        print(self.t('scan_current'))
        print("=" * 60)
        while True:
            choice = self.get_user_input(self.t('scan_choice'))
            if choice == '1':
                self.recursive_scan = True
                print("✅ " + self.t('scan_recursive_done'))
                return
            elif choice == '2':
                self.recursive_scan = False
                print("✅ " + self.t('scan_current_done'))
                return
            else:
                print(self.t('invalid_choice', range='1 或 2'))

    def select_silence_threshold(self):
        print("\n" + "=" * 60)
        print(self.t('silence_select'))
        print("=" * 60)
        print(self.t('silence_low'))
        print(self.t('silence_medium'))
        print(self.t('silence_high'))
        print(self.t('silence_manual'))
        print("=" * 60)
        while True:
            choice = self.get_user_input(self.t('silence_choice'))
            if choice == '1':
                self.silence_threshold = 0.02
                print("✅ " + self.t('silence_low_done', threshold=self.silence_threshold))
                return
            elif choice == '2':
                self.silence_threshold = 0.01
                print("✅ " + self.t('silence_medium_done', threshold=self.silence_threshold))
                return
            elif choice == '3':
                self.silence_threshold = 0.005
                print("✅ " + self.t('silence_high_done', threshold=self.silence_threshold))
                return
            elif choice == '4':
                while True:
                    try:
                        threshold = float(self.get_user_input(self.t('silence_manual_input')))
                        if 0.001 <= threshold <= 0.1:
                            self.silence_threshold = threshold
                            print("✅ " + self.t('silence_manual_done', threshold=self.silence_threshold))
                            return
                        else:
                            print(self.t('threshold_range'))
                    except ValueError:
                        print(self.t('invalid_number'))
            else:
                print(self.t('invalid_choice', range='1、2、3 或 4'))

    def select_offset_adjust(self):
        print("\n" + "=" * 60)
        print(self.t('offset_adjust_select'))
        print("=" * 60)
        print(self.t('offset_adjust_hint'))
        print("=" * 60)
        while True:
            value = self.get_user_input(self.t('offset_adjust_input'))
            if value == '':
                self.offset_adjust = 0
                print(self.t('offset_adjust_done_zero'))
                return
            try:
                self.offset_adjust = int(value)
                if self.offset_adjust > 0:
                    print(self.t('offset_adjust_done_positive', value=self.offset_adjust))
                elif self.offset_adjust < 0:
                    print(self.t('offset_adjust_done_negative', value=abs(self.offset_adjust)))
                else:
                    print(self.t('offset_adjust_done_zero'))
                return
            except ValueError:
                print(self.t('invalid_number'))

    def select_breath_alias(self):
        print("\n" + "=" * 60)
        print(self.t('breath_alias_select'))
        print("=" * 60)
        print(self.t('breath_alias_hint'))
        print(self.t('breath_alias_examples'))
        print("=" * 60)
        while True:
            template = self.get_user_input(self.t('breath_alias_input'))
            if template == '':
                template = 'breath'
            self.breath_alias_template = template
            if 'x' in template or '{x}' in template or '<x>' in template:
                self.breath_has_placeholder = True
                self.breath_warned = True
                print("✅ " + self.t('breath_alias_done', template=template))
                return
            else:
                if not self.breath_warned:
                    print(self.t('breath_alias_warning'))
                    self.breath_warned = True
                    continue
                else:
                    print(self.t('breath_alias_warning2'))
                    self.breath_has_placeholder = False
                    print("✅ " + self.t('breath_alias_done', template=template))
                    return

    def select_alias_mode(self):
        print("\n" + "=" * 60)
        print(self.t('alias_select'))
        print("=" * 60)
        if self.language == 'japanese':
            print(self.t('alias_none'))
            print(self.t('alias_add_prefix'))
            print(self.t('alias_remove_prefix'))
            print(self.t('alias_remove_suffix'))
            print(self.t('alias_add_suffix'))
            print(self.t('alias_slice'))
            print(self.t('alias_keep_kana'))
            print(self.t('alias_keep_romaji'))
        elif self.language == 'korean':
            print(self.t('alias_none'))
            print(self.t('alias_add_prefix'))
            print(self.t('alias_remove_prefix'))
            print(self.t('alias_remove_suffix'))
            print(self.t('alias_add_suffix'))
            print(self.t('alias_slice'))
            print(self.t('alias_keep_hangul'))
            print(self.t('alias_keep_roman'))
        else:
            print(self.t('alias_none'))
            print(self.t('alias_add_prefix'))
            print(self.t('alias_remove_prefix'))
            print(self.t('alias_remove_suffix'))
            print(self.t('alias_add_suffix'))
            print(self.t('alias_slice'))
        print("=" * 60)
        while True:
            choice = self.get_user_input(self.t('alias_choice'))
            if choice == '1':
                self.alias_mode = 'none'
                print("✅ " + self.t('alias_none_done'))
                return
            elif choice == '2':
                self.alias_mode = 'add_prefix'
                prefix = self.get_user_input(self.t('alias_prefix_input'))
                self.alias_prefix = prefix
                print("✅ " + self.t('alias_add_prefix_done', prefix=prefix))
                return
            elif choice == '3':
                self.alias_mode = 'remove_prefix'
                prefix = self.get_user_input(self.t('alias_prefix_remove_input'))
                self.alias_prefix = prefix
                while True:
                    remove_all = self.get_user_input(self.t('alias_remove_all_prefix')).upper()
                    if remove_all == '' or remove_all == 'N':
                        self.remove_all_prefix = False
                        break
                    elif remove_all == 'Y':
                        self.remove_all_prefix = True
                        break
                    else:
                        print(self.t('invalid_choice', range='Y 或 N'))
                print("✅ " + self.t('alias_remove_prefix_done', prefix=prefix))
                if self.remove_all_prefix:
                    print("   💡 将删除所有匹配的前缀")
                else:
                    print("   💡 只删除第一个匹配的前缀")
                return
            elif choice == '4':
                self.alias_mode = 'remove_suffix'
                suffix = self.get_user_input(self.t('alias_suffix_remove_input'))
                self.alias_suffix = suffix
                while True:
                    remove_all = self.get_user_input(self.t('alias_remove_all_suffix')).upper()
                    if remove_all == '' or remove_all == 'N':
                        self.remove_all_suffix = False
                        break
                    elif remove_all == 'Y':
                        self.remove_all_suffix = True
                        break
                    else:
                        print(self.t('invalid_choice', range='Y 或 N'))
                print("✅ " + self.t('alias_remove_suffix_done', suffix=suffix))
                if self.remove_all_suffix:
                    print("   💡 将删除所有匹配的后缀")
                else:
                    print("   💡 只删除第一个匹配的后缀")
                return
            elif choice == '5':
                self.alias_mode = 'add_suffix'
                suffix = self.get_user_input(self.t('alias_suffix_input'))
                self.alias_suffix = suffix
                print("✅ " + self.t('alias_add_suffix_done', suffix=suffix))
                return
            elif choice == '6':
                self.alias_mode = 'slice'
                print(self.t('alias_slice_hint'))
                while True:
                    try:
                        start = self.get_user_input(self.t('alias_slice_start'))
                        end = self.get_user_input(self.t('alias_slice_end'))
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
                        print("✅ " + self.t('alias_slice_done', start=start, end=end))
                        return
                    except ValueError:
                        print(self.t('invalid_number'))
                        continue
            elif choice == '7':
                if self.language == 'japanese':
                    self.alias_mode = 'keep_kana_remove_romaji'
                    print("✅ " + self.t('alias_keep_kana_done'))
                    return
                elif self.language == 'korean':
                    self.alias_mode = 'keep_hangul_remove_roman'
                    print("✅ " + self.t('alias_keep_hangul_done'))
                    return
                else:
                    print(self.t('invalid_choice', range='1、2、3、4、5、6、7、8'))
            elif choice == '8':
                if self.language == 'japanese':
                    self.alias_mode = 'keep_romaji_remove_kana'
                    print("✅ " + self.t('alias_keep_romaji_done'))
                    return
                elif self.language == 'korean':
                    self.alias_mode = 'keep_roman_remove_hangul'
                    print("✅ " + self.t('alias_keep_roman_done'))
                    return
                else:
                    print(self.t('invalid_choice', range='1、2、3、4、5、6、7、8'))
            else:
                print(self.t('invalid_choice', range='1、2、3、4、5、6、7、8'))

    def select_romaji_fix(self):
        if self.language in ['japanese', 'korean']:
            print("\n" + "=" * 60)
            print(self.t('romaji_fix_select'))
            print("=" * 60)
            print(self.t('romaji_fix_enable'))
            print(self.t('romaji_fix_disable'))
            print("=" * 60)
            while True:
                choice = self.get_user_input(self.t('romaji_fix_choice'))
                if choice == '1':
                    self.fix_romaji = True
                    print("✅ " + self.t('romaji_fix_enabled'))
                    return
                elif choice == '2':
                    self.fix_romaji = False
                    print("✅ " + self.t('romaji_fix_disabled'))
                    return
                else:
                    print(self.t('invalid_choice', range='1 或 2'))
        else:
            self.fix_romaji = False
            print(self.t('romaji_fix_skip'))

    def select_smart_prewhite(self):
        print("\n" + "=" * 60)
        print(self.t('smart_prewhite_select'))
        print("=" * 60)
        print(self.t('smart_prewhite_hint'))
        print("=" * 60)
        print(self.t('smart_prewhite_enable'))
        print(self.t('smart_prewhite_disable'))
        print("=" * 60)
        while True:
            choice = self.get_user_input(self.t('smart_prewhite_choice'))
            if choice == '' or choice == '1':
                self.smart_prewhite = True
                print(self.t('smart_prewhite_enabled'))
                return
            elif choice == '2':
                self.smart_prewhite = False
                print(self.t('smart_prewhite_disabled'))
                return
            else:
                print(self.t('invalid_choice', range='1 或 2'))

    def select_vowel_protection(self):
        print("\n" + "=" * 60)
        print(self.t('vowel_protect_select'))
        print("=" * 60)
        print(self.t('vowel_protect_hint'))
        print("=" * 60)
        print(self.t('vowel_protect_enable'))
        print(self.t('vowel_protect_disable'))
        print("=" * 60)
        while True:
            choice = self.get_user_input(self.t('vowel_protect_choice'))
            if choice == '' or choice == '1':
                self.vowel_protection = True
                print(self.t('vowel_protect_enabled'))
                return
            elif choice == '2':
                self.vowel_protection = False
                print(self.t('vowel_protect_disabled'))
                return
            else:
                print(self.t('invalid_choice', range='1 或 2'))

    def select_frq(self):
        print("\n" + "=" * 60)
        print(self.t('frq_select'))
        print("=" * 60)
        print(self.t('frq_hint'))
        print("=" * 60)
        print(self.t('frq_enable'))
        print(self.t('frq_disable'))
        print("=" * 60)
        while True:
            choice = self.get_user_input(self.t('frq_choice'))
            if choice == '' or choice == '2':
                self.generate_frq = False
                print(self.t('frq_disabled'))
                return
            elif choice == '1':
                self.generate_frq = True
                print(self.t('frq_enabled'))
                return
            else:
                print(self.t('invalid_choice', range='1 或 2'))

    def select_normalize_volume(self):
        print("\n" + "=" * 60)
        print(self.t('normalize_select'))
        print("=" * 60)
        print(self.t('normalize_hint'))
        print("=" * 60)
        print(self.t('normalize_enable'))
        print(self.t('normalize_disable'))
        print("=" * 60)
        while True:
            choice = self.get_user_input(self.t('normalize_choice'))
            if choice == '' or choice == '2':
                self.normalize_volume = False
                print(self.t('normalize_disabled'))
                return
            elif choice == '1':
                if not self.check_ffmpeg():
                    print(self.err.get('ffmpeg_missing'))
                    print(self.t('normalize_disabled'))
                    self.normalize_volume = False
                    return
                self.normalize_volume = True
                print(self.t('normalize_enabled'))
                return
            else:
                print(self.t('invalid_choice', range='1 或 2'))

    def select_health_check(self):
        print("\n" + "=" * 60)
        print(self.t('health_check_select'))
        print("=" * 60)
        print(self.t('health_check_hint'))
        print("=" * 60)
        print(self.t('health_check_enable'))
        print(self.t('health_check_disable'))
        print("=" * 60)
        while True:
            choice = self.get_user_input(self.t('health_check_choice'))
            if choice == '' or choice == '2':
                self.health_check = False
                print(self.t('health_check_disabled'))
                return
            elif choice == '1':
                self.health_check = True
                print(self.t('health_check_enabled'))
                return
            else:
                print(self.t('invalid_choice', range='1 或 2'))

    def select_character_generation(self):
        print("\n" + "=" * 60)
        print(self.t('character_select'))
        print("=" * 60)
        print(self.t('character_enable'))
        print(self.t('character_disable'))
        print("=" * 60)
        while True:
            choice = self.get_user_input(self.t('character_choice'))
            if choice == '1':
                self.generate_character = True
                print("✅ " + self.t('character_enabled'))
                name = self.get_user_input(self.t('character_name_input'))
                if name:
                    self.character_name = name
                    print("✅ " + self.t('character_name_done', name=name))
                else:
                    self.character_name = ''
                    print("⚠️  歌手名称未填写，将跳过此字段")
                version = self.get_user_input(self.t('character_version_input'))
                if version:
                    self.character_version = version
                    print("✅ " + self.t('character_version_done', version=version))
                else:
                    self.character_version = ''
                web = self.get_user_input(self.t('character_web_input'))
                if web:
                    self.character_web = web
                    print("✅ " + self.t('character_web_done', web=web))
                else:
                    self.character_web = ''
                self.select_character_image()
                return
            elif choice == '2':
                self.generate_character = False
                print("✅ " + self.t('character_disabled'))
                return
            else:
                print(self.t('invalid_choice', range='1 或 2'))

    def select_character_image(self):
        print("\n" + "=" * 60)
        print(self.t('character_image_select'))
        print("=" * 60)
        print(self.t('character_image_hint'))
        image_path = self.get_user_input(self.t('character_image_input'))
        if image_path:
            self.character_image = image_path
            print("✅ " + self.t('character_image_done', image=image_path))
        else:
            self.character_image = ''
            print(self.t('character_image_skip'))

    def is_breath_file(self, filename):
        base_name = os.path.splitext(filename)[0].lower()
        if re.match(r'^br(_?\d+)?$', base_name):
            return True
        breath_words = ['呼', '吸', 'breathe', 'breath']
        for word in breath_words:
            if word in base_name.split('_'):
                return True
            if base_name == word:
                return True
        return False

    def get_breath_alias(self):
        self.breath_counter += 1
        template = self.breath_alias_template
        if self.breath_has_placeholder:
            template = template.replace('{x}', str(self.breath_counter))
            template = template.replace('<x>', str(self.breath_counter))
            template = template.replace('x', str(self.breath_counter))
        else:
            if self.breath_counter > 1:
                template = template + str(self.breath_counter)
        return template

    def extract_kana(self, text):
        kana_pattern = re.compile(r'[\u3040-\u309f\u30a0-\u30ff\u31f0-\u31ff]')
        return ''.join(kana_pattern.findall(text))

    def extract_hangul(self, text):
        hangul_pattern = re.compile(r'[\uac00-\ud7af\u1100-\u11ff\u3130-\u318f]')
        return ''.join(hangul_pattern.findall(text))

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
        if '_' in base_name:
            parts = base_name.split('_', 1)
            kana_part = parts[0]
            romaji_part = parts[1] if len(parts) > 1 else ''
            if self.language == 'japanese':
                script = self.extract_kana(kana_part)
                if script:
                    fixed_kana = self.kana_to_romaji_str(script)
                    new_base = fixed_kana + '_' + romaji_part
                    return new_base + ext
            elif self.language == 'korean':
                script = self.extract_hangul(kana_part)
                if script:
                    fixed_kana = self.hangul_to_roman_str(script)
                    new_base = fixed_kana + '_' + romaji_part
                    return new_base + ext
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

    def apply_alias(self, filename, is_breath=False):
        base_name = os.path.splitext(filename)[0]
        if is_breath:
            alias = self.get_breath_alias()
        else:
            if self.fix_romaji and self.language in ['japanese', 'korean']:
                alias = self.fix_romaji_in_filename(base_name)
            else:
                alias = base_name
        if self.alias_mode == 'none':
            return alias
        elif self.alias_mode == 'add_prefix':
            return self.alias_prefix + alias
        elif self.alias_mode == 'remove_prefix':
            if self.remove_all_prefix:
                while alias.startswith(self.alias_prefix):
                    alias = alias[len(self.alias_prefix):]
                return alias
            else:
                if alias.startswith(self.alias_prefix):
                    return alias[len(self.alias_prefix):]
                return alias
        elif self.alias_mode == 'remove_suffix':
            if self.remove_all_suffix:
                while alias.endswith(self.alias_suffix):
                    alias = alias[:-len(self.alias_suffix)]
                return alias
            else:
                if alias.endswith(self.alias_suffix):
                    return alias[:-len(self.alias_suffix)]
                return alias
        elif self.alias_mode == 'add_suffix':
            return alias + self.alias_suffix
        elif self.alias_mode == 'slice':
            if len(alias) < self.alias_end:
                print(self.t('alias_slice_warning', length=len(alias), end=self.alias_end))
                return alias
            return alias[:self.alias_start] + alias[self.alias_end:]
        elif self.alias_mode == 'keep_kana_remove_romaji':
            parts = alias.split('_')
            if len(parts) >= 2:
                return parts[0]
            return alias
        elif self.alias_mode == 'keep_romaji_remove_kana':
            parts = alias.split('_')
            if len(parts) >= 2:
                return '_'.join(parts[1:])
            return alias
        elif self.alias_mode == 'keep_hangul_remove_roman':
            parts = alias.split('_')
            if len(parts) >= 2:
                return parts[0]
            return alias
        elif self.alias_mode == 'keep_roman_remove_hangul':
            parts = alias.split('_')
            if len(parts) >= 2:
                return '_'.join(parts[1:])
            return alias
        return alias

    def is_audio_file(self, filepath):
        audio_extensions = {'.mp3', '.flac', '.m4a', '.aac', '.ogg', '.wma', '.aiff', '.aif', '.opus', '.wav', '.pcm', '.mp4', '.m4p', '.m4b', '.m4r', '.3gp', '.amr', '.awb'}
        ext = os.path.splitext(filepath)[1].lower()
        if ext in audio_extensions:
            return True
        try:
            with open(filepath, 'rb') as f:
                header = f.read(12)
                magic_bytes = {b'ID3': True, b'fLaC': True, b'ftyp': True, b'OggS': True, b'RIFF': True, b'FORM': True, b'MThd': True}
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
                    offset_val = 128
                elif sampwidth == 2:
                    max_val = 32768
                    offset_val = 0
                else:
                    return 0
                chunk_size = min(1024, frames)
                silent_samples = 0
                max_amplitude = 0
                scan_samples = int(rate * self.silence_scan_duration / 1000)
                scan_duration = min(scan_samples, frames)
                for _ in range(0, scan_duration, chunk_size):
                    data = wf.readframes(chunk_size)
                    if not data:
                        break
                    samples = []
                    for i in range(0, len(data), sampwidth):
                        if sampwidth == 1:
                            sample = data[i] - offset_val
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

    def detect_breath_zone(self, wav_path, silence_pos):
        if not self.smart_prewhite:
            return 0
        try:
            with wave.open(wav_path, 'rb') as wf:
                frames = wf.getnframes()
                rate = wf.getframerate()
                sampwidth = wf.getsampwidth()
                if sampwidth == 1:
                    max_val = 127
                    offset_val = 128
                elif sampwidth == 2:
                    max_val = 32768
                    offset_val = 0
                else:
                    return 0
                chunk_size = min(2048, frames)
                breath_samples = 0
                breath_threshold = 0.005
                start_sample = int(silence_pos / 1000 * rate)
                if start_sample >= frames:
                    return 0
                wf.setpos(start_sample)
                max_scan = min(rate // 5, frames - start_sample)
                scanned = 0
                while scanned < max_scan:
                    data = wf.readframes(min(chunk_size, max_scan - scanned))
                    if not data:
                        break
                    samples = []
                    for i in range(0, len(data), sampwidth):
                        if sampwidth == 1:
                            sample = data[i] - offset_val
                        elif sampwidth == 2:
                            sample = int.from_bytes(data[i:i+2], 'little', signed=True)
                        else:
                            break
                        samples.append(sample)
                    if len(samples) == 0:
                        break
                    rms = (sum(s**2 for s in samples) / len(samples)) ** 0.5
                    normalized_rms = rms / max_val
                    if normalized_rms > breath_threshold:
                        break
                    if normalized_rms > 0.0005:
                        breath_samples += len(samples)
                    scanned += len(samples)
                breath_duration = int(breath_samples / rate * 1000)
                if breath_duration < 30 or breath_duration > 200:
                    return 0
                return breath_duration
        except:
            return 0

    def is_vowel_only(self, filename):
        vowels = ['a', 'i', 'u', 'e', 'o']
        name = os.path.splitext(filename)[0].lower()
        if name in ['q', '-']:
            return False
        if name in vowels:
            return True
        return False

    def normalize_audio_volume(self, audio_path):
        if not self.normalize_volume or not self.check_ffmpeg():
            return audio_path
        try:
            base_name = os.path.splitext(audio_path)[0]
            temp_path = base_name + '_norm.wav'
            cmd = ['ffmpeg', '-i', audio_path, '-af', 'loudnorm=I=-23:LRA=7:TP=-2', '-y', temp_path]
            result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60)
            if result.returncode == 0 and os.path.exists(temp_path):
                os.replace(temp_path, audio_path)
                return audio_path
            else:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                return audio_path
        except:
            return audio_path

    def generate_frq(self, wav_path):
        try:
            with wave.open(wav_path, 'rb') as wf:
                frames = wf.getnframes()
                rate = wf.getframerate()
                sampwidth = wf.getsampwidth()
                data = wf.readframes(frames)
            if sampwidth != 2:
                return None
            samples = []
            for i in range(0, len(data), 2):
                sample = struct.unpack('<h', data[i:i+2])[0]
                samples.append(sample)
            block_size = 256
            step = 128
            total_blocks = max(1, (len(samples) - block_size) // step + 1)
            frq_values = []
            for i in range(total_blocks):
                start = i * step
                end = min(start + block_size, len(samples))
                chunk = samples[start:end]
                max_amp = max(abs(s) for s in chunk) or 1
                chunk = [s / max_amp for s in chunk]
                min_period = int(rate / 800)
                max_period = int(rate / 80)
                best_period = 1
                best_corr = 0
                for period in range(min_period, min(max_period, len(chunk) // 2)):
                    corr = 0
                    for j in range(len(chunk) - period):
                        corr += chunk[j] * chunk[j + period]
                    if corr > best_corr:
                        best_corr = corr
                        best_period = period
                if best_corr > 10 and best_period > 0:
                    pitch = rate / best_period
                    pitch = max(60, min(1000, pitch))
                else:
                    pitch = -1
                frq_values.append(pitch)
            frq_path = wav_path.replace('.wav', '.frq')
            with open(frq_path, 'wb') as f:
                f.write(struct.pack('<i', len(frq_values)))
                f.write(struct.pack('<i', rate))
                for val in frq_values:
                    f.write(struct.pack('<f', val))
            return frq_path
        except:
            return None

    def convert_to_wav(self, audio_path, retry=2):
        if not self.check_ffmpeg():
            return None
        if self.temp_mode:
            temp_dir = tempfile.gettempdir()
            base_name = os.path.splitext(os.path.basename(audio_path))[0]
            wav_path = os.path.join(temp_dir, base_name + '.wav')
        else:
            base_name = os.path.splitext(audio_path)[0]
            wav_path = base_name + '.wav'
        if not self.force_reconvert and os.path.exists(wav_path) and self.is_wav_file(wav_path):
            if os.path.getmtime(wav_path) >= os.path.getmtime(audio_path):
                return wav_path
        for attempt in range(retry):
            try:
                if not self.fast_mode:
                    print(self.t('scan_found_audio', filename=os.path.basename(audio_path)))
                cmd = ['ffmpeg', '-i', audio_path, '-ar', '44100', '-ac', '1', '-sample_fmt', 's16', '-y', wav_path]
                result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30)
                if result.returncode == 0 and os.path.exists(wav_path) and self.is_wav_file(wav_path):
                    self.converted_files.append(audio_path)
                    if self.temp_mode:
                        self.temp_wav_files.append(wav_path)
                    if not self.fast_mode:
                        print(self.t('convert_success', filename=os.path.basename(wav_path)))
                    return wav_path
                else:
                    if attempt < retry - 1:
                        if not self.fast_mode:
                            print("⏰ 转码失败，重试 " + str(attempt+2) + "/" + str(retry))
                        continue
                    print(self.err.get('ffmpeg_timeout', filename=os.path.basename(audio_path)))
                    return None
            except subprocess.TimeoutExpired:
                if attempt < retry - 1:
                    if not self.fast_mode:
                        print("⏰ 超时，重试 " + str(attempt+2) + "/" + str(retry))
                    continue
                print(self.err.get('ffmpeg_timeout', filename=os.path.basename(audio_path)))
                return None
            except Exception:
                if attempt < retry - 1:
                    continue
                print(self.err.get('ffmpeg_missing'))
                return None
        return None

    def repair_wav_with_ffmpeg(self, wav_path):
        print(self.t('wave_read_fail'))
        temp_path = wav_path + '.tmp.wav'

        print(self.t('wave_fix_first'))
        cmd1 = ['ffmpeg', '-i', wav_path, '-ar', '44100', '-ac', '1', '-sample_fmt', 's16', '-acodec', 'pcm_s16le', '-y', temp_path]
        result1 = subprocess.run(cmd1, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30)
        if result1.returncode == 0 and self.is_wav_file(temp_path):
            os.replace(temp_path, wav_path)
            print(self.t('wave_fix_success'))
            return True

        print(self.t('wave_fix_second'))
        cmd2 = ['ffmpeg', '-i', wav_path, '-ar', '22050', '-ac', '1', '-sample_fmt', 's16', '-acodec', 'pcm_s16le', '-af', 'aresample=async=1', '-y', temp_path]
        result2 = subprocess.run(cmd2, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30)
        if result2.returncode == 0 and self.is_wav_file(temp_path):
            os.replace(temp_path, wav_path)
            print(self.t('wave_fix_success'))
            return True

        if os.path.exists(temp_path):
            os.remove(temp_path)
        print(self.t('wave_fix_fail', filename=os.path.basename(wav_path)))
        return False

    def check_wave_readable(self, wav_path):
        try:
            with wave.open(wav_path, 'rb') as wf:
                wf.getnframes()
                return True
        except:
            return False

    def analyze_waveform(self, wav_path):
        if not self.check_wave_readable(wav_path):
            if not self.repair_wav_with_ffmpeg(wav_path):
                print(self.t('wave_fix_skip'))
                return None
        try:
            with wave.open(wav_path, 'rb') as wf:
                frames = wf.getnframes()
                rate = wf.getframerate()
                sampwidth = wf.getsampwidth()
                data = wf.readframes(frames)
            if sampwidth != 2:
                return None
            samples = []
            for i in range(0, len(data), 2):
                sample = struct.unpack('<h', data[i:i+2])[0]
                samples.append(sample)
            rms = (sum(s**2 for s in samples) / len(samples)) ** 0.5
            max_amp = max(abs(s) for s in samples)
            return {'rms': rms, 'max_amp': max_amp, 'rate': rate, 'samples': samples}
        except:
            return None

    def detect_nonhuman_waveform(self, wav_path):
        result = self.analyze_waveform(wav_path)
        if result is None:
            return False
        rms = result['rms']
        max_amp = result['max_amp']
        if rms < 10 or max_amp < 50:
            return True
        return False

    def get_wav_duration(self, wav_path):
        try:
            with wave.open(wav_path, 'rb') as wf:
                frames = wf.getnframes()
                rate = wf.getframerate()
                return int(frames / rate * 1000)
        except:
            if self.check_ffprobe():
                try:
                    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', wav_path], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=5)
                    if result.returncode == 0 and result.stdout:
                        duration = float(result.stdout.decode().strip())
                        return int(duration * 1000)
                except:
                    pass
            print(self.err.get('wav_corrupt', filename=os.path.basename(wav_path)))
            return 500

    def select_output_directory(self):
        print("\n" + "=" * 60)
        print(self.t('output_dir_select'))
        print("=" * 60)
        print(self.t('output_dir_hint'))
        print("=" * 60)
        print(self.t('output_dir_default'))
        print(self.t('output_dir_custom'))
        print("=" * 60)
        while True:
            choice = self.get_user_input(self.t('output_dir_choice'))
            if choice == '' or choice == '1':
                return self.wav_dir
            elif choice == '2':
                while True:
                    custom_dir = self.get_user_input(self.t('output_dir_input'))
                    if os.path.exists(custom_dir):
                        if os.path.isdir(custom_dir):
                            return custom_dir
                        else:
                            print(self.t('output_dir_invalid'))
                            continue
                    else:
                        print(self.t('output_dir_not_exists'))
                        while True:
                            create_choice = self.get_user_input(self.t('output_dir_choice'))
                            if create_choice == '1':
                                try:
                                    os.makedirs(custom_dir)
                                    print(self.t('output_dir_created', path=custom_dir))
                                    return custom_dir
                                except:
                                    print(self.t('output_dir_invalid'))
                                    break
                            elif create_choice == '2':
                                break
                            else:
                                print(self.t('invalid_choice', range='1 或 2'))
            else:
                print(self.t('invalid_choice', range='1 或 2'))

    def estimate_oto_params(self, wav_path):
        filename = os.path.basename(wav_path)
        duration = self.get_wav_duration(wav_path)
        silence = self.detect_silence(wav_path)

        if self.is_breath_file(filename):
            return {'offset': silence, 'consonant': 0, 'cutoff': duration, 'preutterance': 0, 'overlap': 0, 'is_breath': True}

        breath_zone = self.detect_breath_zone(wav_path, silence) if self.smart_prewhite else 0

        effective_duration = duration - silence - breath_zone

        if self.is_vowel_only(filename):
            params = {
                'offset': silence + breath_zone,
                'consonant': min(15, effective_duration // 6),
                'cutoff': effective_duration,
                'preutterance': min(10, effective_duration // 8),
                'overlap': min(10, effective_duration // 10),
                'is_breath': False
            }
        else:
            if effective_duration < 200:
                params = {
                    'offset': silence + breath_zone,
                    'consonant': max(20, int(effective_duration * 0.15)),
                    'cutoff': max(50, int(effective_duration * 0.5)),
                    'preutterance': max(30, int(effective_duration * 0.2)),
                    'overlap': max(20, int(effective_duration * 0.1)),
                    'is_breath': False
                }
            elif effective_duration < 500:
                params = {
                    'offset': silence + breath_zone,
                    'consonant': max(50, int(effective_duration * 0.2)),
                    'cutoff': max(100, int(effective_duration * 0.4)),
                    'preutterance': max(60, int(effective_duration * 0.25)),
                    'overlap': max(30, int(effective_duration * 0.12)),
                    'is_breath': False
                }
            else:
                params = {
                    'offset': silence + breath_zone,
                    'consonant': max(80, int(effective_duration * 0.15)),
                    'cutoff': max(150, int(effective_duration * 0.35)),
                    'preutterance': max(80, int(effective_duration * 0.2)),
                    'overlap': max(40, int(effective_duration * 0.1)),
                    'is_breath': False
                }

            params['consonant'] = min(params['consonant'], effective_duration // 2)
            params['cutoff'] = min(params['cutoff'], effective_duration)
            params['preutterance'] = min(params['preutterance'], effective_duration // 2)
            params['overlap'] = min(params['overlap'], effective_duration // 4)

        if self.vowel_protection and not self.is_vowel_only(filename):
            min_vowel_space = 150
            if params['cutoff'] < min_vowel_space:
                params['cutoff'] = min(params['cutoff'] + 50, effective_duration)
            if params['cutoff'] > effective_duration - 20:
                params['cutoff'] = effective_duration - 20

        if self.offset_adjust != 0:
            params['offset'] = max(0, params['offset'] + self.offset_adjust)

        return params

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

        if not self.fast_mode:
            print("\n" + self.t('scanning', directory=directory))
            print(self.t('scan_files', count=str(len(all_files))))
            print("-" * 60)
        else:
            print("\n⚡ 快速扫描: " + directory)

        for idx, filepath in enumerate(all_files, 1):
            filename = os.path.basename(filepath)
            if not self.fast_mode:
                progress_msg = self.t('scan_progress', current=str(idx), total=str(len(all_files)))
                print(progress_msg + " " * 50, end='\r')

            if not self.is_audio_file(filepath):
                self.skipped_files.append(filepath)
                continue

            if self.is_wav_file(filepath):
                wav_files.append(filepath)
                continue

            wav_path = self.convert_to_wav(filepath)
            if wav_path and os.path.exists(wav_path):
                wav_files.append(wav_path)
                if wav_path != filepath and not self.fast_mode:
                    print(self.t('converted_generated', filename=os.path.basename(wav_path)))
            else:
                if not self.fast_mode:
                    print(self.t('convert_skip', filename=filename))
                self.skipped_files.append(filepath)

        if not self.fast_mode:
            print("\n" + self.t('scan_complete', count=str(len(wav_files))))
            if self.converted_files:
                print(self.t('converted_count', count=str(len(self.converted_files))))
            if self.skipped_files:
                print(self.t('skipped_count', count=str(len(self.skipped_files))))
        else:
            print("✅ 快速扫描完成: " + str(len(wav_files)) + " 个 wav 文件")

        if random.random() < 0.05 and not self.fast_mode:
            print("\n" + self.t('egg_scan'))

        return wav_files

    def run_health_check(self):
        if not self.health_check:
            return True
        print("\n" + "=" * 60)
        print(self.t('health_check_title'))
        print("=" * 60)

        if self.language == 'japanese':
            standard = self.standard_japanese
        elif self.language == 'chinese':
            standard = self.standard_chinese
        elif self.language == 'korean':
            standard = self.standard_korean
        else:
            standard = self.standard_english

        existing = set()
        for note in self.notes:
            filename = os.path.splitext(note['filename'])[0]
            for phoneme in standard:
                if phoneme in filename:
                    existing.add(phoneme)

        missing = [p for p in standard if p not in existing]
        if missing:
            print("\n这都能录少，你是按照50音表录的吗？")
            print("别磨叽，把你剩下那点音录完。")
            print("\n你现在还差这些音：")

            for i, p in enumerate(missing):
                if self.language == 'japanese':
                    romaji = self.kana_to_romaji.get(p, p)
                    print("   " + str(i+1) + ". " + p + "（" + romaji + "）")
                elif self.language == 'korean':
                    romaji = self.hangul_to_roman.get(p, p)
                    print("   " + str(i+1) + ". " + p + "（" + romaji + "）")
                else:
                    print("   " + str(i+1) + ". " + p)

            print("-" * 60)

            while True:
                choice = self.get_user_input(self.t('health_check_continue'))
                if choice == '1':
                    print(self.t('health_check_continue_yes'))
                    return True
                elif choice == '2':
                    print(self.t('health_check_continue_no'))
                    return False
                else:
                    print(self.t('invalid_choice', range='1 或 2'))
        else:
            print(self.t('health_check_complete'))
            return True

    def generate_frq_files(self):
        if not self.generate_frq:
            return
        print("\n📈 正在生成 frq 文件...")
        success = 0
        total = len(self.notes)
        for note in self.notes:
            wav_path = os.path.join(self.wav_dir, note['filename'])
            if os.path.exists(wav_path):
                result = self.generate_frq(wav_path)
                if result:
                    success += 1
        if success > 0:
            print("✅ 已生成 " + str(success) + " 个 frq 文件")

    def generate_oto(self):
        if not self.notes:
            print(self.err.get('no_data'))
            return False
        try:
            with open(self.output_path, 'w', encoding=self.encoding) as f:
                f.write('[#VERSION]\n')
                f.write('VERSION=100\n\n')
                for note in self.notes:
                    line = note['filename'] + "=" + note['alias'] + "," + str(note['offset']) + "," + str(note['consonant']) + "," + str(note['cutoff']) + "," + str(note['preutterance']) + "," + str(note['overlap']) + "\n"
                    f.write(line)
            print("\n" + self.t('generate_success', path=os.path.abspath(self.output_path)))
            print(self.t('generate_count', count=str(len(self.notes))))
            print(self.t('generate_encoding', encoding=self.encoding))
            return True
        except UnicodeEncodeError:
            print(self.err.get('encoding_error'))
            self.encoding = 'utf-8'
            return self.generate_oto()
        except Exception:
            print(self.err.get('unknown'))
            return False

    def generate_character_file(self):
        if not self.generate_character:
            return
        character_path = os.path.join(self.wav_dir, 'character.txt')
        try:
            with open(character_path, 'w', encoding='utf-8') as f:
                if self.character_name:
                    f.write('name=' + self.character_name + '\n')
                if self.character_version:
                    f.write('version=' + self.character_version + '\n')
                if self.character_web:
                    f.write('web=' + self.character_web + '\n')
                if self.character_image:
                    f.write('image=' + self.character_image + '\n')
            print("\n" + self.t('character_generated', path=os.path.abspath(character_path)))
        except Exception:
            print(self.err.get('unknown'))

    def preview_oto(self):
        if not self.notes:
            print(self.err.get('no_data'))
            return False
        print("\n" + "=" * 60)
        print(self.t('preview_title'))
        print("=" * 60)
        print(self.t('preview_count', count=str(len(self.notes))))
        print("-" * 60)
        show_count = min(20, len(self.notes))
        for i in range(show_count):
            note = self.notes[i]
            print(self.t('preview_show',
                index=str(i+1),
                filename=note['filename'][:30],
                alias=note['alias'][:20],
                offset=str(note['offset']),
                consonant=str(note['consonant']),
                cutoff=str(note['cutoff']),
                preutterance=str(note['preutterance']),
                overlap=str(note['overlap'])
            ))
        if len(self.notes) > 20:
            print(self.t('preview_more', count=str(len(self.notes) - 20)))
        print("-" * 60)
        while True:
            choice = self.get_user_input(self.t('preview_confirm')).upper()
            if choice == 'Y':
                return True
            elif choice == 'N':
                print(self.err.get('user_cancel'))
                return False
            else:
                print(self.t('invalid_choice', range='Y 或 N'))

    def interactive_path_selection(self):
        print("\n" + "=" * 60)
        print(self.t('no_audio_found'))
        print("=" * 60)
        print(self.t('no_audio_menu'))
        print("=" * 60)
        print(self.t('no_audio_hint'))
        print("=" * 60)
        while True:
            print(self.t('drag_hint'))
            user_input = self.get_user_input(self.t('no_audio_input'))
            user_input = user_input.strip('"\'')
            if user_input.lower() in ['exit', 'quit', 'q', '3']:
                print(self.t('exit'))
                sys.exit(0)
            if self.is_valid_directory(user_input):
                audio_files = self.scan_audio_files(user_input)
                if audio_files:
                    return user_input, audio_files
                else:
                    print(self.err.get('no_audio'))
                    continue
            else:
                print(self.err.get('dir_not_found', path=user_input))
                continue

    def is_valid_directory(self, path):
        try:
            return os.path.isdir(path) and os.path.exists(path)
        except:
            return False

    def handle_oto_exists(self):
        oto_path = os.path.join(self.wav_dir, 'oto.ini')
        if os.path.exists(oto_path):
            print("\n" + "=" * 60)
            print(self.t('oto_exists_title'))
            print("=" * 60)
            print(self.t('oto_exists_hint'))
            print("=" * 60)
            print(self.t('oto_exists_rewrite'))
            print(self.t('oto_exists_keep'))
            print("=" * 60)
            while True:
                choice = self.get_user_input(self.t('oto_exists_choice'))
                if choice == '1':
                    try:
                        os.remove(oto_path)
                        print(self.t('oto_exists_deleted'))
                        return True
                    except:
                        print(self.err.get('rename_fail', filename='oto.ini'))
                        return True
                elif choice == '2':
                    print(self.t('oto_exists_keep_confirm'))
                    return False
                else:
                    print(self.t('invalid_choice', range='1 或 2'))
        return True

    def process_files(self, wav_files):
        if not wav_files:
            print(self.err.get('no_audio'))
            return False

        if not self.handle_oto_exists():
            if self.generate_character:
                print(self.t('oto_exists_char_ask'))
                while True:
                    choice = self.get_user_input(self.t('oto_exists_choice'))
                    if choice == '1':
                        self.generate_character_file()
                        print(self.t('oto_exists_char_generated'))
                        return False
                    elif choice == '2':
                        print(self.t('oto_exists_char_skip'))
                        return False
                    else:
                        print(self.t('invalid_choice', range='1 或 2'))
            return False

        print("\n" + self.t('processing_start', count=str(len(wav_files))))
        print("-" * 60)

        story_triggered = False
        story_index = 0
        story_char_index = 0
        story_start_time = 0

        if len(wav_files) >= 1000 and self.stories_loaded:
            story_triggered = True
            print("\n" + self.t('story_trigger'))
            print("=" * 60)
            print(self.t('story_trigger_yes'))
            print(self.t('story_trigger_no'))
            print("=" * 60)
            while True:
                choice = self.get_user_input(self.t('story_trigger_choice'))
                if choice == '1':
                    print(self.t('story_generating'))
                    story_index = random.randint(0, len(self.stories) - 1)
                    story_text = self.stories[story_index]
                    self.current_story = story_text
                    story_char_index = 0
                    total_files = len(wav_files)
                    estimated_time = total_files * 0.3 + sum(1 for f in wav_files if not f.endswith('.wav')) * 1.5
                    char_delay = max(0.05, estimated_time / len(story_text) * 1.3)
                    print("📊 预计需要 " + str(int(estimated_time // 60)) + " 分 " + str(int(estimated_time % 60)) + " 秒")
                    print("📖 ", end='', flush=True)
                    story_start_time = time.time()
                    break
                elif choice == '2':
                    story_triggered = False
                    break
                else:
                    print(self.t('invalid_choice', range='1 或 2'))

        for idx, wav_path in enumerate(wav_files, 1):
            if self.normalize_volume:
                wav_path = self.normalize_audio_volume(wav_path)

            filename = os.path.basename(wav_path)
            if not self.fast_mode:
                print("\n" + self.t('processing_file', idx=str(idx), total=str(len(wav_files)), filename=filename))
            else:
                if idx % 10 == 0:
                    print("⚡ 处理进度: " + str(idx) + "/" + str(len(wav_files)))

            if story_triggered and story_char_index < len(self.stories[story_index]):
                if random.random() < 0.02:
                    print("\n" + self.t('egg_progress'))

            if self.detect_abnormal_chars(filename):
                self.abnormal_files.append(filename)
                if self.clean_mode == 'ask':
                    if not self.fast_mode:
                        print(self.t('abnormal_detected', filename=filename))
                    while True:
                        choice = self.get_user_input(self.t('abnormal_choice')).upper()
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
                                    if not self.fast_mode:
                                        print(self.t('abnormal_renamed', old=filename, new=new_name))
                                    filename = new_name
                                    wav_path = new_path
                                except Exception:
                                    if not self.fast_mode:
                                        print(self.err.get('rename_fail', filename=filename))
                                    continue
                            else:
                                if not self.fast_mode:
                                    print(self.err.get('abnormal_empty'))
                                continue
                            break
                        elif choice == 'N':
                            if not self.fast_mode:
                                print(self.t('abnormal_skip', filename=filename))
                            break
                        else:
                            if not self.fast_mode:
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
                            if not self.fast_mode:
                                print(self.t('abnormal_auto_clean', old=filename, new=new_name))
                            filename = new_name
                            wav_path = new_path
                        except Exception:
                            if not self.fast_mode:
                                print(self.err.get('rename_fail', filename=filename))
                    elif not new_filename:
                        if not self.fast_mode:
                            print(self.t('abnormal_auto_empty', filename=filename))
                        continue
                else:
                    if not self.fast_mode:
                        print(self.t('abnormal_skip_all', filename=filename))
                    continue

            waveform = self.analyze_waveform(wav_path)
            if waveform and self.detect_nonhuman_waveform(wav_path):
                print("\n" + self.t('nonhuman_detect'))
                print("=" * 60)
                print(self.t('nonhuman_choice_1'))
                print(self.t('nonhuman_choice_2'))
                print(self.t('nonhuman_choice_3'))
                print("=" * 60)
                while True:
                    choice = self.get_user_input(self.t('nonhuman_choice_prompt'))
                    if choice == '1':
                        break
                    elif choice == '2':
                        self.language = 'special'
                        self.silence_threshold = 0.1
                        print(self.t('special_threshold_warn'))
                        print(self.t('special_threshold_apply'))
                        break
                    elif choice == '3':
                        print(self.t('wave_fix_skip'))
                        break
                    else:
                        print(self.t('invalid_choice', range='1/2/3'))

            params = self.estimate_oto_params(wav_path)
            is_breath = params.get('is_breath', False)
            alias = self.apply_alias(filename, is_breath)

            if is_breath and not self.fast_mode:
                print(self.t('breath_detected', filename=filename, alias=alias))

            self.notes.append({
                'filename': filename,
                'alias': alias,
                'offset': params['offset'],
                'consonant': params['consonant'],
                'cutoff': params['cutoff'],
                'preutterance': params['preutterance'],
                'overlap': params['overlap']
            })

            if not self.fast_mode:
                duration = self.get_wav_duration(wav_path)
                silence = self.detect_silence(wav_path)
                print(self.t('processed', filename=filename, alias=alias, duration=str(duration), silence=str(silence), offset=str(params['offset'])))

            if story_triggered and story_char_index < len(self.stories[story_index]):
                story_text = self.stories[story_index]
                remaining = len(story_text) - story_char_index
                chunk_size = min(50, remaining)
                chunk = story_text[story_char_index:story_char_index + chunk_size]
                print(chunk, end='', flush=True)
                story_char_index += chunk_size
                if story_char_index < len(story_text):
                    time.sleep(0.06)

        if story_triggered and story_char_index < len(self.stories[story_index]):
            print("\n" + self.t('story_export_hint'))
            user_input = self.get_user_input(self.t('story_export_prompt'))
            if user_input == '6':
                story_path = os.path.join(self.wav_dir, 'story.txt')
                try:
                    with open(story_path, 'w', encoding='utf-8') as f:
                        f.write(self.current_story)
                    print(self.t('story_exported', path=story_path))
                except:
                    pass

        if not self.fast_mode:
            print("")
        return True

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
            new_name = base_name + "_" + str(counter) + extension
            new_path = os.path.join(directory, new_name)
        return new_name, new_path

    def export_config(self):
        config = {
            'ismakeoto': 'yes',
            'version': VERSION,
            'language': self.language,
            'encoding': self.encoding,
            'clean_mode': self.clean_mode,
            'temp_mode': self.temp_mode,
            'force_reconvert': self.force_reconvert,
            'recursive_scan': self.recursive_scan,
            'silence_threshold': self.silence_threshold,
            'offset_adjust': self.offset_adjust,
            'breath_alias_template': self.breath_alias_template,
            'alias_mode': self.alias_mode,
            'alias_prefix': self.alias_prefix,
            'alias_suffix': self.alias_suffix,
            'fix_romaji': self.fix_romaji,
            'smart_prewhite': self.smart_prewhite,
            'vowel_protection': self.vowel_protection,
            'generate_frq': self.generate_frq,
            'normalize_volume': self.normalize_volume,
            'health_check': self.health_check
        }
        config_path = os.path.join(self.wav_dir, '.makeotoini_config.moic')
        self.save_moic(config_path, config)
        print(self.t('end_menu_config_exported', path=config_path))
        print(self.t('end_menu_config_export_success'))

    def export_log(self):
        log_path = os.path.join(self.wav_dir, 'makeotoini_' + time.strftime('%Y%m%d_%H%M%S') + '.log')
        try:
            with open(log_path, 'w', encoding='utf-8') as f:
                f.write("==================================================\n")
                f.write("makeotoini v" + VERSION + " Run Log\n")
                f.write("Time: " + time.strftime('%Y-%m-%d %H:%M:%S') + "\n")
                f.write("System: " + platform.system() + "\n")
                f.write("==================================================\n\n")
                f.write("[Configuration]\n")
                f.write("Language: " + self.language + "\n")
                f.write("Encoding: " + self.encoding + "\n")
                f.write("Alias Mode: " + self.alias_mode + "\n")
                f.write("Romaji Fix: " + ("Enabled" if self.fix_romaji else "Disabled") + "\n")
                f.write("Smart Pre-white: " + ("Enabled" if self.smart_prewhite else "Disabled") + "\n")
                f.write("Vowel Protection: " + ("Enabled" if self.vowel_protection else "Disabled") + "\n")
                f.write("FRQ: " + ("Generated" if self.generate_frq else "Skipped") + "\n")
                f.write("Health Check: " + ("Enabled" if self.health_check else "Disabled") + "\n\n")
                f.write("[Scan Results]\n")
                f.write("Total WAV Files: " + str(len(self.notes)) + "\n")
                f.write("Converted Files: " + str(len(self.converted_files)) + "\n")
                f.write("Skipped Files: " + str(len(self.skipped_files)) + "\n\n")
                f.write("[Generation Results]\n")
                f.write("oto.ini: Generated\n")
                if self.generate_character:
                    f.write("character.txt: Generated\n")
                if self.generate_frq:
                    f.write("FRQ Files: Generated\n")
                elapsed = int(time.time() - START_TIME)
                f.write("\n[Time]\n")
                f.write("Total Time: " + str(elapsed) + " seconds\n")
                f.write("==================================================\n")
            print(self.t('log_export_success', path=log_path))
        except:
            print("❌ 日志导出失败")

    def cleanup_temp_files(self):
        if self.cleanup_done:
            return
        if self.temp_mode and self.temp_wav_files:
            print("\n" + self.t('cleanup_temp'))
            for wav_path in self.temp_wav_files:
                try:
                    if os.path.exists(wav_path):
                        os.remove(wav_path)
                        print(self.t('cleanup_deleted', filename=os.path.basename(wav_path)))
                except Exception as e:
                    print(self.t('cleanup_fail', filename=os.path.basename(wav_path), error=str(e)))
        self.cleanup_done = True

    def show_end_menu(self):
        while True:
            print("\n" + "=" * 60)
            print(self.t('end_menu_title'))
            print("=" * 60)
            print(self.t('end_menu_1'))
            print(self.t('end_menu_2'))
            print(self.t('end_menu_3'))
            print(self.t('end_menu_4'))
            print(self.t('end_menu_5'))
            print("=" * 60)

            choice = self.get_user_input(self.t('end_menu_choice'))
            if choice == '1':
                if self.open_url('https://www.openutau.com'):
                    print(self.t('end_menu_open_success', name='OpenUTAU'))
                input(self.t('end_menu_press_enter'))
            elif choice == '2':
                if self.open_url('http://utau2008.xrea.jp'):
                    print(self.t('end_menu_open_success', name='UTAU'))
                input(self.t('end_menu_press_enter'))
            elif choice == '3':
                if self.open_url('https://github.com/tyy485/makeotoini'):
                    print("✅ 已打开项目主页")
                input(self.t('end_menu_press_enter'))
            elif choice == '4':
                self.export_config()
                input(self.t('end_menu_press_enter'))
            elif choice == '5':
                print("\n" + "=" * 60)
                print(self.t('log_export_title'))
                print("=" * 60)
                print(self.t('log_export_hint'))
                print("=" * 60)
                print(self.t('log_export_yes'))
                print(self.t('log_export_no'))
                print("=" * 60)
                while True:
                    log_choice = self.get_user_input(self.t('log_export_choice'))
                    if log_choice == '1':
                        self.export_log()
                        print("\n" + self.t('log_export_press'))
                        input()
                        print(self.t('exit_goodbye'))
                        sys.exit(0)
                    elif log_choice == '2':
                        print(self.t('exit_goodbye'))
                        sys.exit(0)
                    else:
                        print(self.t('invalid_choice', range='1 或 2'))
            else:
                print(self.t('invalid_choice', range='1、2、3、4 或 5'))

    def run(self):
        try:
            if sys.version_info[0] < 3:
                print("=" * 60)
                print("❌ 您所用的 Python 2 已经过时")
                print("💡 请安装 Python 3 来使用此工具")
                print("=" * 60)
                sys.exit(1)

            progress = self.load_progress()
            if progress:
                print("\n" + "=" * 60)
                print("📂 检测到上次未完成的任务")
                print("  是否继续？")
                print("=" * 60)
                print("  1. 继续上次任务")
                print("  2. 重新开始")
                print("  3. 删除进度文件")
                print("=" * 60)
                while True:
                    choice = self.get_user_input("请选择 1/2/3: ")
                    if choice == '1':
                        self.apply_progress(progress)
                        break
                    elif choice == '2':
                        self.clear_progress()
                        break
                    elif choice == '3':
                        self.clear_progress()
                        print("✅ 进度文件已删除")
                        print("👋 程序退出")
                        sys.exit(0)
                    else:
                        print("❌ 请输入 1/2/3")

            self.select_ui_language()

            print("=" * 60)
            print(self.t('title', version=VERSION))
            print("=" * 60)

            print(self.t('loading'))
            print(self.t('loading_done'))
            print(self.t('loading_mood'))

            print(self.t('detecting'))
            self.detect_platform()

            self.check_termux_wake_lock()

            self.select_story_source()

            config_loaded = self.load_config()

            if not config_loaded and not progress:
                self.select_language()
                self.select_encoding()
                self.select_clean_mode()
                self.select_temp_mode()
                self.select_reconvert_mode()
                self.select_scan_mode()
                self.select_silence_threshold()
                self.select_offset_adjust()
                self.select_breath_alias()
                self.select_alias_mode()
                self.select_romaji_fix()
                self.select_smart_prewhite()
                self.select_vowel_protection()
                self.select_frq()
                self.select_normalize_volume()
                self.select_health_check()

            self.select_character_generation()

            self.check_ffmpeg()
            self.check_ffprobe()

            if self.ffmpeg_available:
                print(self.t('ffmpeg_ready'))
            else:
                print(self.t('ffmpeg_hint'))

            if self.wav_dir is None:
                self.wav_dir = os.getcwd()

            print("\n" + self.t('default_dir', path=os.path.abspath(self.wav_dir)))

            audio_files = self.scan_audio_files(self.wav_dir)

            if not audio_files:
                self.wav_dir, audio_files = self.interactive_path_selection()
            else:
                print("\n" + self.t('dir_current', count=str(len(audio_files))))
                print(self.t('dir_hint'))

                user_input = self.get_user_input(self.t('dir_input'))
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
                            print(self.err.get('no_audio'))
                    else:
                        print(self.err.get('dir_not_found', path=user_input))

            output_dir = self.select_output_directory()
            self.output_path = os.path.join(output_dir, 'oto.ini')
            self.wav_dir = output_dir

            print("\n" + self.t('dir_processing', path=os.path.abspath(self.wav_dir)))
            print("=" * 60)

            if not self.process_files(audio_files):
                return False

            if not self.run_health_check():
                return False

            if not self.preview_oto():
                return False

            if self.abnormal_files:
                print(self.t('abnormal_summary', count=str(len(self.abnormal_files))))
                print(self.t('abnormal_summary_list'))
                for f in self.abnormal_files:
                    print("   - " + f)

            if self.converted_files:
                print(self.t('converted_summary', count=str(len(self.converted_files))))
                for f in self.converted_files:
                    print("   - " + os.path.basename(f))

            if self.skipped_files:
                print(self.t('skipped_summary', count=str(len(self.skipped_files))))

            self.generate_oto()

            self.generate_frq_files()

            self.generate_character_file()

            self.cleanup_temp_files()

            elapsed = int(time.time() - START_TIME)
            print(self.t('time_elapsed', seconds=str(elapsed)))

            print("\n" + "=" * 60)
            print(self.t('complete'))
            print(self.t('complete_path', path=os.path.abspath(self.output_path)))
            if self.generate_character:
                print("📋 character.txt 位置: " + os.path.join(self.wav_dir, 'character.txt'))
            if self.generate_frq:
                print("📈 frq 文件已生成")
            print(self.t('complete_hint'))
            print("=" * 60)

            self.show_end_menu()

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
        print("\n❌ 程序出错: " + str(e))
        import traceback
        traceback.print_exc()
        input("按回车键退出...")
        sys.exit(1)
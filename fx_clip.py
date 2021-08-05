from moviepy.editor import *
import time
import math
import random
import sys
from moviepy.video.io.ffmpeg_tools import *
#from moviepy.video.fx.all import fadein
from moviepy.video.fx.all import *

#l = TextClip.list('font')
#print(l)
#sys.exit(1)

#def scroll(get_frame, t):
#    """
#    This function returns a 'region' of the current frame.
#    The position of this region depends on the time.
#    """
#    frame = get_frame(t)
#    frame_region = frame[int(t):int(t)+360,:]
#    return frame_region

class LinkMap:
    is_begin = False
    is_end = False
    def __init__(self, entry):
        self.entry = entry

    def add(self, entry):
        self.next_entry = entry

    def set_begin(self):
        self.is_begin = True

    def set_end(self):
        self.is_end = True

audio_file = "./audio/fengyun.mp3"
tag_file = "./banner/banner_00%d.png"
arrows_file = "./arrows.gif"

random.seed(int(time.time()))

#meta_video_path = "./meta_mater"
#meta_video_files = os.listdir(meta_video_path)

meta_video_path = "./yuansucai"
ctgy_dirs = os.listdir(meta_video_path)

meta_video_mix_count = 5

font = "宋体-简-粗体"

fiction_texts = [
    "女儿打来求救电话\n凌浩的声音冰冷刺骨\n判官道：完了\n你们惹他干嘛？这天要塌了",
    "血影战队最高统帅\n西境之王\n一架军用战机直冲云霄\n如一道闪电般划破长空直射东洲方位"
]

for j in range(100):
    random_int = random.randint(1, 6)
    new_tag_file = tag_file % random_int
    meta_video_files = []
    for i in range(meta_video_mix_count):
        tmp_id = random.randint(0, len(ctgy_dirs) - 1)
        #print(tmp_id, ctgy_dirs)
        ctgy_dir = ctgy_dirs[tmp_id]
        mater_files = os.listdir(meta_video_path + "/" + ctgy_dir)
        if len(mater_files) == 0:
            continue
        tmp_mater_id = random.randint(0, len(mater_files)-1)
        mater_file = mater_files[tmp_mater_id]
        meta_video_files.append("{}/{}/{}".format(meta_video_path, ctgy_dir, mater_file))
    #add 尾帧
    end_frame_files = os.listdir("./other/end_frame")
    end_frame_file = random.choice(end_frame_files)
    meta_video_files.append("./other/end_frame/" + end_frame_file)

    #meta_video_cout = len(meta_video_files)
    #meta_linkmap = LinkMap(meta_video_files[0])
    #first_linkmap = meta_linkmap
    #meta_linkmap.set_begin()
    #for i in range(1, meta_video_cout):
    #    lkmap = LinkMap(meta_video_files[i])
    #    meta_linkmap.add(lkmap)
    #    meta_linkmap = lkmap
    #meta_linkmap.set_end()
    #meta_linkmap.add(first_linkmap)
    #
    #range_meta_linkmap = meta_linkmap
    #print(range_meta_linkmap.entry)
    #for i in range(100):
    #    n = range_meta_linkmap.next_entry
    #    print(n.entry, "begin:", n.is_begin, "end: ", n.is_end)
    #    range_meta_linkmap = n
    #sys.exit(1)
    #print(meta_video_files)
    #continue


    clips = []
    for meta_video_file in meta_video_files:
        clip_serial = VideoFileClip("{}".format(meta_video_file))
        clips.append(clip_serial)
    #clip2 = VideoFileClip("myvideo2.mp4").subclip(50,60)
    # concat
    clip = concatenate_videoclips(clips)
    #final_clip.add_mask().write_videofile("clip_{}.mp4".format(str("test")))
    w, h = clip.size
    clip_duration = clip.duration
    if clip_duration <= 0:
        continue
    text_duration = int(float(clip_duration - 5) / len(fiction_texts))

    audio_clip = AudioFileClip("./audio/fengyun.mp3")
    r = random.randint(0, 2)
    if r == 0:
        audio_clip = audio_clip.subclip(5, 5+clip.duration)
    #elif r == 1:
    #    audio_clip = audio_clip.subclip(5, 5+clip.duration)
    #    #audio_clip = audio_clip.subclip(35, 35+clip.duration)
    elif r == 1:
        audio_clip = AudioFileClip("./audio/hu.mp3")
        audio_clip = audio_clip.subclip(10, 10+clip.duration)
    elif r == 2:
        audio_file = "./audio/varien_future.mp3"
        audio_clip = AudioFileClip(audio_file)
        audio_clip = audio_clip.subclip(0, clip.duration)

    n = 0
    text_clips = []
    for fiction_text in fiction_texts:
        text_clip = TextClip(fiction_text, fontsize=70, font=font, color='yellow', kerning=5)
        text_clip = text_clip.set_position(("center", 120)).set_duration(text_duration).set_start(n).crossfadein(0.1)
        n += text_duration
        text_clips.append(text_clip)

    #text_clip2 = TextClip("""“你这个丧门星！你故意把汐月的未婚夫气走是不是！给我滚！死出去！”许""",fontsize=60, font= "宋体-简-粗体", color='yellow')
    #text_clip2 = text_clip1.set_position(lambda t: ("center", 50+t)).set_duration(2)

    #tag_clip = ImageClip(new_tag_file)
    tag_clip = TextClip("热门小说", fontsize=50, font=font, color="white", kerning=5)
    tag_clip = tag_clip.set_position(("right", "top"))#.resize((tag_clip.size[0]/2, tag_clip.size[1]/2))

    arrows_text_clip = TextClip("点击下方链接\n阅读全文", fontsize=80, font=font, color = "white", kerning=10).set_position(("center", 1400))
    #arrows_clip = ImageClip(arrows_file).resize((w/8, h/8)).set_position(("center", 1600)).fl_time(lambda t: 1+sin(t))
    arrows_clip = VideoFileClip("./jiantou.mp4").set_duration(clip_duration).resize((w/8, h/8)).set_position(("center", 1600))#.fl_time(lambda t: 1+sin(t))


    clip1 =CompositeVideoClip([ clip, tag_clip, arrows_clip, arrows_text_clip] + text_clips)
    clip1.set_duration(clip.duration).set_audio(audio_clip).write_videofile("video_%d.mp4" % j,  codec="libx264", audio_codec="aac", threads=5)
    clip1.close()

    #clip = VideoFileClip("clip_0.mp4")#.fx(vfx.speedx, 2)#.fx(vfx.colorx, 0.9)
    #audio_clip.write_audiofile("./audio_a.mp3")
    #clip2 = clip.set_audio(audio_clip)
    #clip2.write_videofile("audio_b.mp4")

    #clip1 = clip.set_audio(audio_clip)
    #clip1 = clip.fl_time(lambda t : 3*t).set_duration(10)
    #clip1 = clip.fl_time(lambda t : 3 + math.sin(t)).set_duration(30)
    #clip1 = clip.fl(scroll)
    #clip1.write_videofile("video.mp4")
    #ffmpeg_merge_video_audio("./video.mp4", audio_file, "output.mp4")

    #clip.save_frame("frame.jpeg", t=1)
    #clip.show()
    #clip.preview(fps=25)

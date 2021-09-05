from .models import ResolutionVideos, UploadVideo
import moviepy.editor as mp

from moviepy.video.io.ffmpeg_reader import FFMPEG_VideoReader
import base64
import io

# 🍔 GETTING VIDEO RESOLUTION USING MOVIEPY ------
def get_resolution(video_path):
    video = mp.VideoFileClip(video_path)
    height = video.h
    print("resolution", height)
    return height

# 🍔 CONVERT VIDEO RESOLUTION USING MOVIEPY ----------
def convert_video_resolution(video_path, height, file_name, video_id, token):
    clip = mp.VideoFileClip(video_path)
    clip_resized = clip.resize(height=height) # make the height 360px ( According to moviePy documenation The width is then computed so that the width/height ratio is conserved.)

    new_video_path = "%s.mp4" %file_name
    clip_resized.write_videofile("%s.mp4" %file_name)

# video_query = UploadVideo.objects.get(id=78)
# video_path = 'FreeFootage.mp4'
# height = get_resolution(video_path)
# convert_video_resolution(video_path, 480, "%s_480p" %video_path.split('.')[0], video_query, video_query.token)

# import speedtest
# wifi  = speedtest.Speedtest()
# d = download_mbs = round(wifi.download() / (10**6), 2)
# u = upload_mbs = round(wifi.upload() / (10**6), 2)

# print("Wifi Download Speed is ", d)
# print("Wifi Upload Speed is ", u)



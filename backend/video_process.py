from __future__ import print_function

from scenedetect.video_manager import VideoManager
from scenedetect.scene_manager import SceneManager
from scenedetect.stats_manager import StatsManager
from scenedetect.detectors import ContentDetector
from scenedetect.video_splitter import split_video_ffmpeg

import cv2
import os

# output_path: should be a directory
def video_to_frames(video_path, output_path):
    filename = os.path.basename(video_path)
    video_name, video_ext, media_root = filename.split('.')[0], filename.split('.')[1], video_path.replace(os.path.basename(video_path), '')

    os.system('ffmpeg -y -i "{}" "{}"'.format(video_path, output_path + video_name + '_"%05d".png'))


def frames_to_video(frames_path, output_path):
    #os.system('ffmpeg -y -i {} -codec:v h264 {}'.format()))
    pass

def video_split(video_path):
	#定义re_scene_list 为视频切分场景的列表结果
    re_scene_list = []
    cap = cv2.VideoCapture(video_path)
    filename = os.path.basename(video_path)
    video_name, video_ext, media_root = filename.split('.')[0], filename.split('.')[1], video_path.replace(os.path.basename(video_path), '')

	#创建一个video_manager指向视频文件
    video_manager = VideoManager([video_path])
    stats_manager = StatsManager()
    scene_manager = SceneManager(stats_manager)
    #＃添加ContentDetector算法（构造函数采用阈值等检测器选项）。
    scene_manager.add_detector(ContentDetector())
    base_timecode = video_manager.get_base_timecode()

    try:
        frames_num = cap.get(7)
        # 设置缩减系数以提高处理速度。
        video_manager.set_downscale_factor()

        # 启动 video_manager.
        video_manager.start()

        # 在video_manager上执行场景检测。
        scene_manager.detect_scenes(frame_source=video_manager)

        # 获取检测到的场景列表。
        scene_list = scene_manager.get_scene_list(base_timecode)
        #与FrameTimecodes一样，如果是，则可以对scene_list中的每个场景进行排序
        #场景列表变为未排序。

        print('List of scenes obtained:')
        print(scene_list)
        #如果scene_list不为空，整理结果列表，否则，视频为单场景
        if scene_list:
            for index, scene in enumerate(scene_list):
                split_video_ffmpeg(video_path, [scene], f"{media_root}{video_name}_{index + 1}.{video_ext}", "", show_output=False)
        else:
            print('"{}" has only 1 scene'.format(video_path))
        #输出切分场景的列表结果
    finally:
        video_manager.release()
    return scene_list

# xxx.mp4 - xxx_1.mp4 + xxx_2.mp4 + xxx_3.mp4 - xxx_1_2X.mp4 + xxx_2_2X.mp4 + xxx_3_2X.mp4 - xxx_concat.mp4 - xxx.mp4
# xxx.mp4 - xxx_2X.mp4 - xxx.mp4
def video_fix(video_path):
    scene_list = video_split(video_path)
    filename = os.path.basename(video_path)
    video_name, video_ext, media_root = filename.split('.')[0], filename.split('.')[1], video_path.replace(os.path.basename(video_path), '')
    '''
    if scene_list:
        fp = open('temp.txt', 'a')
        for i in range(len(scene_list)):
            scene_path = media_root + video_name + f'_{i+1}.' + video_ext
            new_scene_path = media_root + video_name + f'_{i+1}_2X.' + video_ext
            os.system(f'cd frame_interpolation && python inference_video.py --exp=1 --video="{scene_path}"')
            os.remove(scene_path)
            fp.write(f'file "{new_scene_path}"\n')
        
        # combine
        os.system('ffmpeg -f concat -i temp.txt -c copy {}'.format(media_root + video_name + '_concat.' + video_ext)) # TODO
        os.remove('temp.txt')
        os.system('ffmpeg -y -loglevel quiet -i "{}" -codec:v h264 "{}"'.format(media_root + video_name + '_concat.' + video_ext, video_path))
        
        
    else:
        os.system(f'cd frame_interpolation && python inference_video.py --exp=1 --video="{video_path}"')
        os.system('ffmpeg -y -loglevel quiet -i "{}" -codec:v h264 "{}"'.format(media_root + video_name + '_2X.' + video_ext, video_path))
    '''


    return video_path


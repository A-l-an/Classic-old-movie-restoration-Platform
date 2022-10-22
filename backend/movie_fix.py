from lzma import FORMAT_RAW
from urllib import response
from django.http import HttpResponse, Http404, FileResponse
from django.conf.urls.static import static
from backend import settings
from backend.video_process import video_scene_detect, video_to_frames, frames_to_video

import os
import ffmpeg

MEDIA_ROOT = os.path.join(settings.BASE_DIR, 'uploadsave/')

def add_escape(value):
    reserved_chars = r'''?&|!{}[]()^~*:\\"'+- '''
    replace = ['\\' + l for l in reserved_chars]
    trans = str.maketrans(dict(zip(reserved_chars, replace)))
    return value.translate(trans)

def video_fix(video_path):
    # scene_list = video_scene_detect(video_path)
    filename = os.path.basename(video_path)
    # video_name, video_ext, media_root = filename.split('.')[0], filename.split('.')[1], video_path.replace(os.path.basename(video_path), '')

    # get fps
    probe = ffmpeg.probe(video_path)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    fps = int(video_stream['r_frame_rate'].split('/')[0])/int(video_stream['r_frame_rate'].split('/')[1])

    # resolution enhancement
    frames_path = MEDIA_ROOT + 'frames'
    video_to_frames(video_path, frames_path)
    os.remove(video_path)
    output_frames_path = MEDIA_ROOT + 'res_output'
    os.system('cd resolution_enhancement && python inference.py --path="{}" --outpath="{}"'.format(frames_path, output_frames_path))
    os.system('rm "{}"/*'.format(frames_path))
    video_path = os.path.join(settings.BASE_DIR, 'colorization/video/source/{}'.format(add_escape(filename)))
    frames_to_video(output_frames_path, video_path, fps)
    os.system('rm "{}"/*'.format(output_frames_path))

    
    # frame interpolation
    os.system('cd frame_interpolation && python inference_video.py --exp=1 --video=' + video_path)
    video_path = video_path.replace(os.path.basename(video_path), '') + filename.split('.')[0] + '_2X.' + filename.split('.')[1]
    print(video_path)

    # colorization
    os.system('cd colorization && python test_video.py --video={}'.format(add_escape(os.path.basename(video_path))))
    video_path = os.path.join(settings.BASE_DIR, 'colorization/video/result/{}'.format(add_escape(os.path.basename(video_path))))


    codec_video = video_path.split('.')[0] + '_codec.' + video_path.split('.')[1]
    os.system('ffmpeg -y -loglevel quiet -i "{}" -codec:v h264 "{}"'.format(video_path, codec_video))
    os.remove(video_path)

    return codec_video


# url
def save_fix(request):
    file_obj = request.FILES['f1']
    print(file_obj)
    if (not os.path.exists(MEDIA_ROOT)):
        os.mkdir(MEDIA_ROOT)

    video = '%s%s' % (MEDIA_ROOT, file_obj.name)
    print(video)
    with open(video, 'wb') as f:
        for files in file_obj.chunks():
            f.write(files)

    # fix
    codec_video = video_fix(video)

    try:
        file_response = FileResponse(open(codec_video, 'rb'))
        file_response['content_type'] = "application/octet-stream"
        file_response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(video)
        return file_response
    except Exception:
        raise Http404
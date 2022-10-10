from urllib import response
from django.http import HttpResponse, Http404, FileResponse
from django.conf.urls.static import static
from backend import settings
from backend.video_process import video_split

import os

MEDIA_ROOT = os.path.join(settings.BASE_DIR, 'uploadsave/')

def add_escape(value):
    reserved_chars = r'''?&|!{}[]()^~*:\\"'+- '''
    replace = ['\\' + l for l in reserved_chars]
    trans = str.maketrans(dict(zip(reserved_chars, replace)))
    return value.translate(trans)


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
    
    # split

    # fix
    os.system('cd frame_interpolation && python inference_video.py --exp=1 --video=' + MEDIA_ROOT + add_escape(os.path.basename(video)))

    # api
    filename = os.path.basename(video)
    os.remove(video)
    video = MEDIA_ROOT + filename.split('.')[0] + '_2X.' + filename.split('.')[1]
    print(video)
    codec_video = video.split('.')[0] + '_codec.' + video.split('.')[1]

    try:
        os.system('ffmpeg -y -loglevel quiet -i "{}" -codec:v h264 "{}"'.format(video, codec_video))
        os.remove(video)
        file_response = FileResponse(open(codec_video, 'rb'))
        file_response['content_type'] = "application/octet-stream"
        file_response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(video)
        return file_response
    except Exception:
        raise Http404
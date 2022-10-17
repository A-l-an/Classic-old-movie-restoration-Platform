from deoldify import device
from deoldify.device_id import DeviceId
#choices:  CPU, GPU0...GPU7
device.set(device=DeviceId.GPU0)

from deoldify.visualize import *
plt.style.use('dark_background')
import warnings
warnings.filterwarnings("ignore", category=UserWarning, message=".*?Your .*? set is empty.*?")

colorizer = get_video_colorizer()

#NOTE:  Max is 44 with 11GB video cards.  21 is a good default
render_factor=21
#NOTE:  Make source_url None to just read from file at ./video/source/[file_name] directly without modification
#NOTE:  if the video is local, set source_url = None
# source_url='https://twitter.com/silentmoviegifs/status/1116751583386034176'
# source_url = 'https://www.youtube.com/watch?v=oFqr77T6pBc'
# file_name = 'The Godfather (Black and White Sample)'
source_url = None
file_name = 'IMG_9567'
file_name_ext = file_name + '.MOV'
result_path = None

if source_url is not None:
    result_path = colorizer.colorize_from_url(source_url, file_name_ext, render_factor=render_factor)
else:
    result_path = colorizer.colorize_from_file_name(file_name_ext, render_factor=render_factor)

# print(result_path)
show_video_in_notebook(result_path)
for i in range(10,45,2):
    colorizer.vis.plot_transformed_image('video/bwframes/' + file_name + '/00001.jpg', render_factor=i, display_render_factor=True, figsize=(8,8))

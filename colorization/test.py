#NOTE:  This must be the first call in order to work properly!
from deoldify import device
from deoldify.device_id import DeviceId
#choices:  CPU, GPU0...GPU7
device.set(device=DeviceId.GPU0)

from deoldify.visualize import *
plt.style.use('dark_background')
import warnings
warnings.filterwarnings("ignore", category=UserWarning, message=".*?Your .*? set is empty.*?")

#Adjust render_factor (int) if image doesn't look quite right (max 64 on 11GB GPU).  The default here works for most photos.  
#It literally just is a number multiplied by 16 to get the square render resolution.  
#Note that this doesn't affect the resolution of the final output- the output is the same resolution as the input.
#Example:  render_factor=21 => color is rendered at 16x21 = 336x336 px.  
render_factor=35

vis = get_image_colorizer(render_factor=render_factor, artistic=True)
vis.plot_transformed_image("test_images/IMG_8226.JPG", render_factor=38, compare=True)
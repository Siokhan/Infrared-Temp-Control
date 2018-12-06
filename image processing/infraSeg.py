import matplotlib.pyplot as plt
import numpy as np

from skimage import data
from skimage import io
from skimage import filters
from skimage import morphology
from skimage.viewer import ImageViewer
from skimage.feature import canny
from skimage.filters import sobel
from skimage.morphology import watershed
from skimage.color import label2rgb
from skimage.color import rgb2hed
from skimage.exposure import rescale_intensity
from skimage.color.adapt_rgb import adapt_rgb, each_channel, hsv_value
from scipy import ndimage as ndi
from matplotlib.colors import LinearSegmentedColormap

atlantis = io.imread('./images/atlantis.png')
histo = np.histogram(atlantis, bins=np.arange(0,256))

fig, atlantisHisto = plt.subplots(figsize=(4, 3))
atlantisHisto.plot(histo[1][:-1], histo[0], lw=2)
atlantisHisto.set_title('atlantis histogram')

#simple thresholding based on histogram

fig, atlantisThresh = plt.subplots(figsize=(4, 3), sharey=True)

atlantisThresh.imshow(atlantis)
atlantisThresh.set_title('image')
atlantisThresh.axis('off')

#applying grayscale filter to rgb picture

@adapt_rgb(each_channel)
def sobel_each(atlantis):
    return filters.sobel(atlantis)


@adapt_rgb(hsv_value)
def sobel_hsv(atlantis):
    return filters.sobel(atlantis)

fig, (ax_each, ax_hsv) = plt.subplots(ncols=2, figsize=(11, 5))

ax_each.imshow(rescale_intensity(1 - sobel_each(atlantis)))
ax_each.set_xticks([]), ax_each.set_yticks([])
ax_each.set_title("Sobel filter computed\n on individual RGB channels")

ax_hsv.imshow(rescale_intensity(1 - sobel_hsv(atlantis)))
ax_hsv.set_xticks([]), ax_hsv.set_yticks([])
ax_hsv.set_title("Sobel filter computed\n on (V)alue converted image (HSV)")

#attempting to detect human body using color deconvolution

cmap_custom = LinearSegmentedColormap.from_list('mycmap', ['white', 'green'])
atlantis_hed = rgb2hed(atlantis)

fig, custom_color = plt.subplots(figsize=(4, 3))
custom_color.imshow(atlantis_hed[:, :, 0], cmap=cmap_custom)
custom_color.set_title('color separation')
custom_color.axis('off')

plt.show()

import matplotlib.pyplot as plt
import numpy as np

from skimage import data
from skimage import io
from skimage import filters
from skimage import morphology
from skimage import img_as_uint
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

atlantis = io.imread('./images/atlantis.jpg')
histo = np.histogram(atlantis, bins=np.arange(0,256))

fig, atlantisHisto = plt.subplots(figsize=(4, 3))
atlantisHisto.plot(histo[1][:-1], histo[0], lw=2)
atlantisHisto.set_title('atlantis histogram')

#simple thresholding based on histogram

fig, atlantisThresh = plt.subplots(figsize=(4, 3), sharey=True)

atlantisThresh.imshow(atlantis)
atlantisThresh.set_title('image')
atlantisThresh.axis('off')

#attempting to detect human body using color deconvolution

cmap_custom = LinearSegmentedColormap.from_list('mycmap', ['white', 'green'])
atlantis_hed = rgb2hed(atlantis)

finalSeg = atlantis_hed[:, :, 0]

fig, custom_color = plt.subplots(figsize=(4, 3))
custom_color.imshow(finalSeg, cmap=cmap_custom)
custom_color.set_title('color separation')
custom_color.axis('off')


#f = open("humanSeperation.png", "w+")
#io.imsave("./images/humanSeperation.png", finalSeg)
#f.close()

plt.show()

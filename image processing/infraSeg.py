import matplotlib.pyplot as plt
import numpy as np

from skimage import data
from skimage import io
from skimage.viewer import ImageViewer
from skimage.feature import canny
from skimage.filters import sobel
from skimage.morphology import watershed
from skimage.color import label2rgb
from skimage import morphology
from scipy import ndimage as ndi

atlantis = io.imread('./images/atlantis.jpg')
histo = np.histogram(atlantis, bins=np.arange(0,256))

fig, atlantisHisto = plt.subplots(figsize=(4, 3))
atlantisHisto.plot(histo[1][:-1], histo[0], lw=2)
atlantisHisto.set_title('atlantis histogram')
plt.show()

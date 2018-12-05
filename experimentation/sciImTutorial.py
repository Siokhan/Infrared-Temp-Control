import matplotlib.pyplot as plt
import numpy as np

from skimage import data
from skimage.viewer import ImageViewer
from skimage.feature import canny
from skimage import morphology
from scipy import ndimage as ndi

coins = data.coins()
histo = np.histogram(coins, bins=np.arange(0,256))

fig, axes = plt.subplots(1, 2, figsize=(8, 3))
axes[0].imshow(coins, cmap=plt.cm.gray, interpolation='nearest')
axes[0].axis('off')
axes[1].plot(histo[1][:-1], histo[0], lw=2)
axes[1].set_title('histogram of gray values')

#thresholding

fig, axes2 = plt.subplots(1, 2, figsize=(8, 3))
axes2[0].imshow(coins > 100, cmap=plt.cm.gray, interpolation='nearest')
axes2[0].set_title('coins > 100')

axes2[1].imshow(coins > 150, cmap=plt.cm.gray, interpolation='nearest')
axes2[1].set_title('coins > 150')
for a in axes2:
    a.axis('off')

#edge-based segmentation (canny edge detector)

edges = canny(coins)

fig, axes3 = plt.subplots(1, 2, figsize=(8, 3))
axes3[0].imshow(edges, cmap=plt.cm.gray, interpolation='nearest')
axes3[0].set_title('Canny detector')

#filling up the coins to make them white circles

fill_coins = ndi.binary_fill_holes(edges)

axes3[1].imshow(fill_coins, cmap=plt.cm.gray, interpolation='nearest')
axes3[1].set_title('filling the holes')

for a in axes3:
    a.axis('off')

#remove small objects

coins_cleaned = morphology.remove_small_objects(fill_coins, 21)
fig, no_small = plt.subplots(figsize=(4, 3))
no_small.imshow(coins_cleaned, cmap=plt.cm.gray, interpolation='nearest')
no_small.set_title('removing small objects')
no_small.axis('off')

plt.show()

#viewer = ImageViewer(coins)
#viewer.show()

import matplotlib.pyplot as plt
import numpy as np

from skimage import data
from skimage.viewer import ImageViewer
from skimage.feature import canny
from skimage.filters import sobel
from skimage.morphology import watershed
from skimage.color import label2rgb
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

#region based segmentation

elevation_map = sobel(coins)

fig, axes4 = plt.subplots(figsize=(4, 3))
axes4.imshow(elevation_map, cmap=plt.cm.gray, interpolation='nearest')
axes4.set_title('elevation map')
axes4.axis('off')

#using region segmentation to define markers of background and object

markers = np.zeros_like(coins)
markers[coins < 30] = 1
markers[coins > 150] = 2

fig, axes5 = plt.subplots(figsize=(4, 3))
axes5.imshow(markers, cmap=plt.cm.nipy_spectral, interpolation='nearest')
axes5.set_title('markers')
axes5.axis('off')

#use watershed transform to fill regions of elevation map, starting with defined markers

segmentation = morphology.watershed(elevation_map, markers)

fig, axes6 = plt.subplots(figsize=(4, 3))
axes6.imshow(segmentation, cmap=plt.cm.gray, interpolation='nearest')
axes6.set_title('segmentation')
axes6.axis('off')

#individually labeled coins, as well as filling small holes

segmentation = ndi.binary_fill_holes(segmentation - 1)
labeled_coins, _ = ndi.label(segmentation)
image_label_overlay = label2rgb(labeled_coins, image=coins)

fig, axes7 = plt.subplots(1, 2, figsize=(8, 3), sharey=True)
axes7[0].imshow(coins, cmap=plt.cm.gray, interpolation='nearest')
axes7[0].contour(segmentation, [0.5], linewidths=1.2, colors='y')
axes7[1].imshow(image_label_overlay, interpolation='nearest')
for a in axes7:
    a.axis('off')

plt.tight_layout()

plt.show()



#viewer = ImageViewer(coins)
#viewer.show()

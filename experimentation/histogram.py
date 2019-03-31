import matplotlib.pyplot as plt

from skimage import data
from skimage import exposure
from skimage import io

reference = data.coffee()
image = io.imread('atlantis.png')


fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(8, 3),
                                    sharex=True, sharey=True)
for aa in (ax1, ax2, ax3):
    aa.set_axis_off()

ax1.imshow(image)
ax1.set_title('Source')

fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(5, 8))


for c, c_color in enumerate(('red', 'green', 'blue')):
    img_hist, bins = exposure.histogram(image[..., c])
    axes[c].plot(bins, img_hist / img_hist.max())
    img_cdf, bins = exposure.cumulative_distribution(image[..., c])
    axes[c].plot(bins, img_cdf)
    axes[c].set_ylabel(c_color)

axes[0].set_title('Source')

plt.tight_layout()
plt.show()
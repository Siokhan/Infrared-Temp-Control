import matplotlib.pyplot as plt

from skimage import io
from skimage import exposure
from skimage.color import rgb2hed
from skimage.color import hed2rgb
from matplotlib.colors import LinearSegmentedColormap

#Seperating human from the rest of the image using IHC colour deconvolution
#This function accomplishes what is described above on specified image
def segment_histo(image_path, colour1, colour2):
    image = io.imread(image_path)
    image_hed = rgb2hed(image)

    cmap_custom = LinearSegmentedColormap.from_list('mycmap', [colour1, colour2])
    final_seg = image_hed[:, :, 0]

    fig, human_seperation = plt.subplots(figsize=(4, 3))
    human_seperation.imshow(final_seg, cmap=cmap_custom)
    human_seperation.set_title('colour deconvolution')
    human_seperation.axis('off')

    #return histogram of segmented image split between RGB channels

    final_seg_rgb = hed2rgb(final_seg)

    fig, rgb_histo = plt.subplots(nrows=3, ncols=1, figsize=(5, 8)) 

    for c, c_color in enumerate(('red', 'green', 'blue')):
        img_hist, bins = exposure.histogram(final_seg_rgb[..., c])
        rgb_histo[c].plot(bins, img_hist / img_hist.max())
        img_cdf, bins = exposure.cumulative_distribution(final_seg_rgb[..., c])
        rgb_histo[c].plot(bins, img_cdf)
        rgb_histo[c].set_ylabel(c_color) 

    rgb_histo[0].set_title('Histogram of RGB channels')

    #attempt at saving the image onto machine, not crucial
    #massive precision loss look into conservation
    io.imsave('./images/' + image_path[9:17] + '_seg.jpg', final_seg_rgb)
    
    print(final_seg_rgb.min(), final_seg_rgb.max())  
    return human_seperation, final_seg, rgb_histo

def infra_histogram(image):
   fig, rgb_histo = plt.subplots(nrows=3, ncols=1, figsize=(5, 8)) 

   for c, c_color in enumerate(('red', 'green', 'blue')):
    img_hist, bins = exposure.histogram(image[..., c])
    rgb_histo[c].plot(bins, img_hist / img_hist.max())
    img_cdf, bins = exposure.cumulative_distribution(image[..., c])
    rgb_histo[c].plot(bins, img_cdf)
    rgb_histo[c].set_ylabel(c_color)

    return rgb_histo

image_seg = segment_histo('./images/atlantis.jpg', 'white', 'green')

plt.show()


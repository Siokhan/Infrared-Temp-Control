import matplotlib.pyplot as plt

from skimage import io
from skimage import exposure
from skimage.color import rgb2hed
from skimage.color import hed2rgb
from matplotlib.colors import LinearSegmentedColormap

##   functions used to analyse and break down thermal image   ##
#Histogram function
def infra_histogram(image):
   fig, rgb_histo = plt.subplots(nrows=3, ncols=1, figsize=(5, 8)) 

   for c, c_color in enumerate(('red', 'green', 'blue')):
    img_hist, bins = exposure.histogram(image[..., c])
    rgb_histo[c].plot(bins, img_hist / img_hist.max())
    img_cdf, bins = exposure.cumulative_distribution(image[..., c])
    rgb_histo[c].plot(bins, img_cdf)
    rgb_histo[c].set_ylabel(c_color)

    return rgb_histo

#FLC input function, returns value between 0 and 10 based on "heating level felt"
#takes mean of rgb numpy array of an image as input
def flc_input(mean):
    #old_min derived by lowest cold image mean detected from gathered data(study)
    #old_max derived by highest hot image mean detected from gathered data(study)
    old_max = 141
    old_min = 129
    #if mean falls outside of the min and max bounds, mean is set to old_min if below
    #old_min, mean is set to old_max if higher than old_max
    detected_mean = mean
    if detected_mean < old_min:
        detected_mean = old_min
    elif detected_mean > old_max:
        detected_mean = old_max
    else:
        detected_mean = mean
    
    new_max = 10
    new_min = 0
    old_range = (old_max - old_min)
    new_range = (new_max - new_min)
    #Heat level derived based on detected mean, returns value between 0 and 10
    heat_level = (((detected_mean - old_min) * new_range) / old_range) + new_min
    return heat_level

#Seperating human from the rest of the image using IHC colour deconvolution
#This function accomplishes what is described above on specified image (main function)
def segment_histo(image_path, colour1, colour2):
    image = io.imread(image_path)
    image_hed = rgb2hed(image)

    cmap_custom = LinearSegmentedColormap.from_list('mycmap', [colour1, colour2])
    final_seg = image_hed[:, :, 0]

    fig, image_original = plt.subplots(figsize=(4, 3))
    image_original.imshow(image)
    image_original.set_title('Original Image')
    image_original.axis('off')

    fig, human_seperation = plt.subplots(figsize=(4, 3))
    human_seperation.imshow(final_seg, cmap=cmap_custom)
    human_seperation.set_title('colour deconvolution')
    human_seperation.axis('off')

    #return histogram of segmented image split between RGB channels

    final_seg_rgb = hed2rgb(final_seg)

    fig, rgb_histo = plt.subplots(nrows=3, ncols=1, figsize=(5, 8)) 

    #plotting the histogram and cummulative histogram across each colour channel
    for c, c_color in enumerate(('red', 'green', 'blue')):
        img_hist, bins = exposure.histogram(image[..., c])
        rgb_histo[c].plot(bins, img_hist / img_hist.max())
        img_cdf, bins = exposure.cumulative_distribution(image[..., c])
        rgb_histo[c].plot(bins, img_cdf)
        rgb_histo[c].set_ylabel(c_color) 

    rgb_histo[0].set_title('Histogram of RGB channels (original image)')

    #attempt at saving the image onto machine, not crucial
    #massive precision loss look into conservation
    io.imsave('./images/' + image_path[9:17] + '_seg.jpg', final_seg_rgb)
    
    #derive heat level based on thermaml image, this will be the FLC input
    controller_input = flc_input(image.mean())

    print(image.min(), image.max())  
    print(image.mean())
    print(controller_input)
    return human_seperation, final_seg, rgb_histo

#excuting main function with detected image
image_seg = segment_histo('./images/hot/emptyrainbow.jpg', 'white', 'green')

#show relevant figures onto the screen
plt.show()
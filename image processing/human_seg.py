import matplotlib.pyplot as plt

from skimage import io
from skimage import img_as_float
from skimage import img_as_ubyte
from skimage import img_as_uint
from skimage import img_as_int
from skimage.color import rgb2hed
from matplotlib.colors import LinearSegmentedColormap

#Seperating human from the rest of the image using IHC colour deconvolution
#This function accomplishes what is described above on specified image
def color_seperation(image_path, colour1, colour2):
    image = io.imread(image_path)
    image_hed = rgb2hed(image)

    cmap_custom = LinearSegmentedColormap.from_list('mycmap', [colour1, colour2])
    final_seg = image_hed[:, :, 0]

    fig, human_seperation = plt.subplots(figsize=(4, 3))
    human_seperation.imshow(final_seg, cmap=cmap_custom)
    human_seperation.set_title('colour deconvolution')
    human_seperation.axis('off')

    #attempt at saving the image onto machine, not crucial
    #having issues, come back to this at the end
    #io.imsave('./images/' + image_path[9:17] + '_seg.jpg', final_seg)

    return human_seperation
    return final_seg

atlantis_seg = color_seperation('./images/atlantis.jpg', 'white', 'green')

plt.show()


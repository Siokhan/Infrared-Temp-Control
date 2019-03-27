import matplotlib.pyplot as plt

from skimage import io
from skimage.color import rgb2hed
from matplotlib.colors import LinearSegmentedColormap

#Seperating human from the rest of the image using IHC colour deconvolution

def color_seperation(image_path, colour1, colour2):
    image = io.imread(image_path)
    image_hed = rgb2hed(image)

    cmap_custom = LinearSegmentedColormap.from_list('mycmap', [colour1, colour2])
    final_seg = image_hed[:, :, 0]

    fig, human_seperation = plt.subplots(figsize=(4, 3))
    human_seperation.imshow(final_seg, cmap=cmap_custom)
    human_seperation.set_title('colour deconvolution')
    human_seperation.axis('off')

    return human_seperation

color_seperation('./images/atlantis.jpg', 'white', 'green')

plt.show()


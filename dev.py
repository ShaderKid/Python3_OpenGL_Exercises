import numpy as np
from PIL import Image

array = np.uint8(np.random.rand(1000,1000)*128+128)
img = Image.fromarray(array)
img.show()

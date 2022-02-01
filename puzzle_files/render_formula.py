from matplotlib.mathtext import MathTextParser
from matplotlib.image import imsave
from PIL import Image, ImageDraw
import numpy as np


class RendMath:

    def __init__(self, formula):
        parser = MathTextParser('bitmap')
        data, someint = parser.parse(formula, dpi=1000)
        some_array = np.asarray(data)
        inverted_data = np.invert(some_array)
        self.image = Image.fromarray(np.asarray(inverted_data))

    def get_image(self):
        return self.image


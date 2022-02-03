from matplotlib.mathtext import MathTextParser
from PIL import Image, ImageDraw, ImageFont
from urllib.request import urlopen
import numpy as np

import puzzle_files.constants as con


class RendMath:

    def __init__(self, formula):
        parser = MathTextParser('bitmap')
        data, someint = parser.parse(formula, dpi=1000)
        some_array = np.asarray(data)
        inverted_data = np.invert(some_array)
        self.image = Image.fromarray(np.asarray(inverted_data))

    def get_image(self):
        return self.image


class RendText:
    font_name = con.FONT_URL
    fontsize = con.TEXT_SIZE

    colour_text = con.TEXT_COLOUR
    colour_outline = con.LINE_COLOUR
    colour_background = con.BACK_COLOUR

    def __init__(self, text):
        self.text = text
        self.font = ImageFont.truetype(urlopen(self.font_name), size=self.fontsize)
        self.width, self.height = self.get_size(text)
        self.image = self.create_image()

    def get_size(self, text):
        test_image = Image.new('RGB', (0, 0))
        test_draw = ImageDraw.Draw(test_image)
        return test_draw.textsize(text, self.font)

    def create_image(self):
        image = Image.new('RGB', (self.width, self.height), self.colour_background)
        d = ImageDraw.Draw(image)
        d.text((0, 0), self.text, fill=self.colour_text, font=self.font)
        d.rectangle((0, 0, self.width, self.height))
        return image

    def get_image(self):
        return self.image

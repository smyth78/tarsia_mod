# main library imports
import matplotlib as plt
from matplotlib.mathtext import MathTextParser
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# local imports
import puzzle_files.constants as con


class RenderText:
    font = {'size': con.TEXT_SIZE}
    plt.rc('font', **font)

    font_name = con.FONT_URL
    fontsize = con.TEXT_SIZE

    colour_text = con.TEXT_COLOUR
    colour_outline = con.LINE_COLOUR
    colour_background = con.BACK_COLOUR

    def __init__(self, text, is_math):
        if is_math:
            data, some_int = MathTextParser('bitmap').parse(text, dpi=100)
            some_array = np.asarray(data)
            inverted_data = np.invert(some_array)
            self.image = Image.fromarray(inverted_data)
        else:
            self.text = text
            self.font = ImageFont.truetype("arial.ttf", self.fontsize)
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


class RenderJoinedTextImage:
    blank_image = Image.new('RGB', (0, 0))

    def __init__(self, normal_text, math_text):
        normal_text = RenderText(normal_text, False)
        math_text = RenderText(r"${}$".format(math_text), True) if math_text != '' else RenderText(math_text, False)
        self.images = [normal_text.get_image(), math_text.get_image()]
        self.final_joined_image = self.join_images()

    def join_images(self):
        final_image_width = max([image.width for image in self.images])
        final_image_height = sum([image.height for image in self.images])
        problem_image = Image.new('RGB', (final_image_width, final_image_height + con.COMB_IM_FUDGE), (255, 255, 255))
        text_is_max_width = True if self.images[0].width > self.images[1].width else False
        if text_is_max_width:
            offset = ((final_image_width - self.images[1].width) // 2, self.images[0].height + con.COMB_IM_FUDGE)
            problem_image.paste(self.images[0], (0, 0))
            problem_image.paste(self.images[1], offset)
        else:
            offset = ((final_image_width - self.images[0].width) // 2, 0)
            problem_image.paste(self.images[0], offset)
            problem_image.paste(self.images[1], (0, self.images[0].height + con.COMB_IM_FUDGE))

        return problem_image

    def get_joined_image(self):
        return self.final_joined_image


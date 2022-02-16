# main library imports
import matplotlib as plt
from matplotlib.mathtext import MathTextParser
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import textwrap

# local imports
import puzzle_files.constants as con


class RenderText:
    colour_text = con.TEXT_COLOUR
    colour_outline = con.LINE_COLOUR
    colour_background = con.BACK_COLOUR

    def __init__(self, text, is_math, is_treasure, text_size, side_length):
        self.side_length = side_length
        self.font = {'size': text_size}
        plt.rc('font', **self.font)
        self.fontsize = text_size
        self.is_treasure = is_treasure
        if text is not None:
            if is_math:
                try:
                    data, some_int = MathTextParser('bitmap').parse(text, dpi=100)
                    some_array = np.asarray(data)
                    inverted_data = np.invert(some_array)
                    self.image = Image.fromarray(inverted_data)
                except:
                    self.image = None
            else:
                try:
                    if text == '':
                        self.image = None
                    else:
                        self.text = text
                        self.font = ImageFont.truetype("arial.ttf", self.fontsize)
                        self.width, self.height = self.get_size(text)
                        self.image = self.create_image_of_text()
                except:
                    self.image = None
        else:
            self.image = None

    def get_size(self, text):
        test_image = Image.new('RGB', (0, 0))
        test_draw = ImageDraw.Draw(test_image)
        return test_draw.textsize(text, self.font)

    def create_image_of_text(self):
        # can resize the images depending on desired output size
        width_1char, height_1char = self.font.getsize('A')
        # subtract 100 here for the 'blank space' on the TH clue card
        width_of_line_in_chars = (con.WIDTH_TREASURE_CLUE - 100) // width_1char if self.is_treasure else \
            (self.side_length * con.TEXT_OVERLAP_FACTOR) // width_1char
        # split the text if mult lines
        lines = textwrap.wrap(self.text, width=width_of_line_in_chars)
        longest_line = max(lines, key=len)
        width_longest_line, height_line = self.font.getsize(longest_line)
        # new_image_width = int(con.WIDTH_TREASURE_CLUE) if self.is_treasure else \
        #     int(con.SIDE_LENGTH * con.TEXT_OVERLAP_FACTOR)
        image = Image.new('RGB', (width_longest_line, (len(lines) + 1) * height_1char), self.colour_background)
        d = ImageDraw.Draw(image)
        y_text = 0
        for line in lines:
            width, height = self.font.getsize(line)
            d.text((0, y_text), line, font=self.font,
                   fill=con.LINE_COLOUR)
            y_text += height
        return image

    def get_image(self):
        return self.image


class RenderJoinedTextImage:
    blank_image = Image.new('RGB', (0, 0))

    def __init__(self, normal_text, math_text, is_treasure, text_size, side_length):
        self.side_length = side_length
        self.plain_normal_text = normal_text
        self.plain_math_text = math_text
        self.normal_text = RenderText(normal_text, False, is_treasure, text_size, side_length) if normal_text is not None else None
        self.math_text = RenderText(r"${}$".format(math_text), True, is_treasure, text_size, side_length) if math_text is not None else None
        self.images = self.collect_problem_images()
        self.final_joined_image = self.join_images()

    def collect_problem_images(self):
        problem_images = []
        if self.normal_text is not None and self.plain_normal_text != '':
            if self.normal_text.get_image() is not None:
                problem_images.append(self.normal_text.get_image())
        if self.math_text is not None and self.plain_math_text != '':
            if self.math_text.get_image() is not None:
                problem_images.append(self.math_text.get_image())
        return problem_images

    def join_images(self):
        # first look at when there is math and normal text
        if len(self.images) == 2:
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
        # this is when only math OR normal textis used
        elif len(self.images) == 1:
            problem_image = self.images[0]
        else:
            # if the textbox is empty do nothing -MAYBE NEED CLIENT SIDE WARNING?
            problem_image = None

        return problem_image

    def get_joined_image(self):
        return self.final_joined_image


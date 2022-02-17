from PIL import Image
import puzzle_files.constants as con


class TreasureHunt:
    aspect_ratio = con.TH_ASPECT_RATIO
    clues_per_row = con.TH_CLUES_PER_ROW

    def __init__(self, question_images, answer_images):
        self.number_of_clues = len(question_images)
        self.clue_template = Image.open('puzzle_files/th_templates/th_clue_template.png')
        self.answer_template = self.get_answer_template()
        self.question_images = question_images
        self.answer_images = answer_images
        self.clue_templates = self.stamp_clue_template()
        self.final_image = self.make_final_image()

    def get_answer_template(self):
        if self.number_of_clues == 4:
            answer_template = Image.open('puzzle_files/th_templates/th_hunt_ans_4.png')
        elif self.number_of_clues == 9:
            answer_template = Image.open('puzzle_files/th_templates/th_hunt_ans_9.png')
        elif self.number_of_clues == 3:
            answer_template = Image.open('puzzle_files/th_templates/th_hunt_ans_3.png')
        elif self.number_of_clues == 18:
            answer_template = Image.open('puzzle_files/th_templates/th_hunt_ans_18.png')
        elif self.number_of_clues == 12:
            answer_template = Image.open('puzzle_files/th_templates/th_hunt_ans_12.png')
        elif self.number_of_clues == 24:
            answer_template = Image.open('puzzle_files/th_templates/th_hunt_ans_24.png')
        elif self.number_of_clues == 30:
            answer_template = Image.open('puzzle_files/th_templates/th_hunt_ans_30.png')
        elif self.number_of_clues == 40:
            answer_template = Image.open('puzzle_files/th_templates/th_hunt_ans_40.png')
        else:
            answer_template = None
        return answer_template

    def get_final_image(self):
        return self.final_image

    def stamp_clue_template(self):
        clue_templates = []
        for clue_num in range(self.number_of_clues):
            question = self.question_images[clue_num]
            if clue_num < self.number_of_clues - 1:
                answer = self.answer_images[clue_num + 1]
            else:
                answer = self.answer_images[0]
            current_clue = self.clue_template.copy()
            if question is not None:
                resized_question = resize_image_aspect(question, 2)
                offset = ((con.WIDTH_TREASURE_CLUE - resized_question.width) // 2, 155)
                current_clue.paste(resized_question, offset)
            if answer is not None:
                current_clue.paste(answer, (89, 24))
            clue_templates.append(current_clue)
        return clue_templates

    def make_final_image(self):
        width_clue, height_clue = self.clue_template.size
        is_make_larger_for_answer_sheet = True if self.number_of_clues % self.clues_per_row == 0 else False
        # make final image 3 clues wide
        total_width_final_image = width_clue * self.clues_per_row
        height_add_depends_on_answer_sheet = 2 if is_make_larger_for_answer_sheet else 1
        total_height_final_image = (self.number_of_clues // self.clues_per_row + height_add_depends_on_answer_sheet) * height_clue
        final_image = Image.new('RGB', (total_width_final_image, total_height_final_image), (255, 255, 255))
        for i, clue_image in enumerate(self.clue_templates):
            final_image.paste(clue_image, (i % self.clues_per_row * width_clue,
                                           i // self.clues_per_row * height_clue))
            final_i_val = i + 1
        final_image.paste(self.answer_template, (final_i_val % self.clues_per_row * width_clue,
                                                 final_i_val // self.clues_per_row * height_clue))
        return final_image


def resize_image_aspect(image, ratio):
    width, height = image.size
    image = image.resize((int(width * ratio), int(height * ratio)))
    return image






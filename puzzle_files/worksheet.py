from PIL import Image, ImageFont, ImageDraw, ImageOps

import puzzle_files.constants as con
import helper_functions as hf


class Worksheet:
    font = ImageFont.truetype("arial.ttf", 12)
    questions_per_row = 3

    def __init__(self, question_images, answer_images):
        self.total_questions = len(question_images)
        self.question_template = Image.open('puzzle_files/th_templates/ws_q_template.png')
        self.temp_w, self.temp_h = self.question_template.size
        self.questions = question_images
        self.answers = answer_images
        self.stamped_quest_templates, self.stamped_ans_templates = self.create_stamped_templates()
        self.question_sheet, self.answer_sheet = self.make_worksheet()
        # self.final_image = self.join_images()
        self.final_image = hf.combine_puz_and_soln_images(self.question_sheet, 'Questions', self.answer_sheet, 'Answers')

    def get_final_image(self):
        return self.final_image

    def join_images(self):
        w, h = self.question_sheet.size
        final_h = h * 2
        final_image = Image.new("RGB", (w, final_h))
        final_image.paste(self.question_sheet, (0, 0))
        final_image.paste(self.answer_sheet, (0, h))
        return final_image

    def make_worksheet(self):
        worksheet_w = self.questions_per_row * self.temp_w
        worksheet_h = (self.total_questions // self.questions_per_row + 1) * self.temp_h
        question_sheet = Image.new("RGB", (worksheet_w, worksheet_h), (255, 255, 255))
        ans_sheet = question_sheet.copy()
        for i, (question_image, ans_image) in enumerate(zip(self.stamped_quest_templates, self.stamped_ans_templates)):
            question_sheet.paste(question_image, (i % self.questions_per_row * self.temp_w,
                                                  i // self.questions_per_row * self.temp_h))
            ans_sheet.paste(ans_image, (i % self.questions_per_row * self.temp_w,
                                        i // self.questions_per_row * self.temp_h))
        return question_sheet, ans_sheet

    def create_stamped_templates(self):
        stamped_question_templates = []
        stamped_answer_templates = []
        question_num = 1
        for i, (question_image, answer_image) in enumerate(zip(self.questions, self.answers)):
            question = self.question_template.copy()
            d = ImageDraw.Draw(question)
            d.text((5, 5), str(question_num) + ')', fill='black', font=self.font)

            # useable space in template 150 x 130
            if question_image is not None:
                resized_question = resize_image(question_image)
                question.paste(resized_question, (20, 20))
                stamped_question_templates.append(question)

            copy_question = question.copy()
            if answer_image is not None:
                resized_answer = resize_image(answer_image)
                resized_answer = add_border_to_image(resized_answer)
                copy_question.paste(resized_answer, (20, 140))
                stamped_answer_templates.append(copy_question)

            question_num += 1

        return stamped_question_templates, stamped_answer_templates


def resize_image(image):
    # see if h or w is largest
    w, h = image.size
    if w > h:
        new_w = con.USE_TEMP_W
        aspect = int(w / h)
        new_h = int(con.USE_TEMP_H / aspect)
    else:
        new_h = con.USE_TEMP_H
        aspect = int(h / w)
        new_w = int(con.USE_TEMP_W / aspect)
    image = image.resize((new_w, new_h))
    return image

def add_border_to_image(image):
    img_with_border = ImageOps.expand(image, border=2, fill='black')
    return img_with_border



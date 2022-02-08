from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

from flask import send_file

import puzzle_files.render_input as rend
import puzzle_files.constants as con

def generate_fields(num_questions):
    form_fields = []
    for i in range(num_questions):
        question_text_label = 'Q' + str(i + 1) + ' - text'
        question_math_label = 'Q' + str(i + 1) + ' - math tex'
        answer_text_label = 'A' + str(i + 1) + ' - text'
        answer_math_label = 'A' + str(i + 1) + ' - math tex'
        question_text_name = 'qt' + str(i + 1)
        question_math_name = 'qm' + str(i + 1)
        answer_text_name = 'at' + str(i + 1)
        answer_math_name = 'am' + str(i + 1)
        new_question_text = {
                      "tag": question_text_name,
                      "name": question_text_name,
                      "type": "text",
                      "human_label": question_text_label
                    }
        new_question_math_tex = {
                      "tag": question_math_name,
                      "name": question_math_name,
                      "type": "text",
                      "human_label": question_math_label
                    }
        new_answer_text = {
          "tag": answer_text_name,
          "name": answer_text_name,
          "type": "text",
          "human_label": answer_text_label
        }
        new_answer_math_tex = {
            "tag": answer_math_name,
            "name": answer_math_name,
            "type": "text",
            "human_label": answer_math_label
        }
        form_fields.append(new_question_text)
        form_fields.append(new_question_math_tex)
        form_fields.append(new_answer_text)
        form_fields.append(new_answer_math_tex)
    return form_fields

def calculate_square_puzzle_problem_count(size):
    return int((4 * size**2 - 4 * size) * (1/2))

def calculate_triangle_puzzle_question_count(size):
    return int(4)


def parse_form_content(form, is_norm_text, is_math_text):
    question_text_images = []
    question_math_images = []
    answer_text_images = []
    answer_math_images = []
    for key in form:
        # note each append has a 'placeholder' so later function works
        if key[0:2] == 'qt':
            question_text_images.append(form[key] if is_norm_text else '')
        elif key[0:2] == 'qm':
            question_math_images.append(form[key] if is_math_text else '')
        elif key[0:2] == 'at':
            answer_text_images.append(form[key] if is_norm_text else '')
        elif key[0:2] == 'am':
            answer_math_images.append(form[key] if is_math_text else '')

    return question_text_images, question_math_images, answer_text_images, answer_math_images


def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')


def combine_puz_and_soln_images(soln_image, puzzle_image):
    comb_w, comb_h = soln_image.size
    # make height larger to accomadate both images and some text
    full_height = comb_h * 2 + con.GAP_IN_FINAL_IMAGE * 2
    combined_image = Image.new('RGB', (comb_w, full_height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(combined_image)
    font = ImageFont.truetype("puzzle_files/arial.ttf", 30)
    draw.text((50, 10), "Solution", (0, 0, 0), font=font)
    combined_image.paste(soln_image, (0, con.GAP_IN_FINAL_IMAGE))
    draw.text((50, comb_h + con.GAP_IN_FINAL_IMAGE + 10), "Puzzle", (0, 0, 0), font=font)
    combined_image.paste(puzzle_image, (0, comb_h + con.GAP_IN_FINAL_IMAGE * 2))
    return combined_image

from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

from flask import send_file

import puzzle_files.render_formula as rend
import puzzle_files.constants as con

def generate_fields(num_questions):
    form_fields = []
    for i in range(num_questions):
        question_label = 'Question ' + str(i + 1)
        answer_label = 'Answer ' + str(i + 1)
        question_name = 'q' + str(i + 1)
        answer_name = 'a' + str(i + 1)
        new_question = {
                      "tag": question_name,
                      "name": question_name,
                      "type": "text",
                      "human_label": question_label
                    }
        new_answer = {
          "tag": answer_name,
          "name": answer_name,
          "type": "text",
          "human_label": answer_label
        }
        form_fields.append(new_question)
        form_fields.append(new_answer)
    return form_fields

def calculate_square_puzzle_question_count(size):
    return int((4 * size**2 - 4 * size) * (1/2))


def parse_form(form):
    question_images = []
    answer_images = []
    for key in form:
        image_string = "$" + form[key] + "$"
        if key[0] == 'q':
            question_images.append(rend.RendMath(image_string).get_image())
        else:
            answer_images.append(rend.RendMath(image_string).get_image())

    return question_images, answer_images


def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')


def combine_images(soln_image, puzzle_image):
    comb_w, comb_h = soln_image.size
    # make height larger to accomadate both images and some text
    full_height = comb_h * 2 + con.COMB_IM_FUDGE * 2
    combined_image = Image.new('RGB', (comb_w, full_height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(combined_image)
    font = ImageFont.truetype("puzzle_files/arial.ttf", 30)
    draw.text((50, 10), "Solution", (0, 0, 0), font=font)
    combined_image.paste(soln_image, (0, con.COMB_IM_FUDGE))
    draw.text((50, comb_h + con.COMB_IM_FUDGE + 10), "Puzzle", (0, 0, 0), font=font)
    combined_image.paste(puzzle_image, (0, comb_h + con.COMB_IM_FUDGE * 2))
    return combined_image

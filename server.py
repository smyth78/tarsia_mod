from flask import Flask, render_template, redirect, request

import helper_functions as hf
from puzzle_files.square_puzzle import AbstractPuzzle, ParseImages, SquarePuzzle
from puzzle_files.treasure_hunt import TreasureHunt
from puzzle_files.worksheet import Worksheet


app = Flask(__name__,
            template_folder="templates",
            static_folder="static/",
            static_url_path="/static/")
app.secret_key = "ABC"


@app.route('/', methods=["GET"])
def main_page():
    return render_template("puzzle_size.html")


@app.route('/problems', methods=["POST"])
def enter_problems():
    form_as_dict = request.form.to_dict()
    number_of_questions = int(form_as_dict['size'])

    problem_fields = hf.generate_fields(number_of_questions)
    return render_template("puzzle_problems.html", size=number_of_questions, fields=problem_fields)


@app.route('/puzzle', methods=["POST"])
def final_puzzle():
    form_as_dict = request.form.to_dict()
    total_questions = int(form_as_dict['size'])
    text_size = int(form_as_dict['text-size'])
    is_math_text = True if 'math-text' in form_as_dict.keys() else False
    is_norm_text = True if 'normal-text' in form_as_dict.keys() else False
    questions_text, questions_math, answers_text, answers_math = hf.parse_form_content(form_as_dict, is_norm_text,
                                                                                       is_math_text)

    if form_as_dict['options'] == 'tarsia':
        is_treasure = False
        parsed_form = ParseImages(total_questions, questions_text, questions_math, answers_text, answers_math, True,
                                  is_treasure, text_size)
        parsed_problems = parsed_form.get_parsed_images()
        square_puzzle_size = hf.calculate_square_size_from_question_total(total_questions)
        puzzle = SquarePuzzle(square_puzzle_size, parsed_problems)
        soln_image = puzzle.get_solution_image()
        puzzle_image = puzzle.get_final_puzzle_image()

        combined_image = hf.combine_puz_and_soln_images(soln_image, 'Solution', puzzle_image, 'Puzzle')

        return hf.serve_pil_image(combined_image)

    elif form_as_dict['options'] == 'treasure':
        is_treasure = True
        parsed_form = ParseImages(total_questions, questions_text, questions_math, answers_text, answers_math, False,
                                  is_treasure, text_size)
        question_images, answer_images = parsed_form.get_quest_answer_images()
        t_h = TreasureHunt(question_images, answer_images)
        t_h_final_image = t_h.get_final_image()
        return hf.serve_pil_image(t_h_final_image)
    elif form_as_dict['options'] == 'worksheet':
        is_treasure = False
        parsed_form = ParseImages(total_questions, questions_text, questions_math, answers_text, answers_math, False,
                                  is_treasure, text_size)
        question_images, answer_images = parsed_form.get_quest_answer_images()
        w_s = Worksheet(question_images, answer_images)
        return hf.serve_pil_image(w_s.get_final_image())

    else:
        print('not generated yet')
        return redirect("/", code=302)

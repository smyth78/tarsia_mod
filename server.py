from flask import Flask, render_template, redirect, request

import helper_functions as hf
from puzzle_files.square_puzzle import AbstractPuzzle, ParseImages, SquarePuzzle


app = Flask(__name__,
            template_folder="templates",
            static_folder="static/",
            static_url_path="/static/")
app.secret_key = "ABC"


@app.route('/', methods=["GET"])
def enter_puzzle_size():
    size_field = [{
        "tag": 'size',
        "name": 'size',
        "type": "number",
        "human_label": 'Puzzle size'
    }]
    # renders puzzle_size with blank form for puzzle size
    return render_template("puzzle_size.html",
                           fields=size_field,
                           text_1='Enter puzzle size...',
                           text_2='Minimum size of 2 and maximum size of 5.')


@app.route('/problems', methods=["POST"])
def enter_problems():
    try:
        size = int(request.form['size'])
        # verify puzzle size is acceptable - try to do clientside....
        if size <= 0 or size >= 5:
            size_field = [{
                "tag": 'size',
                "name": 'size',
                "type": "number",
                "human_label": 'Puzzle size'
            }]
            return render_template("puzzle_size.html",
                                   fields=size_field,
                                   text_1='Enter puzzle size...',
                                   text_2='Error, try again...minimum size of 2 and maximum size of 5.')

        number_of_questions = hf.calculate_square_puzzle_problem_count(size)
        problem_fields = hf.generate_fields(number_of_questions)
        return render_template("puzzle_problems.html", size=size, fields=problem_fields, text='Enter problems...')

    except:
        return redirect("/", code=302)

@app.route('/puzzle', methods=["POST"])
def final_puzzle():
    form_as_dict = request.form.to_dict()
    if form_as_dict['options'] == 'tarsia':
        puzzle_size = int(form_as_dict['size'])
        is_math_text = True if 'math-text' in form_as_dict.keys() else False
        is_norm_text = True if 'normal-text' in form_as_dict.keys() else False
        questions_text, questions_math, answers_text, answers_math = hf.parse_form_content(form_as_dict, is_norm_text, is_math_text)
        parsed_form = ParseImages(puzzle_size, questions_text, questions_math, answers_text, answers_math)
        parsed_problems = parsed_form.get_parsed_images()
        puzzle = SquarePuzzle(parsed_form.get_size_of_puzzle(), parsed_problems)
        soln_image = puzzle.get_solution_image()
        puzzle_image = puzzle.get_final_puzzle_image()

        combined_image = hf.combine_puz_and_soln_images(soln_image, puzzle_image)

        return hf.serve_pil_image(combined_image)
    else:
        print('not generated yet')
        return redirect("/", code=302)

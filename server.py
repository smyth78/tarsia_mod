from flask import Flask, render_template, redirect, request

import helper_functions as hf
from puzzle_files.square_puzzle import Puzzle, ParseImages


app = Flask(__name__)
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

        number_of_questions = hf.calculate_square_puzzle_question_count(size)
        problem_fields = hf.generate_fields(number_of_questions)
        return render_template("puzzle_problems.html", fields=problem_fields, text='Enter problems...')

    except:
        return redirect("/", code=302)

@app.route('/puzzle', methods=["POST"])
def final_puzzle():
    try:
        questions, answers = hf.parse_form(request.form)
        parsed_form = ParseImages(questions, answers)
        parsed_problems = parsed_form.get_parsed_images()
        puzzle = Puzzle(parsed_form.get_size_of_puzzle(), parsed_problems)
        soln_image = puzzle.get_solution_image()
        puzzle_image = puzzle.get_final_puzzle_image()

        combined_image = hf.combine_images(soln_image, puzzle_image)

        return hf.serve_pil_image(combined_image)
    except:
        print('error generating puzzle')
        return redirect("/", code=302)


if __name__ == "__main__":
    app.run(port=5000, host='0.0.0.0')
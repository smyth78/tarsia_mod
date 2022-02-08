import puzzle_files.render_input as rend
import helper_functions as hf
import puzzle_files.square_puzzle as sp
import sim_form as sf

questions_text, questions_math, answers_text, answers_math = hf.parse_form(sf.form)
parsed_form = sp.ParseImages(2, questions_text, questions_math, answers_text, answers_math)
parsed_problems = parsed_form.get_parsed_images()
puzzle = sp.SquarePuzzle(parsed_form.get_size_of_puzzle(), parsed_problems)
soln_image = puzzle.get_solution_image()
puzzle_image = puzzle.get_final_puzzle_image()

soln_image.show()
puzzle_image.show()


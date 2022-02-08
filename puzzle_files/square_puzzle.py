# main library
from PIL import Image, ImageDraw
import random

# local imports
import helper_functions as hf
import puzzle_files.constants as con
from puzzle_files.render_input import RenderJoinedTextImage as rjti


class PuzzlePiece:
    def __init__(self, coord, num_sides):
        self.coord = coord
        self.num_sides = num_sides
        self.exterior_angle = int(360 / self.num_sides)
        self.side_length = con.SIDE_LENGTH
        self.image = None

    def insert_text_image(self, text_image, position):
        # need to rotate the image so the position is at top
        self.image = self.image.rotate(position * self.exterior_angle)
        self.stamp_text_image(text_image)
        # rotate image back to original position
        self.image = self.image.rotate(position * (-self.exterior_angle))

    def stamp_text_image(self, text_image):
        bg_w, bg_h = self.image.size
        text_w, text_h = text_image.size
        offset = ((bg_w - text_w) // 2, con.TEXT_IMAGE_OFFSET)
        self.image.paste(text_image, offset)

    def get_image(self):
        return self.image

    def get_coord(self):
        return self.coord


class Square(PuzzlePiece):
    def __init__(self, coord):
        self.num_sides = 4
        super().__init__(coord, self.num_sides)
        self.image = self.draw_square()

    def draw_square(self):
        vertices = [0, 0, self.side_length, self.side_length]

        image = Image.new('RGBA', (self.side_length, self.side_length),
                          (255, 255, 255, 0))
        draw = ImageDraw.Draw(image)
        draw.rectangle(vertices, fill=con.BACK_COLOUR, outline=con.LINE_COLOUR, width=con.LINE_WIDTH)
        return image


class AbstractPuzzle:
    def __init__(self, puzzle_size, text_images):
        self.text_images = text_images
        self.puzzle_size = puzzle_size
        self.solution_image = None
        self.final_puzzle_image = None
        # if is_square:
        #
        # elif is_triangle:
        #     self.puzzle_pieces = self.create_puzzle_triangles()
        #     self.coords_in_puzzle = self.create_triangle_coords_list()
        #     self.num_of_questions = hf.calculate_triangle_puzzle_question_count(puzzle_size)

    def create_puzzle_triangles(self):
        return ''

    def get_solution_image(self):
        return self.solution_image

    def get_final_puzzle_image(self):
        return self.final_puzzle_image

    def create_triangle_coords_list(self):
        return ''


class SquarePuzzle(AbstractPuzzle):
    def __init__(self, puzzle_size, text_images):
        super().__init__(puzzle_size, text_images)
        self.puzzle_pieces = self.create_puzzle_squares()
        self.coords_in_puzzle = self.create_square_coords_list()
        self.num_of_questions = hf.calculate_square_puzzle_problem_count(puzzle_size)
        self.insert_text_images_square()
        self.solution_image, self.final_puzzle_image = self.construct_puzzle_images()

    def get_square_by_coord(self, coord):
        for row in self.puzzle_pieces:
            for square in row:
                if square.get_coord() == coord:
                    return square

    def create_square_coords_list(self):
        i, j = range(0, self.puzzle_size), range(0, self.puzzle_size)
        coords_list = []
        for x in i:
            for y in j:
                coords_list.append([x, y])
        return coords_list

    def create_puzzle_squares(self):
        puzzle_squares = []
        # i is the row number from top to bottom
        for i in range(self.puzzle_size):
            row_images = []
            # j is the square number from left to right
            for j in range(self.puzzle_size):
                row_images.append(Square((i, j)))
            puzzle_squares.append(row_images)
        return puzzle_squares

    def construct_puzzle_images(self):
        puzzle_length = self.puzzle_size * con.SIDE_LENGTH
        solution_image = Image.new('RGB', (puzzle_length, puzzle_length))
        final_puzzle_image = Image.new('RGB', (puzzle_length, puzzle_length))
        random_coords_remaining = self.coords_in_puzzle
        for i, puzzle_images_row in enumerate(self.puzzle_pieces):
            for j, square in enumerate(puzzle_images_row):
                solution_image.paste(square.get_image(), (j * con.SIDE_LENGTH, i * con.SIDE_LENGTH))
                a_random_coord, random_coords_remaining = get_remaining_coord(random_coords_remaining)
                final_puzzle_image.paste(square.get_image().rotate(random.randint(0, 4) * 90), (a_random_coord[1] *
                                                                                                con.SIDE_LENGTH,
                                                                                                a_random_coord[0] *
                                                                                                con.SIDE_LENGTH))
        return solution_image, final_puzzle_image

    def insert_text_images_square(self):
        # vertical (green) lines
        question_counter = 0
        for i in range(self.puzzle_size):
            for j in range(self.puzzle_size):
                if j < self.puzzle_size - 1:
                    # square_1 is the left square of the pair so insert at 'R'
                    square_1 = self.get_square_by_coord((i, j))
                    square_1.insert_text_image(self.text_images[question_counter][0], 1)
                    # square_2 is the right square of the pair so insert at 'L'
                    square_2 = self.get_square_by_coord((i, j + 1))
                    square_2.insert_text_image(self.text_images[question_counter][1], 3)
                    question_counter += 1

                    # square_3 is the top square of the pair so insert at 'B'
                    square_3 = self.get_square_by_coord((j, i))
                    square_3.insert_text_image(self.text_images[question_counter][0], 2)
                    # square_4 is the bottom square of the pair so insert at 'T'
                    square_4 = self.get_square_by_coord((j + 1, i))
                    square_4.insert_text_image(self.text_images[question_counter][1], 0)
                    question_counter += 1


class ParseImages:
    def __init__(self, size, q_text_images, q_math_images, a_text_images, a_math_images):
        self.total = hf.calculate_square_puzzle_problem_count(size) * 2
        self.question_images, self.answer_images = join_problem_strings_as_images(q_text_images,  q_math_images,
                                                                                  a_text_images, a_math_images)
        self.parsed_images = []
        self.parse_images()

    def parse_images(self):
        for question_image, answer_image in zip(self.question_images, self.answer_images):
            paring = [question_image, answer_image]
            random.shuffle(paring)
            self.parsed_images.append(paring)
        random.shuffle(self.parsed_images)

    def get_parsed_images(self):
        return self.parsed_images

    def get_size_of_puzzle(self):
        return int((1 + (1 + self.total) ** (1/2)) / 2)


def get_remaining_coord(remaining_coords):
    random.shuffle(remaining_coords)
    chosen_coord = remaining_coords.pop()
    return chosen_coord, remaining_coords


def join_problem_strings_as_images(qt, qm, at, am):
    # # oragnise images into [[[qt1,qm1],[at1,am1]], [[qt2,qm2],[at2,am2]],...etc
    collated_strings = []
    for qtp, qmp, atp, amp in zip(qt, qm, at, am):
        collated_strings.append([[qtp, qmp], [atp, amp]])

    final_question_images = []
    final_answer_images = []

    for problem_strings in collated_strings:
        question = problem_strings[0]
        answer = problem_strings[1]
        final_question_images.append(rjti(question[0], question[1]).get_joined_image())
        final_answer_images.append(rjti(answer[0], answer[1]).get_joined_image())

    return final_question_images, final_answer_images










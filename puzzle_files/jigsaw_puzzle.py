# main library
from PIL import Image, ImageDraw, ImageFont
import random
import math

# local imports
import helper_functions as hf
import puzzle_files.constants as con
from puzzle_files.render_input import RenderJoinedTextImage as rjti
# import puzzle_files.parsed_images_practice as pr_img


class PuzzlePiece:
    def __init__(self, coord, num_sides, side_length):
        self.coord = coord
        self.num_sides = num_sides
        self.exterior_angle = int(360 / self.num_sides)
        self.side_length = side_length
        self.image = None

    def insert_text_image(self, text_image, position, is_regular):
        # need to rotate the image so the position is at top
        self.image = self.image.rotate(position * self.exterior_angle, expand=not is_regular)
        needs_offset = True if (not is_regular and position != 0) else False
        self.stamp_text_image(text_image, needs_offset, position)
        # rotate image back to original position
        self.image = self.image.rotate(position * (-self.exterior_angle))
        # now crop if irregular
        if not is_regular:
            self.image = crop_rotated_triangular_image(self.image, self.side_length)

    def stamp_text_image(self, text_image, needs_offset, position):
        fudge_offset_w, fudge_offset_h = 0, 0
        if needs_offset:
            fudge_offset_w, fudge_offset_h = triangle_fudge_offset(position, self.side_length)
        if text_image is not None:
            bg_w, bg_h = self.image.size
            # if not regular need to
            text_w, text_h = text_image.size
            offset = ((bg_w - text_w + fudge_offset_w) // 2, con.TEXT_IMAGE_OFFSET + fudge_offset_h)
            self.image.paste(text_image, offset)

    def get_image(self):
        return self.image

    def get_coord(self):
        return self.coord


class Triangle(PuzzlePiece):
    def __init__(self, coord, side_length):
        self.num_sides = 3
        super().__init__(coord, self.num_sides, side_length)
        self.image = self.draw_triangle()

    def draw_triangle(self):
        l = self.side_length
        h = int(math.sqrt(3) / 2 * l)
        # h = int(math.sqrt(2) / 2 * l)
        # h = l
        image = Image.new('RGBA', (l, h), (255, 255, 255, 0))
        draw = ImageDraw.Draw(image)
        base_vertices = [(0, h), (l, h)]
        draw.line(base_vertices, fill=con.LINE_COLOUR, width=con.LINE_WIDTH * 2)
        # diag are half line width
        diagonal_vertices = [(l, h), (int(l / 2), 0), (0, h)]
        draw.line(diagonal_vertices, fill=con.LINE_COLOUR, width=con.LINE_WIDTH)
        return image

    def rotate_image(self, angle):
        self.image = self.image.rotate(angle)

    def crop_image(self):
        cropped_image = Image.new()

    def flip_horiz_image(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)


class Square(PuzzlePiece):
    def __init__(self, coord, side_length):
        self.num_sides = 4
        super().__init__(coord, self.num_sides, side_length)
        self.image = self.draw_square()

    def draw_square(self):
        vertices = [0, 0, self.side_length, self.side_length]

        image = Image.new('RGBA', (self.side_length, self.side_length),
                          (255, 255, 255, 0))
        draw = ImageDraw.Draw(image)
        draw.rectangle(vertices, fill=con.BACK_COLOUR, outline=con.LINE_COLOUR, width=con.LINE_WIDTH)
        return image


class AbstractPuzzle:
    def __init__(self, puzzle_size, text_images, side_length):
        self.side_length = side_length
        self.text_images = text_images
        self.puzzle_size = puzzle_size
        self.puzzle_pieces = None
        self.solution_image = None
        self.final_puzzle_image = None
        self.combined_image = None

    def get_solution_image(self):
        return self.solution_image

    def get_final_puzzle_image(self):
        return self.final_puzzle_image

    def get_piece_by_coord(self, coord):
        for row in self.puzzle_pieces:
            for piece in row:
                if piece.get_coord() == coord:
                    return piece

    def combine_puz_and_soln_images(self, top_text, bottom_text):
        comb_w, comb_h = self.solution_image.size
        # make height larger to accomadate both images and some text
        full_height = comb_h * 2 + con.GAP_IN_FINAL_IMAGE * 2
        combined_image = Image.new('RGB', (comb_w, full_height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(combined_image)
        font = ImageFont.truetype("arial.ttf", 30)
        draw.text((50, 10), top_text, (0, 0, 0), font=font)
        combined_image.paste(self.solution_image, (0, con.GAP_IN_FINAL_IMAGE))
        draw.text((50, comb_h + con.GAP_IN_FINAL_IMAGE + 10), bottom_text, (0, 0, 0), font=font)
        combined_image.paste(self.final_puzzle_image, (0, comb_h + con.GAP_IN_FINAL_IMAGE * 2))
        return combined_image


class TrianglePuzzle(AbstractPuzzle):
    def __init__(self, puzzle_size, text_images, side_length):
        super().__init__(puzzle_size, text_images, side_length)
        self.is_regular = False
        # create the tri coords list simultanously
        self.puzzle_pieces, self.triangle_coords_list = self.create_puzzle_pieces()
        # is a square number of questions!
        self.num_of_questions = int(puzzle_size ** 2)
        self.insert_text_triangles()
        self.solution_image, self.final_puzzle_image = self.construct_puzzle_images()

    def get_soln_image(self):
        return self.solution_image

    def get_puzzle_image(self):
        return self.final_puzzle_image

    def construct_puzzle_images(self):
        row_height = int(math.sqrt(3) / 2 * self.side_length)
        puzzle_width = int(self.puzzle_size * self.side_length)
        puzzle_height = int(self.puzzle_size * row_height)
        solution_image = Image.new('RGBA', (puzzle_width, puzzle_height), (255, 255, 255, 0))
        puzzle_image = Image.new('RGBA', (puzzle_width, puzzle_height), (255, 255, 255, 0))
        random_coords_remaining = self.triangle_coords_list
        # get i's in opposite direction so that can draw from the base up...
        for i in range(self.puzzle_size - 1, -1, -1):
            for j in range(i * 2 + 1):
                tri_image = self.puzzle_pieces[i][j].get_image()
                # tri_image.show()
                # if j is even is posn 0 DOWN if j is odd posn ZERO UP
                if j % 2 == 0:
                    # need j //2 as the up rows are joined together!
                    solution_image.paste(tri_image, (j // 2 * self.side_length + (self.puzzle_size - i - 1) * self.side_length // 2 , i * row_height), tri_image)
                else:
                    # rotate image
                    tri_image = tri_image.rotate(180)
                    solution_image.paste(tri_image, (int(j * self.side_length / 2) + (self.puzzle_size - i - 1) * self.side_length // 2 , i * row_height), tri_image)
                # now paste the puzzle soln
                # past the chosen answer in a random posn and rotate it
                a_random_coord, random_coords_remaining = get_remaining_coord(random_coords_remaining)
                i_puzz, j_puzz = a_random_coord
                tri_puzzle_image = self.puzzle_pieces[i][j].get_image()
                tri_puzzle_image.rotate(random.randint(0, 2) * 120)
                if j_puzz % 2 == 0:
                    puzzle_image.paste(tri_puzzle_image, (j_puzz // 2 * self.side_length + (self.puzzle_size - i_puzz - 1) * self.side_length // 2, i_puzz * row_height), tri_puzzle_image)
                else:
                    # rotate image
                    tri_puzzle_image = tri_puzzle_image.rotate(180)
                    puzzle_image.paste(tri_puzzle_image, (int(j_puzz * self.side_length / 2) + (self.puzzle_size - i_puzz - 1) * self.side_length // 2, i_puzz * row_height), tri_puzzle_image)

        return solution_image, puzzle_image

    def insert_text_triangles(self):
        question_counter = 0
        # first do the horiz line of tris
        # i is the row
        # number from top to bottom
        for i in range(self.puzzle_size):
            row_images = []
            # dont include the top tri in this algo
            if i > 0:
                # j is the tri number from left  to right
                for j in range(i * 2):
                    # if j is even then the 2s join, if odd the 1s join
                    position_to_join = 2 if j % 2 == 0 else 1
                    tri_1 = self.get_piece_by_coord((i, j))
                    # rotate original 180 so position 0 is at top
                    tri_1.rotate_image(180)
                    tri_1.insert_text_image(self.text_images[question_counter][0], position_to_join, self.is_regular)
                    # now back to original position
                    tri_1.rotate_image(180)

                    tri_2 = self.get_piece_by_coord((i, j + 1))
                    # rotate original 180 so position 0 is at top
                    tri_2.rotate_image(180)
                    tri_2.insert_text_image(self.text_images[question_counter][1], position_to_join, self.is_regular)
                    # now back to original position
                    tri_2.rotate_image(180)
                    question_counter += 1

            # now start again for the posns 0, note: can choose when i == 0
            if i < self.puzzle_size - 1:
                for j in range(i * 2 + 1):
                    if j % 2 == 0:
                        # this is for debugging
                        position_to_join = 0
                        tri_1 = self.get_piece_by_coord((i, j))
                        # rotate original 180 so position 0 is at top
                        tri_1.rotate_image(180)
                        tri_1.insert_text_image(self.text_images[question_counter][0], 0,
                                                self.is_regular)
                        # now back to original position
                        tri_1.rotate_image(180)

                        tri_2 = self.get_piece_by_coord((i + 1, j + 1))
                        # rotate original 180 so position 0 is at top
                        tri_2.rotate_image(180)
                        tri_2.insert_text_image(self.text_images[question_counter][1], 0,
                                                self.is_regular)
                        # now back to original position
                        tri_2.rotate_image(180)
                        question_counter += 1

    def create_puzzle_pieces(self):
        puzzle_triangles = []
        coords_list = []
        # i is the row number from left to right
        for i in range(self.puzzle_size):
            row_images = []
            # j is the square number from bottom to top
            for j in range(i * 2 + 1):
                row_images.append(Triangle((i, j), self.side_length))
                coords_list.append((i, j))
            puzzle_triangles.append(row_images)
        return puzzle_triangles, coords_list


class SquarePuzzle(AbstractPuzzle):
    def __init__(self, puzzle_size, text_images, side_length):
        super().__init__(puzzle_size, text_images, side_length)
        self.is_regular = True
        self.puzzle_pieces = self.create_puzzle_squares()
        self.coords_in_puzzle = self.create_square_coords_list()
        self.num_of_questions = hf.calculate_square_puzzle_problem_count(puzzle_size)
        self.insert_text_images_square()
        self.solution_image, self.final_puzzle_image = self.construct_puzzle_images()

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
                row_images.append(Square((i, j), self.side_length))
            puzzle_squares.append(row_images)
        return puzzle_squares

    def construct_puzzle_images(self):
        puzzle_length = self.puzzle_size * self.side_length
        solution_image = Image.new('RGB', (puzzle_length, puzzle_length))
        final_puzzle_image = Image.new('RGB', (puzzle_length, puzzle_length))
        random_coords_remaining = self.coords_in_puzzle
        for i, puzzle_images_row in enumerate(self.puzzle_pieces):
            for j, square in enumerate(puzzle_images_row):
                solution_image.paste(square.get_image(), (j * self.side_length, i * self.side_length))
                a_random_coord, random_coords_remaining = get_remaining_coord(random_coords_remaining)
                final_puzzle_image.paste(square.get_image().rotate(random.randint(0, 4) * 90), (a_random_coord[1] *
                                                                                                self.side_length,
                                                                                                a_random_coord[0] *
                                                                                                self.side_length))
        return solution_image, final_puzzle_image

    def insert_text_images_square(self):
        # vertical (green) lines
        question_counter = 0
        for i in range(self.puzzle_size):
            for j in range(self.puzzle_size):
                # this is for posns 1 and 2
                if j < self.puzzle_size - 1:
                    # square_1 is the left square of the pair so insert at 'R'
                    square_1 = self.get_piece_by_coord((i, j))
                    square_1.insert_text_image(self.text_images[question_counter][0], 1, self.is_regular)
                    # square_2 is the right square of the pair so insert at 'L'
                    square_2 = self.get_piece_by_coord((i, j + 1))
                    square_2.insert_text_image(self.text_images[question_counter][1], 3, self.is_regular)
                    question_counter += 1

                    # square_3 is the top square of the pair so insert at 'B'
                    square_3 = self.get_piece_by_coord((j, i))
                    square_3.insert_text_image(self.text_images[question_counter][0], 2, self.is_regular)
                    # square_4 is the bottom square of the pair so insert at 'T'
                    square_4 = self.get_piece_by_coord((j + 1, i))
                    square_4.insert_text_image(self.text_images[question_counter][1], 0, self.is_regular)
                    question_counter += 1


class ParseImages:
    def __init__(self, total_questions, q_text_images, q_math_images, a_text_images, a_math_images, is_random, is_treasure,
                 text_size, side_length):
        self.side_length = side_length
        self.total = total_questions
        self.question_images, self.answer_images = join_problem_strings_as_images(q_text_images,  q_math_images,
                                                                                  a_text_images, a_math_images,
                                                                                  is_treasure, text_size, side_length)
        self.parsed_images = []
        self.parse_images(is_random)

    def parse_images(self, is_random):
        for question_image, answer_image in zip(self.question_images, self.answer_images):
            paring = [question_image, answer_image]
            random.shuffle(paring) if is_random else None
            self.parsed_images.append(paring)
        random.shuffle(self.parsed_images)

    def get_parsed_images(self):
        return self.parsed_images

    def get_quest_answer_images(self):
        return self.question_images, self.answer_images

    def get_size_of_puzzle(self):
        return int((1 + (1 + self.total) ** (1/2)) / 2)


def get_remaining_coord(remaining_coords):
    random.shuffle(remaining_coords)
    chosen_coord = remaining_coords.pop()
    return chosen_coord, remaining_coords


def join_problem_strings_as_images(qt, qm, at, am, is_treasure, text_size, side_length):
    # # oragnise images into [[[qt1,qm1],[at1,am1]], [[qt2,qm2],[at2,am2]],...etc
    collated_strings = []
    for qtp, qmp, atp, amp in zip(qt, qm, at, am):
        collated_strings.append([[qtp, qmp], [atp, amp]])

    final_question_images = []
    final_answer_images = []

    for problem_strings in collated_strings:
        question = problem_strings[0]
        answer = problem_strings[1]
        final_question_images.append(rjti(question[0], question[1], is_treasure, text_size, side_length).get_joined_image())
        final_answer_images.append(rjti(answer[0], answer[1], is_treasure, text_size, side_length).get_joined_image())

    return final_question_images, final_answer_images


def triangle_fudge_offset(position, side_length):
    width = int(1 / 4 * side_length) * (-1) ** position
    length = int(math.sqrt(3) / 4 * side_length)
    return width, length


def crop_rotated_triangular_image(full_image, side_length):
    # hard coded height argh!!!!!
    h = int(math.sqrt(3) / 2 * side_length)
    x1 = int((full_image.width - side_length) / 2)
    y1 = int((full_image.height - h) / 2)
    x2 = x1 + side_length
    y2 = y1 + h
    return full_image.crop((x1, y1, x2, y2))


# parsed_problems = pr_img.parsed_problems
# tri = Triangle((0, 0))
# tri_puzz = TrianglePuzzle(3, parsed_problems)
# final = tri_puzz.combine_puz_and_soln_images('Soln', 'Puz')
# final.show()









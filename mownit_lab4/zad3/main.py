import sys
import numpy as np
import random
import matplotlib.pyplot as plt


def parse_sudoku_board(file_path):

    with open(file_path, 'r') as file:
        sudoku_board = []
        for line in file:
            sudoku_row = []
            for x in line[:9]:
                if x=='x':
                    sudoku_row.append(0)
                else:
                    sudoku_row.append(int(x))
            sudoku_board.append(sudoku_row)

    #looking for empty spots in each square, we have to fill them with ints that are left over
    empty_spots_in_squares = []
    for x in range(0, 3):
        square_row = []
        for y in range(0, 3):
            square = []
            for r in range(3*x, 3*x + 3):
                for c in range(3*y, 3*y + 3):
                    if sudoku_board[r][c] == 0:
                        square.append((r, c))
            square_row.append(square)
        empty_spots_in_squares.append(square_row)

    return sudoku_board, empty_spots_in_squares


def fill_empty_spots(sudoku_board, empty_spots_in_squares):
    for board_row in range(0, 7, 3):
        for board_column in range(0, 7, 3):
            required_numbers = set(range(1, 10)).difference(
                {x for row in sudoku_board[board_row:board_row+3] for x in row[board_column:board_column+3]})
            available_indexes = [xy for xy in empty_spots_in_squares[board_row//3][board_column//3]]
            for number, coordinate in zip(required_numbers, np.random.permutation(available_indexes)):
                sudoku_board[coordinate[0]][coordinate[1]] = number
    return sudoku_board

#simulated annealing functions

def sim_ann(maximum_temperature, iterations, sudoku_board, empty_spots_in_squares):
    current_board = sudoku_board
    best_board = sudoku_board
    current_value = get_board_energy(current_board)
    print(current_value)
    best_value = current_value
    current_temperature = maximum_temperature
    # anneal_progress = [(0, current_value)]  #for showing the progress of anneal
    for i in range(1, iterations):
        helper = [row[:] for row in current_board] #pointers are hard, this is also much better than what i did in task2
        #i just consolidated everything there into one clear function and a simple swap of pointers on two objects
        next_board, next_value = generate_next_board(helper, current_value, empty_spots_in_squares)
        probabilty = probability_function(maximum_temperature, current_value, next_value, current_temperature)
        if current_value > next_value or random.random() <= probabilty:
            current_board = next_board
            current_value = next_value
            # anneal_progress.append((i, next_value))
            if best_value > next_value:
                best_board, best_value = next_board, next_value
                #due to this choice of energy function, we can break eariler if sudoku is solved
                if next_value == 0:
                    print("Found perfect solution")
                    break
        if i%1000 == 0:
            print("Temp = " + str(current_temperature) + " current best val " + str(best_value))
        current_temperature = cooling_function(current_temperature)
    ## uncomment everything above with anneal_progress and everything below to display progression graph
    #anneal_progress.append((iterations, best_value))
    # x, y = zip(*anneal_progress)
    # for i in range(0, len(anneal_progress) - 1):
    #     plt.plot([anneal_progress[i][0], anneal_progress[(i + 1)][0]], [anneal_progress[i][1], anneal_progress[(i + 1)][1]], linewidth=1, c='blue')
    # plt.plot(x, y, 'ro')
    # plt.show()
    return best_board, best_value


def get_board_energy(sudoku_board):
    board_value = 0
    for row in sudoku_board:
        board_value += 9 - len(set(row))
    for column in range(9):
        board_value += 9 - len({sudoku_board[x][column] for x in range(9)})
    return board_value


def generate_next_board(sudoku_board, current_value, empty_spots_in_squares):
    #pick two points to swap
    points_to_swap = []
    while len(points_to_swap) < 2:
        points_to_swap = empty_spots_in_squares[random.choice(range(3))][random.choice(range(3))]
    points_to_swap = random.sample(points_to_swap, 2)
    point_a, point_b = points_to_swap[0], points_to_swap[1]

    #find the energy value of the part we are about to swap, return it as negative for future addition
    #faster to do it like this, rather than finiding the energy state of an entire new board every iteration
    part_value = 0
    for row in (sudoku_board[point_a[0]], sudoku_board[point_b[0]]):
        part_value -= 9 - len(set(row))
    for column in (point_a[1], point_b[1]):
        part_value -= 9 - len({sudoku_board[x][column] for x in range(9)})
    #swap them
    sudoku_board[point_a[0]][point_a[1]], sudoku_board[point_b[0]][point_b[1]] = \
        sudoku_board[point_b[0]][point_b[1]], sudoku_board[point_a[0]][point_a[1]]

    #swapped find the new energy value of that part
    for row in (sudoku_board[point_a[0]], sudoku_board[point_b[0]]):
        part_value += 9 - len(set(row))
    for column in (point_a[1], point_b[1]):
        part_value += 9 - len({sudoku_board[x][column] for x in range(9)})
    # return the new state and energy difference
    return sudoku_board, current_value + part_value


def probability_function(max_temp, current_value, next_value, temperature):
    return np.exp((current_value - next_value)/temperature)

def cooling_function(t):
    return t*0.9999


def main():
    if len(sys.argv) <= 1:
        print("Please put in the name of file with the sudoku board\n")
        return
    file_path = sys.argv[1]
    sudoku_board, empty_spots_in_squares = parse_sudoku_board(file_path)
    sudoku_board = fill_empty_spots(sudoku_board, empty_spots_in_squares)
    #now the board is filled with the required numbers in each of the 9 squares
    for a in sudoku_board:
        print(a)

    #simulated annealing method code
    maximum_temperature = 30000
    iterations = 300000
    result, result_value = sim_ann(maximum_temperature, iterations, sudoku_board, empty_spots_in_squares)
    print("____")
    for a in result:
        print(a)
    print(result_value)

main()
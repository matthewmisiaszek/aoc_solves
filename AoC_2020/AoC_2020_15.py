import blitzen
import numba


@numba.njit
def game(starting_numbers, turns):
    memory = {number: turn for turn, number in enumerate(starting_numbers[:-1])}
    last = starting_numbers[-1]
    for turn in range(len(starting_numbers) - 1, turns - 1):
        memory[last], last = turn, turn - memory[last] if last in memory else 0
    return last


@blitzen.run
def main(input_string, verbose=False):
    starting_numbers = [int(i) for i in input_string.split(',')]
    p1 = game(starting_numbers, 2020)
    p2 = game(starting_numbers, 30000000)
    return p1, p2


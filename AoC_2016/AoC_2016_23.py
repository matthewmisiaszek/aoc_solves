import dancer
import math
import assembunny


def main(input_string, verbose=False):
    instructions = [line.split() for line in input_string.split('\n')]
    a = int(instructions[20][1])
    b = int(instructions[19][1])
    p1 = math.factorial(7)+a*b
    p2 = math.factorial(12)+a*b
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2016, day=23, verbose=True)

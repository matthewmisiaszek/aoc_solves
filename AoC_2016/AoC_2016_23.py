import blitzen
import math
from AoC_2016.assembunny import AsmBny


@blitzen.run
def main(input_string, verbose=False):
    aby = AsmBny(input_string, initial={'a':7})
    p1 = aby.run()
    instructions = [line.split() for line in input_string.split('\n')]
    a = int(instructions[20][1])
    b = int(instructions[19][1])
    p2 = math.factorial(12)+a*b
    return p1, p2


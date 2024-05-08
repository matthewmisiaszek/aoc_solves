import blitzen
from AoC_2016.assembunny import AsmBny


@blitzen.run
def main(input_string, verbose=False):
    assembunny = AsmBny(input_string, return_reg='out')
    i = 0
    while not assembunny.run():
        assembunny.reset()
        i += 1
        assembunny.regs['a'] = i
    p1 = i
    p2 = blitzen.holiday_greeting
    return p1, p2


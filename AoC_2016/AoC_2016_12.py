import dancer
from AoC_2016.assembunny import AsmBny


def main(input_string, verbose=False):
    asmbny1 = AsmBny(input_string)
    asmbny2 = AsmBny(input_string, {'c': 1})
    p1 = asmbny1.run()
    p2 = asmbny2.run()
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2016, day=12, verbose=True)

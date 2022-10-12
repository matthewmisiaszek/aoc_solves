import dancer
from common import constants as con, elementwise as ew


def pad(input_string, keypad_file, start):
    keypad_string = open(keypad_file).read().split('\n')
    keypad = {(x, y): c for y, line in enumerate(keypad_string) for x, c in enumerate(line[::2]) if c != ' '}
    inv_keypad = {val: key for key, val in keypad.items()}
    position = inv_keypad[start]
    code = []
    for line in input_string.split('\n'):
        for c in line:
            new_pos = ew.sum2d(position, con.UDLR_YINV[c])
            if new_pos in keypad:
                position = new_pos
        code.append(keypad[position])
    return ''.join(code)


def main(input_string, verbose=False):
    p1 = pad(input_string, dancer.root_path + '/AoC_2016/keypad', '5')
    p2 = pad(input_string, dancer.root_path + '/AoC_2016/fancy_keypad', '5')
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2016, day=2, verbose=True)

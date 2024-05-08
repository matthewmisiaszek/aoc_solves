import blitzen
from donner import spatial as sp, graph


def pad(input_string, keypad_file, start):
    keypad_string = open(keypad_file).read()
    keypad = graph.text_to_dict(keypad_string, exclude=' ')
    keypad = {sp.Point(key.x//2, key.y): val for key, val in keypad.items()}
    inv_keypad = {val: key for key, val in keypad.items()}
    position = inv_keypad[start]
    code = []
    for line in input_string.split('\n'):
        for c in line:
            new_pos = position + sp.NAMES_2D[c]
            if new_pos in keypad:
                position = new_pos
        code.append(keypad[position])
    return ''.join(code)


@blitzen.run
def main(input_string, verbose=False):
    p1 = pad(input_string, blitzen.root_path + '/AoC_2016/keypad', '5')
    p2 = pad(input_string, blitzen.root_path + '/AoC_2016/fancy_keypad', '5')
    return p1, p2


import blitzen
import re


@blitzen.run
def main(input_string, verbose=False):
    p1 = p2 = 0
    enabled = 1
    for a, b, do, dont in re.findall(r'mul\((\d+),(\d+)\)|(do)\(\)|(don\'t)\(\)', input_string):
        enabled = (enabled or do) and not dont
        if a and b:
            mul = int(a) * int(b)
            p1 += mul
            if enabled:
                p2 += mul
    return p1, p2

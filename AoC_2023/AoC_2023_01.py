import blitzen
import re


def calibration(lines, digits):
    calibration_value = 0
    pattern = '|'.join(digits.keys())
    pattern_rev = pattern[::-1]
    for line in lines:
        first = re.search(pattern, line).group(0)
        last = re.search(pattern_rev, line[::-1]).group(0)[::-1]
        calibration_value += digits[first] * 10 + digits[last]
    return calibration_value


@blitzen.run
def main(input_string, verbose=False):
    lines = input_string.split('\n')
    digits = {str(i): i for i in range(1, 10)}
    p1 = calibration(lines, digits)
    spelled_out = ('one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine')
    digits.update({s: i + 1 for i, s in enumerate(spelled_out)})
    p2 = calibration(lines, digits)
    return p1, p2


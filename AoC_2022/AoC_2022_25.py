import blitzen
from donner.misc import digits, roughlog

DIGITS = {'2': 2, '1': 1, '0': 0, '-': -1, '=': -2}
DIGITS_INV = {val: key for key, val in DIGITS.items()}


def SNAFU_to_int(snafu):
    return sum(DIGITS[c] * 5 ** j for j, c in enumerate(snafu[::-1]))


def int_to_SNAFU(i):
    i -= sum(-2 * 5 ** j for j in range(roughlog(i, 5) + 1))
    return ''.join(DIGITS_INV[n - 2] for n in digits(i, 5))


@blitzen.run
def main(input_string, verbose=False):
    p1 = int_to_SNAFU(sum(SNAFU_to_int(i) for i in input_string.split('\n')))
    p2 = blitzen.holiday_greeting
    return p1, p2


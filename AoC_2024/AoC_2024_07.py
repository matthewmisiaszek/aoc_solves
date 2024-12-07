import blitzen
from itertools import product


def fadd(a, b):
    return a + b


def fmul(a, b):
    return a * b


def fconc(a, b):
    return int(str(a) + str(b))


def safety_check(calibrations, operators):
    calibration_result = 0
    for id, vals in calibrations:
        for operlist in product(*(operators, )*len(vals[1:])):
            test_value = vals[0]
            for o, b in zip(operlist, vals[1:]):
                test_value = o(test_value, b)
            if id == test_value:
                calibration_result += id
                break
    return calibration_result


@blitzen.run
def main(input_string, verbose=False):
    calibrations = [line.split(': ') for line in input_string.split('\n')]
    calibrations = [(int(id), [int(i) for i in vals.split()]) for id, vals in calibrations]
    p1 = safety_check(calibrations, (fadd, fmul))
    p2 = safety_check(calibrations, (fadd, fmul, fconc))
    return p1, p2


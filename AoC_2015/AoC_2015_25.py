import blitzen
import re


@blitzen.run
def main(input_string, verbose=False):
    pattern = 'To continue, please consult the code grid in the manual.  Enter the code at row (.*), column (.*).'
    row, column = (int(i) for i in re.findall(pattern, input_string)[0])
    codeno = 1
    for i in range(1, column):
        codeno += i + 1
    for i in range(column, column + row - 1):
        codeno += i
    code = 20151125
    for i in range(codeno - 1):
        code = code * 252533
        code = code % 33554393
    p1 = code
    p2 = blitzen.holiday_greeting
    return p1, p2


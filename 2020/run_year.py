from common2020 import aoc_input
import os
import importlib
import time

timeall = time.time()
cwd = os.getcwd()
print('Day |     Part 1     |      Part 2                                   |  Time  ')
print('------------------------------------------------------------------------------')
for day in range(1, 26):
    start = time.time()
    solve = importlib.import_module('AoC_2020_{:02d}'.format(day))
    p1, p2 = solve.main(aoc_input(2020, day))
    print(' | '.join([str(j).rjust(w)[:w] for j, w in
                      [(day, 3), (p1, 14), (p2, 45), (time.time() - start, 5)]]))

print('Total time: ', time.time() - timeall)

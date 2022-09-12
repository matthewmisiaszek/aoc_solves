from common2021 import aoc_input
import os
import importlib
import time
import re

days = sorted(os.listdir('.'))
timeall = time.time()
cwd = os.getcwd()
print('Day |     Part 1     |      Part 2      |  Time  ')
print('------------------------------------------------')
for i, day in enumerate([day for day in days[:-1] if bool(re.match('day[0-9]{1,2}.py',day))]):
    start = time.time()
    solve = importlib.import_module(day[:-3])
    p1, p2 = solve.main(aoc_input(2021, i+1))
    print(' | '.join([str(j).rjust(w)[:w] for j, w in
                      [(i + 1, 3), (p1, 14), (p2, 16), (time.time() - start, 5)]]))

print('Total time: ', time.time() - timeall)

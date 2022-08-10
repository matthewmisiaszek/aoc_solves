import os
import importlib
import time

days = sorted(os.listdir('.'))
# print(days)
timeall = time.time()
cwd = os.getcwd()
print('Day |     Part 1     |      Part 2      |  Time  ')
print('------------------------------------------------')
for i, day in enumerate(days[:-1]):
    os.chdir(cwd + '/' + day)
    start = time.time()
    solve = importlib.import_module(day + '.' + day)
    p1, p2 = solve.main()
    print(' | '.join([str(j).rjust(w)[:w] for j, w in
                      [(i + 1, 3), (p1, 14), (p2, 16), (time.time() - start, 5)]]))
    # if i == 12:
    #     print('\n' + p2)

print('Total time: ', time.time() - timeall)

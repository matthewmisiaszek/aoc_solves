import dancer
import re
from sympy import symbols, solve

x = symbols('x')
expr = ((691+((817.0+(6259659210072.0-((10+(((((875.0+(308+((((((2*(((683.0+((((2*((((((2*((((((2*(((((((((((((((((11*(810.0+(((((((813.0+(92.0*(((251+((((x-611)*4)+930.0)/6))/2)-198)))+473)/3)-477)*2)-209)/7)))-213)*2)+387.0)+733)/2)+921)*2)-380)/6)+335.0)/6)-715)*21)+436)/2)-260))-646.0)*2)+623)/3)-115.0))+714.0)/2)+787.0)/2)-300.0))-592)*2)+599))/2)-421.0))+511.0)/3)-275)*2)+897)))/12)+711)*3)-635.0))/7)))/2))*19)-21608329599731.0
print(solve(expr))

# def main(input_string, verbose=False):
#     math_monkeys = {}
#     val_monkeys = {}
#     monkey_queue = set()
#     waiting = {}
#     for line in input_string.split('\n'):
#         name, op = line.split(': ')
#         if op.isdigit():
#             val_monkeys[name]=op
#         else:
#             (a, op, b), = re.findall('(\S*) ([\+\-\*/]) (\S*)', op)
#             for i in (a,b):
#                 if i not in waiting:
#                     waiting[i]={name}
#                 else:
#                     waiting[i].add(name)
#             math_monkeys[name]=(a, op, b)
#     val_monkeys['humn'] = 'x'
#     a, op, b = math_monkeys['root']
#     math_monkeys['root'] = a, '=', b
#     for monkey in val_monkeys:
#         monkey_queue.update(waiting[monkey])
#     while monkey_queue:
#         curr = monkey_queue.pop()
#         a, op, b = math_monkeys[curr]
#         if a in val_monkeys and b in val_monkeys:
#             a = val_monkeys[a]
#             b = val_monkeys[b]
#             if curr == 'root':
#                 if a.isdigit():
#             # if op == '+':
#             #     r = a + b
#             # elif op == '-':
#             #     r = a - b
#             # elif op == '*':
#             #     r = a * b
#             # elif op == '/':
#             #     r = a / b
#             r = '('+a + op + b+')'
#             try:
#                 r = str(eval(r))
#             except:
#                 pass
#             val_monkeys[curr]=r
#             if curr in waiting:
#                 monkey_queue.update(waiting[curr])
#     print(val_monkeys['root'])
#     x = symbols('x')
#     expr = eval(val_monkeys['root'][1:-1])
#     p1 = solve(expr)
#     p2 = 1
#     return p1, p2
#
#
# if __name__ == "__main__":
#     dancer.run(main, year=2022, day=21, verbose=True)

# ((691+((817.0+(6259659210072.0-((10+(((((875.0+(308+((((((2*(((683.0+((((2*((((((2*((((((2*(((((((((((((((((11*(810.0+(((((((813.0+(92.0*(((251+((((x-611)*4)+930.0)/6))/2)-198)))+473)/3)-477)*2)-209)/7)))-213)*2)+387.0)+733)/2)+921)*2)-380)/6)+335.0)/6)-715)*21)+436)/2)-260))-646.0)*2)+623)/3)-115.0))+714.0)/2)+787.0)/2)-300.0))-592)*2)+599))/2)-421.0))+511.0)/3)-275)*2)+897)))/12)+711)*3)-635.0))/7)))/2))*19==21608329599731.0

import core


def findparens(problem):
    plevel = 0
    parens = []
    for i, c in enumerate(problem):
        if c == '(':
            if plevel == 0:
                pstart = i
            plevel += 1
        elif c == ')':
            plevel -= 1
            if plevel == 0:
                pend = i
                parens.append((pstart, pend))
    return parens


def reduce(expression_list, ooops):
    for opset in ooops:
        for i in range(len(expression_list) - 2):
            x, op, y = expression_list[i:i + 3]
            if op in opset:
                if op == '+':
                    c = x + y
                elif op == '*':
                    c = x * y
                else:
                    c = 0
                expression_list = expression_list[:i] + [c] + expression_list[i + 3:]
                return expression_list


def evaluate(input_string, ooops):
    expressions = input_string.split('\n')
    todo = expressions.copy()
    answers = {}
    while todo:
        orig_expression = todo.pop()
        expression = orig_expression
        parens = findparens(expression)
        paren_exps = {expression[a + 1:b] for a, b in parens}
        new_todo = paren_exps - answers.keys()
        if new_todo:
            todo.append(orig_expression)
            todo += list(new_todo)
        else:
            for exp in paren_exps:
                expression = expression.replace('(' + exp + ')', answers[exp])
            expression_list = [int(i) if i.isdigit() else i for i in expression.split()]
            while len(expression_list) > 1:
                expression_list = reduce(expression_list, ooops)
            answers[orig_expression] = str(expression_list[0])
    return sum((int(answers[problem]) for problem in expressions))


def main(input_string, verbose=False):
    p1 = evaluate(input_string, [{'+', '*'}])
    p2 = evaluate(input_string, [{'+'}, {'*'}])
    return p1, p2


if __name__ == "__main__":
    core.run(main, year=2020, day=18, verbose=True)

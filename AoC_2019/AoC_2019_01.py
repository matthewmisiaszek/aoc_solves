import blitzen


def total_fuel(module):
    fuel = fuel_req(module)
    if fuel > 0:
        fuel += total_fuel(fuel)
    return fuel


def fuel_req(module):
    return max(module // 3 - 2, 0)


@blitzen.run
def main(input_string, verbose=False):
    modules = [int(i) for i in input_string.split('\n')]
    p1 = sum(fuel_req(module) for module in modules)
    p2 = sum(total_fuel(module) for module in modules)
    return p1, p2


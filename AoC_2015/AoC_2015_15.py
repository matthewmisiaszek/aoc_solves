import blitzen
from math import prod
from itertools import combinations_with_replacement as combo


def main(input_string, verbose=False):
    calories = 'calories'
    meal = 500
    ingredients = {}
    for line in input_string.split('\n'):
        ingredient, properties = line.split(': ')
        ingredients[ingredient] = {}
        for prop in properties.split(', '):
            name, value = prop.split()
            ingredients[ingredient][name] = int(value)
    ingredient_list = list(ingredients.keys())
    p1, p2 = 0, 0
    for divs in combo(range(101), len(ingredient_list) - 1):
        qties = [b - a for a, b in zip((0,) + divs, divs + (100,))]
        properties = {}
        for ingredient, qty in zip(ingredient_list, qties):
            for prop, value in ingredients[ingredient].items():
                if prop not in properties:
                    properties[prop] = 0
                properties[prop] += value * qty
        score = prod((max(value, 0) for key, value in properties.items() if key != calories))
        if properties[calories] == meal:
            p2 = max(p2, score)
        p1 = max(p1, score)
    return p1, p2


if __name__ == "__main__":
    blitzen.run(main, year=2015, day=15, verbose=True)

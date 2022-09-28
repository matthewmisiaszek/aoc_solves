import DANCER


def get_possibilities(input_string):
    input_string = input_string.translate({ord(c): None for c in '(,)'})
    allergen_possibilities = {}
    all_ingredients = set()
    for food in input_string.split('\n'):
        food_ingredients, food_allergens = (set(x.split()) for x in food.split('contains'))
        all_ingredients.update(food_ingredients)
        for allergen in food_allergens:
            if allergen in allergen_possibilities:
                allergen_possibilities[allergen] &= food_ingredients
            else:
                allergen_possibilities[allergen] = food_ingredients.copy()
    return allergen_possibilities, all_ingredients


def reduce(allergen_possibilities):
    allergen_ingredients = {}
    change = True
    while change is True:
        change = False
        for allergen, possible_ingredients in allergen_possibilities.items():
            if len(possible_ingredients) == 1:
                change = True
                ingredient = possible_ingredients.pop()
                allergen_ingredients[allergen] = ingredient
                for ingredients2 in allergen_possibilities.values():
                    ingredients2.discard(ingredient)
    return allergen_ingredients


def main(input_string, verbose=False):
    allergen_possibilities, all_ingredients = get_possibilities(input_string)
    ingredients_w_allergens = set().union(*allergen_possibilities.values())
    ingredients_wo_allergens = all_ingredients - ingredients_w_allergens
    p1 = sum((input_string.count(ingredient) for ingredient in ingredients_wo_allergens))
    allergen_ingredients = reduce(allergen_possibilities)
    p2 = ','.join((allergen_ingredients[x] for x in sorted(allergen_ingredients.keys())))
    return p1, p2


if __name__ == "__main__":
    DANCER.run(main, year=2020, day=21, verbose=True)

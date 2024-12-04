import blitzen
from donner import graph, spatial


def wordsearch(grid, word):
    score = 0
    for turn in range(4):
        for point in grid:
            for position, letter in word:
                if point + position not in grid or grid[point + position] != letter:
                    break
            else:
                score += 1
        word = [(point.right(), letter) for point, letter in word]
    return score


@blitzen.run
def main(input_string, verbose=False):
    grid = graph.text_to_dict(input_string)

    I = tuple((spatial.Point(i, 0), letter) for i, letter in enumerate('XMAS'))
    Z = tuple((point + point.left(), letter) for point, letter in I)
    p1 = wordsearch(grid, I)
    p1 += wordsearch(grid, Z)

    X = (
        (spatial.Point(), 'A'),
        (spatial.NORTHWEST, 'M'),
        (spatial.SOUTHWEST, 'M'),
        (spatial.SOUTHEAST, 'S'),
        (spatial.NORTHEAST, 'S')
    )
    p2 = wordsearch(grid, X)

    return p1, p2

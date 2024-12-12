import blitzen
from donner import graph, spatial


@blitzen.run
def main(input_string, verbose=False):
    p1 = p2 = 0
    garden = graph.text_to_dict(input_string)
    while garden:
        for plot, crop in garden.items():
            break
        q = {plot}
        region = set()
        while q:
            plot = q.pop()
            if plot in region:
                continue
            region.add(plot)
            garden.pop(plot, None)
            for d in spatial.ENWS:
                neighbor = plot + d
                if neighbor in garden and garden[neighbor] == crop:
                    q.add(neighbor)
        perimeter = sides = 0
        for plot in region:
            for d in spatial.ENWS:
                a = plot + d in region
                b = plot + d.left() in region
                perimeter += not a
                sides += (not a and not b) or (a and b and plot + d + d.left() not in region)
        area = len(region)
        p1 += area * perimeter
        p2 += area * sides
    return p1, p2

import blitzen
from donner import printer, spatial


def main(input_string, verbose=False):
    w_px, h_px = 25, 6
    n_px = h_px * w_px
    black, white, transparent = '0', '1', '2'
    img_data = [c for c in input_string]
    layers = [img_data[i:i + n_px] for i in range(0, len(img_data), n_px)]

    black_count = [layer.count(black) for layer in layers]
    least_black_layer = layers[black_count.index(min(black_count))]
    p1 = least_black_layer.count(white) * least_black_layer.count(transparent)

    layers += [[black] * n_px, [white] * n_px]
    pixels = tuple(zip(*layers))
    points = [spatial.Point(x, y) for y in range(h_px) for x in range(w_px)]
    img = {point for point, pixel in zip(points, pixels) if pixel.index(white) < pixel.index(black)}
    img_str = printer.strset(img)
    p2 = img_str
    return p1, p2


if __name__ == "__main__":
    blitzen.run(main, year=2019, day=8, verbose=True)

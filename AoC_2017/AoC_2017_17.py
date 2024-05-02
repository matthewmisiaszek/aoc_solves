import blitzen


def main(input_string, verbose=False):
    step = 363
    position = 0
    buffer = [0]
    for i in range(1, 2018):
        position = (position + step + 1) % len(buffer)
        buffer.insert(position, i)
    p1 = buffer[position + 1]

    buffer_length = 1
    position = 0
    for i in range(1, 50000001):
        if verbose and i % 500000 == 0:
            print('\rCalculating Part 2: ', int(i / 500000), '%', end='')
        if position == 0:
            p2 = i
        buffer_length += 1
        position = (position + step + 1) % buffer_length
    return p1, p2


if __name__ == "__main__":
    blitzen.run(main, year=2017, day=17, verbose=True)

import blitzen


def recstones(stone, blinks, cache={}):
    if (stone, blinks) in cache:
        return cache[(stone, blinks)]
    if blinks == 0:
        ret = 1
    elif stone == '0':
        ret = recstones('1', blinks - 1)
    elif len(stone) % 2 == 0:
        ret = 0
        ret += recstones(stone[:len(stone)//2], blinks-1)
        ret += recstones(str(int(stone[len(stone)//2:])), blinks-1)
    else:
        ret = recstones(str(int(stone)*2024), blinks-1)
    cache[(stone, blinks)] = ret
    return ret


@blitzen.run
def main(input_string, verbose=False):
    stones = [i for i in input_string.split()]
    p1 = sum(recstones(stone, 25) for stone in stones)
    p2 = sum(recstones(stone, 75) for stone in stones)
    return p1, p2


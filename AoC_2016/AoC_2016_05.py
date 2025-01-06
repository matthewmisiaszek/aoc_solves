import blitzen
from donner.misc import md5hash


@blitzen.run
def main(input_string, verbose=False):
    seed = input_string
    p2 = {}
    p1 = []
    i = 0
    while True:
        hash = md5hash(seed + i.__str__())
        if hash[:5] == '00000':
            key = hash[5]
            p1.append(key)
            if key.isdigit() and key not in p2 and 0 <= int(key) <= 7:
                p2[key] = hash[6]
                if len(p2) == 8:
                    break
        i += 1
    p2 = ''.join(p2[c] for c in sorted(p2))
    p1 = ''.join(p1[:8])
    return p1, p2

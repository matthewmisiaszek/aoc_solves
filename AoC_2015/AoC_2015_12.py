import dancer
import json


def count(file, exclude=None):
    if exclude is None:
        exclude = set()
    ret = 0
    if isinstance(file, list):
        for obj in file:
            if isinstance(obj, list) or isinstance(obj, dict):
                ret += count(obj, exclude)
            elif isinstance(obj, int):
                ret += obj
    elif isinstance(file, dict):
        for key, val in file.items():
            if isinstance(val, list) or isinstance(val, dict):
                ret += count(val, exclude)
            elif val in exclude:
                return 0
            elif isinstance(val, int):
                ret += val
            if isinstance(key, int):
                ret += key
    return ret


def main(input_string, verbose=False):
    file = json.loads(input_string)

    p1 = count(file)
    p2 = count(file, {"red"})
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2015, day=12, verbose=True)

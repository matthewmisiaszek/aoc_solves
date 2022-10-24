import dancer


def main(input_string, verbose=False):
    replacements_string, molecule = input_string.split('\n\n')
    replacements_list = [line.split(' => ') for line in replacements_string.split('\n')]
    replacements = {}
    for a, b in replacements_list:
        if a not in replacements:
            replacements[a] = set()
        replacements[a].add(b)

    new_molecules = set()
    for a, bs in replacements.items():
        i = molecule.find(a)
        while i >= 0:
            head = molecule[:i]
            tail = molecule[i + len(a):]
            for b in bs:
                new_molecules.add(head + b + tail)
            i = molecule.find(a, i + 1)

    p1 = len(new_molecules)

    Rn, Y = 'Rn', 'Y'
    Rnc, Yc = (molecule.count(i) for i in (Rn, Y))
    p2 = sum(c.isupper() for c in molecule) - 1 - 2 * Rnc - 2 * Yc
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2015, day=19, verbose=True)

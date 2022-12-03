import dancer
from string import ascii_letters


def main(input_string, verbose=False):
    priority = '_' + ascii_letters
    rucksacks = input_string.split('\n')
    p1, p2 = 0, 0
    for rucksack in rucksacks:
        csize = len(rucksack)//2
        common_items = {i for i in rucksack[:csize]} & {i for i in rucksack[csize:]}
        for i in common_items:
            p1 += priority.find(i)
    rucksack_sets = [{i for i in rucksack} for rucksack in rucksacks]
    elf_groups = zip(*[rucksack_sets[i::3] for i in range(3)])
    for a, b, c in elf_groups:
        common_items = a & b & c
        for i in common_items:
            p2 += priority.find(i)
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2022, day=3, verbose=True)

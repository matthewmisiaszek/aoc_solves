import dancer
from string import ascii_letters


def main(input_string, verbose=False):
    rucksacks = input_string.split('\n')
    p1, p2 = 0, 0
    for rucksack in rucksacks:
        csize = len(rucksack)//2
        common_items = set(rucksack[:csize]) & set(rucksack[csize:])
        for i in common_items:
            p1 += ascii_letters.find(i)+1
    elf_groups = zip(*[rucksacks[i::3] for i in range(3)])
    for a, b, c in elf_groups:
        common_items = set(a) & set(b) & set(c)
        for i in common_items:
            p2 += ascii_letters.find(i)+1
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2022, day=3, verbose=True)

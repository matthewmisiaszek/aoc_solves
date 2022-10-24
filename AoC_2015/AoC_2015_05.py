import dancer
from string import ascii_lowercase as alph
from itertools import product

vow = 'aeiou'


def main(input_string, verbose=False):
    p1, p2 = 0, 0
    invalid = ('ab', 'cd', 'pq', 'xy')
    for string in input_string.split('\n'):
        vowel_count = 0
        double_letter = False
        invalid_strings = False
        double_pair = False
        aba = False

        for i in invalid:
            if string.count(i) > 0:
                invalid_strings = True
                break

        for a, b in product(alph, alph):
            if string.count(a + b) >= 2:
                double_pair = True
            if string.find(a + b + a) >= 0:
                aba = True
            if double_pair and aba:
                break

        for a in alph:
            if string.find(a + a) >= 0:
                double_letter = True
                break

        for a in vow:
            vowel_count += string.count(a)
            if vowel_count >= 3:
                break

        if vowel_count >= 3 and double_letter and invalid_strings == False:
            p1 += 1
        if double_pair and aba:
            p2 += 1
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2015, day=5, verbose=True)

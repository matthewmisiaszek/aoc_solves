import blitzen
import numpy as np


class BoardClass:
    def __init__(self, board):
        self.values = np.array([[int(i) for i in l.split()] for l in board.split('\n')])
        self.mask = np.full(self.values.shape, False)

    def mark(self, num):
        self.mask = np.logical_or(self.mask, self.values == num)

    def win(self):
        return max([max(self.mask.sum(axis=a)) == self.mask.shape[a] for a in range(len(self.mask.shape))])

    def score(self, num):
        return num * (np.multiply(self.values, np.logical_not(self.mask))).sum()


@blitzen.run
def main(input_string, verbose=False):
    f = input_string.split('\n\n')

    nums = [int(i) for i in f[0].split(',')]
    boards = [BoardClass(board) for board in f[1:]]
    scores = []
    for num in nums:
        i = 0
        while i < len(boards):
            boards[i].mark(num)
            if boards[i].win():
                scores.append(boards[i].score(num))
                boards.pop(i)
            else:
                i += 1
    p1, p2 = scores[0], scores[-1]

    return p1, p2


import dancer


class expandArray:
    def __init__(self, default=0):
        self.default = default
        self.array = np.array([[self.default]])
        self.center = [0, 0]

    def write(self, loc, val):
        acoord = tuple(c + l for c, l in zip(self.center, loc))
        if acoord[0] < 0:
            self.array = np.vstack((np.full((-acoord[0], self.array.shape[1]), self.default), self.array))
            self.center[0] += -acoord[0]
            acoord = tuple(c + l for c, l in zip(self.center, loc))
        elif acoord[0] >= self.array.shape[0]:
            self.array = np.vstack(
                (self.array, np.full((acoord[0] - self.array.shape[0] + 1, self.array.shape[1]), self.default)))
        if acoord[1] < 0:
            self.array = np.hstack((np.full((self.array.shape[0], -acoord[1]), self.default), self.array))
            self.center[1] += -acoord[1]
            acoord = tuple(c + l for c, l in zip(self.center, loc))
        elif acoord[1] >= self.array.shape[1]:
            self.array = np.hstack(
                (self.array, np.full((self.array.shape[0], acoord[1] - self.array.shape[1] + 1), self.default)))
        self.array[acoord[0], acoord[1]] = val
        while sum([self.default != self.array[0, i] for i in range(self.array.shape[1])]) == 0:
            self.array = self.array[1:, :]
            self.center[0] += -1
        while sum([self.default != self.array[i, 0] for i in range(self.array.shape[0])]) == 0:
            self.array = self.array[:, 1:]
            self.center[1] += -1
        while sum([self.default != self.array[-1, i] for i in range(self.array.shape[1])]) == 0:
            self.array = self.array[:-1, :]
        while sum([self.default != self.array[i, -1] for i in range(self.array.shape[0])]) == 0:
            self.array = self.array[:, :-1]

    def read(self, loc):
        acoord = tuple(c + l for c, l in zip(self.center, loc))
        shape = self.array.shape
        if 0 <= acoord[0] < shape[0] and 0 <= acoord[1] < shape[1]:
            return self.array[acoord[0], acoord[1]]
        else:
            return self.default

    def print(self, width=0):
        shape = self.array.shape
        s = ''
        for i in range(shape[0]):
            for j in range(shape[1]):
                s += str(self.array[i, j]).rjust(width)
            s += '\n'
        print(s)
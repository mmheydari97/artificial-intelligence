import numpy as np


class Rubik:
    def __init__(self, s0):
        if np.array(s0).shape != (6, 4):
            self.state = None
        else:
            self.state = np.array(s0)

    def __eq__(self, other):
        eq = self.state == other.state
        return np.sum(eq) == 24

    def __str__(self):
        return str(self.state)

    def move(self, num):
        rub = self.state.copy()
        if num > 12 or num < 1:
            pass
        elif num == 1: # side0 clock
            rub[0][0] = self.state[1][2]
            rub[0][1] = self.state[1][0]
            rub[3][1] = self.state[0][0]
            rub[3][3] = self.state[0][1]
            rub[4][3] = self.state[3][1]
            rub[4][2] = self.state[3][3]
            rub[1][2] = self.state[4][3]
            rub[1][0] = self.state[4][2]
        elif num == 2: # side0 counter
            rub[0][0] = self.state[3][1]
            rub[0][1] = self.state[3][3]
            rub[3][1] = self.state[4][3]
            rub[3][3] = self.state[4][2]
            rub[4][3] = self.state[1][2]
            rub[4][2] = self.state[1][0]
            rub[1][2] = self.state[0][0]
            rub[1][0] = self.state[0][1]
        elif num == 3 or 5 or 7: # side1 clock
            rub[1][0] = self.state[5][3]
            rub[1][1] = self.state[5][2]
            rub[2][0] = self.state[1][0]
            rub[2][1] = self.state[1][1]
            rub[3][0] = self.state[2][0]
            rub[3][1] = self.state[2][1]
            rub[5][3] = self.state[3][0]
            rub[5][2] = self.state[3][1]
        elif num == 4 or 6 or 8: # side1 counter
            rub[1][0] = self.state[2][0]
            rub[1][1] = self.state[2][1]
            rub[2][0] = self.state[3][0]
            rub[2][1] = self.state[3][1]
            rub[3][0] = self.state[5][3]
            rub[3][1] = self.state[5][2]
            rub[5][3] = self.state[1][0]
            rub[5][2] = self.state[1][1]

        elif num == 9: # side4 clock
            rub[4][0] = self.state[1][1]
            rub[4][1] = self.state[1][3]
            rub[3][2] = self.state[4][0]
            rub[3][0] = self.state[4][1]
            rub[0][3] = self.state[3][2]
            rub[0][2] = self.state[3][0]
            rub[1][1] = self.state[0][3]
            rub[1][3] = self.state[0][2]
        elif num == 10: # side4 counter
            rub[4][0] = self.state[3][2]
            rub[4][1] = self.state[3][0]
            rub[3][2] = self.state[0][3]
            rub[3][0] = self.state[0][2]
            rub[0][3] = self.state[1][1]
            rub[0][2] = self.state[1][3]
            rub[1][1] = self.state[4][0]
            rub[1][3] = self.state[4][1]
        elif num == 11: # side5 clock
            rub[5][0] = self.state[1][3]
            rub[5][1] = self.state[1][2]
            rub[3][3] = self.state[5][0]
            rub[3][2] = self.state[5][1]
            rub[2][3] = self.state[3][3]
            rub[2][2] = self.state[3][2]
            rub[1][3] = self.state[2][3]
            rub[1][2] = self.state[4][2]
        elif num == 12: # side5 counter
            rub[5][0] = self.state[3][3]
            rub[5][1] = self.state[3][2]
            rub[3][3] = self.state[2][3]
            rub[3][2] = self.state[2][2]
            rub[2][3] = self.state[1][3]
            rub[2][2] = self.state[1][2]
            rub[1][3] = self.state[5][0]
            rub[1][2] = self.state[5][1]
        y = Rubik(rub)
        return y

    def is_answer(self):
        for a in self.state:
            if np.dot(a, np.array([0.5, 0.5, 0.5, 0.5]))/np.linalg.norm(a) != 1:
                return False
        return True


class UCS:
    def __init__(self):
        self.available_nodes = []
        self.visited_nodes = []
        self.created_nodes = 0

    def solve(self, rubik):
        self.available_nodes.append(rubik)
        while True:
            current = self.available_nodes.pop(0)
            if current.is_answer():
                print('solved')
                print(current)
                return True
            self.visited_nodes.append(current)
            for i in range(1, 13):
                rb = current.move(i)
                if rb not in self.visited_nodes + self.available_nodes:
                    self.available_nodes.append(rb)
                    self.created_nodes += 1


if __name__ == "__main__":
    cs = [
        [1, 1, 1, 1],
        [2, 2, 3, 3],
        [3, 3, 4, 4],
        [4, 4, 5, 5],
        [6, 6, 6, 6],
        [2, 2, 5, 5]
    ]
    rubik = Rubik(cs)
    ucs = UCS()
    ucs.solve(rubik)
    print('max number of saved nodes = {}'.format(len(ucs.available_nodes + ucs.visited_nodes)))
    print('expanded nodes = {}'.format(len(ucs.visited_nodes)))
    print('created nodes = {}'.format(ucs.created_nodes))

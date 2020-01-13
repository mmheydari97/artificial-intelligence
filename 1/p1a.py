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


class IDS:
    def __init__(self, d):
        self.created_nodes = 0
        self.expanded_nodes = list()
        self.path = list()
        self.count = 0
        self.d = d

    def solve(self, rubik):
        status = False
        self.path.append(rubik)
        while not status and self.d < 30:
            self.path = [rubik]
            status = self.solve_rubik(rubik)
            if not status:
                self.d += 1
        if status:
            print('solved')
            print('depth of goal = {}'.format(self.d))
            print('max number of saved nodes = {}'.format(self.d + 1))
        else:
            print('unable to find  a solution with this depth limit')

    def solve_rubik(self, rubik):
        valid_rotations = list(range(1, 13))
        current = rubik
        if current.is_answer():
            print(current)
            return current
        while len(self.path) <= self.d:
            if current not in self.expanded_nodes:
                self.expanded_nodes.append(current)
            if len(valid_rotations) != 0:
                mode = valid_rotations.pop()
                next_ = rubik.move(mode)
                self.created_nodes += 1
            else:
                break
            if next_ not in self.path:
                self.path.append(next_)
                status = self.solve_rubik(next_)
            else:
                status = False
            if status:
                return next_

        if len(self.path) != 0:
            self.path.pop()
        return False


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

    init_d = 1
    ids = IDS(init_d)
    ids.solve(rubik)

    print('expanded nodes = {}'.format(len(ids.expanded_nodes)))
    print('created nodes = {}'.format(ids.created_nodes))


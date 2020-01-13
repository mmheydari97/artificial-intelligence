import numpy as np
import networkx as nx
import math


IRAN_PROVINCES = ["Alborz", "Ardabil", "East Azerbaijan", "West Azerbaijan", "Bushehr", "Chaharmahal and Bakhtiari",
                  "Fars", "Gilan", "Golestan", "Hamedan", "Hormozgan", "Ilam", "Isfahan",
                  "Kerman", "Kermanshah", "North Khorasan", "Razavi Khorasan", "South Khorasan", "Khuzestan",
                  "Kohgiluyeh and Boyer-Ahmad", "Kurdistan", "Lorestan", "Markazi", "Mazandaran",
                  "Qazvin", "Qom", "Semnan", "Sistan and Baluchestan", "Tehran", "Yazd", "Zanjan"]

IRAN_MAP = {
    "West Azerbaijan": ["East Azerbaijan", "Zanjan", "Kurdistan"],
    "East Azerbaijan": ["West Azerbaijan", "Ardabil", "Zanjan"],
    "Ardabil": ["East Azerbaijan", "Zanjan", "Gilan"],
    "Gilan": ["Ardabil", "Zanjan", "Qazvin", "Mazandaran"],
    "Mazandaran": ["Gilan", "Qazvin", "Alborz", "Tehran", "Semnan", "Golestan"],
    "Golestan": ["Mazandaran", "Semnan", "North Khorasan"],
    "North Khorasan": ["Golestan", "Semnan", "Razavi Khorasan"],
    "Razavi Khorasan": ["North Khorasan", "Semnan", "South Khorasan"],
    "Semnan": ["Razavi Khorasan", "North Khorasan", "Golestan", "Mazandaran", "Tehran", "Qom", "Isfahan", "South Khorasan"],
    "Tehran": ["Alborz", "Mazandaran", "Semnan", "Qom", "Markazi"],
    "Alborz": ["Qazvin", "Mazandaran", "Tehran", "Qom", "Markazi"],
    "Qazvin": ["Gilan", "Mazandaran", "Alborz", "Markazi", "Hamedan", "Zanjan"],
    "Zanjan": ["Kurdistan", "West Azerbaijan", "East Azerbaijan", "Ardabil", "Gilan", "Qazvin", "Hamedan"],
    "Kurdistan": ["West Azerbaijan", "Zanjan", "Hamedan", "Kermanshah"],
    "Kermanshah": ["Kurdistan", "Hamedan", "Lorestan", "Ilam"],
    "Hamedan": ["Kermanshah", "Kurdistan", "Zanjan", "Qazvin", "Markazi", "Lorestan", "Kermanshah"],
    "Markazi": ["Hamedan", "Qazvin", "Alborz", "Tehran", "Qom", "Isfahan", "Lorestan"],
    "Qom": ["Markazi", "Tehran", "Semnan", "Isfahan"],
    "Isfahan": ["Qom", "Semnan", "South Khorasan", "Yazd", "Fars", "Kohgiluyeh and Boyer-Ahmad", "Chaharmahal and Bakhtiari", "Lorestan", "Markazi"],
    "South Khorasan": ["Razavi Khorasan", "Semnan", "Isfahan", "Yazd", "Kerman", "Sistan and Baluchestan"],
    "Yazd": ["Isfahan", "South Khorasan", "Kerman", "Fars"],
    "Fars": ["Yazd", "Isfahan", "Kohgiluyeh and Boyer-Ahmad", "Bushehr", "Hormozgan", "Kerman"],
    "Kohgiluyeh and Boyer-Ahmad": ["Fars", "Isfahan", "Chaharmahal and Bakhtiari", "Khuzestan", "Bushehr"],
    "Chaharmahal and Bakhtiari": ["Isfahan", "Kohgiluyeh and Boyer-Ahmad", "Khuzestan", "Lorestan"],
    "Khuzestan": ["Bushehr", "Kohgiluyeh and Boyer-Ahmad", "Chaharmahal and Bakhtiari", "Lorestan", "Ilam"],
    "Ilam": ["Khuzestan", "Lorestan", "Kermanshah"],
    "Lorestan": ["Ilam", "Kermanshah", "Hamedan", "Markazi", "Isfahan", "Chaharmahal and Bakhtiari", "Khuzestan"],
    "Bushehr": ["Khuzestan", "Kohgiluyeh and Boyer-Ahmad", "Fars", "Hormozgan"],
    "Hormozgan": ["Bushehr", "Fars", "Kerman", "Sistan and Baluchestan"],
    "Kerman": ["Fars", "Yazd", "South Khorasan", "Sistan and Baluchestan", "Hormozgan"],
    "Sistan and Baluchestan": ["Hormozgan", "Kerman", "South Khorasan"]
}

n = len(IRAN_MAP)
# K = 1.38e-23

G = nx.Graph()
G.add_nodes_from(IRAN_PROVINCES)
for edgs in IRAN_MAP.items():
    u = edgs[0]
    for v in edgs[1]:
        G.add_edge(u, v)

matrix = nx.to_numpy_array(G, IRAN_MAP, np.int, weight=None)
m = np.sum(matrix)/2


def delta(mat, c, i, j):
    if mat[i, j] == 1 and c[i] != c[j]:
        return 1
    return 0


class Sample:
    def __init__(self, min_=0, max_=4, length=n):
        self.col = np.random.randint(min_, max_, length)
        self.score = 0

    def evaluate(self, m_, n_, matrix_):
        for i in range(n_):
            for j in range(i + 1, n_):
                self.score += delta(matrix_, self.col, i, j)
        self.score /= m_

    def __str__(self):
        return str(self.col)

    def next(self, t, m_, n_, mat_):

        f1 = self.score
        col_old = self.col

        # pivot = np.random.randint(n_)
        #
        # # change the color of a city randomly
        # can = [0, 1, 2, 3]
        # can.remove(self.col[pivot])
        #
        # self.col[pivot] = np.random.choice(can, 1)
        self.col = np.random.randint(0, 4, n)
        self.evaluate(m_, n_, mat_)
        f2 = self.score

        if f2 > f1:
            pass
        else:
            try:
                # p = math.exp((f2-f1)/(K*t))
                p = math.exp((f2-f1)/t)
                if np.random.choice([0, 1], 1, p=[p, 1-p]):
                    self.col = col_old
            except ValueError:
                self.col = col_old
        return self


def temp(t0, alpha_, k_, mode):
    if mode == 1:
        return t0*alpha_**k_
    elif mode == 2:
        return t0/(1+alpha_*math.log(1+k_))
    elif mode == 3:
        return t0/(1+alpha_*k_)
    elif mode == 4:
        return t0/(1+alpha_*k_**2)
    else:
        return t0


if __name__ == "__main__":    
    EPOCHS = 5000
    sample = Sample()
    t0 = 1500
    for i in range(EPOCHS):
        t = temp(t0, 0.85, i, 1)
        sample.evaluate(m, n, matrix)
        # if i % 1000 == 0:
        print(sample.score)

        sample = sample.next(t, m, n, matrix)

    # sample = Sample()
    # t0 = 1
    # for i in range(EPOCHS):
    #     t = temp(t0, 1000, i, 2)
    #     sample.evaluate(m, n, matrix)
    #     # if i % 1000 == 0:
    #     print(sample.score)
    #
    #     sample = sample.next(t, m, n, matrix)

    # sample = Sample()
    # t0 = 10
    # for i in range(EPOCHS):
    #     t = temp(t0, 1000, i, 3)
    #     sample.evaluate(m, n, matrix)
    #     # if i % 1000 == 0:
    #     print(sample.score)
    #
    #     sample = sample.next(t, m, n, matrix)

    # sample = Sample()
    # t0 = 2
    # for i in range(EPOCHS):
    #     t = temp(t0, 10, i, 4)
    #     sample.evaluate(m, n, matrix)
    #     # if i % 1000 == 0:
    #     print(sample.score)
    #
    #     sample = sample.next(t, m, n, matrix)
    #

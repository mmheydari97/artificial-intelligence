import numpy as np
import matplotlib.pyplot as plt
import networkx as nx


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


def delta(m, c, i, j):
    if m[i, j] == 1 and c[i] != c[j]:
        return 1
    return 0


class Chromosome:
    def __init__(self, min_=0, max_=4, chromosome_length=n):
        self.gene = np.random.randint(min_, max_, chromosome_length)
        self.score = 0
        self.min_ = min_
        self.max_ = max_

    def evaluate(self, m, n, matrix_):
        for i in range(n):
            for j in range(i + 1, n):
                self.score += delta(matrix_, self.gene, i, j)
        self.score /= m

    def __str__(self):
        return str(self.gene)


def generate_initial_population(p_size):
    list_of_chromosomes = []
    for _ in range(p_size):
        list_of_chromosomes.append(Chromosome())
    return list_of_chromosomes


def crossover(chrom1, chrom2):
    dice = np.random.randint(0, 2, len(chrom1.gene))
    res = Chromosome()
    for i in range(len(dice)):
        if dice[i] == 0:
            res.gene[i] = chrom1.gene[i]
        else:
            res.gene[i] = chrom2.gene[i]
    return res


def mutation(population_, mutation_rate):
    num_mutate = int(n * mutation_rate * len(population_))
    iis = np.random.randint(0, len(population_), num_mutate)
    jjs = np.random.randint(0, n, num_mutate)
    new_population = population_
    min_, max_ = new_population[0].min_, new_population[0].max_
    idxs = zip(iis, jjs)
    for idx in idxs:
        new_population[idx[0]].gene[idx[1]] = np.random.randint(min_, max_)
    return new_population


def evaluate_generation(lof_chroms, m_, n_, mx):
    scores = []
    for chromosome in lof_chroms:
        chromosome.evaluate(m_, n_, mx)
        scores.append(chromosome.score)
    return np.min(scores), np.mean(scores), np.max(scores)


def select_parents(pop, k=4):
    total_score = 0
    new_parents = list()
    n_iter = len(pop)//k
    for i in range(n_iter):
        q = np.random.choice(pop, k, replace=False)
        q = sorted(q, key=lambda j: j.score, reverse=True)
        for j in range(k):
            total_score += q[j].score
        p_best = q[0].score / total_score
        probs = [p_best * (1 - p_best) ** l for l in range(k)]

        # slightly increasing the chance of the best chromosome in a tournament
        probs[0] += 1 - sum(probs)
        winner = np.random.choice(q, 1, p=probs)[0]
        new_parents.append(winner)
    return new_parents


def offspring(population_, n_child=100):
    children = []
    for i in range(n_child):
        p1, p2 = np.random.choice(population_, 2, replace=False)
        children.append(crossover(p1, p2))
    return children


def plotting(result, Ep, pop, k, mu):
    plt.figure()
    result = np.array(result)
    x = np.arange(len(result))
    plt.plot(x, result[:, 0])
    plt.plot(x, result[:, 1])
    plt.plot(x, result[:, 2])
    plt.legend(["min", "avg", "max"])
    plt.xlabel("# of epochs")
    plt.ylabel("fitness")
    if mu*100 < 9:
        mm = "0{}".format(int(mu*100))
    else:
        mm = "10"
    # plt.show()
    plt.savefig("./pics/{}_{}_{}_{}.png".format(Ep, pop, k, mm))
    plt.close()


G = nx.Graph()
G.add_nodes_from(IRAN_PROVINCES)
for edgs in IRAN_MAP.items():
    u = edgs[0]
    for v in edgs[1]:
        G.add_edge(u, v)

# nx.draw_networkx_nodes()
# plt.show()

# matrix = nx.adjacency_matrix(G, IRAN_PROVINCES, None)
matrix = nx.to_numpy_array(G, IRAN_MAP, np.int, weight=None)

m = np.sum(matrix)/2

if __name__ == "__main__":
    for EPOCHS in [50, 500, 5000]:
        for psize in [100, 1000]:
            for k in [2, 5, 10]:
                for MU in [0.01, 0.02, 0.05, 0.1]:
                    population = generate_initial_population(psize)
                    results = list()
                    results.append(evaluate_generation(population, m, n, matrix))
                    for _ in range(EPOCHS):
                        parents = select_parents(population, k)
                        offsprings = offspring(parents, psize)
                        population = mutation(offsprings, MU)
                        res = evaluate_generation(population, m, n, matrix)
                        results.append(res)

                    plotting(results, EPOCHS, psize, k, MU)
                    print("done.")

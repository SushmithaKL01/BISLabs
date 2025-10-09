import numpy as np
import random

def aco_tsp(dist, m=5, alpha=1, beta=5, rho=0.5, iters=10, delta=1):
    n = len(dist)
    tau = np.ones((n, n))
    eta = 1 / (dist + 1e-10)
    best_path, best_len = None, float('inf')

    for t in range(1, iters + 1):
        paths, lens = [], []
        for _ in range(m):
            path = [random.randrange(n)]
            S = set(range(n)) - {path[0]}
            while S:
                i = path[-1]
                probs = [tau[i][j]**alpha * eta[i][j]**beta for j in S]
                j = random.choices(list(S), weights=probs)[0]
                path.append(j)
                S.remove(j)
            path.append(path[0])
            length = sum(dist[path[i]][path[i+1]] for i in range(n))
            paths.append(path)
            lens.append(length)
        tau *= (1 - rho)
        best_iter = paths[np.argmin(lens)]
        best_iter_len = min(lens)
        if best_iter_len < best_len:
            best_path, best_len = best_iter, best_iter_len
        for (i, j) in zip(best_iter[:-1], best_iter[1:]):
            tau[i][j] += delta / 2
        for (i, j) in zip(best_path[:-1], best_path[1:]):
            tau[i][j] += delta / 2
        print(f"Iter {t}: best_iter={best_iter}, len={best_iter_len:.2f}, global_best_len={best_len:.2f}")
    return best_path, best_len

dist = np.array([
    [0, 2, 2, 5, 7],
    [2, 0, 4, 8, 2],
    [2, 4, 0, 1, 3],
    [5, 8, 1, 0, 2],
    [7, 2, 3, 2, 0]
], dtype=float)

path, length = aco_tsp(dist, m=4, iters=8)
print("\nFinal best path:", path)
print("Final shortest distance:", length)

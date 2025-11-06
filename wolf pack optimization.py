import numpy as np

def f(x):
    # objective function
    return np.sum(x**2)

def gwo(obj, dim=5, n_wolves=20, max_iter=100, lb=-10, ub=10):

    wolves = np.random.uniform(lb, ub, (n_wolves, dim))
    fitness = np.apply_along_axis(obj, 1, wolves)

    alpha, beta, delta = np.argsort(fitness)[:3]

    for _ in range(max_iter):

        a = 2 - 2 * (_ / max_iter)

        for i in range(n_wolves):

            for leader in [alpha, beta, delta]:
                r1 = np.random.rand(dim)
                r2 = np.random.rand(dim)

                A = 2 * a * r1 - a
                C = 2 * r2

                D = abs(C * wolves[leader] - wolves[i])
                X = wolves[leader] - A * D

                # accumulate influence
                if leader == alpha:
                    X1 = X
                elif leader == beta:
                    X2 = X
                else:
                    X3 = X

            wolves[i] = (X1 + X2 + X3) / 3

            # boundaries
            wolves[i] = np.clip(wolves[i], lb, ub)

        fitness = np.apply_along_axis(obj, 1, wolves)
        alpha, beta, delta = np.argsort(fitness)[:3]

    return wolves[alpha], fitness[alpha]


best_pos, best_val = gwo(f)
print("Best position:", best_pos)
print("Best fitness:", best_val)

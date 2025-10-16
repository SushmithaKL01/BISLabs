import numpy as np

class CuckooSearchKnapsack:
    def __init__(self, n_nests=25, pa=0.25, max_iter=100):
        self.n_nests = n_nests
        self.pa = pa
        self.max_iter = max_iter
        self.best_nest = None
        self.best_fitness = float('-inf')
        self.fitness_history = []
        
    def levy_flight(self, dim):
        from math import gamma, sin, pi
        beta = 1.5
        sigma_u = (gamma(1 + beta) * sin(pi * beta / 2) / 
                   (gamma((1 + beta) / 2) * beta * 2**((beta - 1) / 2)))**(1 / beta)
        u = np.random.normal(0, sigma_u, dim)
        v = np.random.normal(0, 1, dim)
        return u / np.abs(v)**(1 / beta)
    
    def repair_solution(self, solution, weights, capacity):
        solution = (solution > 0.5).astype(int)
        while np.sum(solution * weights) > capacity:
            included = np.where(solution == 1)[0]
            if len(included) == 0:
                break
            remove = np.random.choice(included)
            solution[remove] = 0
        return solution
    
    def fitness(self, solution, values, weights, capacity):
        total_weight = np.sum(solution * weights)
        if total_weight > capacity:
            return 0
        return np.sum(solution * values)
    
    def optimize(self, values, weights, capacity):
        n_items = len(values)
        nests = np.random.rand(self.n_nests, n_items)
        
        fitness_vals = np.zeros(self.n_nests)
        for i in range(self.n_nests):
            repaired = self.repair_solution(nests[i].copy(), weights, capacity)
            fitness_vals[i] = self.fitness(repaired, values, weights, capacity)
        
        best_idx = np.argmax(fitness_vals)
        self.best_nest = self.repair_solution(nests[best_idx].copy(), weights, capacity)
        self.best_fitness = fitness_vals[best_idx]
        
        for t in range(self.max_iter):
            for i in range(self.n_nests):
                step = self.levy_flight(n_items)
                new_nest = nests[i] + 0.01 * step
                new_nest = np.clip(new_nest, 0, 1)
                new_nest_repaired = self.repair_solution(new_nest.copy(), weights, capacity)
                new_fitness = self.fitness(new_nest_repaired, values, weights, capacity)
                
                j = np.random.randint(0, self.n_nests)
                if new_fitness > fitness_vals[j]:
                    nests[j] = new_nest
                    fitness_vals[j] = new_fitness
                    if new_fitness > self.best_fitness:
                        self.best_nest = new_nest_repaired.copy()
                        self.best_fitness = new_fitness
            
            worst_idx = np.argsort(fitness_vals)[:int(self.pa * self.n_nests)]
            for idx in worst_idx:
                nests[idx] = np.random.rand(n_items)
                repaired = self.repair_solution(nests[idx].copy(), weights, capacity)
                fitness_vals[idx] = self.fitness(repaired, values, weights, capacity)
            
            self.fitness_history.append(self.best_fitness)
        
        return self.best_nest, self.best_fitness


if __name__ == "__main__":
    print("=== Cuckoo Search for 0/1 Knapsack Problem ===\n")
    
    values = np.array([60, 100, 120, 80, 50, 70, 90, 110])
    weights = np.array([10, 20, 30, 15, 12, 18, 25, 22])
    capacity = 80
    
    print(f"Number of items: {len(values)}")
    print(f"Knapsack capacity: {capacity}")
    print(f"Items (Value, Weight):")
    for i in range(len(values)):
        print(f"  Item {i+1}: (${values[i]}, {weights[i]}kg)")
    
    cs = CuckooSearchKnapsack(n_nests=30, pa=0.25, max_iter=100)
    best_solution, best_value = cs.optimize(values, weights, capacity)
    
    selected_items = np.where(best_solution == 1)[0]
    total_weight = np.sum(best_solution * weights)
    
    print(f"\n=== SOLUTION ===")
    print(f"Selected items: {selected_items + 1}")
    print(f"Total value: ${best_value:.0f}")
    print(f"Total weight: {total_weight:.0f}kg / {capacity}kg")
    
    print(f"\nItem details:")
    for idx in selected_items:
        print(f"  Item {idx+1}: Value=${values[idx]}, Weight={weights[idx]}kg")
    
    print(f"\nConvergence (every 20 iterations):")
    for i in range(0, len(cs.fitness_history), 20):
        print(f"  Iter {i+1:3d}: Best Value = ${cs.fitness_history[i]:.0f}")
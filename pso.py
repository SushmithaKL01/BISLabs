import random

def objective(pos):
    # Objective function to maximize: squared sum of x and y coordinates
    return pos[0]**2 + pos[1]**2

# PSO parameters
num_particles = 5
num_iterations = 10
w = 0.5  # inertia
c1 = 1.0  # cognitive coefficient
c2 = 1.0  # social coefficient

# Initial positions and velocities
positions = [[random.uniform(-5, 5), random.uniform(-5, 5)] for _ in range(num_particles)]
velocities = [[random.uniform(-1, 1), random.uniform(-1, 1)] for _ in range(num_particles)]

# Initialize personal best positions and scores
pbests = [pos[:] for pos in positions]
pbest_scores = [objective(p) for p in positions]

# Initialize the global best position and score
gbest_score = max(pbest_scores)
gbest = pbests[pbest_scores.index(gbest_score)][:]

# PSO main loop
for it in range(num_iterations):
    for i in range(num_particles):
        for d in range(2):  # Iterate for each dimension (x and y)
            # Randomize r1 and r2 each iteration
            r1 = random.random()
            r2 = random.random()

            # Update velocity
            velocities[i][d] = (
                w * velocities[i][d]
                + c1 * r1 * (pbests[i][d] - positions[i][d])
                + c2 * r2 * (gbest[d] - positions[i][d])
            )
            # Update position
            positions[i][d] += velocities[i][d]

        # Calculate the score for the new position
        score = objective(positions[i])

        # Update personal best if the new position is better (for maximization)
        if score > pbest_scores[i]:
            pbests[i] = positions[i][:]
            pbest_scores[i] = score

    # Update the global best position if a personal best is better (for maximization)
    gbest_score = max(pbest_scores)
    gbest = pbests[pbest_scores.index(gbest_score)][:]

    # Print the global best position and score for the current iteration
    print(f"Iteration {it+1}: Best fitness value = {gbest_score}")

print("\nFinal drone waypoints:")
for i, pos in enumerate(positions):
    print(f"Drone {i+1}: {[round(coord, 2) for coord in pos]}")
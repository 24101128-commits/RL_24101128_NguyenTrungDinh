import numpy as np

P = np.array([
    [0.7, 0.2, 0.1],
    [0.3, 0.5, 0.2],
    [0.2, 0.3, 0.5]
])

def state_distribution(p0, P, n_steps):
    distribution = p0.copy()
    for _ in range(n_steps):
        distribution = distribution @ P
    return distribution

p0 = np.array([1.0, 0.0, 0.0])

for t in [1, 2, 5, 10, 50]:
    distribution = state_distribution(p0, P, t)
    print(f"t = {t}: {distribution}")
    
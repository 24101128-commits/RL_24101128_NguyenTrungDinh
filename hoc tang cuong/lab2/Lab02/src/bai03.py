import numpy as np

P = np.array([
    [0.7, 0.2, 0.1],
    [0.3, 0.5, 0.2],
    [0.2, 0.3, 0.5]
])

p0 = np.array([1.0, 0.0, 0.0])
p1 = p0 @ P

print("Initial distribution:", p0)
print("Distribution after one step:", p1)
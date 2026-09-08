import numpy as np

P = np.array([
    [0.7, 0.2, 0.1],
    [0.3, 0.5, 0.2],
    [0.2, 0.3, 0.5]
])

print("Transition matrix:")
print(P)
print("Row sums:")
print(P.sum(axis=1))
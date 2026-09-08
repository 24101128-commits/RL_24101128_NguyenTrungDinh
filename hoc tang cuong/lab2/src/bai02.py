import numpy as np

def validate_transition_matrix(P, tol=1e-10):
    P = np.asarray(P)
    if P.ndim != 2:
        return False
    if P.shape[0] != P.shape[1]:
        return False
    if np.any(P < 0) or np.any(P > 1):
        return False
    if not np.allclose(P.sum(axis=1), 1.0, atol=tol):
        return False
    return True

P = np.array([
    [0.7, 0.2, 0.1],
    [0.3, 0.5, 0.2],
    [0.2, 0.3, 0.5]
])

print("Valid:", validate_transition_matrix(P))
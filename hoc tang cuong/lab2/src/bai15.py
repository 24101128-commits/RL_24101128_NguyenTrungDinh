import numpy as np

n_states = 2
n_actions = 2
policy = np.ones((n_states, n_actions)) / n_actions

print("Stochastic policy:")
print(policy)
print("Probability sum for each state:")
print(policy.sum(axis=1))
print("Valid:", np.allclose(policy.sum(axis=1), 1.0))
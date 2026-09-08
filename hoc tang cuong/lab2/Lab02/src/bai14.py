import numpy as np

policy = np.array([0, 1])
def print_policy(policy):
    for state, action in enumerate(policy):
        print(f"State {state} -> Action {action}")

print("Deterministic policy:")
print_policy(policy)
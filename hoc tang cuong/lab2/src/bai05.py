import numpy as np

P = np.array([
    [0.7, 0.2, 0.1],
    [0.3, 0.5, 0.2],
    [0.2, 0.3, 0.5]
])

def sample_next_state(current_state, P, rng):
    return rng.choice(len(P), p=P[current_state])

rng = np.random.default_rng(42)
current_state = 0
states = [current_state]

for _ in range(30):
    current_state = sample_next_state(current_state, P, rng)
    states.append(current_state)

print("State sequence:")
print(states)
P = {
    0: {
        0: [(1.0, 1, 1.0, False)],
        1: [(1.0, 0, 0.0, False)]
    },
    1: {
        0: [(1.0, 0, 0.0, False)],
        1: [(1.0, 1, 1.0, True)]
    }
}

n_states = 2
n_actions = 2
print("Number of states:", n_states)
print("Number of actions:", n_actions)
print("MDP model:")

for state in range(n_states):
    for action in range(n_actions):
        print(f"State {state}, Action {action}: {P[state][action]}")
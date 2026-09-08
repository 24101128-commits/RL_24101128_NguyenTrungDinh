def validate_mdp(P, n_states, n_actions):
    for state in range(n_states):
        for action in range(n_actions):
            transitions = P[state][action]
            probability_sum = sum(
                transition[0]
                for transition in transitions
            )
            if abs(probability_sum - 1.0) > 1e-10:
                print(
                    f"Invalid transition at state={state}, action={action}"
                )
                return False
    return True

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
print("Valid MDP:", validate_mdp(P, n_states, n_actions))
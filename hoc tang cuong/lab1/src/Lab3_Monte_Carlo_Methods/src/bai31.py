Q = {}
N = {}

state = (15, 10, 0)
action = 1
returns = [1, -1, 1, 1, -1]

print("Incremental Mean")
print("=" * 50)

for G in returns:
    state_action = (state, action)
    N[state_action] = N.get(state_action, 0) + 1
    if state_action not in Q:
        Q[state_action] = 0.0
    Q[state_action] = (
        Q[state_action]
        + (G - Q[state_action]) / N[state_action]
    )
    print(f"Return G = {G}")
    print(f"N(s,a) = {N[state_action]}")
    print(f"Q(s,a) = {Q[state_action]:.4f}")
    print()

print("Final result")
print("=" * 50)
print("State:", state)
print("Action:", action)
print("N(s,a):", N[(state, action)])
print("Q(s,a):", f"{Q[(state, action)]:.4f}")
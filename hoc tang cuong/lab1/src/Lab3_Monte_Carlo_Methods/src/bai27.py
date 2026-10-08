import random

def epsilon_greedy_action(Q, state, epsilon, n_actions=2):
    if random.random() < epsilon:
        return random.randrange(n_actions)
    q_values = []
    for action in range(n_actions):
        state_action = (state, action)
        if state_action in Q:
            q_values.append((action, Q[state_action]))
    if len(q_values) == 0:
        return random.randrange(n_actions)
    return max(q_values, key=lambda x: x[1])[0]
Q = {
    ((10, 5, 0), 0): 1.0,
    ((10, 5, 0), 1): 5.0
}

state = (10, 5, 0)
epsilon = 0.1
num_trials = 1000
count_action_0 = 0
count_action_1 = 0

for _ in range(num_trials):
    action = epsilon_greedy_action(
        Q,
        state,
        epsilon
    )
    if action == 0:
        count_action_0 += 1
    else:
        count_action_1 += 1

print("Epsilon-Greedy")
print("=" * 50)
print("Q(s,0) =", Q[(state, 0)])
print("Q(s,1) =", Q[(state, 1)])
print("Epsilon =", epsilon)
print()
print("Number of trials:", num_trials)
print("Action 0:", count_action_0)
print("Action 1:", count_action_1)
print()
print("Greedy action: 1")
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
epsilons = [0.01, 0.05, 0.10, 0.20, 0.50]
num_trials = 1000

print("So sanh Epsilon-Greedy")
print("=" * 50)

for epsilon in epsilons:
    greedy_count = 0
    for _ in range(num_trials):
        action = epsilon_greedy_action(
            Q,
            state,
            epsilon
        )
        if action == 1:
            greedy_count += 1
    frequency = greedy_count / num_trials

    print(f"Epsilon = {epsilon:.2f}")
    print(f"Greedy action frequency: {frequency:.3f}")
    print(f"Greedy action count: {greedy_count}/{num_trials}")
    print()
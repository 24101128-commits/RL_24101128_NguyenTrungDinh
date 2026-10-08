import random
import os
import matplotlib.pyplot as plt

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
greedy_frequencies = []

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
    greedy_frequencies.append(frequency)

    print(f"Epsilon = {epsilon:.2f}")
    print(f"Greedy action frequency: {frequency:.3f}")
    print()

plt.figure(figsize=(8, 5))

plt.plot(
    epsilons,
    greedy_frequencies,
    marker="o"
)

plt.xlabel("Epsilon")
plt.ylabel("Greedy Action Frequency")
plt.title("Epsilon-Greedy Comparison")
plt.grid(True)

current_dir = os.path.dirname(os.path.abspath(__file__))
lab03_dir = os.path.dirname(current_dir)
figures_dir = os.path.join(lab03_dir, "figures")
os.makedirs(figures_dir, exist_ok=True)

save_path = os.path.join(
    figures_dir,
    "epsilon_comparison.png"
)

plt.savefig(
    save_path,
    dpi=300,
    bbox_inches="tight"
)

plt.show()
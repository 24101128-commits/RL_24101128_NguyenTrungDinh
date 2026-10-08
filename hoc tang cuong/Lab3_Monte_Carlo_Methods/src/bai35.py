import gymnasium as gym
import random
import os
import numpy as np
import matplotlib.pyplot as plt

def epsilon_greedy_action(Q, state, epsilon, n_actions=2):
    if random.random() < epsilon:
        return random.randrange(n_actions)
    q_values = []
    for action in range(n_actions):
        if (state, action) in Q:
            q_values.append((action, Q[(state, action)]))
    if not q_values:
        return random.randrange(n_actions)

    return max(q_values, key=lambda x: x[1])[0]

def compute_returns(rewards, gamma=1.0):
    returns = []
    G = 0
    for reward in reversed(rewards):
        G = reward + gamma * G
        returns.insert(0, G)

    return returns

env = gym.make("Blackjack-v1")

Q = {}
N = {}

num_episodes = 100000
gamma = 1.0
epsilon = 0.1
episode_rewards = []

for episode_number in range(num_episodes):
    state, info = env.reset(seed=episode_number)
    episode = []
    while True:
        action = epsilon_greedy_action(
            Q,
            state,
            epsilon
        )
        next_state, reward, terminated, truncated, info = env.step(action)
        episode.append((state, action, reward))
        state = next_state
        if terminated or truncated:
            break
    rewards = [x[2] for x in episode]
    episode_rewards.append(sum(rewards))
    returns = compute_returns(rewards, gamma)
    visited = set()
    for (state, action, reward), G in zip(episode, returns):
        state_action = (state, action)
        if state_action in visited:
            continue
        visited.add(state_action)
        N[state_action] = N.get(state_action, 0) + 1
        Q[state_action] = Q.get(state_action, 0)
        Q[state_action] += (
            G - Q[state_action]
        ) / N[state_action]

window = 1000

moving_average = np.convolve(
    episode_rewards,
    np.ones(window) / window,
    mode="valid"
)

plt.figure(figsize=(8, 5))

plt.plot(
    range(window, num_episodes + 1),
    moving_average
)

plt.xlabel("Episode")
plt.ylabel("Average Reward")
plt.title("MC Control Learning Curve")
plt.grid(True)

current_dir = os.path.dirname(os.path.abspath(__file__))
lab03_dir = os.path.dirname(current_dir)
figures_dir = os.path.join(lab03_dir, "figures")
os.makedirs(figures_dir, exist_ok=True)

save_path = os.path.join(
    figures_dir,
    "mc_convergence.png"
)

plt.savefig(
    save_path,
    dpi=300,
    bbox_inches="tight"
)

plt.show()
env.close()
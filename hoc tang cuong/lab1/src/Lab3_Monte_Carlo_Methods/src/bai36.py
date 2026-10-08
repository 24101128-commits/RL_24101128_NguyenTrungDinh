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

def mc_control(env, num_episodes, gamma, epsilon):
    Q = {}
    N = {}
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
        returns = compute_returns(
            rewards,
            gamma
        )
        visited = set()
        for (state, action, reward), G in zip(
            episode,
            returns
        ):
            state_action = (state, action)
            if state_action in visited:
                continue
            visited.add(state_action)
            N[state_action] = (
                N.get(state_action, 0) + 1
            )
            Q[state_action] = Q.get(
                state_action,
                0
            )
            Q[state_action] += (
                G - Q[state_action]
            ) / N[state_action]

    return Q, episode_rewards

def greedy_action(Q, state):
    q_values = []
    for action in [0, 1]:
        if (state, action) in Q:
            q_values.append(
                (action, Q[(state, action)])
            )
    if not q_values:
        return 0
    
    return max(
        q_values,
        key=lambda x: x[1]
    )[0]

def evaluate_policy(env, Q, num_episodes=10000):
    total_reward = 0
    wins = 0
    losses = 0
    draws = 0
    for episode_number in range(num_episodes):
        state, info = env.reset(
            seed=episode_number
        )
        while True:
            action = greedy_action(
                Q,
                state
            )
            next_state, reward, terminated, truncated, info = env.step(action)
            state = next_state
            if terminated or truncated:
                total_reward += reward
                if reward > 0:
                    wins += 1
                elif reward < 0:
                    losses += 1
                else:
                    draws += 1
                break
    average_reward = total_reward / num_episodes
    win_rate = wins / num_episodes
    return (
        average_reward,
        win_rate,
        wins,
        losses,
        draws
    )

env = gym.make("Blackjack-v1")
num_episodes = 100000
gamma = 1.0
epsilon = 0.1

Q, episode_rewards = mc_control(
    env,
    num_episodes,
    gamma,
    epsilon
)

print("MONTE CARLO CONTROL - MINI PROJECT")
print("=" * 50)
print("Training episodes:", num_episodes)
print("Number of state-action pairs:", len(Q))
print()
print("Sample Q(s,a):")
print("=" * 50)

sample_states = [
    (20, 10, 0),
    (20, 7, 0),
    (19, 10, 0),
    (17, 10, 0),
    (15, 10, 0)
]

for state in sample_states:
    print("State:", state)
    for action in [0, 1]:
        if (state, action) in Q:
            print(
                f"Action {action}: "
                f"{Q[(state, action)]:.4f}"
            )
        else:
            print(
                f"Action {action}: "
                "chưa có dữ liệu"
            )

    print()

average_reward, win_rate, wins, losses, draws = evaluate_policy(
    env,
    Q
)

print("Policy Evaluation")
print("=" * 50)
print("Average reward:", f"{average_reward:.4f}")
print("Win rate:", f"{win_rate:.4f}")
print("Wins:", wins)
print("Losses:", losses)
print("Draws:", draws)

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
plt.title("Monte Carlo Control Learning Curve")
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
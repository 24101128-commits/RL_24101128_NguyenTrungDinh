"""
Bai 28. So sanh FrozenLake deterministic (is_slippery=False) va
stochastic (is_slippery=True), moi truong hop 500 episode.
"""

import gymnasium as gym
import numpy as np


def run_random_policy(is_slippery, n_episodes=500):
    env = gym.make("FrozenLake-v1", is_slippery=is_slippery)

    successes = 0
    rewards = []
    lengths = []

    for ep in range(n_episodes):
        observation, info = env.reset(seed=ep)
        terminated = False
        truncated = False
        total_reward = 0.0
        length = 0
        while not (terminated or truncated):
            action = env.action_space.sample()
            observation, reward, terminated, truncated, info = env.step(action)
            total_reward += reward
            length += 1

        if terminated and total_reward > 0:
            successes += 1
        rewards.append(total_reward)
        lengths.append(length)

    env.close()
    rewards = np.array(rewards)
    lengths = np.array(lengths)

    return {
        "success_rate": successes / n_episodes,
        "avg_reward": rewards.mean(),
        "avg_length": lengths.mean(),
    }


def main():
    deterministic = run_random_policy(is_slippery=False)
    stochastic = run_random_policy(is_slippery=True)

    print("Deterministic (is_slippery=False):", deterministic)
    print("Stochastic (is_slippery=True):   ", stochastic)

    # Ket luan:
    # Moi truong deterministic co success_rate va reward trung binh cao hon
    # nhieu so voi stochastic, vi trong che do stochastic (truot bang),
    # action thuc te co the khac voi action agent chon, khien random agent
    # de roi xuong ho hon va kho den Goal hon.


if __name__ == "__main__":
    main()

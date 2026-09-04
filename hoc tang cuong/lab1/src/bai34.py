"""
Bai 34. Ham evaluate_policy(env_name, policy, n_episodes=100, seed=42)
tra ve mean_reward, std_reward, min_reward, max_reward, mean_length.
"""

import gymnasium as gym
import numpy as np
from bai33 import run_episode, random_policy


def evaluate_policy(env_name, policy, n_episodes=100, seed=42, max_steps=1000):
    env = gym.make(env_name)
    rewards = []
    lengths = []

    for ep in range(n_episodes):
        result = run_episode(env, policy, seed=seed + ep, max_steps=max_steps)
        rewards.append(result["reward"])
        lengths.append(result["length"])

    env.close()
    rewards = np.array(rewards)
    lengths = np.array(lengths)

    return {
        "mean_reward": float(rewards.mean()),
        "std_reward": float(rewards.std()),
        "min_reward": float(rewards.min()),
        "max_reward": float(rewards.max()),
        "mean_length": float(lengths.mean()),
    }


def main():
    stats = evaluate_policy("CartPole-v1", random_policy, n_episodes=100, seed=42)
    print(stats)


if __name__ == "__main__":
    main()

"""
Bai 22. Ham experiment(seed, n_episodes) tra ve dict thong ke,
chay voi it nhat 5 seed khac nhau.
"""

import gymnasium as gym
import numpy as np


def experiment(seed, n_episodes):
    env = gym.make("CartPole-v1")
    rewards = []
    for ep in range(n_episodes):
        observation, info = env.reset(seed=seed + ep)
        total_reward = 0.0
        terminated = False
        truncated = False
        while not (terminated or truncated):
            action = env.action_space.sample()
            observation, reward, terminated, truncated, info = env.step(action)
            total_reward += reward
        rewards.append(total_reward)
    env.close()

    rewards = np.array(rewards)
    return {
        "seed": seed,
        "mean_reward": float(rewards.mean()),
        "std_reward": float(rewards.std()),
        "max_reward": float(rewards.max()),
        "min_reward": float(rewards.min()),
    }


def main():
    seeds = [0, 1, 42, 100, 2024]
    for seed in seeds:
        result = experiment(seed, n_episodes=20)
        print(result)


if __name__ == "__main__":
    main()

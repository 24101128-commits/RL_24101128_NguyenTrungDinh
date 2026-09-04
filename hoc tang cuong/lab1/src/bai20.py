"""
Bai 20. So sanh reward trung binh giua seed=42 va seed=100, moi seed 20 episode.
"""

import gymnasium as gym
import numpy as np


def run_group(seed, n_episodes=20):
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
    return np.array(rewards)


def main():
    rewards_42 = run_group(seed=42)
    rewards_100 = run_group(seed=100)

    print(f"Seed 42  -> mean reward: {rewards_42.mean():.2f}")
    print(f"Seed 100 -> mean reward: {rewards_100.mean():.2f}")


if __name__ == "__main__":
    main()

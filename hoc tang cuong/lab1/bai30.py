"""
Bai 30. always_left_policy va always_right_policy tren CartPole,
chay moi policy 100 episode va so sanh reward trung binh.
"""

import gymnasium as gym
import numpy as np


def always_left_policy(observation):
    return 0


def always_right_policy(observation):
    return 1


def run_policy(policy_fn, n_episodes=100):
    env = gym.make("CartPole-v1")
    rewards = []
    for ep in range(n_episodes):
        observation, info = env.reset(seed=ep)
        total_reward = 0.0
        terminated = False
        truncated = False
        while not (terminated or truncated):
            action = policy_fn(observation)
            observation, reward, terminated, truncated, info = env.step(action)
            total_reward += reward
        rewards.append(total_reward)
    env.close()
    return np.array(rewards)


def main():
    left_rewards = run_policy(always_left_policy)
    right_rewards = run_policy(always_right_policy)

    print(f"Always-left  mean reward: {left_rewards.mean():.2f}")
    print(f"Always-right mean reward: {right_rewards.mean():.2f}")


if __name__ == "__main__":
    main()

"""
Bai 15. Tinh thong ke reward (mean, min, max, std) bang NumPy tu ket qua Bai 14.
"""

import numpy as np
import gymnasium as gym
from bai11 import random_agent


def main():
    env = gym.make("CartPole-v1")

    episode_rewards = []
    for ep in range(100):
        total_reward, length = random_agent(env)
        episode_rewards.append(total_reward)
    env.close()

    rewards = np.array(episode_rewards)

    print(f"Mean reward : {rewards.mean():.2f}")
    print(f"Min reward  : {rewards.min():.2f}")
    print(f"Max reward  : {rewards.max():.2f}")
    print(f"Std reward  : {rewards.std():.2f}")


if __name__ == "__main__":
    main()

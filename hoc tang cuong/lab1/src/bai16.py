"""
Bai 16. Tim episode tot nhat (reward lon nhat) va do dai tuong ung,
KHONG duyet lai moi truong - chi dung du lieu da luu tu qua trinh chay.
"""

import numpy as np
import gymnasium as gym
from bai11 import random_agent


def main():
    env = gym.make("CartPole-v1")

    episode_rewards = []
    episode_lengths = []
    for ep in range(100):
        total_reward, length = random_agent(env)
        episode_rewards.append(total_reward)
        episode_lengths.append(length)
    env.close()

    rewards = np.array(episode_rewards)
    lengths = np.array(episode_lengths)

    best_index = int(np.argmax(rewards))

    print("Episode tot nhat:", best_index)
    print("Reward tuong ung:", rewards[best_index])
    print("Do dai tuong ung:", lengths[best_index])


if __name__ == "__main__":
    main()

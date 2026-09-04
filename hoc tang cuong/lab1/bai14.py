"""
Bai 14. Chay random agent trong 100 episode, luu reward vao episode_rewards.
Khong in tung timestep.
"""

import gymnasium as gym
from bai11 import random_agent


def main():
    env = gym.make("CartPole-v1")

    episode_rewards = []
    for ep in range(100):
        total_reward, length = random_agent(env)
        episode_rewards.append(total_reward)

    print("Da chay 100 episode.")
    print("5 reward dau tien:", episode_rewards[:5])

    env.close()
    return episode_rewards


if __name__ == "__main__":
    main()

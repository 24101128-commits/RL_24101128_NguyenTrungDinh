"""
Bai 13. Chay 10 episode bang random agent, in bang Episode | Reward | Length.
"""

import gymnasium as gym
from bai11 import random_agent


def main():
    env = gym.make("CartPole-v1")

    print(f"{'Episode':<10}{'Reward':<10}{'Length':<10}")
    for ep in range(10):
        total_reward, length = random_agent(env)
        print(f"{ep:<10}{total_reward:<10}{length:<10}")

    env.close()


if __name__ == "__main__":
    main()

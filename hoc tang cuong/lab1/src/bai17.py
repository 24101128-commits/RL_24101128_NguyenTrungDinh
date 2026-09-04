"""
Bai 17. Ve bieu do reward theo episode bang Matplotlib, luu vao
Lab01/figures/reward_cartpole.png
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import gymnasium as gym
from bai11 import random_agent

FIGURES_DIR = os.path.join(os.path.dirname(__file__), "..", "figures")


def main():
    env = gym.make("CartPole-v1")

    episode_rewards = []
    for ep in range(100):
        total_reward, length = random_agent(env)
        episode_rewards.append(total_reward)
    env.close()

    plt.figure(figsize=(8, 5))
    plt.plot(episode_rewards)
    plt.title("Reward theo Episode - CartPole-v1 (Random Agent)")
    plt.xlabel("Episode")
    plt.ylabel("Total reward")
    plt.grid(True)

    os.makedirs(FIGURES_DIR, exist_ok=True)
    out_path = os.path.join(FIGURES_DIR, "reward_cartpole.png")
    plt.savefig(out_path)
    print("Da luu bieu do tai:", out_path)


if __name__ == "__main__":
    main()

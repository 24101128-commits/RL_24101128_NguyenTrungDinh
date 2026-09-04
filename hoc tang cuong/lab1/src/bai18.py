"""
Bai 18. Tinh moving average (window_size=10) khong dung Pandas.
Ve dong thoi reward goc va moving average, luu vao
Lab01/figures/moving_average.png
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import gymnasium as gym
from bai11 import random_agent

FIGURES_DIR = os.path.join(os.path.dirname(__file__), "..", "figures")


def moving_average(values, window_size):
    values = np.asarray(values, dtype=float)
    result = []
    for i in range(len(values)):
        start = max(0, i - window_size + 1)
        result.append(values[start:i + 1].mean())
    return np.array(result)


def main():
    env = gym.make("CartPole-v1")

    episode_rewards = []
    for ep in range(100):
        total_reward, length = random_agent(env)
        episode_rewards.append(total_reward)
    env.close()

    ma = moving_average(episode_rewards, window_size=10)

    plt.figure(figsize=(8, 5))
    plt.plot(episode_rewards, label="Reward goc", alpha=0.5)
    plt.plot(ma, label="Moving average (window=10)", linewidth=2)
    plt.title("Reward va Moving Average - CartPole-v1")
    plt.xlabel("Episode")
    plt.ylabel("Total reward")
    plt.legend()
    plt.grid(True)

    os.makedirs(FIGURES_DIR, exist_ok=True)
    out_path = os.path.join(FIGURES_DIR, "moving_average.png")
    plt.savefig(out_path)
    print("Da luu bieu do tai:", out_path)


if __name__ == "__main__":
    main()

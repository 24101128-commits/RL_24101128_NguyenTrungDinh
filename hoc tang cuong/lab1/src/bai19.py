"""
Bai 19. Chay env.reset(seed=42) 10 lan tren 10 environment doc lap,
ghi lai initial observation va kiem tra chung co giong nhau khong.
"""

import gymnasium as gym
import numpy as np


def main():
    observations = []
    for i in range(10):
        env = gym.make("CartPole-v1")
        observation, info = env.reset(seed=42)
        observations.append(observation)
        env.close()

    all_same = all(np.allclose(observations[0], obs) for obs in observations)
    print("Cac observation:")
    for i, obs in enumerate(observations):
        print(f"  [{i}] {obs}")
    print("Tat ca giong nhau:", all_same)

    # Ket luan:
    # Voi cung mot seed=42, moi environment doc lap deu tra ve cung mot
    # initial observation. Dieu nay chung to seed dieu khien bo sinh so
    # ngau nhien noi bo cua environment, giup thi nghiem co the tai lap.
    # Neu khong dat seed, moi lan reset() se cho observation khac nhau.


if __name__ == "__main__":
    main()

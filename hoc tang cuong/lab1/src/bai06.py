"""
Bai 06. Sinh 20 action ngau nhien, luu vao list, in danh sach
va tinh tan suat xuat hien cua tung action.
"""

import gymnasium as gym
from collections import Counter


def main():
    env = gym.make("CartPole-v1")
    env.reset(seed=42)

    actions = [env.action_space.sample() for _ in range(20)]
    print("Danh sach 20 action:", actions)

    frequency = Counter(actions)
    print("Tan suat xuat hien:")
    for action, count in sorted(frequency.items()):
        print(f"  action={action}: {count} lan")

    env.close()


if __name__ == "__main__":
    main()

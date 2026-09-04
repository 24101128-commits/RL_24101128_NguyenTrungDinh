"""
Bai 03. Kham pha action_space cua CartPole-v1.
So action duoc xac dinh tu env.action_space.n, khong gan cung bang hang so.
"""

import gymnasium as gym


def main():
    env = gym.make("CartPole-v1")
    print("Action space:", env.action_space)

    num_actions = env.action_space.n
    print("Number of actions:", num_actions)

    env.close()


if __name__ == "__main__":
    main()

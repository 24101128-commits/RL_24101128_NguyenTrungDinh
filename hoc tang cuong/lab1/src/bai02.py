"""
Bai 02. Tao moi truong CartPole-v1, in doi tuong env, roi dong moi truong.
"""

import gymnasium as gym


def main():
    env = gym.make("CartPole-v1")
    print(env)
    env.close()


if __name__ == "__main__":
    main()

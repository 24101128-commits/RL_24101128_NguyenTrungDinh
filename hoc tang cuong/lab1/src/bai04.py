"""
Bai 04. Kham pha observation_space cua CartPole-v1: shape, dtype, low, high.
"""

import gymnasium as gym


def main():
    env = gym.make("CartPole-v1")
    obs_space = env.observation_space
    print("Observation space:", obs_space)

    print("Shape:", obs_space.shape)
    print("Dtype:", obs_space.dtype)
    print("Low:", obs_space.low)
    print("High:", obs_space.high)

    env.close()


if __name__ == "__main__":
    main()

"""
Bai 10. Mo rong Bai 09: cong don total_reward, in episode length va total reward.
"""

import gymnasium as gym


def main():
    env = gym.make("CartPole-v1")
    observation, info = env.reset(seed=42)

    total_reward = 0.0
    length = 0

    for t in range(20):
        action = env.action_space.sample()
        observation, reward, terminated, truncated, info = env.step(action)
        total_reward += reward
        length += 1
        if terminated or truncated:
            break

    print("Episode length:", length)
    print("Total reward:", total_reward)

    env.close()


if __name__ == "__main__":
    main()

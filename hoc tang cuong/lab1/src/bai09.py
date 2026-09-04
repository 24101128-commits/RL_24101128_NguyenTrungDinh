"""
Bai 09. Chay toi da 20 timestep, in t, action, reward moi buoc.
Dung ngay khi terminated or truncated.
"""

import gymnasium as gym


def main():
    env = gym.make("CartPole-v1")
    observation, info = env.reset(seed=42)

    for t in range(20):
        action = env.action_space.sample()
        observation, reward, terminated, truncated, info = env.step(action)
        print(f"t={t}, action={action}, reward={reward}")
        if terminated or truncated:
            print("Episode ket thuc som.")
            break

    env.close()


if __name__ == "__main__":
    main()

"""
Bai 08. Ham run_one_step(env, action) tra ve day du 5 gia tri cua API moi.
Kiem thu voi it nhat 5 action.
"""

import gymnasium as gym


def run_one_step(env, action):
    observation, reward, terminated, truncated, info = env.step(action)
    return observation, reward, terminated, truncated, info


def main():
    env = gym.make("CartPole-v1")
    env.reset(seed=42)

    for i in range(5):
        action = env.action_space.sample()
        observation, reward, terminated, truncated, info = run_one_step(env, action)
        print(f"[{i}] action={action}, reward={reward}, "
              f"terminated={terminated}, truncated={truncated}")
        if terminated or truncated:
            env.reset(seed=42 + i)

    env.close()


if __name__ == "__main__":
    main()

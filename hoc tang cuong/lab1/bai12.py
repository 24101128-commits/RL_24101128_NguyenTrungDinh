"""
Bai 12. Viet lai random agent nhung KHONG nhan bien done tu API cu.
Tu tao episode_finished = terminated or truncated,
va in ro nguyen nhan episode ket thuc (Termination / Truncation).
"""

import gymnasium as gym


def random_agent_v2(env, max_steps=500):
    observation, info = env.reset()
    total_reward = 0.0
    length = 0
    terminated = False
    truncated = False

    for _ in range(max_steps):
        action = env.action_space.sample()
        observation, reward, terminated, truncated, info = env.step(action)
        total_reward += reward
        length += 1

        episode_finished = terminated or truncated
        if episode_finished:
            break

    return total_reward, length, terminated, truncated


def main():
    env = gym.make("CartPole-v1")
    total_reward, length, terminated, truncated = random_agent_v2(env)

    print("Total reward:", total_reward)
    print("Episode length:", length)

    if terminated:
        print("Nguyen nhan ket thuc: Termination")
    if truncated:
        print("Nguyen nhan ket thuc: Truncation")

    env.close()


if __name__ == "__main__":
    main()

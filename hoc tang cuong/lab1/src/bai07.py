"""
Bai 07. Thuc hien dung 1 buoc tuong tac voi CartPole va in day du thong tin.
"""

import gymnasium as gym


def main():
    env = gym.make("CartPole-v1")
    state_before, info = env.reset(seed=42)
    print("State before action:", state_before)

    action = env.action_space.sample()
    print("Action:", action)

    state_after, reward, terminated, truncated, info = env.step(action)
    print("State after action:", state_after)
    print("Reward:", reward)
    print("Terminated:", terminated)
    print("Truncated:", truncated)
    print("Info:", info)

    env.close()


if __name__ == "__main__":
    main()

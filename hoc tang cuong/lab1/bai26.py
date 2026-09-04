"""
Bai 26. Tu xay dung chuoi action dua agent tu Start toi Goal tren
FrozenLake 4x4 mac dinh (is_slippery=False).

Ban do mac dinh:
SFFF
FHFH
FFFH
HFFG

Chuoi action: RIGHT, RIGHT, DOWN, DOWN, DOWN, RIGHT (0-based: LEFT=0 DOWN=1 RIGHT=2 UP=3)
"""

import gymnasium as gym

ACTION_NAMES = {0: "LEFT", 1: "DOWN", 2: "RIGHT", 3: "UP"}


def main():
    env = gym.make("FrozenLake-v1", is_slippery=False, render_mode="ansi")
    observation, info = env.reset(seed=42)
    print(env.render())

    actions = [2, 2, 1, 1, 1, 2]  # RIGHT, RIGHT, DOWN, DOWN, DOWN, RIGHT

    for action in actions:
        observation, reward, terminated, truncated, info = env.step(action)
        print(f"Action: {ACTION_NAMES[action]} -> state={observation}, reward={reward}")
        print(env.render())
        if terminated or truncated:
            break

    env.close()


if __name__ == "__main__":
    main()

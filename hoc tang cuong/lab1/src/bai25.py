"""
Bai 25. Anh xa y nghia cac action trong FrozenLake: 0=LEFT, 1=DOWN, 2=RIGHT, 3=UP
(theo tai lieu chinh thuc cua Gymnasium FrozenLake).
"""

import gymnasium as gym

ACTION_NAMES = {
    0: "LEFT",
    1: "DOWN",
    2: "RIGHT",
    3: "UP",
}


def main():
    env = gym.make("FrozenLake-v1", is_slippery=False)
    env.reset(seed=42)

    action = env.action_space.sample()
    print(f"Action {action} -> {ACTION_NAMES[action]}")

    env.close()


if __name__ == "__main__":
    main()

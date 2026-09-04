"""
Bai 24. Hien thi FrozenLake dang text (render_mode="ansi").
"""

import gymnasium as gym


def main():
    env = gym.make("FrozenLake-v1", is_slippery=False, render_mode="ansi")
    observation, info = env.reset(seed=42)

    text = env.render()
    print(text)
    # Quan sat: S = Start, F = Frozen (di duoc), H = Hole (roi xuong ho, thua),
    # G = Goal (dich, thang).

    env.close()


if __name__ == "__main__":
    main()

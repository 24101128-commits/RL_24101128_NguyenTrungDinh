"""
Bai 05. Quan sat trang thai ban dau cua CartPole-v1 sau reset(seed=42).

Comment mo ta kieu du lieu cua tung phan tu observation:
    observation[0] -> cart position   (float, vi tri xe tren truc x)
    observation[1] -> cart velocity   (float, van toc xe)
    observation[2] -> pole angle      (float, goc nghieng cua thanh, radian)
    observation[3] -> pole angular velocity (float, van toc goc cua thanh)
"""

import gymnasium as gym


def main():
    env = gym.make("CartPole-v1")
    observation, info = env.reset(seed=42)

    print("Observation:", observation)
    print("Type:", type(observation))
    print("Shape:", observation.shape)
    print("Info:", info)

    env.close()


if __name__ == "__main__":
    main()

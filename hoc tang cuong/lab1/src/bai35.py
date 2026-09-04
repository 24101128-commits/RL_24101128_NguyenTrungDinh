"""
Bai 35. So sanh 3 agent tren CartPole-v1: Random, Angle-based, Improved.
Moi agent chay it nhat 500 episode. In bang thong ke va ve bieu do so sanh
mean reward, luu vao Lab01/figures/comparison_agents.png.
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from bai34 import evaluate_policy
from bai33 import random_policy

FIGURES_DIR = os.path.join(os.path.dirname(__file__), "..", "figures")


def angle_based_policy(observation, env):
    pole_angle = observation[2]
    return 1 if pole_angle > 0 else 0


def improved_policy(observation, env):
    pole_angle = observation[2]
    pole_angular_velocity = observation[3]
    predicted_angle = pole_angle + 0.5 * pole_angular_velocity
    return 1 if predicted_angle > 0 else 0


def main():
    n_episodes = 500

    agents = {
        "Random": random_policy,
        "Angle-based": angle_based_policy,
        "Improved": improved_policy,
    }

    results = {}
    for name, policy_fn in agents.items():
        stats = evaluate_policy("CartPole-v1", policy_fn, n_episodes=n_episodes, seed=42)
        results[name] = stats

    print(f"{'Agent':<15}{'Mean reward':<14}{'Std':<10}{'Min':<8}{'Max':<8}{'Mean length':<12}")
    for name, stats in results.items():
        print(f"{name:<15}{stats['mean_reward']:<14.2f}{stats['std_reward']:<10.2f}"
              f"{stats['min_reward']:<8.2f}{stats['max_reward']:<8.2f}{stats['mean_length']:<12.2f}")

    names = list(results.keys())
    means = [results[name]["mean_reward"] for name in names]

    plt.figure(figsize=(7, 5))
    plt.bar(names, means, color=["gray", "steelblue", "seagreen"])
    plt.title("So sanh Mean Reward giua 3 Agent - CartPole-v1")
    plt.xlabel("Agent")
    plt.ylabel("Mean reward")
    plt.grid(True, axis="y")

    os.makedirs(FIGURES_DIR, exist_ok=True)
    out_path = os.path.join(FIGURES_DIR, "comparison_agents.png")
    plt.savefig(out_path)
    print("Da luu bieu do tai:", out_path)

    # Nhan xet:
    # 1. Random agent co mean reward thap nhat vi khong su dung bat ky
    #    thong tin nao tu observation, hanh dong hoan toan ngau nhien.
    # 2. Angle-based agent (chi dung pole_angle) cai thien dang ke so voi
    #    random, vi no phan ung truc tiep voi chieu nghieng hien tai cua pole.
    # 3. Improved agent (dung ca pole_angle va pole_angular_velocity) cho
    #    ket qua tot nhat, thuong dat gan hoac bang reward toi da (500),
    #    vi no du doan duoc xu huong nghieng trong tuong lai gan thay vi
    #    chi phan ung voi trang thai hien tai.
    # 4. Ket qua nay minh hoa nguyen tac co ban cua RL: mot policy tot hon
    #    (khai thac nhieu thong tin tu observation hon) se cho hieu suat
    #    (reward trung binh) cao hon mot policy ngau nhien.
    # 5. Do lech chuan (std) cua random agent cung lon hon, cho thay hieu
    #    suat cua no khong on dinh giua cac episode.


if __name__ == "__main__":
    main()

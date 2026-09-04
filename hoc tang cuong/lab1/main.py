"""
Bai 36 - Mini project: pipeline Agent-Environment hoan chinh cho CartPole-v1.

Cau truc: create_environment() -> policy() -> run_episode() ->
evaluate_policy() -> plot_results() -> main()
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import gymnasium as gym

FIGURES_DIR = os.path.join(os.path.dirname(__file__), "..", "figures")
ENV_NAME = "CartPole-v1"
N_EPISODES = 500
SEED = 42


def create_environment(env_name=ENV_NAME):
    """Tao va tra ve mot moi truong Gymnasium."""
    env = gym.make(env_name)
    return env


def policy(observation, env):
    """
    Policy cai tien cho CartPole: ket hop pole_angle va
    pole_angular_velocity de du doan huong nghieng trong tuong lai gan.
    """
    pole_angle = observation[2]
    pole_angular_velocity = observation[3]
    predicted_angle = pole_angle + 0.5 * pole_angular_velocity
    return 1 if predicted_angle > 0 else 0


def run_episode(env, policy_fn, seed=None, max_steps=1000):
    """Chay 1 episode hoan chinh, tra ve dict ket qua."""
    if seed is not None:
        observation, info = env.reset(seed=seed)
    else:
        observation, info = env.reset()

    total_reward = 0.0
    length = 0
    terminated = False
    truncated = False

    for _ in range(max_steps):
        action = policy_fn(observation, env)
        observation, reward, terminated, truncated, info = env.step(action)
        total_reward += reward
        length += 1
        if terminated or truncated:
            break

    return {
        "reward": total_reward,
        "length": length,
        "terminated": terminated,
        "truncated": truncated,
    }


def evaluate_policy(env, policy_fn, n_episodes=N_EPISODES, seed=SEED, max_steps=1000):
    """Chay nhieu episode va tong hop thong ke."""
    rewards = []
    lengths = []

    for ep in range(n_episodes):
        result = run_episode(env, policy_fn, seed=seed + ep, max_steps=max_steps)
        rewards.append(result["reward"])
        lengths.append(result["length"])

    rewards = np.array(rewards)
    lengths = np.array(lengths)

    stats = {
        "mean_reward": float(rewards.mean()),
        "std_reward": float(rewards.std()),
        "min_reward": float(rewards.min()),
        "max_reward": float(rewards.max()),
        "mean_length": float(lengths.mean()),
        "best_episode": int(np.argmax(rewards)),
        "worst_episode": int(np.argmin(rewards)),
        "rewards": rewards,
        "lengths": lengths,
    }
    return stats


def moving_average(values, window_size=10):
    values = np.asarray(values, dtype=float)
    result = []
    for i in range(len(values)):
        start = max(0, i - window_size + 1)
        result.append(values[start:i + 1].mean())
    return np.array(result)


def plot_results(rewards, out_dir=FIGURES_DIR):
    """Ve reward theo episode va moving average, luu vao figures/."""
    os.makedirs(out_dir, exist_ok=True)
    ma = moving_average(rewards, window_size=10)

    plt.figure(figsize=(8, 5))
    plt.plot(rewards, alpha=0.4, label="Reward moi episode")
    plt.plot(ma, linewidth=2, label="Moving average (window=10)")
    plt.title(f"Mini-project: Reward theo Episode - {ENV_NAME}")
    plt.xlabel("Episode")
    plt.ylabel("Total reward")
    plt.legend()
    plt.grid(True)

    out_path = os.path.join(out_dir, "mini_project_rewards.png")
    plt.savefig(out_path)
    print("Da luu bieu do tai:", out_path)


def main():
    env = create_environment(ENV_NAME)

    stats = evaluate_policy(env, policy, n_episodes=N_EPISODES, seed=SEED)

    print(f"So episode         : {N_EPISODES}")
    print(f"Mean reward         : {stats['mean_reward']:.2f}")
    print(f"Std reward          : {stats['std_reward']:.2f}")
    print(f"Min reward          : {stats['min_reward']:.2f}")
    print(f"Max reward          : {stats['max_reward']:.2f}")
    print(f"Mean episode length : {stats['mean_length']:.2f}")
    print(f"Episode tot nhat    : {stats['best_episode']} (reward={stats['rewards'][stats['best_episode']]:.2f})")
    print(f"Episode te nhat     : {stats['worst_episode']} (reward={stats['rewards'][stats['worst_episode']]:.2f})")

    plot_results(stats["rewards"])

    env.close()

    # Ket luan:
    # Policy heuristic ket hop pole_angle va pole_angular_velocity dat
    # mean reward rat cao (gan hoac bang muc toi da 500) va do lech
    # chuan rat thap, cho thay day la mot policy on dinh hon nhieu so
    # voi random policy da khao sat o cac bai truoc. Pipeline nay
    # (create_environment -> policy -> run_episode -> evaluate_policy ->
    # plot_results) la nen tang de mo rong sang cac thuat toan RL
    # chinh thuc (Q-Learning, SARSA, DQN...) trong cac bai sau.


if __name__ == "__main__":
    main()

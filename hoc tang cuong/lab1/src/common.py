"""
common.py
---------
Module tien ich dung chung cho cac bai tap trong Lab01.
Chua cac ham lap lai nhieu lan: random_policy, run_one_step,
run_episode, moving_average, evaluate_policy, experiment.

Sinh vien co the import cac ham nay trong tung bai (bai08, bai11, ...)
de tranh copy-paste code, nhung moi bai van duoc yeu cau chay doc lap
duoc (python src/baiXX.py).
"""

import numpy as np


def random_policy(observation, env):
    """Policy ngau nhien: khong quan tam observation, chi sample action."""
    return env.action_space.sample()


def run_one_step(env, action):
    """Thuc hien dung 1 buoc tuong tac va tra ve day du 5 gia tri cua API moi."""
    observation, reward, terminated, truncated, info = env.step(action)
    return observation, reward, terminated, truncated, info


def run_episode(env, policy, seed=None, max_steps=1000):
    """
    Chay 1 episode hoan chinh voi mot policy bat ky.

    policy: ham nhan (observation, env) -> action
    Ham nay khong phu thuoc rieng vao CartPole, co the dung cho
    bat ky moi truong Gymnasium nao (CartPole, FrozenLake, Taxi, ...).
    """
    if seed is not None:
        observation, info = env.reset(seed=seed)
    else:
        observation, info = env.reset()

    total_reward = 0.0
    length = 0
    terminated = False
    truncated = False

    for _ in range(max_steps):
        action = policy(observation, env)
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


def moving_average(values, window_size):
    """Tinh moving average don gian, khong dung Pandas."""
    values = np.asarray(values, dtype=float)
    if window_size <= 1:
        return values.copy()
    result = []
    for i in range(len(values)):
        start = max(0, i - window_size + 1)
        window = values[start:i + 1]
        result.append(window.mean())
    return np.array(result)


def evaluate_policy(env_name, policy, n_episodes=100, seed=42, max_steps=1000, env_kwargs=None):
    """
    Danh gia mot policy tren mot moi truong Gymnasium bang cach chay
    nhieu episode va tong hop thong ke.
    """
    import gymnasium as gym

    env_kwargs = env_kwargs or {}
    env = gym.make(env_name, **env_kwargs)

    rewards = []
    lengths = []
    for ep in range(n_episodes):
        result = run_episode(env, policy, seed=seed + ep, max_steps=max_steps)
        rewards.append(result["reward"])
        lengths.append(result["length"])

    env.close()

    rewards = np.array(rewards)
    lengths = np.array(lengths)

    return {
        "mean_reward": float(rewards.mean()),
        "std_reward": float(rewards.std()),
        "min_reward": float(rewards.min()),
        "max_reward": float(rewards.max()),
        "mean_length": float(lengths.mean()),
        "rewards": rewards,
        "lengths": lengths,
    }


def experiment(seed, n_episodes, env_name="CartPole-v1", policy=None, max_steps=1000):
    """Chay mot thi nghiem hoan chinh voi mot seed cu the va tra ve dict thong ke."""
    import gymnasium as gym

    if policy is None:
        policy = random_policy

    env = gym.make(env_name)
    rewards = []
    for ep in range(n_episodes):
        result = run_episode(env, policy, seed=seed + ep, max_steps=max_steps)
        rewards.append(result["reward"])
    env.close()

    rewards = np.array(rewards)
    return {
        "seed": seed,
        "mean_reward": float(rewards.mean()),
        "std_reward": float(rewards.std()),
        "max_reward": float(rewards.max()),
        "min_reward": float(rewards.min()),
    }

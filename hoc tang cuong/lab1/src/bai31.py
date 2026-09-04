"""
Bai 31. Policy heuristic dua tren goc nghieng cua pole (observation[2]).
Neu goc > 0 (nghieng phai) -> day xe sang phai; nguoc lai day sang trai.
So sanh voi random policy.
"""

import gymnasium as gym
import numpy as np


def angle_based_policy(observation):
    pole_angle = observation[2]
    if pole_angle > 0:
        return 1  # day sang phai
    else:
        return 0  # day sang trai


def random_policy(observation, env):
    return env.action_space.sample()


def run_policy(policy_fn, n_episodes=100, needs_env=False):
    env = gym.make("CartPole-v1")
    rewards = []
    for ep in range(n_episodes):
        observation, info = env.reset(seed=ep)
        total_reward = 0.0
        terminated = False
        truncated = False
        while not (terminated or truncated):
            action = policy_fn(observation, env) if needs_env else policy_fn(observation)
            observation, reward, terminated, truncated, info = env.step(action)
            total_reward += reward
        rewards.append(total_reward)
    env.close()
    return np.array(rewards)


def main():
    angle_rewards = run_policy(angle_based_policy, needs_env=False)
    random_rewards = run_policy(random_policy, needs_env=True)

    print(f"Angle-based mean reward: {angle_rewards.mean():.2f}")
    print(f"Random      mean reward: {random_rewards.mean():.2f}")


if __name__ == "__main__":
    main()

"""
Bai 32. Cai tien heuristic: dung ca pole_angle va pole_angular_velocity.
Muc tieu: mean reward > mean reward cua random policy.
"""

import gymnasium as gym
import numpy as np


def improved_policy(observation):
    pole_angle = observation[2]
    pole_angular_velocity = observation[3]

    # Du doan huong nghieng trong tuong lai gan bang cach cong them
    # mot phan cua van toc goc vao goc hien tai.
    predicted_angle = pole_angle + 0.5 * pole_angular_velocity

    if predicted_angle > 0:
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
    improved_rewards = run_policy(improved_policy, needs_env=False)
    random_rewards = run_policy(random_policy, needs_env=True)

    print(f"Improved mean reward: {improved_rewards.mean():.2f}")
    print(f"Random   mean reward: {random_rewards.mean():.2f}")
    print("Cai tien tot hon random:", improved_rewards.mean() > random_rewards.mean())


if __name__ == "__main__":
    main()

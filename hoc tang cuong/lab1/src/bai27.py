"""
Bai 27. Chay it nhat 100 episode bang random policy tren FrozenLake,
dem so success/failure va tinh success_rate.
"""

import gymnasium as gym


def main():
    env = gym.make("FrozenLake-v1", is_slippery=False)

    n_episodes = 100
    success = 0
    failure = 0

    for ep in range(n_episodes):
        observation, info = env.reset(seed=ep)
        terminated = False
        truncated = False
        total_reward = 0.0
        while not (terminated or truncated):
            action = env.action_space.sample()
            observation, reward, terminated, truncated, info = env.step(action)
            total_reward += reward

        if terminated and total_reward > 0:
            success += 1
        else:
            failure += 1

    env.close()

    success_rate = success / n_episodes
    print("Success:", success)
    print("Failure:", failure)
    print(f"Success rate: {success_rate:.2f}")


if __name__ == "__main__":
    main()

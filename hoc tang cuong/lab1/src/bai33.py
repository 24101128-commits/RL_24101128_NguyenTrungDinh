"""
Bai 33. Ham tong quat run_episode(env, policy, seed=None, max_steps=1000),
khong phu thuoc rieng CartPole. policy nhan (observation, env) -> action.
"""

import gymnasium as gym


def run_episode(env, policy, seed=None, max_steps=1000):
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


def random_policy(observation, env):
    return env.action_space.sample()


def main():
    env = gym.make("CartPole-v1")
    result = run_episode(env, random_policy, seed=42)
    print(result)
    env.close()

    env2 = gym.make("FrozenLake-v1", is_slippery=False)
    result2 = run_episode(env2, random_policy, seed=42)
    print(result2)
    env2.close()


if __name__ == "__main__":
    main()

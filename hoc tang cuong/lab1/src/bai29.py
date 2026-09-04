"""
Bai 29. Viet policy(observation) dang ham, ban dau chi tra ve action ngau nhien.
Thay the env.action_space.sample() truc tiep bang policy(observation) trong agent.
"""

import gymnasium as gym

_ENV_FOR_SAMPLING = None


def policy(observation):
    """Policy ngau nhien: dung mot bien toan cuc de goi action_space.sample()."""
    global _ENV_FOR_SAMPLING
    return _ENV_FOR_SAMPLING.action_space.sample()


def run_agent_with_policy(env, max_steps=500):
    global _ENV_FOR_SAMPLING
    _ENV_FOR_SAMPLING = env

    observation, info = env.reset()
    total_reward = 0.0
    length = 0

    for _ in range(max_steps):
        action = policy(observation)
        observation, reward, terminated, truncated, info = env.step(action)
        total_reward += reward
        length += 1
        if terminated or truncated:
            break

    return total_reward, length


def main():
    env = gym.make("CartPole-v1")
    total_reward, length = run_agent_with_policy(env)
    print("Total reward:", total_reward)
    print("Episode length:", length)
    env.close()


if __name__ == "__main__":
    main()

import gymnasium as gym

env = gym.make("CartPole-v1", render_mode="human")

obs, info = env.reset()

for step in range(500):

    action = env.action_space.sample()

    obs, reward, terminated, truncated, info = env.step(action)

    print("Step:", step)
    print("Observation:", obs)
    print("Reward:", reward)

    if terminated or truncated:
        obs, info = env.reset()

env.close
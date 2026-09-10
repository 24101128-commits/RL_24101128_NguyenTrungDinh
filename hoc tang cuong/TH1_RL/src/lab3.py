import gymnasium as gym

# Tạo môi trường CartPole
env = gym.make("CartPole-v1")

# Reset môi trường
obs, info = env.reset()

print("===== CARTPOLE ENVIRONMENT =====")

print("\nAction space:")
print(env.action_space)

print("\nObservation space:")
print(env.observation_space)

print("\nCurrent observation:")
print(obs)

print("\nRandom action:")
print(env.action_space.sample())

# Đóng môi trường
env.close()
import gymnasium as gym

# Tạo môi trường
env = gym.make("Blackjack-v1")
# Reset môi trường
observation, info = env.reset()
# In thông tin
print("Observation:", observation)
print("Info:", info)
print("Observation Space:", env.observation_space)
print("Action Space:", env.action_space)
# Đóng môi trường
env.close()
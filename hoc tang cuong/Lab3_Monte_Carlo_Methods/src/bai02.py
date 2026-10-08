import gymnasium as gym

# Tạo môi trường Blackjack
env = gym.make("Blackjack-v1")
# In thông tin về observation
print("Observation Space:", env.observation_space)
print()
# In 10 observation từ 10 episode khác nhau
print("10 Observation:")
print("-" * 40)

for i in range(10):
    observation, info = env.reset()
    player_sum, dealer_card, usable_ace = observation

    print(f"Episode {i + 1}:")
    print(f"  Observation: {observation}")
    print(f"  Player sum: {player_sum}")
    print(f"  Dealer showing card: {dealer_card}")
    print(f"  Usable ace: {usable_ace}")
    print()
# Đóng môi trường
env.close()
import gymnasium as gym

# Tạo môi trường Blackjack
env = gym.make("Blackjack-v1")
# Reset môi trường
state, info = env.reset()
print("Random Episode")
print("=" * 50)
step = 0

while True:
    # Chọn action ngẫu nhiên
    action = env.action_space.sample()
    # Thực hiện action
    next_state, reward, terminated, truncated, info = env.step(action)
    # In thông tin của bước hiện tại
    print(f"Step {step + 1}:")
    print(f"  State: {state}")
    print(f"  Action: {action}")
    print(f"  Reward: {reward}")
    print(f"  Next State: {next_state}")
    print(f"  Terminated: {terminated}")
    print(f"  Truncated: {truncated}")
    print()
    # Cập nhật state
    state = next_state
    step += 1
    # Kiểm tra episode đã kết thúc chưa
    if terminated or truncated:
        break
# Đóng môi trường
env.close()
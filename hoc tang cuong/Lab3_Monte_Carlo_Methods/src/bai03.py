import gymnasium as gym

# Tạo môi trường Blackjack
env = gym.make("Blackjack-v1")
# In action space
print("Action Space:", env.action_space)
print()
# Tạo dictionary mô tả action
ACTION_NAMES = {
    0: "Stick",
    1: "Hit"
}
# In ý nghĩa của từng action
print("Action Names:")
print("-" * 40)

for action, name in ACTION_NAMES.items():
    print(f"Action {action}: {name}")
# Đóng môi trường
env.close()
import gymnasium as gym

def generate_episode(env, policy, seed=None):
    """
    Tạo một episode bằng policy.

    Parameters:
        env: Gymnasium environment
        policy: hàm nhận state và trả về action
        seed: seed dùng để reset environment

    Returns:
        episode: danh sách các tuple
                  (state, action, reward)
    """

    # Reset environment
    state, info = env.reset(seed=seed)
    # Danh sách lưu episode
    episode = []
    while True:
        # Chọn action theo policy
        action = policy(state)
        # Thực hiện action
        next_state, reward, terminated, truncated, info = env.step(action)
        # Lưu state, action, reward
        episode.append((state, action, reward))
        # Cập nhật state
        state = next_state
        # Episode kết thúc
        if terminated or truncated:
            break

    return episode

def random_policy(state):
    """
    Chọn action ngẫu nhiên.
    """
    return env.action_space.sample()

env = gym.make("Blackjack-v1")

# Sinh một episode
episode = generate_episode(
    env,
    random_policy,
    seed=42
)

# In episode
print("Episode:")
print("=" * 50)

for i, (state, action, reward) in enumerate(episode):
    print(f"Step {i + 1}:")
    print(f"  State: {state}")
    print(f"  Action: {action}")
    print(f"  Reward: {reward}")
    print()

# Độ dài episode
print("Episode length:", len(episode))

env.close()
import gymnasium as gym

def generate_episode(env, policy, seed=None):
    """
    Generate one complete episode.
    Returns a list of (state, action, reward).
    """
    state, info = env.reset(seed=seed)
    episode = []
    while True:
        action = policy(state)
        next_state, reward, terminated, truncated, info = env.step(action)

        episode.append((state, action, reward))

        state = next_state

        if terminated or truncated:
            break

    return episode

def random_policy(env):
    def policy(state):
        return env.action_space.sample()

    return policy

env = gym.make("Blackjack-v1")
policy = random_policy(env)
episode = generate_episode(env, policy, seed=42)

# Lấy reward từ episode
rewards = [reward for state, action, reward in episode]

print("Episode:")
print("=" * 50)

for i, reward in enumerate(rewards):
    print(f"Step {i + 1}: Reward = {reward}")
    print()
    print("Reward sequence:", rewards)

env.close()
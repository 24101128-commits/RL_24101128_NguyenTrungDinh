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

def compute_returns(rewards, gamma=1.0):
    """
    Calculate returns for all time steps.
    """
    returns = []
    for t in range(len(rewards)):
        G = 0
        for k in range(t, len(rewards)):
            G += (gamma ** (k - t)) * rewards[k]
        returns.append(G)
    return returns


env = gym.make("Blackjack-v1")
policy = random_policy(env)
episode = generate_episode(env, policy, seed=42)
# Lấy rewards
rewards = [reward for state, action, reward in episode]
# Tính returns
returns = compute_returns(rewards, gamma=1.0)
# Gắn return vào episode
episode_with_returns = []

for (state, action, reward), G in zip(episode, returns):
    episode_with_returns.append((state, action, reward, G))

print("Episode with Returns:")
print("=" * 60)

for i, (state, action, reward, G) in enumerate(episode_with_returns):
    print(f"Step {i + 1}:")
    print(f"  State: {state}")
    print(f"  Action: {action}")
    print(f"  Reward: {reward}")
    print(f"  Return: {G}")
    print()

env.close()
import gymnasium as gym

def stick_on_20_policy(state):
    """
    Stick when player sum is 20 or more.
    Otherwise, hit.
    """
    player_sum, dealer_card, usable_ace = state
    if player_sum >= 20:
        return 0
    else:
        return 1

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

env = gym.make("Blackjack-v1")

episode = generate_episode(
    env,
    stick_on_20_policy,
    seed=42
)

print("Episode:")
print("=" * 50)

for i, (state, action, reward) in enumerate(episode):
    print(f"Step {i + 1}:")
    print(f"  State: {state}")
    print(f"  Action: {action}")
    print(f"  Reward: {reward}")
    print()

env.close()
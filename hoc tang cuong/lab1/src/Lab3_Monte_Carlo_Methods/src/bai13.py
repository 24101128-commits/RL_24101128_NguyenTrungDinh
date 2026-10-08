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
state_returns = {}

# Sinh 100 episode
for episode_number in range(100):
    episode = generate_episode(
        env,
        stick_on_20_policy,
        seed=episode_number
    )
    rewards = [reward for state, action, reward in episode]
    returns = compute_returns(rewards, gamma=1.0)
    for (state, action, reward), G in zip(episode, returns):
        if state not in state_returns:
            state_returns[state] = []
        state_returns[state].append(G)

V = {}
for state, returns in state_returns.items():
    V[state] = sum(returns) / len(returns)

print("Number of episodes:", 100)
print("Number of states:", len(V))
print()
print("Sample state values:")
print("=" * 50)

count = 0

for state, value in V.items():
    print(f"State: {state}")
    print(f"V(s): {value:.4f}")
    print()
    count += 1
    if count >= 10:
        break

env.close()
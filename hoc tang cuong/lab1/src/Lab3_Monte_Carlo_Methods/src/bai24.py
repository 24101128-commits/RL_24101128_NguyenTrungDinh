import gymnasium as gym

def stick_on_20_policy(state):
    player_sum, dealer_card, usable_ace = state
    if player_sum >= 20:
        return 0
    else:
        return 1

def generate_episode(env, policy, seed=None):
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
    returns = []
    for t in range(len(rewards)):
        G = 0
        for k in range(t, len(rewards)):
            G += (gamma ** (k - t)) * rewards[k]
        returns.append(G)

    return returns

env = gym.make("Blackjack-v1")
num_episodes = 1000
gamma = 1.0
state_action_returns = {}

for episode_number in range(num_episodes):
    episode = generate_episode(
        env,
        stick_on_20_policy,
        seed=episode_number
    )
    rewards = [
        reward
        for state, action, reward in episode
    ]
    returns = compute_returns(
        rewards,
        gamma
    )
    for (state, action, reward), G in zip(
        episode,
        returns
    ):
        state_action = (state, action)
        if state_action not in state_action_returns:
            state_action_returns[state_action] = []
        state_action_returns[state_action].append(G)

Q = {}

for state_action, returns in state_action_returns.items():
    Q[state_action] = sum(returns) / len(returns)

print("State-Action Returns")
print("=" * 50)
print("Number of episodes:", num_episodes)
print("Number of state-action pairs:", len(Q))
print()
print("Sample Q(s,a) values:")
print("=" * 50)

count = 0

for (state, action), value in Q.items():
    print(f"State: {state}")
    print(f"Action: {action}")
    print(f"Q(s,a): {value:.4f}")
    print()
    count += 1
    if count >= 10:
        break

env.close()
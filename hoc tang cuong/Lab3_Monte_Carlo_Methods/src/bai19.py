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


def first_visit_mc_prediction(env, policy, num_episodes, gamma=1.0):
    state_returns = {}
    for episode_number in range(num_episodes):
        episode = generate_episode(
            env,
            policy,
            seed=episode_number
        )
        rewards = [
            reward
            for state, action, reward in episode
        ]
        returns = compute_returns(rewards, gamma)
        visited_states = set()
        for (state, action, reward), G in zip(
            episode, returns
        ):
            if state in visited_states:
                continue
            visited_states.add(state)
            if state not in state_returns:
                state_returns[state] = []
            state_returns[state].append(G)

    V = {}

    for state, returns in state_returns.items():
        V[state] = sum(returns) / len(returns)

    return V

env = gym.make("Blackjack-v1")

V = first_visit_mc_prediction(
    env,
    stick_on_20_policy,
    num_episodes=50000,
    gamma=1.0
)

print("First-Visit MC Prediction")
print("=" * 50)
print("Number of episodes: 50000")
print("Number of states:", len(V))
print()
print("Sample state values:")
print("=" * 50)

sample_states = [
    (20, 10, 0),
    (19, 10, 0),
    (18, 10, 0),
    (17, 10, 0),
    (16, 10, 0),
    (15, 10, 0)
]

for state in sample_states:
    if state in V:
        print(f"State: {state}")
        print(f"V(s): {V[state]:.4f}")
    else:
        print(f"State: {state}")
        print("V(s): Not visited")
        print()

env.close()
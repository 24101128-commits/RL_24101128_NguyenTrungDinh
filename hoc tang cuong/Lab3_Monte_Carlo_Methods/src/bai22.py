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
            episode,
            returns
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

def every_visit_mc_prediction(env, policy, num_episodes, gamma=1.0):
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
        for (state, action, reward), G in zip(
            episode,
            returns
        ):
            if state not in state_returns:
                state_returns[state] = []
            state_returns[state].append(G)

    V = {}

    for state, returns in state_returns.items():
        V[state] = sum(returns) / len(returns)

    return V

env = gym.make("Blackjack-v1")
num_episodes = 10000
gamma = 1.0

V_first = first_visit_mc_prediction(
    env,
    stick_on_20_policy,
    num_episodes,
    gamma
)

V_every = every_visit_mc_prediction(
    env,
    stick_on_20_policy,
    num_episodes,
    gamma
)

common_states = set(V_first.keys()) & set(V_every.keys())
differences = []

for state in common_states:
    difference = abs(
        V_first[state] - V_every[state]
    )
    differences.append(difference)
if len(differences) > 0:
    mean_absolute_difference = sum(differences) / len(differences)
else:
    mean_absolute_difference = 0

print("First-Visit vs Every-Visit")
print("=" * 50)
print("Number of episodes:", num_episodes)
print("Gamma:", gamma)
print("Common states:", len(common_states))
print()
print( f"Mean Absolute Difference: "
       f"{mean_absolute_difference:.6f}"
)

env.close()
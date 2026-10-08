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
    rewards = [reward for state, action, reward in episode]
    returns = compute_returns(rewards, gamma)
    for (state, action, reward), G in zip(episode, returns):
        state_action = (state, action)
        if state_action not in state_action_returns:
            state_action_returns[state_action] = []
        state_action_returns[state_action].append(G)

Q = {}

for state_action, returns in state_action_returns.items():
    Q[state_action] = sum(returns) / len(returns)
def greedy_action(Q, state):
    q_values = []
    for action in [0, 1]:
        state_action = (state, action)
        if state_action in Q:
            q_values.append((action, Q[state_action]))
    if len(q_values) == 0:
        return None
    return max(q_values, key=lambda x: x[1])[0]

sample_states = [
    (20, 7, 0),
    (20, 10, 0),
    (19, 10, 0),
    (17, 10, 0),
    (15, 10, 0)
]

print("GREEDY ACTION")
print("=" * 50)

for state in sample_states:
    action = greedy_action(Q, state)
    print("State:", state)
    if action is not None:
        if action == 0:
            action_name = "Stick"
        else:
            action_name = "Hit"
        print("Greedy action:", action)
        print("Action name:", action_name)
    else:
        print("Không có dữ liệu")
        print()

env.close()
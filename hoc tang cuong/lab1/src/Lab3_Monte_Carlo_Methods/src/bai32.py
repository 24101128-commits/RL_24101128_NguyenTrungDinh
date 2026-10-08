import gymnasium as gym
import random

def epsilon_greedy_action(Q, state, epsilon, n_actions=2):
    if random.random() < epsilon:
        return random.randrange(n_actions)
    q_values = []
    for action in range(n_actions):
        state_action = (state, action)
        if state_action in Q:
            q_values.append((action, Q[state_action]))
    if len(q_values) == 0:
        return random.randrange(n_actions)

    return max(q_values, key=lambda x: x[1])[0]

def generate_episode(env, Q, epsilon, seed=None):
    state, info = env.reset(seed=seed)
    episode = []
    while True:
        action = epsilon_greedy_action(
            Q,
            state,
            epsilon,
            env.action_space.n
        )
        next_state, reward, terminated, truncated, info = env.step(action)
        episode.append((state, action, reward))
        state = next_state
        if terminated or truncated:
            break

    return episode

def compute_returns(rewards, gamma=1.0):
    returns = []
    G = 0
    for reward in reversed(rewards):
        G = reward + gamma * G
        returns.insert(0, G)

    return returns

def on_policy_mc_control(
    env,
    num_episodes=10000,
    gamma=1.0,
    epsilon=0.1
):
    Q = {}
    N = {}
    for episode_number in range(num_episodes):
        episode = generate_episode(
            env,
            Q,
            epsilon,
            seed=episode_number
        )
        rewards = [
            reward
            for state, action, reward in episode
        ]
        returns = compute_returns(rewards, gamma)
        visited = set()
        for (state, action, reward), G in zip(
            episode,
            returns
        ):
            state_action = (state, action)
            if state_action in visited:
                continue
            visited.add(state_action)
            N[state_action] = (
                N.get(state_action, 0) + 1
            )
            if state_action not in Q:
                Q[state_action] = 0.0
            Q[state_action] = (
                Q[state_action]
                + (
                    G - Q[state_action]
                ) / N[state_action]
            )
    return Q

env = gym.make("Blackjack-v1")

Q = on_policy_mc_control(
    env,
    num_episodes=10000,
    gamma=1.0,
    epsilon=0.1
)

print("On-policy First-Visit MC Control")
print("=" * 50)
print("Number of state-action pairs:", len(Q))
print()
print("Sample Q(s,a) values:")
print("=" * 50)

count = 0

for (state, action), value in Q.items():
    print("State:", state)
    print("Action:", action)
    print(f"Q(s,a): {value:.4f}")
    print()
    count += 1
    if count >= 10:
        break

env.close()
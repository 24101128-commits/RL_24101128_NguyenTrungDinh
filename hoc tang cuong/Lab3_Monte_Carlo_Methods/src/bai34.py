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

def train_mc_control(
    env,
    num_episodes=100000,
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

def greedy_action(Q, state, n_actions=2):
    q_values = []
    for action in range(n_actions):
        state_action = (state, action)
        if state_action in Q:
            q_values.append(
                (action, Q[state_action])
            )
    if len(q_values) == 0:
        return 0
    return max(
        q_values,
        key=lambda x: x[1]
    )[0]

def evaluate_policy(
    env,
    Q,
    num_episodes=10000
):
    total_reward = 0
    wins = 0
    losses = 0
    draws = 0
    for episode_number in range(num_episodes):
        state, info = env.reset(
            seed=episode_number
        )
        while True:
            action = greedy_action(
                Q,
                state,
                env.action_space.n
            )
            next_state, reward, terminated, truncated, info = env.step(action)
            state = next_state
            if terminated or truncated:
                total_reward += reward
                if reward > 0:
                    wins += 1
                elif reward < 0:
                    losses += 1
                else:
                    draws += 1
                break
    average_reward = total_reward / num_episodes
    win_rate = wins / num_episodes

    return (
        average_reward,
        win_rate,
        wins,
        losses,
        draws
    )

env = gym.make("Blackjack-v1")

Q = train_mc_control(
    env,
    num_episodes=100000,
    gamma=1.0,
    epsilon=0.1
)

num_test_episodes = 10000
average_reward, win_rate, wins, losses, draws = evaluate_policy(
    env,
    Q,
    num_test_episodes
)

print("Evaluate Learned Policy")
print("=" * 50)
print("Training episodes:", 100000)
print("Testing episodes:", num_test_episodes)
print()
print("Average reward:", f"{average_reward:.4f}")
print("Win rate:", f"{win_rate:.4f}")
print()
print("Wins:", wins)
print("Losses:", losses)
print("Draws:", draws)

env.close()
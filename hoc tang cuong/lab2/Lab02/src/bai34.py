import gymnasium as gym
import numpy as np

def evaluate_policy_by_simulation(
    env,
    policy,
    n_episodes=1000,
    seed=42
):
    rewards = []
    lengths = []
    successes = 0
    for episode in range(n_episodes):
        state, info = env.reset(seed=seed + episode)
        total_reward = 0
        for step in range(1000):
            action = policy[state]
            state, reward, terminated, truncated, info = env.step(action)
            total_reward += reward
            if terminated or truncated:
                if reward == 1:
                    successes += 1
                break
        rewards.append(total_reward)
        lengths.append(step + 1)
    return {
        "success_rate": successes / n_episodes,
        "mean_reward": np.mean(rewards),
        "mean_length": np.mean(lengths),
        "min_length": np.min(lengths),
        "max_length": np.max(lengths)
    }

def value_iteration_policy(env, gamma=0.99):
    V = np.zeros(env.observation_space.n)
    theta = 1e-8
    for _ in range(10000):
        new_V = np.zeros_like(V)
        for state in range(env.observation_space.n):
            q_values = []
            for action in range(env.action_space.n):
                q_value = 0.0
                for probability, next_state, reward, terminated in env.unwrapped.P[state][action]:
                    if terminated:
                        q_value += probability * reward
                    else:
                        q_value += probability * (
                            reward + gamma * V[next_state]
                        )
                q_values.append(q_value)
            new_V[state] = max(q_values)
        delta = np.max(np.abs(new_V - V))
        V = new_V
        if delta < theta:
            break
    policy = np.zeros(
        env.observation_space.n,
        dtype=int
    )

    for state in range(env.observation_space.n):
        q_values = []
        for action in range(env.action_space.n):
            q_value = 0.0
            for probability, next_state, reward, terminated in env.unwrapped.P[state][action]:
                if terminated:
                    q_value += probability * reward
                else:
                    q_value += probability * (
                        reward + gamma * V[next_state]
                    )
            q_values.append(q_value)
        policy[state] = np.argmax(q_values)
    return policy

def policy_iteration_policy(env, gamma=0.99):
    n_states = env.observation_space.n
    n_actions = env.action_space.n
    policy = np.ones(
        (n_states, n_actions)
    ) / n_actions
    theta = 1e-8
    for _ in range(1000):
        # Policy Evaluation
        V = np.zeros(n_states)
        for _ in range(10000):
            new_V = np.zeros_like(V)
            for state in range(n_states):
                for action in range(n_actions):
                    action_probability = policy[state, action]
                    for probability, next_state, reward, terminated in env.unwrapped.P[state][action]:
                        if terminated:
                            new_V[state] += (
                                action_probability
                                * probability
                                * reward
                            )
                        else:
                            new_V[state] += (
                                action_probability
                                * probability
                                * (
                                    reward
                                    + gamma * V[next_state]
                                )
                            )
            delta = np.max(np.abs(new_V - V))
            V = new_V
            if delta < theta:
                break
        # Policy Improvement
        new_policy = np.zeros(n_states, dtype=int)
        for state in range(n_states):
            q_values = []
            for action in range(n_actions):
                q_value = 0.0
                for probability, next_state, reward, terminated in env.unwrapped.P[state][action]:
                    if terminated:
                        q_value += probability * reward
                    else:
                        q_value += probability * (
                            reward + gamma * V[next_state]
                        )
                q_values.append(q_value)
            new_policy[state] = np.argmax(q_values)
        old_policy = np.argmax(policy, axis=1)
        if np.array_equal(old_policy, new_policy):
            return new_policy
        policy = np.zeros(
            (n_states, n_actions)
        )
        for state in range(n_states):
            policy[state, new_policy[state]] = 1.0
    return new_policy

env = gym.make(
    "FrozenLake-v1",
    map_name="4x4",
    is_slippery=True
)

# 1. Random policy
rng = np.random.default_rng(42)

random_policy = rng.integers(
    0,
    env.action_space.n,
    size=env.observation_space.n
)
# 2. Value Iteration policy
vi_policy = value_iteration_policy(env)
# 3. Policy Iteration policy
pi_policy = policy_iteration_policy(env)

results = {
    "Random": evaluate_policy_by_simulation(
        env,
        random_policy,
        n_episodes=1000,
        seed=42
    ),
    "Value Iteration": evaluate_policy_by_simulation(
        env,
        vi_policy,
        n_episodes=1000,
        seed=42
    ),
    "Policy Iteration": evaluate_policy_by_simulation(
        env,
        pi_policy,
        n_episodes=1000,
        seed=42
    )
}

print(
    "Policy | Success Rate | Mean Reward | "
    "Mean Length | Min Length | Max Length"
)

for name, result in results.items():
    print(
        f"{name} | "
        f"{result['success_rate']:.4f} | "
        f"{result['mean_reward']:.4f} | "
        f"{result['mean_length']:.2f} | "
        f"{result['min_length']} | "
        f"{result['max_length']}"
    )

env.close()
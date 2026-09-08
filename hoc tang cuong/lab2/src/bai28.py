import gymnasium as gym
import numpy as np

def q_from_v(env, V, state, action, gamma):
    q_value = 0.0
    for probability, next_state, reward, terminated in env.unwrapped.P[state][action]:
        if terminated:
            q_value += probability * reward
        else:
            q_value += probability * (
                reward + gamma * V[next_state]
            )
    return q_value

def policy_evaluation(
    env,
    policy,
    gamma=0.99,
    theta=1e-8,
    max_iterations=10000
):
    V = np.zeros(env.observation_space.n)
    for _ in range(max_iterations):
        new_V = np.zeros_like(V)
        for state in range(env.observation_space.n):
            for action in range(env.action_space.n):
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
    return V

def greedy_policy_from_value(env, V, gamma=0.99):
    policy = np.zeros(
        env.observation_space.n,
        dtype=int
    )
    for state in range(env.observation_space.n):
        q_values = np.zeros(env.action_space.n)
        for action in range(env.action_space.n):
            q_values[action] = q_from_v(
                env,
                V,
                state,
                action,
                gamma
            )
        policy[state] = np.argmax(q_values)
    return policy

env = gym.make(
    "FrozenLake-v1",
    map_name="4x4",
    is_slippery=True
)

n_states = env.observation_space.n
n_actions = env.action_space.n

# Uniform random policy ban đầu
old_policy = np.ones(
    (n_states, n_actions)
) / n_actions

gamma = 0.99

# 1. Policy Evaluation
V = policy_evaluation(
    env,
    old_policy,
    gamma=gamma
)

# 2. Policy Improvement
new_policy = greedy_policy_from_value(
    env,
    V,
    gamma=gamma
)

# 3. So sánh policy cũ và mới
old_policy_actions = np.argmax(old_policy, axis=1)
changed_states = np.sum(
    old_policy_actions != new_policy
)

print("Old policy:")
print(old_policy_actions)
print("\nNew policy:")
print(new_policy)
print("\nState values:")
print(V)
print("\nNumber of changed states:", changed_states)

env.close()
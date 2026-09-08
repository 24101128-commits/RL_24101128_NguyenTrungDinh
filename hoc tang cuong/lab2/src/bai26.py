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

def greedy_policy_from_value(env, V, gamma=0.99):
    policy = np.zeros(env.observation_space.n, dtype=int)
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

# Sử dụng một V đơn giản để kiểm thử
V = np.zeros(env.observation_space.n)

policy = greedy_policy_from_value(
    env,
    V,
    gamma=0.99
)

print("Value function:")
print(V)
print("Greedy policy:")
print(policy)

env.close()
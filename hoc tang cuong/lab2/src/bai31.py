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

def value_iteration_sweep(env, V, gamma):
    new_V = np.zeros_like(V)
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
        new_V[state] = np.max(q_values)
    return new_V

env = gym.make(
    "FrozenLake-v1",
    map_name="4x4",
    is_slippery=True
)

V = np.zeros(env.observation_space.n)
gamma = 0.99

new_V = value_iteration_sweep(
    env,
    V,
    gamma
)

print("Old V:")
print(V)
print("\nNew V after one Value Iteration sweep:")
print(new_V)

env.close()
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

def action_values(env, V, state, gamma):
    q_values = np.zeros(env.action_space.n)
    for action in range(env.action_space.n):
        q_values[action] = q_from_v(
            env,
            V,
            state,
            action,
            gamma
        )
    return q_values

env = gym.make(
    "FrozenLake-v1",
    map_name="4x4",
    is_slippery=True
)

V = np.zeros(env.observation_space.n)
state = 0
gamma = 0.99
q_values = action_values(env, V, state, gamma)

print("State:", state)
print("Gamma:", gamma)
print("V:", V)
print("Q values:", q_values)

env.close()
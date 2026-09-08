import gymnasium as gym
import numpy as np

def q_from_v(env, V, state, action, gamma):
    q_value = 0.0
    for probability, next_state, reward, terminated in env.unwrapped.P[state][action]:

        if terminated:
            q_value += probability * reward
        else:
            q_value += probability * (reward + gamma * V[next_state])
    return q_value

env = gym.make(
    "FrozenLake-v1",
    map_name="4x4",
    is_slippery=True
)

V = np.zeros(env.observation_space.n)
state = 0
action = 2
gamma = 0.99
q_value = q_from_v(env, V, state, action, gamma)

print("State:", state)
print("Action:", action)
print("Gamma:", gamma)
print("V:", V)
print("Q(s,a):", q_value)

env.close()
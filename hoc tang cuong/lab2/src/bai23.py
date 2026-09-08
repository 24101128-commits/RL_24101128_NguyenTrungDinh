import gymnasium as gym
import numpy as np

def policy_evaluation_sweep(env, policy, V, gamma):
    new_V = np.zeros_like(V)
    for state in range(env.observation_space.n):
        value = 0.0
        for action in range(env.action_space.n):
            action_probability = policy[state, action]
            for probability, next_state, reward, terminated in env.unwrapped.P[state][action]:
                if terminated:
                    value += action_probability * probability * reward
                else:
                    value += action_probability * probability * (
                        reward + gamma * V[next_state]
                    )
        new_V[state] = value
    return new_V

env = gym.make(
    "FrozenLake-v1",
    map_name="4x4",
    is_slippery=True
)

n_states = env.observation_space.n
n_actions = env.action_space.n
# Uniform random policy
policy = np.ones((n_states, n_actions)) / n_actions
V = np.zeros(n_states)
gamma = 0.99

new_V = policy_evaluation_sweep(
    env,
    policy,
    V,
    gamma
)

print("Old V:")
print(V)
print("New V after one sweep:")
print(new_V)

env.close()
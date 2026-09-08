import gymnasium as gym
import numpy as np

def policy_evaluation(
    env,
    policy,
    gamma=0.99,
    theta=1e-8,
    max_iterations=10000,
):
    V = np.zeros(env.observation_space.n)
    for iteration in range(1, max_iterations + 1):
        delta = 0.0
        for state in range(env.observation_space.n):
            old_value = V[state]
            new_value = 0.0
            for action in range(env.action_space.n):
                action_probability = policy[state, action]
                for probability, next_state, reward, terminated in env.unwrapped.P[state][action]:
                    if terminated:
                        new_value += (
                            action_probability
                            * probability
                            * reward
                        )
                    else:
                        new_value += (
                            action_probability
                            * probability
                            * (reward + gamma * V[next_state])
                        )
            V[state] = new_value
            delta = max(
                delta,
                abs(old_value - new_value)
            )
        if delta < theta:
            return V, iteration
    return V, max_iterations

env = gym.make(
    "FrozenLake-v1",
    map_name="4x4",
    is_slippery=True
)

n_states = env.observation_space.n
n_actions = env.action_space.n

policy = np.ones(
    (n_states, n_actions)
) / n_actions

V, n_iterations = policy_evaluation(
    env,
    policy,
    gamma=0.99,
    theta=1e-8,
    max_iterations=10000
)

print("State values:")
print(V)
print("Number of iterations:", n_iterations)

env.close()
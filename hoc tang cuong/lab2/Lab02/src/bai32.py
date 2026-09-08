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

def value_iteration(
    env,
    gamma=0.99,
    theta=1e-8,
    max_iterations=10000
):
    V = np.zeros(env.observation_space.n)
    deltas = []
    for iteration in range(1, max_iterations + 1):
        new_V = value_iteration_sweep(
            env,
            V,
            gamma
        )
        delta = np.max(
            np.abs(new_V - V)
        )
        deltas.append(delta)
        V = new_V
        if delta < theta:
            return V, iteration, deltas
    return V, max_iterations, deltas

env = gym.make(
    "FrozenLake-v1",
    map_name="4x4",
    is_slippery=True
)

V, n_iterations, deltas = value_iteration(
    env,
    gamma=0.99,
    theta=1e-8,
    max_iterations=10000
)

print("Optimal state values:")
print(V)
print("\nNumber of iterations:", n_iterations)
print("\nFinal delta:", deltas[-1])

env.close()
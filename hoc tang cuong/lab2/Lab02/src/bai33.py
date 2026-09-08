import gymnasium as gym
import numpy as np

ACTION_SYMBOLS = {
    0: "←",
    1: "↓",
    2: "→",
    3: "↑"
}

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
            break
    return V, iteration, deltas

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

def print_policy(env, policy):
    rows, cols = env.unwrapped.desc.shape
    for row in range(rows):
        line = []
        for col in range(cols):
            state = row * cols + col
            cell = env.unwrapped.desc[row, col].decode("utf-8")
            if cell == "H":
                line.append("H")
            elif cell == "G":
                line.append("G")
            else:
                line.append(ACTION_SYMBOLS[policy[state]])
        print(" ".join(line))

env = gym.make(
    "FrozenLake-v1",
    map_name="4x4",
    is_slippery=True
)

gamma = 0.99

V, n_iterations, deltas = value_iteration(
    env,
    gamma=gamma,
    theta=1e-8,
    max_iterations=10000
)

optimal_policy = greedy_policy_from_value(
    env,
    V,
    gamma
)

print("Optimal state values:")
print(V)
print("\nOptimal policy:")
print(optimal_policy)
print("\nOptimal policy on 4x4 grid:")
print_policy(env, optimal_policy)

env.close()
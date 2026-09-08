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
                if action_probability == 0:
                    continue
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
        q_values = np.zeros(
            env.action_space.n
        )
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

def policy_iteration(
    env,
    gamma=0.99,
    theta=1e-8,
    max_iterations=1000
):
    n_states = env.observation_space.n
    n_actions = env.action_space.n
    # Khởi tạo uniform random policy
    policy = np.ones(
        (n_states, n_actions)
    ) / n_actions
    for iteration in range(1, max_iterations + 1):
        # Policy Evaluation
        V = policy_evaluation(
            env,
            policy,
            gamma=gamma,
            theta=theta
        )
        # Policy Improvement
        new_policy = greedy_policy_from_value(
            env,
            V,
            gamma=gamma
        )
        # Policy cũ dưới dạng deterministic action
        old_policy_actions = np.argmax(
            policy,
            axis=1
        )
        # Kiểm tra policy có thay đổi không
        if np.array_equal(
            old_policy_actions,
            new_policy
        ):
            return new_policy, V, iteration
        # Chuyển deterministic policy mới
        # thành dạng stochastic matrix
        policy = np.zeros(
            (n_states, n_actions)
        )
        for state in range(n_states):
            policy[state, new_policy[state]] = 1.0
    return new_policy, V, max_iterations

env = gym.make(
    "FrozenLake-v1",
    map_name="4x4",
    is_slippery=True
)

policy, V, n_iterations = policy_iteration(
    env,
    gamma=0.99,
    theta=1e-8,
    max_iterations=1000
)

print("Optimal policy:")
print(policy)
print("\nState values:")
print(V)
print(
    "\nPolicy Iteration converged after",
    n_iterations,
    "iterations."
)

env.close()
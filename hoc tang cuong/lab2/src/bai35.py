import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
from time import perf_counter

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

def policy_iteration(
    env,
    gamma=0.99,
    theta=1e-8,
    max_iterations=1000
):
    n_states = env.observation_space.n
    n_actions = env.action_space.n
    policy = np.ones(
        (n_states, n_actions)
    ) / n_actions
    for iteration in range(1, max_iterations + 1):
        V = policy_evaluation(
            env,
            policy,
            gamma,
            theta
        )
        new_policy = greedy_policy_from_value(
            env,
            V,
            gamma
        )
        old_policy = np.argmax(
            policy,
            axis=1
        )
        if np.array_equal(old_policy, new_policy):
            return new_policy, V, iteration
        policy = np.zeros(
            (n_states, n_actions)
        )
        for state in range(n_states):
            policy[state, new_policy[state]] = 1.0
    return new_policy, V, max_iterations

def value_iteration(
    env,
    gamma=0.99,
    theta=1e-8,
    max_iterations=10000
):
    V = np.zeros(env.observation_space.n)
    for iteration in range(1, max_iterations + 1):
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
        delta = np.max(np.abs(new_V - V))
        V = new_V
        if delta < theta:
            policy = greedy_policy_from_value(
                env,
                V,
                gamma
            )
            return policy, V, iteration
    policy = greedy_policy_from_value(
        env,
        V,
        gamma
    )
    return policy, V, max_iterations

def evaluate_policy(
    env,
    policy,
    n_episodes=1000,
    seed=42
):
    rewards = []
    successes = 0
    for episode in range(n_episodes):
        state, info = env.reset(seed=seed + episode)
        total_reward = 0.0
        for step in range(1000):
            action = policy[state]
            state, reward, terminated, truncated, info = env.step(action)
            total_reward += reward
            if terminated or truncated:
                if reward == 1:
                    successes += 1
                break
        rewards.append(total_reward)
    return {
        "success_rate": successes / n_episodes,
        "mean_reward": np.mean(rewards)
    }

env = gym.make(
    "FrozenLake-v1",
    map_name="4x4",
    is_slippery=True
)

gamma = 0.99
theta = 1e-8
n_episodes = 1000

# -----------------------------
# Value Iteration
# -----------------------------
start = perf_counter()

vi_policy, vi_V, vi_iterations = value_iteration(
    env,
    gamma=gamma,
    theta=theta
)

vi_runtime = perf_counter() - start

vi_result = evaluate_policy(
    env,
    vi_policy,
    n_episodes=n_episodes,
    seed=42
)

# -----------------------------
# Policy Iteration
# -----------------------------
start = perf_counter()

pi_policy, pi_V, pi_iterations = policy_iteration(
    env,
    gamma=gamma,
    theta=theta
)

pi_runtime = perf_counter() - start

pi_result = evaluate_policy(
    env,
    pi_policy,
    n_episodes=n_episodes,
    seed=42
)

# -----------------------------
# In kết quả
# -----------------------------
print(
    "Algorithm | Iterations | Runtime (s) | "
    "Success Rate | Mean Reward"
)

print(
    f"Value Iteration | "
    f"{vi_iterations} | "
    f"{vi_runtime:.6f} | "
    f"{vi_result['success_rate']:.4f} | "
    f"{vi_result['mean_reward']:.4f}"
)

print(
    f"Policy Iteration | "
    f"{pi_iterations} | "
    f"{pi_runtime:.6f} | "
    f"{pi_result['success_rate']:.4f} | "
    f"{pi_result['mean_reward']:.4f}"
)

# -----------------------------
# Biểu đồ so sánh
# -----------------------------
algorithms = [
    "Value Iteration",
    "Policy Iteration"
]

success_rates = [
    vi_result["success_rate"],
    pi_result["success_rate"]
]

mean_rewards = [
    vi_result["mean_reward"],
    pi_result["mean_reward"]
]

x = np.arange(len(algorithms))
fig, ax = plt.subplots()
width = 0.35

ax.bar(
    x - width / 2,
    success_rates,
    width,
    label="Success Rate"
)

ax.bar(
    x + width / 2,
    mean_rewards,
    width,
    label="Mean Reward"
)

ax.set_title("Value Iteration vs Policy Iteration")
ax.set_xlabel("Algorithm")
ax.set_ylabel("Value")
ax.set_xticks(x)
ax.set_xticklabels(algorithms)
ax.legend()
ax.grid(axis="y")
plt.tight_layout()
plt.savefig(
    "figures/algorithm_comparison.png"
)
plt.show()

env.close()
import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
from time import perf_counter

from mdp_utils import (
    get_transition_model,
    q_from_v,
    policy_evaluation,
    greedy_policy_from_value,
    policy_iteration,
    value_iteration,
    evaluate_policy_by_simulation,
)

ACTION_NAMES = {
    0: "LEFT",
    1: "DOWN",
    2: "RIGHT",
    3: "UP",
}

ACTION_SYMBOLS = {
    0: "←",
    1: "↓",
    2: "→",
    3: "↑",
}

def create_environment(is_slippery=True):
    """Create FrozenLake-v1 environment."""
    return gym.make(
        "FrozenLake-v1",
        map_name="4x4",
        is_slippery=is_slippery,
    )

def get_transition_model(env):
    """Return the transition model of the environment."""
    return env.unwrapped.P

def q_from_v(env, V, state, action, gamma):
    """Compute Q(s, a) from the current value function."""
    P = get_transition_model(env)

    q_value = 0.0

    for probability, next_state, reward, terminated in P[state][action]:
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
    max_iterations=10000,
):
    """Evaluate a policy using iterative policy evaluation."""

    V = np.zeros(env.observation_space.n)

    for iteration in range(1, max_iterations + 1):
        new_V = np.zeros_like(V)

        for state in range(env.observation_space.n):
            value = 0.0

            for action in range(env.action_space.n):
                action_probability = policy[state, action]

                if action_probability == 0:
                    continue

                value += action_probability * q_from_v(
                    env,
                    V,
                    state,
                    action,
                    gamma,
                )

            new_V[state] = value

        delta = np.max(np.abs(new_V - V))

        V = new_V

        if delta < theta:
            return V, iteration

    return V, max_iterations

def greedy_policy_from_value(env, V, gamma=0.99):
    """Extract a greedy policy from the value function."""

    n_states = env.observation_space.n
    n_actions = env.action_space.n

    policy = np.zeros(
        n_states,
        dtype=int
    )

    for state in range(n_states):
        q_values = np.zeros(n_actions)

        for action in range(n_actions):
            q_values[action] = q_from_v(
                env,
                V,
                state,
                action,
                gamma,
            )

        policy[state] = np.argmax(q_values)

    return policy

def policy_iteration(
    env,
    gamma=0.99,
    theta=1e-8,
    max_iterations=1000,
):
    """Solve the environment using Policy Iteration."""

    n_states = env.observation_space.n
    n_actions = env.action_space.n

    policy = np.ones(
        (n_states, n_actions)
    ) / n_actions

    policy_deltas = []

    for iteration in range(1, max_iterations + 1):

        V = np.zeros(n_states)

        # Policy Evaluation
        for _ in range(10000):
            new_V = np.zeros_like(V)

            for state in range(n_states):
                for action in range(n_actions):
                    action_probability = policy[state, action]

                    if action_probability == 0:
                        continue

                    new_V[state] += (
                        action_probability
                        * q_from_v(
                            env,
                            V,
                            state,
                            action,
                            gamma,
                        )
                    )

            delta = np.max(np.abs(new_V - V))
            V = new_V

            if delta < theta:
                break

        policy_deltas.append(delta)

        # Policy Improvement
        new_policy = greedy_policy_from_value(
            env,
            V,
            gamma,
        )

        old_policy = np.argmax(
            policy,
            axis=1,
        )

        if np.array_equal(old_policy, new_policy):
            return new_policy, V, iteration, policy_deltas

        policy = np.zeros(
            (n_states, n_actions)
        )

        for state in range(n_states):
            policy[state, new_policy[state]] = 1.0

    return new_policy, V, max_iterations, policy_deltas

def value_iteration(
    env,
    gamma=0.99,
    theta=1e-8,
    max_iterations=10000,
):
    """Solve the environment using Value Iteration."""

    V = np.zeros(env.observation_space.n)
    deltas = []

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
                    gamma,
                )

            new_V[state] = np.max(q_values)

        delta = np.max(np.abs(new_V - V))
        deltas.append(delta)

        V = new_V

        if delta < theta:
            policy = greedy_policy_from_value(
                env,
                V,
                gamma,
            )

            return policy, V, iteration, deltas

        policy = greedy_policy_from_value(
        env,
        V,
        gamma,
    )

    return policy, V, max_iterations, deltas

def evaluate_policy_by_simulation(
    env,
    policy,
    n_episodes=1000,
    seed=42,
):
    """Evaluate a policy using environment simulation."""

    rewards = []
    lengths = []
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
        lengths.append(step + 1)

    return {
        "success_rate": successes / n_episodes,
        "mean_reward": np.mean(rewards),
        "mean_length": np.mean(lengths),
        "min_length": np.min(lengths),
        "max_length": np.max(lengths),
    }

def print_policy(env, policy):
    """Print the policy as a FrozenLake grid."""

    action_symbols = {
        0: "←",
        1: "↓",
        2: "→",
        3: "↑",
    }

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
                line.append(action_symbols[policy[state]])

        print(" ".join(line))

def plot_convergence(vi_deltas, pi_deltas):
    """Plot and save convergence curves."""

    # Value Iteration convergence
    plt.figure()
    plt.plot(
        range(1, len(vi_deltas) + 1),
        vi_deltas,
        label="Value Iteration",
    )
    plt.title("Value Iteration Convergence")
    plt.xlabel("Iteration")
    plt.ylabel("Delta")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.savefig(
        "figures/value_iteration_convergence.png"
    )
    plt.show()

    # Policy Iteration convergence
    plt.figure()
    plt.plot(
        range(1, len(pi_deltas) + 1),
        pi_deltas,
        label="Policy Iteration",
    )
    plt.title("Policy Iteration Convergence")
    plt.xlabel("Iteration")
    plt.ylabel("Delta")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.savefig(
        "figures/policy_iteration_convergence.png"
    )
    plt.show()

def main():
    """Run the complete Dynamic Programming experiment."""

    gamma = 0.99
    theta = 1e-8
    max_iterations = 10000
    n_episodes = 1000

    print("Dynamic Programming Solver")
    print("--------------------------")

    env = create_environment(
        is_slippery=True
    )

    P = get_transition_model(env)

    print("Number of states:", env.observation_space.n)
    print("Number of actions:", env.action_space.n)
    print("Transition model loaded:", P is not None)

    n_states = env.observation_space.n
    n_actions = env.action_space.n

    # --------------------------------
    # 1. Policy Evaluation
    # --------------------------------
    policy = np.ones(
        (n_states, n_actions)
    ) / n_actions

    V, n_iterations = policy_evaluation(
        env,
        policy,
        gamma=gamma,
        theta=theta,
        max_iterations=max_iterations,
    )

    print("\nPolicy Evaluation")
    print("State values:")
    print(V)
    print("Number of iterations:", n_iterations)

    # --------------------------------
    # 2. Policy Improvement
    # --------------------------------
    greedy_policy = greedy_policy_from_value(
        env,
        V,
        gamma=gamma,
    )

    print("\nGreedy policy:")
    print(greedy_policy)

       # --------------------------------
    # 3. Policy Iteration
    # --------------------------------
    pi_start = perf_counter()

    pi_policy, pi_V, pi_iterations, pi_deltas = policy_iteration(
        env,
        gamma=gamma,
        theta=theta,
        max_iterations=1000,
    )

    pi_runtime = perf_counter() - pi_start

    print("\nPolicy Iteration")
    print("Optimal policy:")
    print(pi_policy)

    print("State values:")
    print(pi_V)

    print(
        "Policy Iteration converged after",
        pi_iterations,
        "iterations."
    )

    print(
        "Policy Iteration runtime:",
        f"{pi_runtime:.6f} seconds"
    )

    # --------------------------------
    # 4. Value Iteration
    # --------------------------------
    vi_start = perf_counter()

    vi_policy, vi_V, vi_iterations, vi_deltas = value_iteration(
        env,
        gamma=gamma,
        theta=theta,
        max_iterations=max_iterations,
    )

    vi_runtime = perf_counter() - vi_start

    print("\nValue Iteration")
    print("Optimal policy:")
    print(vi_policy)

    print("State values:")
    print(vi_V)

    print(
        "Value Iteration converged after",
        vi_iterations,
        "iterations."
    )

    print("Final delta:", vi_deltas[-1])

    print(
        "Value Iteration runtime:",
        f"{vi_runtime:.6f} seconds"
    )

    # --------------------------------
    # 5. Policy grids
    # --------------------------------
    print("\nPolicy Iteration Policy Grid:")
    print_policy(env, pi_policy)

    print("\nValue Iteration Policy Grid:")
    print_policy(env, vi_policy)

    # --------------------------------
    # 6. Policy evaluation by simulation
    # --------------------------------
    print("\nPolicy Evaluation by Simulation")

    pi_result = evaluate_policy_by_simulation(
        env,
        pi_policy,
        n_episodes=n_episodes,
        seed=42,
    )

    vi_result = evaluate_policy_by_simulation(
        env,
        vi_policy,
        n_episodes=n_episodes,
        seed=42,
    )

    print("\nPolicy Iteration:")
    print("Success rate:", pi_result["success_rate"])
    print("Mean reward:", pi_result["mean_reward"])
    print("Mean episode length:", pi_result["mean_length"])
    print("Min episode length:", pi_result["min_length"])
    print("Max episode length:", pi_result["max_length"])

    print("\nValue Iteration:")
    print("Success rate:", vi_result["success_rate"])
    print("Mean reward:", vi_result["mean_reward"])
    print("Mean episode length:", vi_result["mean_length"])
    print("Min episode length:", vi_result["min_length"])
    print("Max episode length:", vi_result["max_length"])

    # --------------------------------
    # 7. Convergence plots
    # --------------------------------
    plot_convergence(
        vi_deltas,
        pi_deltas,
    )

    # --------------------------------
    # 8. Algorithm comparison
    # --------------------------------
    print("\nAlgorithm Comparison")
    print(
        "Algorithm | Iterations | Runtime (s) | "
        "Success Rate | Mean Reward"
    )

    print(
        f"Policy Iteration | "
        f"{pi_iterations} | "
        f"{pi_runtime:.6f} | "
        f"{pi_result['success_rate']:.4f} | "
        f"{pi_result['mean_reward']:.4f}"
    )

    print(
        f"Value Iteration | "
        f"{vi_iterations} | "
        f"{vi_runtime:.6f} | "
        f"{vi_result['success_rate']:.4f} | "
        f"{vi_result['mean_reward']:.4f}"
    )

    # --------------------------------
    # 9. Algorithm comparison plot
    # --------------------------------
    algorithms = [
        "Policy Iteration",
        "Value Iteration",
    ]

    success_rates = [
        pi_result["success_rate"],
        vi_result["success_rate"],
    ]

    mean_rewards = [
        pi_result["mean_reward"],
        vi_result["mean_reward"],
    ]

    x = np.arange(len(algorithms))
    width = 0.35

    plt.figure()

    plt.bar(
        x - width / 2,
        success_rates,
        width,
        label="Success Rate",
    )

    plt.bar(
        x + width / 2,
        mean_rewards,
        width,
        label="Mean Reward",
    )

    plt.title("Algorithm Comparison")
    plt.xlabel("Algorithm")
    plt.ylabel("Value")
    plt.xticks(x, algorithms)
    plt.legend()
    plt.grid(axis="y")
    plt.tight_layout()

    plt.savefig(
        "figures/algorithm_comparison.png"
    )

    plt.show()

    env.close()

if __name__ == "__main__":
    main()
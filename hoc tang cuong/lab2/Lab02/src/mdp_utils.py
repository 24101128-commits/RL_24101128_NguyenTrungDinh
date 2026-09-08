import numpy as np


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
        dtype=int,
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

        if np.array_equal(
            old_policy,
            new_policy,
        ):
            return new_policy, V, iteration, policy_deltas

        policy = np.zeros(
            (n_states, n_actions)
        )

        for state in range(n_states):
            policy[state, new_policy[state]] = 1.0

    return (
        new_policy,
        V,
        max_iterations,
        policy_deltas,
    )


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
            q_values = np.zeros(
                env.action_space.n
            )

            for action in range(env.action_space.n):
                q_values[action] = q_from_v(
                    env,
                    V,
                    state,
                    action,
                    gamma,
                )

            new_V[state] = np.max(q_values)

        delta = np.max(
            np.abs(new_V - V)
        )

        deltas.append(delta)
        V = new_V

        if delta < theta:
            policy = greedy_policy_from_value(
                env,
                V,
                gamma,
            )

            return (
                policy,
                V,
                iteration,
                deltas,
            )

    policy = greedy_policy_from_value(
        env,
        V,
        gamma,
    )

    return (
        policy,
        V,
        max_iterations,
        deltas,
    )


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
        state, info = env.reset(
            seed=seed + episode
        )

        total_reward = 0.0

        for step in range(1000):
            action = policy[state]

            state, reward, terminated, truncated, info = env.step(
                action
            )

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
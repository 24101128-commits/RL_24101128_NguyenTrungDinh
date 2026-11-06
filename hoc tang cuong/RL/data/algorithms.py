"""
algorithms.py - Reinforcement Learning Algorithms for One-Way Arrow Grid.
Implements 5 core RL algorithms:
1. Value Iteration (Model-based Dynamic Programming)
2. Policy Iteration (Model-based Dynamic Programming: Policy Eval + Policy Improvement)
3. Tabular Q-Learning (Model-free Off-policy Temporal Difference Control)
4. SARSA (Model-free On-policy Temporal Difference Control)
5. Monte Carlo Control (Model-free First-Visit Episodic Control)

Strictly tabular, exact MDP mechanics, full support for action masking and penalty modes.
"""

from typing import Dict, Any, List, Tuple, Optional
import time
import numpy as np


class ValueIteration:
    """
    Value Iteration algorithm for exact MDP solving.
    Applies the Bellman optimality operator until convergence:
        V_{k+1}(s) = max_a sum_{s'} P(s'|s,a) [R(s,a,s') + gamma * V_k(s')]
    Convergence criterion: max_s |V_{k+1}(s) - V_k(s)| < theta
    """

    def __init__(
        self,
        env,
        gamma: float = 0.99,
        theta: float = 1e-6,
        max_iterations: int = 1000
    ):
        self.env = env
        self.gamma = gamma
        self.theta = theta
        self.max_iterations = max_iterations
        self.num_states = env.num_states
        self.num_actions = env.action_space.n

        self.V = np.zeros(self.num_states, dtype=np.float64)
        self.policy = np.zeros(self.num_states, dtype=int)
        self.history_deltas: List[float] = []

    def solve(self) -> Tuple[np.ndarray, np.ndarray, int]:
        self.history_deltas = []
        iteration = 0

        while iteration < self.max_iterations:
            delta = 0.0
            new_V = np.copy(self.V)

            for s_idx in range(self.num_states):
                s = self.env.decode_state(s_idx)
                r, c, tok, sw = s

                if (r, c) == self.env.goal_pos:
                    new_V[s_idx] = 0.0
                    continue

                mask = self.env.get_action_mask(s)
                if self.env.invalid_action_mode == "action_mask":
                    candidate_actions = [a for a in range(self.num_actions) if mask[a]]
                    if not candidate_actions:
                        new_V[s_idx] = self.env.invalid_penalty / (1.0 - self.gamma)
                        continue
                else:
                    candidate_actions = list(range(self.num_actions))

                best_val = -float("inf")
                for a in candidate_actions:
                    transitions = self.env.get_transition_prob(s, a)
                    q_val = 0.0
                    for prob, next_s, reward, terminated in transitions:
                        next_idx = self.env.encode_state(next_s)
                        next_v = 0.0 if terminated else self.V[next_idx]
                        q_val += prob * (reward + self.gamma * next_v)
                    if q_val > best_val:
                        best_val = q_val

                new_V[s_idx] = best_val
                delta = max(delta, abs(new_V[s_idx] - self.V[s_idx]))

            self.V = new_V
            self.history_deltas.append(delta)
            iteration += 1

            if delta < self.theta:
                break

        # Extract deterministic optimal policy
        for s_idx in range(self.num_states):
            s = self.env.decode_state(s_idx)
            r, c, tok, sw = s
            if (r, c) == self.env.goal_pos:
                self.policy[s_idx] = 0
                continue

            mask = self.env.get_action_mask(s)
            if self.env.invalid_action_mode == "action_mask":
                candidate_actions = [a for a in range(self.num_actions) if mask[a]]
                if not candidate_actions:
                    self.policy[s_idx] = 0
                    continue
            else:
                candidate_actions = list(range(self.num_actions))

            best_a = candidate_actions[0]
            best_q = -float("inf")
            for a in candidate_actions:
                transitions = self.env.get_transition_prob(s, a)
                q_val = 0.0
                for prob, next_s, reward, terminated in transitions:
                    next_idx = self.env.encode_state(next_s)
                    next_v = 0.0 if terminated else self.V[next_idx]
                    q_val += prob * (reward + self.gamma * next_v)
                if q_val > best_q:
                    best_q = q_val
                    best_a = a
            self.policy[s_idx] = best_a

        return self.V, self.policy, iteration


class PolicyIteration:
    """
    Policy Iteration algorithm for exact MDP solving.
    Alternates between:
    1. Policy Evaluation: Solves for V^pi(s) using iterative Bellman expectation backup.
    2. Policy Improvement: Greedy action selection wrt V^pi(s).
    Guaranteed finite convergence to optimal policy pi* and value V*.
    """

    def __init__(
        self,
        env,
        gamma: float = 0.99,
        theta: float = 1e-6,
        max_eval_iterations: int = 1000,
        max_policy_iterations: int = 200
    ):
        self.env = env
        self.gamma = gamma
        self.theta = theta
        self.max_eval_iterations = max_eval_iterations
        self.max_policy_iterations = max_policy_iterations
        self.num_states = env.num_states
        self.num_actions = env.action_space.n

        self.V = np.zeros(self.num_states, dtype=np.float64)
        # Initialize policy with legal actions
        self.policy = np.zeros(self.num_states, dtype=int)
        for s_idx in range(self.num_states):
            s = self.env.decode_state(s_idx)
            mask = self.env.get_action_mask(s)
            valid_actions = [a for a in range(self.num_actions) if mask[a]]
            self.policy[s_idx] = valid_actions[0] if valid_actions else 0

        self.policy_iterations = 0
        self.total_eval_iterations = 0

    def policy_evaluation(self) -> int:
        eval_iters = 0
        while eval_iters < self.max_eval_iterations:
            delta = 0.0
            new_V = np.copy(self.V)

            for s_idx in range(self.num_states):
                s = self.env.decode_state(s_idx)
                r, c, tok, sw = s
                if (r, c) == self.env.goal_pos:
                    new_V[s_idx] = 0.0
                    continue

                a = self.policy[s_idx]
                transitions = self.env.get_transition_prob(s, a)
                expected_val = 0.0
                for prob, next_s, reward, terminated in transitions:
                    next_idx = self.env.encode_state(next_s)
                    next_v = 0.0 if terminated else self.V[next_idx]
                    expected_val += prob * (reward + self.gamma * next_v)

                new_V[s_idx] = expected_val
                delta = max(delta, abs(new_V[s_idx] - self.V[s_idx]))

            self.V = new_V
            eval_iters += 1
            if delta < self.theta:
                break
        return eval_iters

    def policy_improvement(self) -> bool:
        policy_stable = True
        for s_idx in range(self.num_states):
            s = self.env.decode_state(s_idx)
            r, c, tok, sw = s
            if (r, c) == self.env.goal_pos:
                continue

            old_a = self.policy[s_idx]
            mask = self.env.get_action_mask(s)
            if self.env.invalid_action_mode == "action_mask":
                candidate_actions = [a for a in range(self.num_actions) if mask[a]]
                if not candidate_actions:
                    continue
            else:
                candidate_actions = list(range(self.num_actions))

            best_a = candidate_actions[0]
            best_q = -float("inf")
            for a in candidate_actions:
                transitions = self.env.get_transition_prob(s, a)
                q_val = 0.0
                for prob, next_s, reward, terminated in transitions:
                    next_idx = self.env.encode_state(next_s)
                    next_v = 0.0 if terminated else self.V[next_idx]
                    q_val += prob * (reward + self.gamma * next_v)
                if q_val > best_q:
                    best_q = q_val
                    best_a = a

            self.policy[s_idx] = best_a
            if best_a != old_a:
                policy_stable = False

        return policy_stable

    def solve(self) -> Tuple[np.ndarray, np.ndarray, int, int]:
        self.policy_iterations = 0
        self.total_eval_iterations = 0

        while self.policy_iterations < self.max_policy_iterations:
            eval_iters = self.policy_evaluation()
            self.total_eval_iterations += eval_iters
            self.policy_iterations += 1

            stable = self.policy_improvement()
            if stable:
                break

        return self.V, self.policy, self.policy_iterations, self.total_eval_iterations


class QLearningAgent:
    """
    Model-free Off-policy Temporal Difference Control (Q-Learning).
    Update equation:
        Q(s, a) <- Q(s, a) + alpha * [r + gamma * max_{a'} Q(s', a') - Q(s, a)]
    Uses epsilon-greedy action selection and action masking for valid moves.
    """

    def __init__(
        self,
        env,
        alpha: float = 0.1,
        gamma: float = 0.99,
        epsilon: float = 1.0,
        epsilon_min: float = 0.01,
        epsilon_decay: float = 0.995,
        seed: Optional[int] = None
    ):
        self.env = env
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.rng = np.random.default_rng(seed)

        self.num_states = env.num_states
        self.num_actions = env.action_space.n
        self.Q = np.zeros((self.num_states, self.num_actions), dtype=np.float64)

    def select_action(
        self,
        state: Tuple[int, int, int, int],
        mask: Optional[np.ndarray] = None,
        explore: bool = True
    ) -> int:
        if mask is None:
            mask = self.env.get_action_mask(state)

        valid_actions = np.where(mask)[0]
        if len(valid_actions) == 0:
            valid_actions = np.arange(self.num_actions)

        if explore and self.rng.random() < self.epsilon:
            return int(self.rng.choice(valid_actions))

        s_idx = self.env.encode_state(state)
        masked_q = np.full(self.num_actions, -np.inf)
        for a in valid_actions:
            masked_q[a] = self.Q[s_idx, a]

        max_val = np.max(masked_q)
        best_actions = [a for a in valid_actions if np.isclose(masked_q[a], max_val, atol=1e-8)]
        return int(self.rng.choice(best_actions))

    def train(self, num_episodes: int = 500) -> Dict[str, Any]:
        rewards_history = []
        steps_history = []
        success_history = []
        epsilon_history = []

        for ep in range(num_episodes):
            obs, info = self.env.reset()
            state = self.env.decode_state(obs)
            total_reward = 0.0
            steps = 0
            terminated = False
            truncated = False

            while not (terminated or truncated):
                mask = self.env.get_action_mask(state)
                action = self.select_action(state, mask, explore=True)
                next_obs, reward, terminated, truncated, _ = self.env.step(action)
                next_state = self.env.decode_state(next_obs)

                s_idx = self.env.encode_state(state)
                next_s_idx = self.env.encode_state(next_state)

                if terminated:
                    target = reward
                else:
                    next_mask = self.env.get_action_mask(next_state)
                    next_valid = np.where(next_mask)[0]
                    if len(next_valid) == 0:
                        next_valid = np.arange(self.num_actions)
                    max_next_q = np.max([self.Q[next_s_idx, a_prime] for a_prime in next_valid])
                    target = reward + self.gamma * max_next_q

                self.Q[s_idx, action] += self.alpha * (target - self.Q[s_idx, action])

                state = next_state
                total_reward += reward
                steps += 1

            self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
            rewards_history.append(total_reward)
            steps_history.append(steps)
            success_history.append(1 if (state[0], state[1]) == self.env.goal_pos else 0)
            epsilon_history.append(self.epsilon)

        return {
            "rewards": rewards_history,
            "steps": steps_history,
            "success": success_history,
            "epsilon": epsilon_history
        }

    def get_policy(self) -> np.ndarray:
        policy = np.zeros(self.num_states, dtype=int)
        for s_idx in range(self.num_states):
            state = self.env.decode_state(s_idx)
            mask = self.env.get_action_mask(state)
            valid_actions = np.where(mask)[0]
            if len(valid_actions) == 0:
                valid_actions = np.arange(self.num_actions)
            masked_q = np.full(self.num_actions, -np.inf)
            for a in valid_actions:
                masked_q[a] = self.Q[s_idx, a]
            policy[s_idx] = int(valid_actions[np.argmax([masked_q[a] for a in valid_actions])])
        return policy

    def get_V(self) -> np.ndarray:
        V = np.zeros(self.num_states, dtype=np.float64)
        for s_idx in range(self.num_states):
            state = self.env.decode_state(s_idx)
            mask = self.env.get_action_mask(state)
            valid_actions = np.where(mask)[0]
            if len(valid_actions) == 0:
                V[s_idx] = np.max(self.Q[s_idx])
            else:
                V[s_idx] = np.max([self.Q[s_idx, a] for a in valid_actions])
        return V


class SARSAAgent:
    """
    Model-free On-policy Temporal Difference Control (SARSA).
    Update equation:
        Q(s, a) <- Q(s, a) + alpha * [r + gamma * Q(s', a') - Q(s, a)]
    On-policy: updates using the actual action a' chosen by the current policy.
    """

    def __init__(
        self,
        env,
        alpha: float = 0.1,
        gamma: float = 0.99,
        epsilon: float = 1.0,
        epsilon_min: float = 0.01,
        epsilon_decay: float = 0.995,
        seed: Optional[int] = None
    ):
        self.env = env
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.rng = np.random.default_rng(seed)

        self.num_states = env.num_states
        self.num_actions = env.action_space.n
        self.Q = np.zeros((self.num_states, self.num_actions), dtype=np.float64)

    def select_action(
        self,
        state: Tuple[int, int, int, int],
        mask: Optional[np.ndarray] = None,
        explore: bool = True
    ) -> int:
        if mask is None:
            mask = self.env.get_action_mask(state)

        valid_actions = np.where(mask)[0]
        if len(valid_actions) == 0:
            valid_actions = np.arange(self.num_actions)

        if explore and self.rng.random() < self.epsilon:
            return int(self.rng.choice(valid_actions))

        s_idx = self.env.encode_state(state)
        masked_q = np.full(self.num_actions, -np.inf)
        for a in valid_actions:
            masked_q[a] = self.Q[s_idx, a]

        max_val = np.max(masked_q)
        best_actions = [a for a in valid_actions if np.isclose(masked_q[a], max_val, atol=1e-8)]
        return int(self.rng.choice(best_actions))

    def train(self, num_episodes: int = 500) -> Dict[str, Any]:
        rewards_history = []
        steps_history = []
        success_history = []
        epsilon_history = []

        for ep in range(num_episodes):
            obs, info = self.env.reset()
            state = self.env.decode_state(obs)
            total_reward = 0.0
            steps = 0
            terminated = False
            truncated = False

            mask = self.env.get_action_mask(state)
            action = self.select_action(state, mask, explore=True)

            while not (terminated or truncated):
                next_obs, reward, terminated, truncated, _ = self.env.step(action)
                next_state = self.env.decode_state(next_obs)
                s_idx = self.env.encode_state(state)
                next_s_idx = self.env.encode_state(next_state)

                if terminated:
                    target = reward
                    self.Q[s_idx, action] += self.alpha * (target - self.Q[s_idx, action])
                else:
                    next_mask = self.env.get_action_mask(next_state)
                    next_action = self.select_action(next_state, next_mask, explore=True)
                    target = reward + self.gamma * self.Q[next_s_idx, next_action]
                    self.Q[s_idx, action] += self.alpha * (target - self.Q[s_idx, action])
                    action = next_action

                state = next_state
                total_reward += reward
                steps += 1

            self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
            rewards_history.append(total_reward)
            steps_history.append(steps)
            success_history.append(1 if (state[0], state[1]) == self.env.goal_pos else 0)
            epsilon_history.append(self.epsilon)

        return {
            "rewards": rewards_history,
            "steps": steps_history,
            "success": success_history,
            "epsilon": epsilon_history
        }

    def get_policy(self) -> np.ndarray:
        policy = np.zeros(self.num_states, dtype=int)
        for s_idx in range(self.num_states):
            state = self.env.decode_state(s_idx)
            mask = self.env.get_action_mask(state)
            valid_actions = np.where(mask)[0]
            if len(valid_actions) == 0:
                valid_actions = np.arange(self.num_actions)
            masked_q = np.full(self.num_actions, -np.inf)
            for a in valid_actions:
                masked_q[a] = self.Q[s_idx, a]
            policy[s_idx] = int(valid_actions[np.argmax([masked_q[a] for a in valid_actions])])
        return policy

    def get_V(self) -> np.ndarray:
        V = np.zeros(self.num_states, dtype=np.float64)
        for s_idx in range(self.num_states):
            state = self.env.decode_state(s_idx)
            mask = self.env.get_action_mask(state)
            valid_actions = np.where(mask)[0]
            if len(valid_actions) == 0:
                V[s_idx] = np.max(self.Q[s_idx])
            else:
                V[s_idx] = np.max([self.Q[s_idx, a] for a in valid_actions])
        return V


class MonteCarloAgent:
    """
    Model-free First-Visit Episodic Monte Carlo Control with epsilon-greedy exploration.
    Generates complete trajectories, accumulates return G_t backwards,
    and updates Q(s, a) on first visits of state-action pairs.
    """

    def __init__(
        self,
        env,
        alpha: float = 0.05,
        gamma: float = 0.99,
        epsilon: float = 1.0,
        epsilon_min: float = 0.01,
        epsilon_decay: float = 0.995,
        seed: Optional[int] = None
    ):
        self.env = env
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.rng = np.random.default_rng(seed)

        self.num_states = env.num_states
        self.num_actions = env.action_space.n
        self.Q = np.zeros((self.num_states, self.num_actions), dtype=np.float64)
        self.returns_count = np.zeros((self.num_states, self.num_actions), dtype=np.int32)

    def select_action(
        self,
        state: Tuple[int, int, int, int],
        mask: Optional[np.ndarray] = None,
        explore: bool = True
    ) -> int:
        if mask is None:
            mask = self.env.get_action_mask(state)

        valid_actions = np.where(mask)[0]
        if len(valid_actions) == 0:
            valid_actions = np.arange(self.num_actions)

        if explore and self.rng.random() < self.epsilon:
            return int(self.rng.choice(valid_actions))

        s_idx = self.env.encode_state(state)
        masked_q = np.full(self.num_actions, -np.inf)
        for a in valid_actions:
            masked_q[a] = self.Q[s_idx, a]

        max_val = np.max(masked_q)
        best_actions = [a for a in valid_actions if np.isclose(masked_q[a], max_val, atol=1e-8)]
        return int(self.rng.choice(best_actions))

    def train(self, num_episodes: int = 500) -> Dict[str, Any]:
        rewards_history = []
        steps_history = []
        success_history = []
        epsilon_history = []

        for ep in range(num_episodes):
            obs, info = self.env.reset()
            state = self.env.decode_state(obs)
            trajectory: List[Tuple[int, int, float]] = []  # (s_idx, action, reward)
            total_reward = 0.0
            steps = 0
            terminated = False
            truncated = False

            while not (terminated or truncated):
                mask = self.env.get_action_mask(state)
                action = self.select_action(state, mask, explore=True)
                next_obs, reward, terminated, truncated, _ = self.env.step(action)
                next_state = self.env.decode_state(next_obs)

                s_idx = self.env.encode_state(state)
                trajectory.append((s_idx, action, reward))

                state = next_state
                total_reward += reward
                steps += 1

            # First-visit Monte Carlo update
            G = 0.0
            visited_sa = set()
            # Traverse backwards
            for t in reversed(range(len(trajectory))):
                s_idx, a, r = trajectory[t]
                G = self.gamma * G + r

                # First-visit check: verify if (s_idx, a) appears earlier in trajectory
                prior_visited = False
                for prev_t in range(t):
                    if trajectory[prev_t][0] == s_idx and trajectory[prev_t][1] == a:
                        prior_visited = True
                        break

                if not prior_visited:
                    self.returns_count[s_idx, a] += 1
                    # Constant step-size alpha for non-stationary control
                    if self.alpha is not None:
                        self.Q[s_idx, a] += self.alpha * (G - self.Q[s_idx, a])
                    else:
                        n = self.returns_count[s_idx, a]
                        self.Q[s_idx, a] += (1.0 / n) * (G - self.Q[s_idx, a])

            self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
            rewards_history.append(total_reward)
            steps_history.append(steps)
            success_history.append(1 if (state[0], state[1]) == self.env.goal_pos else 0)
            epsilon_history.append(self.epsilon)

        return {
            "rewards": rewards_history,
            "steps": steps_history,
            "success": success_history,
            "epsilon": epsilon_history
        }

    def get_policy(self) -> np.ndarray:
        policy = np.zeros(self.num_states, dtype=int)
        for s_idx in range(self.num_states):
            state = self.env.decode_state(s_idx)
            mask = self.env.get_action_mask(state)
            valid_actions = np.where(mask)[0]
            if len(valid_actions) == 0:
                valid_actions = np.arange(self.num_actions)
            masked_q = np.full(self.num_actions, -np.inf)
            for a in valid_actions:
                masked_q[a] = self.Q[s_idx, a]
            policy[s_idx] = int(valid_actions[np.argmax([masked_q[a] for a in valid_actions])])
        return policy

    def get_V(self) -> np.ndarray:
        V = np.zeros(self.num_states, dtype=np.float64)
        for s_idx in range(self.num_states):
            state = self.env.decode_state(s_idx)
            mask = self.env.get_action_mask(state)
            valid_actions = np.where(mask)[0]
            if len(valid_actions) == 0:
                V[s_idx] = np.max(self.Q[s_idx])
            else:
                V[s_idx] = np.max([self.Q[s_idx, a] for a in valid_actions])
        return V


def evaluate_policy(env, policy: np.ndarray, num_episodes: int = 50, max_steps: int = 100) -> Dict[str, float]:
    """
    Evaluates a deterministic policy over multiple episodes.
    Returns mean reward, mean steps, and success rate.
    """
    total_rewards = []
    total_steps = []
    successes = 0

    for _ in range(num_episodes):
        obs, _ = env.reset()
        state = env.decode_state(obs)
        ep_reward = 0.0
        steps = 0
        terminated = False
        truncated = False

        while not (terminated or truncated) and steps < max_steps:
            s_idx = env.encode_state(state)
            action = int(policy[s_idx])
            next_obs, reward, terminated, truncated, _ = env.step(action)
            state = env.decode_state(next_obs)
            ep_reward += reward
            steps += 1

        total_rewards.append(ep_reward)
        total_steps.append(steps)
        if (state[0], state[1]) == env.goal_pos:
            successes += 1

    return {
        "mean_reward": float(np.mean(total_rewards)),
        "std_reward": float(np.std(total_rewards)),
        "mean_steps": float(np.mean(total_steps)),
        "success_rate": float(successes / num_episodes)
    }

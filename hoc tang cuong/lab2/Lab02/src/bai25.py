import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt

def policy_evaluation(
    env,
    policy,
    gamma=0.99,
    theta=1e-8,
    max_iterations=10000,
):
    V = np.zeros(env.observation_space.n)
    deltas = []
    for iteration in range(1, max_iterations + 1):
        new_V = np.zeros_like(V)
        for state in range(env.observation_space.n):
            for action in range(env.action_space.n):
                action_probability = policy[state, action]
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
                            * (reward + gamma * V[next_state])
                        )
        delta = np.max(np.abs(new_V - V))
        deltas.append(delta)
        V = new_V
        if delta < theta:
            break
    return V, iteration, deltas

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

V, n_iterations, deltas = policy_evaluation(
    env,
    policy,
    gamma=0.99,
    theta=1e-8,
    max_iterations=10000
)

print("State values:")
print(V)
print("Number of iterations:", n_iterations)
print("Final delta:", deltas[-1])

plt.plot(range(1, len(deltas) + 1), deltas)
plt.title("Policy Evaluation Convergence")
plt.xlabel("Iteration")
plt.ylabel("Delta")
plt.grid()
plt.savefig("figures/policy_evaluation_convergence.png")
plt.show()

env.close()
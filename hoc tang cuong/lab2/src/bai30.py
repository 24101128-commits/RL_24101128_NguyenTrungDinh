import gymnasium as gym
import numpy as np

def is_policy_stable(old_policy, new_policy):
    old_actions = np.argmax(old_policy, axis=1)
    return np.array_equal(old_actions, new_policy)

env = gym.make(
    "FrozenLake-v1",
    map_name="4x4",
    is_slippery=True
)

# Policy cũ
old_policy = np.ones(
    (env.observation_space.n, env.action_space.n)
) / env.action_space.n

# Policy mới sau improvement
new_policy = np.array([
    0, 3, 3, 3,
    0, 0, 0, 0,
    3, 1, 0, 0,
    0, 2, 1, 0
])

stable = is_policy_stable(
    old_policy,
    new_policy
)

print("Old policy:")
print(np.argmax(old_policy, axis=1))
print("\nNew policy:")
print(new_policy)
print("\nPolicy stable:", stable)

env.close()
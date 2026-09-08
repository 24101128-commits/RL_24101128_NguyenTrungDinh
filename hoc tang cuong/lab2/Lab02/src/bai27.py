import gymnasium as gym
import numpy as np

ACTION_SYMBOLS = {
    0: "←",
    1: "↓",
    2: "→",
    3: "↑"
}

def print_frozenlake_policy(env, policy):
    desc = env.unwrapped.desc
    rows, cols = desc.shape
    for row in range(rows):
        line = []
        for col in range(cols):
            state = row * cols + col
            cell = desc[row, col].decode("utf-8")
            if cell == "H":
                line.append("H")
            elif cell == "G":
                line.append("G")
            else:
                action = policy[state]
                line.append(ACTION_SYMBOLS[action])
        print(" ".join(line))

env = gym.make(
    "FrozenLake-v1",
    map_name="4x4",
    is_slippery=True
)

V = np.zeros(env.observation_space.n)

policy = np.zeros(
    env.observation_space.n,
    dtype=int
)

policy[14] = 1
print("FrozenLake policy:")
print_frozenlake_policy(env, policy)

env.close()
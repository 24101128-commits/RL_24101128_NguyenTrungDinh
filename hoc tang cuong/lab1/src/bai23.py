"""
Bai 23. Tao FrozenLake-v1 (is_slippery=False), in observation_space,
action_space va xac dinh so state, so action bang code.
"""

import gymnasium as gym


def main():
    env = gym.make("FrozenLake-v1", is_slippery=False)

    print("Observation space:", env.observation_space)
    print("Action space:", env.action_space)

    num_states = env.observation_space.n
    num_actions = env.action_space.n

    print("So state:", num_states)
    print("So action:", num_actions)

    env.close()


if __name__ == "__main__":
    main()

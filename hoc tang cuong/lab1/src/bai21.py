"""
Bai 21. Seed cho action_space va kiem tra tinh tai lap cua chuoi action.
"""

import gymnasium as gym


def sample_actions(seed):
    env = gym.make("CartPole-v1")
    env.action_space.seed(seed)
    actions = [env.action_space.sample() for _ in range(20)]
    env.close()
    return actions


def main():
    actions_run1 = sample_actions(seed=123)
    actions_run2 = sample_actions(seed=123)

    print("Lan chay 1:", actions_run1)
    print("Lan chay 2:", actions_run2)
    print("Hai chuoi action giong nhau:", actions_run1 == actions_run2)


if __name__ == "__main__":
    main()

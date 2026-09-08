import gymnasium as gym

def describe_state(env, state):
    print(f"State {state}")
    for action in range(env.action_space.n):
        print(f"  Action {action}:")
        for probability, next_state, reward, terminated in env.unwrapped.P[state][action]:
            print(
                f"    Probability={probability:.4f}, "
                f"Next state={next_state}, "
                f"Reward={reward}, "
                f"Terminated={terminated}"
            )

env = gym.make(
    "FrozenLake-v1",
    map_name="4x4",
    is_slippery=True
)

for state in [0, 1, 14]:
    describe_state(env, state)
    print()

env.close()
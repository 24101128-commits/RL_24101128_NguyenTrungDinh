import gymnasium as gym

env = gym.make(
    "FrozenLake-v1",
    map_name="4x4",
    is_slippery=True
)

state = 0
print(f"Transitions for state {state}:")

for action in range(env.action_space.n):
    print(f"\nAction {action}:")
    for probability, next_state, reward, terminated in env.unwrapped.P[state][action]:
        print(f"  Probability: {probability}")
        print(f"  Next state: {next_state}")
        print(f"  Reward: {reward}")
        print(f"  Terminated: {terminated}")

env.close()
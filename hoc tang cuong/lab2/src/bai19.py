import gymnasium as gym
import numpy as np

env = gym.make(
    "FrozenLake-v1",
    map_name="4x4",
    is_slippery=True
)

all_valid = True
for state in range(env.observation_space.n):
    for action in range(env.action_space.n):
        probabilities = [
            probability
            for probability, next_state, reward, terminated
            in env.unwrapped.P[state][action]
        ]
        probability_sum = sum(probabilities)
        valid = np.isclose(probability_sum, 1.0)
        if not valid:
            print(
                f"Invalid transition at state={state}, "
                f"action={action}, "
                f"sum={probability_sum}"
            )
            all_valid = False

print("All transition probabilities valid:", all_valid)

env.close()
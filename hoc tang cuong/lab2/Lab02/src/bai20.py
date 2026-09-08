import gymnasium as gym

state = 0
action = 2  # RIGHT

for is_slippery in [False, True]:
    env = gym.make(
        "FrozenLake-v1",
        map_name="4x4",
        is_slippery=is_slippery
    )
    transitions = env.unwrapped.P[state][action]
    print(f"is_slippery={is_slippery}")
    print("Number of transitions:", len(transitions))
    for probability, next_state, reward, terminated in transitions:
        print(
            f"  Probability={probability:.4f}, "
            f"Next state={next_state}, "
            f"Reward={reward}, "
            f"Terminated={terminated}"
        )
    print()
    env.close()

# Khi is_slippery=False, action RIGHT dẫn đến một transition xác định.
# Khi is_slippery=True, một action có thể dẫn đến nhiều state kế tiếp.
# Mỗi transition có một xác suất riêng và tổng các xác suất bằng 1.
# Vì vậy môi trường stochastic phức tạp hơn và cần xét đầy đủ transition probability.
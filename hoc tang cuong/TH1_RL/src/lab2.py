import gymnasium as gym

def mountaincar_random():
    print("\n===== MOUNTAIN CAR RANDOM AGENT =====")

    env = gym.make("MountainCar-v0", render_mode="human")

    obs, info = env.reset()

    for step in range(500):

        # Chọn hành động ngẫu nhiên
        action = env.action_space.sample()

        # Thực hiện hành động
        obs, reward, terminated, truncated, info = env.step(action)

        # In kết quả
        print("Step:", step)
        print("Observation:", obs)
        print("Reward:", reward)

        # Nếu episode kết thúc
        if terminated or truncated:
            print("Episode finished!")
            obs, info = env.reset()

    env.close()


# GỌI HÀM
mountaincar_random()
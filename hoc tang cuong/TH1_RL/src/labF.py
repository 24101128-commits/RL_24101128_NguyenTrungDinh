import gymnasium as gym
import matplotlib.pyplot as plt
2
def human_render():

    print("===== HUMAN RENDER =====")

    env = gym.make("CartPole-v1", render_mode="human")

    obs, info = env.reset()

    try:

        for step in range(200):

            action = env.action_space.sample()

            obs, reward, terminated, truncated, info = env.step(action)

            print("Step:", step + 1)

            

            if terminated or truncated:
                obs, info = env.reset()

    except KeyboardInterrupt:
        print("\nĐã dừng!")

    env.close()


def rgb_render():

    print("===== RGB ARRAY RENDER =====")

    env = gym.make("CartPole-v1", render_mode="rgb_array")

    obs, info = env.reset()

    try:

        for step in range(100):

            action = env.action_space.sample()

            obs, reward, terminated, truncated, info = env.step(action)

            frame = env.render()

            plt.clf()
            plt.imshow(frame)
            plt.axis("off")
            plt.title("Step: " + str(step + 1))

            plt.pause(0.05)

            if terminated or truncated:
                obs, info = env.reset()

    except KeyboardInterrupt:
        print("\nĐã dừng!")

    plt.close()
    env.close()


def exercise_F():

    print("===== EXERCISE F =====")

    print("1. Human render")
    print("2. RGB array render")

    choice = input("Chọn: ")

    if choice == "1":
        human_render()

    elif choice == "2":
        rgb_render()

    else:
        print("Lựa chọn không hợp lệ!")


exercise_F()
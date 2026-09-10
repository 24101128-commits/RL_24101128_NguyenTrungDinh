import gymnasium as gym
import matplotlib.pyplot as plt


def exercise_C():

    print("===== EXERCISE C: CUSTOM RENDERING =====")

    env = gym.make("CartPole-v1", render_mode="rgb_array")

    obs, info = env.reset()

    plt.ion()

    try:
        while True:

            for step in range(100):

                action = env.action_space.sample()

                obs, reward, terminated, truncated, info = env.step(action)

                # Lấy hình ảnh
                frame = env.render()

                # Hiển thị hình ảnh
                plt.clf()
                plt.imshow(frame)
                plt.axis("off")
                plt.title("Step: " + str(step + 1))

                plt.pause(0.01)

                if terminated or truncated:
                    print("Episode finished!")
                    break

            

            # Bắt đầu episode mới
            obs, info = env.reset()

    except KeyboardInterrupt:
        print("\nĐã dừng chương trình!")

    plt.close()
    env.close()


exercise_C()
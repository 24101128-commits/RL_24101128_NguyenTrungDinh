import gymnasium as gym
import matplotlib.pyplot as plt


def exercise_D():

    print("===== EXERCISE D: EPISODE STATISTICS =====")

    env = gym.make("CartPole-v1")

    episode_lengths = []

    try:
        for episode in range(20):

            obs, info = env.reset()
            step = 0

            while True:

                action = env.action_space.sample()

                obs, reward, terminated, truncated, info = env.step(action)

                step += 1

            

                if terminated or truncated:
                    break

            episode_lengths.append(step)

            print("Episode:", episode + 1,
                  "| Steps:", step)

        env.close()

        # Vẽ histogram
        plt.hist(episode_lengths, bins=10)
        plt.xlabel("Episode Length")
        plt.ylabel("Number of Episodes")
        plt.title("CartPole Episode Lengths")
        plt.show()

    except KeyboardInterrupt:
        print("\nĐã dừng chương trình!")
        env.close()


exercise_D()
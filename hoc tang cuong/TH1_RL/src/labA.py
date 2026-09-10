import gymnasium as gym
import time

def exercise_A():
    print("===== EXERCISE A =====")

    env = gym.make("CartPole-v1", render_mode="human")

    episode = 1

    try:
        while True:
            print("\n===== EPISODE", episode, "=====")

            obs, info = env.reset()
            step = 0

            while True:
                action = env.action_space.sample()

                obs, reward, terminated, truncated, info = env.step(action)

                step += 1

                print("Step:", step)
                print("Action:", action)
                print("Reward:", reward)

              
                time.sleep(0.1)

                if terminated or truncated:
                    print("Episode finished!")
                    print("Total steps:", step)
                    break

            episode += 1

    except KeyboardInterrupt:
        print("\nĐã dừng chương trình!")

    env.close()


exercise_A()
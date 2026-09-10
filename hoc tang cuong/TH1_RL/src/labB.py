import gymnasium as gym
import time

def exercise_B():

    print("===== EXERCISE B: DETERMINISTIC VS STOCHASTIC =====")

    actions = [0, 1, 0, 1, 0, 1, 1, 0, 0, 1]

    for run in range(3):

        print("\n===== RUN", run + 1, "=====")

        env = gym.make("CartPole-v1")

        obs, info = env.reset(seed=42)

        for step in range(len(actions)):

            action = actions[step]

            obs, reward, terminated, truncated, info = env.step(action)

            print("Step:", step + 1)
            print("Action:", action)
            print("Observation:", obs)
            print("Reward:", reward)

            time.sleep(0.2)

            if terminated or truncated:
                print("Episode finished!")
                break

        env.close()


exercise_B()
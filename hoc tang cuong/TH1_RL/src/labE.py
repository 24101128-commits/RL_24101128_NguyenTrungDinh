import gymnasium as gym
import matplotlib.pyplot as plt
import time

def run_environment(env_name):

    env = gym.make(env_name)

    rewards = []

    for episode in range(20):

        obs, info = env.reset()

        total_reward = 0

        while True:

            action = env.action_space.sample()

            obs, reward, terminated, truncated, info = env.step(action)

            total_reward += reward

            time.sleep(0.01)

            if terminated or truncated:
                break

        rewards.append(total_reward)

        print(env_name,
              "| Episode:", episode + 1,
              "| Reward:", total_reward)

    env.close()

    return rewards


def exercise_E():

    print("===== EXERCISE E: REWARD ANALYSIS =====")

    cartpole_rewards = run_environment("CartPole-v1")

    mountaincar_rewards = run_environment("MountainCar-v0")

    cartpole_average = sum(cartpole_rewards) / len(cartpole_rewards)

    mountaincar_average = sum(mountaincar_rewards) / len(mountaincar_rewards)

    print("\n===== AVERAGE REWARD =====")
    print("CartPole:", cartpole_average)
    print("MountainCar:", mountaincar_average)

    # Vẽ biểu đồ
    plt.plot(cartpole_rewards, label="CartPole")
    plt.plot(mountaincar_rewards, label="MountainCar")

    plt.xlabel("Episode")
    plt.ylabel("Cumulative Reward")
    plt.title("Reward over 20 Episodes")
    plt.legend()
    plt.show()


exercise_E()
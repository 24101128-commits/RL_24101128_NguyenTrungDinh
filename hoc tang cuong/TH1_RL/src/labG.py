import gymnasium as gym
import pygame

def exercise_G():

    print("===== EXERCISE G: KEYBOARD CONTROL =====")
    print("LEFT  = Move left")
    print("RIGHT = Move right")
    print("ESC   = Quit")

    pygame.init()

    env = gym.make("CartPole-v1", render_mode="human")

    obs, info = env.reset()

    running = True

    try:

        while running:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        running = False

                    elif event.key == pygame.K_LEFT:

                        action = 0

                        obs, reward, terminated, truncated, info = env.step(action)

                        print("Action: LEFT | Reward:", reward)

                    elif event.key == pygame.K_RIGHT:

                        action = 1

                        obs, reward, terminated, truncated, info = env.step(action)

                        print("Action: RIGHT | Reward:", reward)

                    if terminated or truncated:

                        print("Episode finished!")

                        obs, info = env.reset()

            

    except KeyboardInterrupt:
        print("\nĐã dừng!")

    env.close()
    pygame.quit()


exercise_G()
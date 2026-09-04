"""
Phan 8. Chuyen code Gym cu sang Gymnasium.

Code cu (API Gym cu - KHONG duoc dung):
    import gym
    env = gym.make("CartPole-v0")
    observation = env.reset()
    for t in range(1000):
        env.render()
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        if done:
            break

Code moi ben duoi da duoc viet lai hoan toan theo Gymnasium hien tai.
"""

import gymnasium as gym


def main():
    env = gym.make("CartPole-v1")  # CartPole-v0 da bi loai bo, dung CartPole-v1

    # API moi: reset() tra ve (observation, info) thay vi chi observation
    observation, info = env.reset(seed=42)

    for t in range(1000):
        action = env.action_space.sample()

        # API moi: step() tra ve 5 gia tri thay vi 4
        observation, reward, terminated, truncated, info = env.step(action)

        # terminated co y nghia gi?
        # terminated = True khi agent den mot trang thai ket thuc "tu nhien"
        # theo dinh nghia cua bai toan (vi du: pole nga qua goc gioi han,
        # xe di ra khoi bien, hoac trong FrozenLake la roi xuong ho / den goal).

        # truncated co y nghia gi?
        # truncated = True khi episode bi dung boi mot gioi han BEN NGOAI
        # ban chat bai toan, vi du da vuot qua so buoc toi da cho phep
        # (time limit), chu khong phai vi agent thuc su "thua" hay "thang".

        # Vi sao khong nen dung done cua API cu?
        # API cu gop terminated va truncated thanh mot bien done duy nhat,
        # khien ta khong the phan biet duoc episode ket thuc vi ly do
        # tu nhien (terminated) hay vi bi cat ngang boi gioi han thoi gian
        # (truncated). Su phan biet nay rat quan trong trong RL, dac biet
        # khi tinh gia tri return/bootstrapping, vi mot trang thai bi
        # truncated van co the con gia tri tuong lai, trong khi trang thai
        # terminated thi khong.

        episode_finished = terminated or truncated
        if episode_finished:
            print(f"Episode ket thuc o buoc {t}, terminated={terminated}, truncated={truncated}")
            break

    env.close()


if __name__ == "__main__":
    main()

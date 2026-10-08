import gymnasium as gym
import matplotlib.pyplot as plt

def stick_on_20_policy(state):
    player_sum, dealer_card, usable_ace = state
    if player_sum >= 20:
        return 0
    else:
        return 1

def generate_episode(env, policy, seed=None):
    state, info = env.reset(seed=seed)
    episode = []
    while True:
        action = policy(state)
        next_state, reward, terminated, truncated, info = env.step(action)
        episode.append((state, action, reward))
        state = next_state
        if terminated or truncated:
            break
    return episode

def compute_returns(rewards, gamma=1.0):
    returns = []
    for t in range(len(rewards)):
        G = 0
        for k in range(t, len(rewards)):
            G += (gamma ** (k - t)) * rewards[k]
        returns.append(G)
    return returns

env = gym.make("Blackjack-v1")
target_state = (20, 10, 0)
checkpoints = [100, 500, 1000, 5000, 10000]
state_returns = []
values = []

for episode_number in range(1, 10001):
    episode = generate_episode(
        env,
        stick_on_20_policy,
        seed=episode_number
    )
    rewards = [
        reward
        for state, action, reward in episode
    ]
    returns = compute_returns(
        rewards,
        gamma=1.0
    )
    for (state, action, reward), G in zip(episode, returns):
        if state == target_state:
            state_returns.append(G)
    if episode_number in checkpoints:
        if len(state_returns) > 0:
            V = sum(state_returns) / len(state_returns)
        else:
            V = 0
        values.append(V)
        print(f"Episodes: {episode_number}")
        print(f"V({target_state}) = {V:.4f}")
        print()

print("Nhận xét:")
print("- Khi số episode tăng, giá trị V(s) dần ổn định.")
print("- Số episode càng lớn thì ước lượng V(s) càng ít dao động.")

import os

plt.figure(figsize=(8, 5))

plt.plot(
    checkpoints,
    values,
    marker="o"
)

plt.xlabel("Number of Episodes")
plt.ylabel("V(s)")
plt.title("Convergence of V(s)")
plt.grid(True)

current_dir = os.path.dirname(os.path.abspath(__file__))
lab03_dir = os.path.dirname(current_dir)
figures_dir = os.path.join(lab03_dir, "figures")
os.makedirs(figures_dir, exist_ok=True)

save_path = os.path.join(
    figures_dir,
    "mc_prediction_convergence_bai15.png"
)

plt.savefig(
    save_path,
    dpi=300,
    bbox_inches="tight"
)

plt.show()
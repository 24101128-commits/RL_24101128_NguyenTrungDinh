import os
import matplotlib.pyplot as plt

def compute_returns(rewards, gamma=1.0):
    """
    Calculate returns for all time steps.
    """
    returns = []
    for t in range(len(rewards)):
        G = 0
        for k in range(t, len(rewards)):
            G += (gamma ** (k - t)) * rewards[k]
        returns.append(G)
    return returns

rewards = [0, 0, 1]
gammas = [1.0, 0.9, 0.5]

all_returns = {}

for gamma in gammas:
    returns = compute_returns(rewards, gamma)
    all_returns[gamma] = returns
    print(f"Gamma = {gamma}")
    print(f"Returns: {returns}")
    print("-" * 40)

steps = [0, 1, 2]

for gamma in gammas:
    plt.plot(
        steps,
        all_returns[gamma],
        marker="o",
        label=f"gamma = {gamma}"
    )

plt.xlabel("Time step")
plt.ylabel("Return")
plt.title("Comparison of Returns for Different Gamma")
plt.xticks(steps)
plt.legend()
plt.grid(True)

current_dir = os.path.dirname(os.path.abspath(__file__))
lab03_dir = os.path.dirname(current_dir)
figures_dir = os.path.join(lab03_dir, "figures")

os.makedirs(figures_dir, exist_ok=True)

save_path = os.path.join(
    figures_dir,
    "return_gamma_comparison.png"
)

plt.savefig(save_path, dpi=300, bbox_inches="tight")
plt.show()
plt.close()
import numpy as np
import matplotlib.pyplot as plt

def compute_return(rewards, gamma):
    total = 0.0
    for t, reward in enumerate(rewards):
        total += (gamma ** t) * reward
    return total

rewards = [0, 0, 0, 0, 10]
gammas = np.linspace(0, 1, 101)
returns = []
for gamma in gammas:
    returns.append(compute_return(rewards, gamma))

plt.plot(gammas, returns)
plt.title("G0 theo Gamma")
plt.xlabel("Gamma")
plt.ylabel("G0")
plt.grid()
plt.savefig("figures/gamma_comparison.png")
plt.show()
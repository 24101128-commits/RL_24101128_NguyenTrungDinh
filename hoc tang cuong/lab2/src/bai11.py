import numpy as np

def compute_return(rewards, gamma):
    total = 0.0
    for t, reward in enumerate(rewards):
        total += (gamma ** t) * reward
    return total

sequence_A = [5, 0, 0, 0, 0]
sequence_B = [0, 0, 0, 0, 10]
gammas = np.linspace(0, 1, 1001)
better_gammas = []

for gamma in gammas:
    return_A = compute_return(sequence_A, gamma)
    return_B = compute_return(sequence_B, gamma)

    if return_B > return_A:
        better_gammas.append(gamma)
if better_gammas:
    print(f"Gamma range where B > A: {better_gammas[0]:.3f} to {better_gammas[-1]:.3f}")
else:
    print("There is no gamma where B > A.")
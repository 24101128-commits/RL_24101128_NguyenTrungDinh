def compute_return(rewards, gamma):
    total = 0.0
    for t, reward in enumerate(rewards):
        total += (gamma ** t) * reward
    return total

rewards = [1, 1, 1, 1, 1]
gammas = [0.0, 0.5, 0.9, 0.99, 1.0]
print("Gamma | Return")
print("------|-------")

for gamma in gammas:
    G = compute_return(rewards, gamma)
    print(f"{gamma:5.2f} | {G:.4f}")

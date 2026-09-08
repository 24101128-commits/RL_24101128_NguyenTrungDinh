def compute_return(rewards, gamma):
    total = 0.0
    for t, reward in enumerate(rewards):
        total += (gamma ** t) * reward
    return total

rewards = [1, 1, 1, 1, 1]
gamma = 1.0
G = compute_return(rewards, gamma)

print("Rewards:", rewards)
print("Gamma:", gamma)
print("Return:", G)
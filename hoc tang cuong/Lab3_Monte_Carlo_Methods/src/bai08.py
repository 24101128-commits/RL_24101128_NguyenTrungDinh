def compute_returns(rewards, gamma=1.0):
    """
    Calculate the return G_t for each time step.
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

for gamma in gammas:
    returns = compute_returns(rewards, gamma)
    print(f"Gamma = {gamma}")
    print(f"Rewards: {rewards}")
    print(f"Returns: {returns}")
    print("-" * 40)
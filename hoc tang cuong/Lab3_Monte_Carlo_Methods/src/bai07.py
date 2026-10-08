def compute_returns(rewards, gamma=1.0):
    """
    Calculate the return G_t for each time step.

    Args:
        rewards: List of rewards.
        gamma: Discount factor.

    Returns:
        List of returns.
    """
    returns = []
    for t in range(len(rewards)):
        G = 0
        for k in range(t, len(rewards)):
            G += (gamma ** (k - t)) * rewards[k]
        returns.append(G)
    return returns

rewards = [0, 0, 1]
returns = compute_returns(rewards, gamma=1.0)

print("Rewards:", rewards)
print("Returns:", returns)
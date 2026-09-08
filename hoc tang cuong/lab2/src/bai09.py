def discounted_returns(rewards, gamma):
    returns = [0.0] * len(rewards)
    returns[-1] = rewards[-1]
    for t in range(len(rewards) - 2, -1, -1):
        returns[t] = rewards[t] + gamma * returns[t + 1]
    return returns

rewards = [0, 0, 0, 1]
gamma = 0.9
returns = discounted_returns(rewards, gamma)

print("Rewards:", rewards)
print("Gamma:", gamma)
print("Discounted returns:", returns)
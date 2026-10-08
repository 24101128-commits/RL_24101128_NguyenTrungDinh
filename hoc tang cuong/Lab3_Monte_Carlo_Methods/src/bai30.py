import gymnasium as gym

env = gym.make("Blackjack-v1")
Q = {}
num_actions = env.action_space.n

print("Q(s,a) Initialization")
print("=" * 50)
print("Number of actions:", num_actions)
print("Initial number of state-action pairs:", len(Q))
print()
print("Q =", Q)

env.close()
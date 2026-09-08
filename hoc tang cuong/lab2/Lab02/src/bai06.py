import numpy as np

P = np.array([
    [0.7, 0.2, 0.1],
    [0.3, 0.5, 0.2],
    [0.2, 0.3, 0.5]
])

def sample_next_state(current_state, P, rng):
    return rng.choice(len(P), p=P[current_state])

rng = np.random.default_rng(42)
n_transitions = 100000
current_state = 0
counts = np.zeros(len(P), dtype=int)

for _ in range(n_transitions):
    current_state = sample_next_state(current_state, P, rng)
    counts[current_state] += 1

simulated_distribution = counts / n_transitions
p0 = np.array([1.0, 0.0, 0.0])
theoretical_distribution = p0.copy()

for _ in range(50):
    theoretical_distribution = theoretical_distribution @ P

print("Simulated distribution:", simulated_distribution)
print("Theoretical distribution:", theoretical_distribution)
print(
    "Absolute difference:",
    np.abs(simulated_distribution - theoretical_distribution)
)

# Với số lượng transition lớn, distribution mô phỏng tiến gần distribution lý thuyết.
# Sai khác nhỏ xuất hiện do quá trình mô phỏng có tính ngẫu nhiên.
# Khi tăng số transition, kết quả mô phỏng thường ổn định hơn.
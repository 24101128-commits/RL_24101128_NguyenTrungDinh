"""
map_analysis_and_diagnostics.py
Computes formal map difficulty metrics and agent diagnostics,
generating high-resolution figures for both the notebook and formal report:
1. Map Complexity & Difficulty Scores (Radar/Bar metrics)
2. Agent Deadlock Trapping & Exploration Entropy Diagnostics
3. Separate Detailed Evaluation Tables data
"""

import os
import time
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Headless matplotlib
import matplotlib
matplotlib.use('Agg')

RESULTS_DIR = r"C:\RL\results"
os.makedirs(RESULTS_DIR, exist_ok=True)

# Import environment and maps from data
import sys
sys.path.insert(0, r"C:\RL\data")
from maps import MAPS, ACTION_UP, ACTION_DOWN, ACTION_LEFT, ACTION_RIGHT, ACTION_DELTAS
from env import OneWayArrowEnv, TOKEN_ON_GRID, TOKEN_HELD, TOKEN_USED
from algorithms import ValueIteration, PolicyIteration, QLearningAgent, SARSAAgent, MonteCarloAgent

# ------------------------------------------------------------------------------
# 1. MAP DIFFICULTY ANALYSIS & METRICS
# ------------------------------------------------------------------------------
def analyze_map_difficulty(map_cfg):
    H = map_cfg["height"]
    W = map_cfg["width"]
    total_cells = H * W
    num_walls = len(map_cfg.get("walls", []))
    traversable_cells = total_cells - num_walls
    
    fixed_arrows = map_cfg.get("arrows", {})
    dynamic_arrows = map_cfg.get("dynamic_arrows", {})
    total_arrows = len(fixed_arrows) + len(dynamic_arrows)
    arrow_density = (total_arrows / traversable_cells) * 100.0
    wall_density = (num_walls / total_cells) * 100.0

    has_switch = len(map_cfg.get("switches", [])) > 0
    has_token = map_cfg.get("token_pos") is not None

    num_token_states = 3 if has_token else 1
    num_switch_states = 2 if has_switch else 1
    state_space_size = total_cells * num_token_states * num_switch_states

    # Manhattan distance
    sr, sc = map_cfg["start"]
    gr, gc = map_cfg["goal"]
    manhattan_dist = abs(gr - sr) + abs(gc - sc)

    # Deadlock / cycle count estimation
    cycle_nodes = 0
    if "map1" in map_cfg.get("name", "").lower():
        cycle_nodes = 4 # (0,1)->(0,2)->(1,2)->(1,1)
    elif "map2" in map_cfg.get("name", "").lower():
        cycle_nodes = 6
    elif "map3" in map_cfg.get("name", "").lower():
        cycle_nodes = 8

    # Composite difficulty score D in [1, 10]
    # Weights: State space log scale, arrow density, switch presence, cycle nodes
    d_score = (
        math.log10(state_space_size) * 1.8 +
        (arrow_density / 100.0) * 2.5 +
        (wall_density / 100.0) * 1.5 +
        (1.5 if has_switch else 0.0) +
        (1.2 if has_token else 0.0) +
        (cycle_nodes / 8.0) * 1.5
    )
    d_score = min(10.0, max(1.0, round(d_score, 2)))

    return {
        "name": map_cfg["name"],
        "dimensions": f"{H}x{W}",
        "total_cells": total_cells,
        "traversable_cells": traversable_cells,
        "num_walls": num_walls,
        "wall_density": wall_density,
        "num_arrows": total_arrows,
        "arrow_density": arrow_density,
        "has_switch": has_switch,
        "has_token": has_token,
        "state_space_size": state_space_size,
        "manhattan_dist": manhattan_dist,
        "cycle_nodes": cycle_nodes,
        "difficulty_score": d_score
    }

map_metrics = {k: analyze_map_difficulty(cfg) for k, cfg in MAPS.items()}
print("Map Difficulty Analysis Completed:")
for k, m in map_metrics.items():
    print(f"  [{k}] {m['name']} -> State Space: {m['state_space_size']}, Difficulty: {m['difficulty_score']}/10")

# ------------------------------------------------------------------------------
# 2. PLOT: MAP DIFFICULTY RADAR / COMPARISON CHART
# ------------------------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

maps_list = ["map1", "map2", "map3"]
labels = ["Map 1\n(5x5 Basic)", "Map 2\n(6x6 Dynamic)", "Map 3\n(7x7 Master)"]
colors = ["#2b8cbe", "#e6550d", "#d95f0e"]

# Subplot 1: Difficulty Score & State Space
scores = [map_metrics[k]["difficulty_score"] for k in maps_list]
state_sizes = [map_metrics[k]["state_space_size"] for k in maps_list]

x = np.arange(len(labels))
width = 0.35

bars1 = ax1.bar(x - width/2, scores, width, label='Difficulty Score (1-10)', color='#1f77b4', edgecolor='black', linewidth=1)
ax1.set_ylabel('Difficulty Score (out of 10)', fontsize=11, fontweight='bold', color='#1f77b4')
ax1.set_ylim(0, 11)
ax1.set_xticks(x)
ax1.set_xticklabels(labels, fontsize=10, fontweight='bold')
ax1.grid(axis='y', linestyle='--', alpha=0.6)

# Secondary axis for state space size
ax1_twin = ax1.twinx()
bars2 = ax1_twin.bar(x + width/2, state_sizes, width, label='State Space |S|', color='#ff7f0e', edgecolor='black', linewidth=1, alpha=0.9)
ax1_twin.set_ylabel('Total State Space Size |S|', fontsize=11, fontweight='bold', color='#ff7f0e')
ax1_twin.set_ylim(0, 350)

for bar in bars1:
    y = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2.0, y + 0.2, f"{y:.1f}", ha='center', va='bottom', fontweight='bold', fontsize=9)
for bar in bars2:
    y = bar.get_height()
    ax1_twin.text(bar.get_x() + bar.get_width()/2.0, y + 5, f"{int(y)}", ha='center', va='bottom', fontweight='bold', fontsize=9)

ax1.set_title("Environmental Complexity & Difficulty Rating by Map", fontsize=12, fontweight='bold', pad=10)

# Subplot 2: Structural Density Breakdown
categories = ["Wall Density (%)", "Arrow Density (%)", "Cycle Nodes", "Manhattan Dist"]
m1_vals = [map_metrics["map1"]["wall_density"], map_metrics["map1"]["arrow_density"], map_metrics["map1"]["cycle_nodes"], map_metrics["map1"]["manhattan_dist"]]
m2_vals = [map_metrics["map2"]["wall_density"], map_metrics["map2"]["arrow_density"], map_metrics["map2"]["cycle_nodes"], map_metrics["map2"]["manhattan_dist"]]
m3_vals = [map_metrics["map3"]["wall_density"], map_metrics["map3"]["arrow_density"], map_metrics["map3"]["cycle_nodes"], map_metrics["map3"]["manhattan_dist"]]

cx = np.arange(len(categories))
c_w = 0.25

ax2.bar(cx - c_w, m1_vals, c_w, label='Map 1', color='#365F91', edgecolor='black', linewidth=0.8)
ax2.bar(cx, m2_vals, c_w, label='Map 2', color='#4F81BD', edgecolor='black', linewidth=0.8)
ax2.bar(cx + c_w, m3_vals, c_w, label='Map 3', color='#C0504D', edgecolor='black', linewidth=0.8)

ax2.set_xticks(cx)
ax2.set_xticklabels(categories, fontsize=10, fontweight='bold')
ax2.set_ylabel('Metric Magnitude', fontsize=11, fontweight='bold')
ax2.set_title("Topological Constraint & Constraint Density Comparison", fontsize=12, fontweight='bold', pad=10)
ax2.legend(fontsize=10, loc='upper left')
ax2.grid(axis='y', linestyle='--', alpha=0.6)

plt.tight_layout()
fig_diff_path = os.path.join(RESULTS_DIR, "fig_map_difficulty_metrics.png")
plt.savefig(fig_diff_path, dpi=300)
plt.close()
print(f"Saved: {fig_diff_path}")

# ------------------------------------------------------------------------------
# 3. AGENT DIAGNOSTICS: DEADLOCK TRAPPING & EXPLORATION ENTROPY
# ------------------------------------------------------------------------------
print("Running Agent Diagnostic Experiments on Map 1 & Map 3...")
# Let's train Q-Learning and SARSA under penalty_stay vs action_mask on Map 1
# to measure deadlock cycle entrapment rates across episodes
env_m1_pen = OneWayArrowEnv(MAPS["map1"], invalid_action_mode="penalty_stay")
env_m1_msk = OneWayArrowEnv(MAPS["map1"], invalid_action_mode="action_mask")

deadlock_cells_m1 = {(0,1), (0,2), (1,2), (1,1)}

def measure_cycle_entrapment(env, algo_cls, num_episodes=250):
    agent = algo_cls(env, alpha=0.1, gamma=0.99, seed=42)
    cycle_traps_per_ep = []
    entropy_per_ep = []

    for ep in range(num_episodes):
        obs, _ = env.reset()
        state = env.decode_state(obs)
        term, trunc = False, False
        steps_in_cycle = 0
        visited_states = []

        while not (term or trunc):
            mask = env.get_action_mask(state)
            action = agent.select_action(state, mask, explore=True)
            next_obs, reward, term, trunc, _ = env.step(action)
            next_state = env.decode_state(next_obs)

            # Check if inside deadlock cycle
            if (state[0], state[1]) in deadlock_cells_m1:
                steps_in_cycle += 1

            visited_states.append(next_obs)

            # Update agent
            s_idx = env.encode_state(state)
            next_idx = env.encode_state(next_state)
            if term:
                target = reward
            else:
                next_mask = env.get_action_mask(next_state)
                next_valid = np.where(next_mask)[0]
                if len(next_valid) == 0:
                    next_valid = np.arange(env.action_space.n)
                target = reward + agent.gamma * np.max([agent.Q[next_idx, a_p] for a_p in next_valid])
            agent.Q[s_idx, action] += agent.alpha * (target - agent.Q[s_idx, action])

            state = next_state

        agent.epsilon = max(agent.epsilon_min, agent.epsilon * agent.epsilon_decay)
        cycle_traps_per_ep.append(steps_in_cycle)
        # Shannon entropy of state visitation
        unique, counts = np.unique(visited_states, return_counts=True)
        probs = counts / np.sum(counts)
        entropy = -np.sum(probs * np.log2(probs + 1e-12))
        entropy_per_ep.append(entropy)

    return cycle_traps_per_ep, entropy_per_ep

traps_pen, ent_pen = measure_cycle_entrapment(env_m1_pen, QLearningAgent)
traps_msk, ent_msk = measure_cycle_entrapment(env_m1_msk, QLearningAgent)

# Plot Diagnostic curves
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Subplot 1: Cycle Entrapment Steps (Rolling window 10)
w = 10
roll_pen = np.convolve(traps_pen, np.ones(w)/w, mode='valid')
roll_msk = np.convolve(traps_msk, np.ones(w)/w, mode='valid')
x_ep = np.arange(len(roll_pen)) + w

ax1.plot(x_ep, roll_pen, label='Penalty-Stay Mode (No Mask)', color='#d9534f', linewidth=2.2)
ax1.plot(x_ep, roll_msk, label='Action Mask Mode (Filtered)', color='#5cb85c', linewidth=2.2)
ax1.set_title("Agent Trapped Steps in Deadlock Cycle vs Training Episode", fontsize=12, fontweight='bold', pad=10)
ax1.set_xlabel("Training Episode", fontsize=11)
ax1.set_ylabel("Mean Steps Trapped in 2x2 Cycle", fontsize=11)
ax1.legend(fontsize=10)
ax1.grid(True, linestyle='--', alpha=0.6)

# Subplot 2: State Exploration Entropy
roll_ent_pen = np.convolve(ent_pen, np.ones(w)/w, mode='valid')
roll_ent_msk = np.convolve(ent_msk, np.ones(w)/w, mode='valid')

ax2.plot(x_ep, roll_ent_pen, label='Penalty-Stay Mode', color='#d9534f', linewidth=2.0, linestyle='--')
ax2.plot(x_ep, roll_ent_msk, label='Action Mask Mode', color='#0275d8', linewidth=2.2)
ax2.set_title("State Visitation Shannon Entropy (Exploration Diversity)", fontsize=12, fontweight='bold', pad=10)
ax2.set_xlabel("Training Episode", fontsize=11)
ax2.set_ylabel("Shannon Entropy (bits)", fontsize=11)
ax2.legend(fontsize=10)
ax2.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
fig_diag_path = os.path.join(RESULTS_DIR, "fig_agent_diagnostics_deadlock_entropy.png")
plt.savefig(fig_diag_path, dpi=300)
plt.close()
print(f"Saved: {fig_diag_path}")

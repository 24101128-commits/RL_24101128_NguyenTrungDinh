"""
train.py - Experiment Runner and Model Training for One-Way Arrow Grid.
Executes:
1. Value Iteration exact solving across all 3 maps.
2. Tabular Q-learning multi-seed training (5 seeds) for all 3 maps.
3. Comparative Experiment: 'penalty_stay' vs 'action_mask' invalid action handling.
4. Comparative Experiment: Reward configurations & penalty sensitivity analysis.
5. Generates and saves all visual plots to results/ directory.
"""

import os
import sys
import time
from typing import Dict, Any, List, Tuple
import numpy as np

# Ensure data/ directory is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import maps
from env import OneWayArrowEnv, TOKEN_ON_GRID, TOKEN_HELD, TOKEN_USED
from algorithms import ValueIteration, QLearningAgent
from visualize import (
    plot_grid_layout, plot_policy_and_values,
    plot_learning_curves, plot_trajectory
)

# Results directory is relative to the data/ folder
RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

SEEDS = [42, 100, 2026, 777, 999]
NUM_EPISODES = 250


def run_value_iteration_experiments() -> Dict[str, Any]:
    """
    Experiment 1: Solve all 3 maps with Value Iteration.
    Reports state space size, convergence, and optimal policy metrics.
    """
    print("\n" + "=" * 60)
    print("1. RUNNING VALUE ITERATION ON ALL MAPS")
    print("=" * 60)
    vi_results = {}

    for map_key in ["map1", "map2", "map3"]:
        cfg = maps.MAPS[map_key]
        env = OneWayArrowEnv(cfg, invalid_action_mode="action_mask")
        vi = ValueIteration(env, gamma=0.99, theta=1e-4, max_iterations=1500)

        start_time = time.time()
        V, policy, iters = vi.solve()
        elapsed = time.time() - start_time

        # Get V*(start)
        _, info = env.reset()
        s_init = info["state_tuple"]
        start_v = V[env.encode_state(s_init)]

        # Evaluate optimal policy with a rollout
        eval_res = vi.evaluate_policy()

        vi_results[map_key] = {
            "name": cfg["name"],
            "states": env.num_states,
            "actions": env.action_space.n,
            "iterations": iters,
            "time_sec": elapsed,
            "start_v": start_v,
            "optimal_steps": eval_res["steps"],
            "optimal_reward": eval_res["total_reward"],
            "success": eval_res["success"],
            "V": V,
            "policy": policy,
            "env": env
        }

        print(f"[{map_key.upper()}] {cfg['name']}")
        print(f"   State Space: {env.num_states} | Action Space: {env.action_space.n}")
        print(f"   Iterations: {iters} | Runtime: {elapsed*1000:.2f} ms | V*(s_start): {start_v:.2f}")
        print(f"   Optimal Policy: {eval_res['steps']} steps | Return: {eval_res['total_reward']:.1f} | Success: {eval_res['success']}")

        # Plot layout
        plot_grid_layout(
            env,
            switch_state=0,
            title=f"{cfg['name']} Layout",
            save_path=os.path.join(RESULTS_DIR, f"{map_key}_layout.png")
        )

    # Plot optimal policy & values for Map 1 and Map 3
    env1 = vi_results["map1"]["env"]
    plot_policy_and_values(
        env1, vi_results["map1"]["V"], vi_results["map1"]["policy"],
        switch_state=0, token_status=0,
        title="Map 1: Optimal Policy & Value Function (Value Iteration)",
        save_path=os.path.join(RESULTS_DIR, "map1_policy_vi.png")
    )

    env3 = vi_results["map3"]["env"]
    # With token held (tok=1, switch=0)
    plot_policy_and_values(
        env3, vi_results["map3"]["V"], vi_results["map3"]["policy"],
        switch_state=0, token_status=TOKEN_HELD,
        title="Map 3: Optimal Policy with Override Token Held (Tok=1, Sw=0)",
        save_path=os.path.join(RESULTS_DIR, "map3_policy_vi_tok_held.png")
    )
    # After token used and switch toggled (tok=2, switch=1)
    plot_policy_and_values(
        env3, vi_results["map3"]["V"], vi_results["map3"]["policy"],
        switch_state=1, token_status=TOKEN_USED,
        title="Map 3: Optimal Policy after Token Used (Tok=2, Sw=1)",
        save_path=os.path.join(RESULTS_DIR, "map3_policy_vi_tok_used.png")
    )

    return vi_results


def run_qlearning_multi_seed_experiments() -> Dict[str, Any]:
    """
    Experiment 2: Multi-seed Q-Learning on all 3 maps.
    Trains 5 seeds, reports mean/std of final performance.
    """
    print("\n" + "=" * 60)
    print("2. RUNNING MULTI-SEED Q-LEARNING ON ALL MAPS")
    print("=" * 60)

    curves_data = {}
    summary = {}

    for map_key in ["map1", "map2", "map3"]:
        cfg = maps.MAPS[map_key]
        all_returns = []
        all_steps = []
        all_success = []

        for seed in SEEDS:
            env = OneWayArrowEnv(cfg, invalid_action_mode="action_mask")
            agent = QLearningAgent(
                env,
                alpha=0.15,
                gamma=0.99,
                epsilon_start=1.0,
                epsilon_min=0.05,
                epsilon_decay=0.985,
                seed=seed
            )
            train_res = agent.train(num_episodes=NUM_EPISODES)
            all_returns.append(train_res["returns"].tolist())
            all_steps.append(train_res["steps"].tolist())
            all_success.append(train_res["success"].tolist())

        arr_returns = np.array(all_returns)
        arr_steps = np.array(all_steps)
        arr_success = np.array(all_success)

        curves_data[cfg["name"]] = {
            "returns": arr_returns,
            "steps": arr_steps
        }

        mean_ret = float(np.mean(arr_returns[:, -10:]))
        mean_steps = float(np.mean(arr_steps[:, -10:]))
        success_rate = float(np.mean(arr_success[:, -10:]))
        summary[map_key] = {
            "mean_return_last10": mean_ret,
            "mean_steps_last10": mean_steps,
            "success_rate_last10": success_rate
        }
        print(f"[{map_key.upper()}] 5 Seeds | "
              f"Final Return: {mean_ret:.1f} | "
              f"Final Steps: {mean_steps:.1f} | "
              f"Success Rate: {success_rate * 100:.0f}%")

    plot_learning_curves(
        curves_data,
        title="Q-Learning Across 3 Environments (5 Seeds, Shaded = ±1 SD)",
        save_path=os.path.join(RESULTS_DIR, "curve_qlearning_all_maps.png")
    )
    return summary


def run_invalid_action_mode_comparison() -> Dict[str, Any]:
    """
    Experiment 3: Compare 'penalty_stay' vs 'action_mask' on Map 1.
    Runs 5 seeds per mode and reports convergence curves.
    """
    print("\n" + "=" * 60)
    print("3. COMPARING INVALID ACTION HANDLING: PENALTY & STAY VS ACTION MASKING")
    print("=" * 60)

    comparison_data = {}
    summary = {}

    for mode, label in [
        ("action_mask", "Action Masking (Excluded)"),
        ("penalty_stay", "Penalty & Stay (-10 penalty)")
    ]:
        all_returns = []
        all_steps = []

        for seed in SEEDS:
            env = OneWayArrowEnv(maps.MAPS["map1"], invalid_action_mode=mode, invalid_penalty=-10.0)
            agent = QLearningAgent(
                env,
                alpha=0.15,
                gamma=0.99,
                epsilon_start=1.0,
                epsilon_min=0.05,
                epsilon_decay=0.985,
                seed=seed
            )
            train_res = agent.train(num_episodes=NUM_EPISODES)
            all_returns.append(train_res["returns"].tolist())
            all_steps.append(train_res["steps"].tolist())

        arr_returns = np.array(all_returns)
        arr_steps = np.array(all_steps)

        comparison_data[label] = {
            "returns": arr_returns,
            "steps": arr_steps
        }
        mean_ret = float(np.mean(arr_returns[:, -10:]))
        summary[label] = {"mean_return_last10": mean_ret}
        print(f"[{mode.upper()}] Mean final 10 eps return: {mean_ret:.1f}")

    plot_learning_curves(
        comparison_data,
        title="Invalid Action Mechanism Comparison on Map 1 (5 Seeds)",
        save_path=os.path.join(RESULTS_DIR, "curve_penalty_vs_mask.png")
    )
    return summary


def run_reward_sensitivity_experiments() -> Dict[str, Any]:
    """
    Experiment 4: Reward configuration sensitivity analysis on Map 2.
    Tests 3 reward setups to understand impact on convergence and policy.
    """
    print("\n" + "=" * 60)
    print("4. EXPERIMENTING WITH REWARD CONFIGURATIONS")
    print("=" * 60)

    configs = [
        ("Config A (Default)", -1.0, 100.0, -10.0),
        ("Config B (Severe Penalty)", -1.0, 100.0, -50.0),
        ("Config C (Zero Step Cost)", 0.0, 100.0, -10.0),
    ]

    reward_data = {}
    summary = {}

    for label, step_cost, goal_rew, invalid_pen in configs:
        all_returns = []
        all_steps = []

        for seed in SEEDS:
            env = OneWayArrowEnv(
                maps.MAPS["map2"],
                invalid_action_mode="penalty_stay",
                step_cost=step_cost,
                goal_reward=goal_rew,
                invalid_penalty=invalid_pen
            )
            agent = QLearningAgent(
                env,
                alpha=0.15,
                gamma=0.99,
                epsilon_start=1.0,
                epsilon_min=0.05,
                epsilon_decay=0.985,
                seed=seed
            )
            train_res = agent.train(num_episodes=NUM_EPISODES)
            all_returns.append(train_res["returns"].tolist())
            all_steps.append(train_res["steps"].tolist())

        arr_returns = np.array(all_returns)
        arr_steps = np.array(all_steps)

        reward_data[label] = {
            "returns": arr_returns,
            "steps": arr_steps
        }
        mean_ret = float(np.mean(arr_returns[:, -10:]))
        summary[label] = {
            "mean_return_last10": mean_ret,
            "step_cost": step_cost,
            "invalid_penalty": invalid_pen
        }
        print(f"[{label}] Final Return: {mean_ret:.1f}")

    plot_learning_curves(
        reward_data,
        title="Reward Configuration Sensitivity on Map 2 (5 Seeds)",
        save_path=os.path.join(RESULTS_DIR, "curve_reward_configurations.png")
    )
    return summary


def generate_demo_trajectories(vi_results: Dict[str, Any]):
    """
    Experiment 5: Generate and visualize demo trajectories for Map 1 and Map 3.
    """
    print("\n" + "=" * 60)
    print("5. GENERATING DEMO TRAJECTORIES USING OPTIMAL POLICIES")
    print("=" * 60)

    for map_key in ["map1", "map3"]:
        res = vi_results[map_key]
        env = res["env"]
        policy = res["policy"]

        obs, info = env.reset()
        trajectory = [info["state_tuple"][:2]]
        terminated = truncated = False

        while not (terminated or truncated):
            s_idx = env.encode_state(info["state_tuple"])
            a = policy[s_idx]
            obs, r, terminated, truncated, info = env.step(a)
            trajectory.append(info["state_tuple"][:2])

        plot_trajectory(
            env,
            trajectory,
            title=f"{res['name']} - Learned Policy Trajectory ({len(trajectory)-1} steps)",
            save_path=os.path.join(RESULTS_DIR, f"demo_trajectory_{map_key}.png")
        )
        print(f"[{map_key.upper()}] Trajectory: {len(trajectory)-1} steps | Path: {trajectory}")

    # Also generate demo_map3_vi_path (compatible with old name)
    res3 = vi_results["map3"]
    env3 = res3["env"]
    policy3 = res3["policy"]

    obs, info = env3.reset()
    traj3 = [info["state_tuple"][:2]]
    terminated = truncated = False
    while not (terminated or truncated):
        a = policy3[env3.encode_state(info["state_tuple"])]
        obs, _, terminated, truncated, info = env3.step(a)
        traj3.append(info["state_tuple"][:2])

    plot_trajectory(
        env3, traj3,
        title=f"Map 3 VI Demo - {len(traj3)-1} steps",
        save_path=os.path.join(RESULTS_DIR, "demo_map3_vi_path.png")
    )


def main():
    print("=" * 60)
    print("STARTING COMPLETE EXPERIMENT SUITE FOR ONE-WAY ARROW GRID")
    print("=" * 60)
    total_start = time.time()

    vi_results = run_value_iteration_experiments()
    run_qlearning_multi_seed_experiments()
    run_invalid_action_mode_comparison()
    run_reward_sensitivity_experiments()
    generate_demo_trajectories(vi_results)

    elapsed = time.time() - total_start
    print(f"\nALL EXPERIMENTS COMPLETED in {elapsed:.1f}s! ALL ARTIFACTS SAVED TO results/")


if __name__ == "__main__":
    main()

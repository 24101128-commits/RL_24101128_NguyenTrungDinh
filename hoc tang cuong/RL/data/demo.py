"""
demo.py - Interactive Demo of an Episode using Learned Policy.
Usage:
    python demo.py --map map3 --algo vi
    python demo.py --map map1 --algo ql
    python demo.py --map map2 --algo vi
"""

import argparse
import time
import os
import maps
from env import OneWayArrowEnv, TOKEN_ON_GRID, TOKEN_HELD, TOKEN_USED
from maps import ACTION_NAMES
from algorithms import ValueIteration, QLearningAgent
from visualize import plot_trajectory

def run_demo(map_name: str = "map3", algo: str = "vi", delay: float = 0.2):
    print("=" * 65)
    print(f"DEMO EPISODE: {map_name.upper()} | ALGORITHM: {algo.upper()}")
    print("=" * 65)

    if map_name not in maps.MAPS:
        print(f"Error: map '{map_name}' not found. Choose from {list(maps.MAPS.keys())}")
        return

    cfg = maps.MAPS[map_name]
    env = OneWayArrowEnv(cfg, invalid_action_mode="action_mask")

    if algo.lower() == "vi":
        print(f"Solving {cfg['name']} with Value Iteration...")
        vi = ValueIteration(env, gamma=0.99, theta=1e-4)
        V, policy, iters = vi.solve()
        print(f"Value Iteration converged in {iters} iterations.")
        def get_action(s_idx, mask):
            return policy[s_idx]
    else:
        print(f"Training Q-Learning Agent on {cfg['name']} (200 episodes)...")
        agent = QLearningAgent(env, alpha=0.15, gamma=0.99, epsilon_decay=0.985, seed=42)
        for _ in range(200):
            agent.train_episode()
        print("Training complete.")
        def get_action(s_idx, mask):
            return agent.select_action(s_idx, mask=mask, greedy=True)

    obs, info = env.reset()
    trajectory = [info["state_tuple"][:2]]
    total_reward = 0.0
    step_num = 0
    terminated = False
    truncated = False

    print("\nInitial State:")
    env.render()

    while not (terminated or truncated):
        mask = info["action_mask"]
        action = get_action(obs, mask)
        act_name = ACTION_NAMES[action]

        prev_pos = info["state_tuple"][:2]
        prev_tok = info["state_tuple"][2]
        prev_sw = info["state_tuple"][3]

        obs, reward, terminated, truncated, info = env.step(action)
        curr_pos = info["state_tuple"][:2]
        curr_tok = info["state_tuple"][2]
        curr_sw = info["state_tuple"][3]

        total_reward += reward
        step_num += 1
        trajectory.append(curr_pos)

        event_msg = []
        if prev_tok == TOKEN_ON_GRID and curr_tok == TOKEN_HELD:
            event_msg.append(">>> PICKED UP OVERRIDE TOKEN! <<<")
        elif prev_tok == TOKEN_HELD and curr_tok == TOKEN_USED:
            event_msg.append(">>> USED OVERRIDE TOKEN TO BYPASS ARROW! <<<")

        if prev_sw != curr_sw:
            event_msg.append(f">>> TOGGLED SWITCH! Arrows flipped to state {curr_sw} <<<")

        if terminated:
            event_msg.append(">>> REACHED GOAL! <<<")

        print(f"Step {step_num:2d}: Action={act_name:<5} | From {prev_pos} -> To {curr_pos} | Reward={reward:+5.1f} | {' '.join(event_msg)}")
        env.render()

        if delay > 0:
            time.sleep(delay)

    print("\n" + "=" * 65)
    print(f"EPISODE COMPLETED!")
    print(f"Total Steps : {step_num}")
    print(f"Total Return: {total_reward:.1f}")
    print(f"Success     : {terminated}")
    print("=" * 65)

    # Save demo trajectory image
    save_path = os.path.join("results", f"demo_{map_name}_{algo}_path.png")
    plot_trajectory(
        env,
        trajectory,
        title=f"Demo Episode: {cfg['name']} ({algo.upper()}, {step_num} steps)",
        save_path=save_path
    )
    print(f"Trajectory saved to {save_path}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run demo episode on One-Way Arrow Grid")
    parser.add_argument("--map", type=str, default="map3", choices=["map1", "map2", "map3"], help="Map to run")
    parser.add_argument("--algo", type=str, default="vi", choices=["vi", "ql"], help="Algorithm (vi or ql)")
    parser.add_argument("--delay", type=float, default=0.05, help="Delay between steps in seconds")
    args = parser.parse_args()

    run_demo(map_name=args.map, algo=args.algo, delay=args.delay)

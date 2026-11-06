"""
visualize.py - Visualization utilities for One-Way Arrow Grid.
Generates:
1. Map grid layout visualization (walls, arrows, switches, token, start, goal).
2. State-value heatmap and optimal policy arrows overlay.
3. Training performance curves (return, steps, success rate) across multiple seeds.
4. Comparative analysis charts (Penalty vs Masking, Reward sensitivity).
5. Visual trajectory of an episode.
"""

from typing import Dict, Any, List, Tuple, Optional
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

from maps import (
    ACTION_UP, ACTION_DOWN, ACTION_LEFT, ACTION_RIGHT,
    ACTION_NAMES, ACTION_DELTAS
)
from env import OneWayArrowEnv, TOKEN_ON_GRID, TOKEN_HELD, TOKEN_USED

# Set non-interactive backend
import matplotlib
matplotlib.use("Agg")

# Color palette
COLOR_WALL = "#2b2d42"
COLOR_START = "#2a9d8f"
COLOR_GOAL = "#e76f51"
COLOR_SWITCH = "#9d4edd"
COLOR_TOKEN = "#00b4d8"
COLOR_ARROW = "#d90429"
COLOR_DYNAMIC_ARROW = "#f77f00"
COLOR_GRID = "#e9ecef"
COLOR_AGENT = "#3a86ff"
COLOR_POLICY_ARROW = "#ffffff"

ACTION_DELTA_DISPLAY = {
    ACTION_UP:    (0.0, -0.3),
    ACTION_DOWN:  (0.0,  0.3),
    ACTION_LEFT:  (-0.3, 0.0),
    ACTION_RIGHT: (0.3,  0.0),
}


def _save_or_show(fig, save_path: Optional[str]):
    """Helper to either save figure or display it."""
    if save_path:
        dirpath = os.path.dirname(os.path.abspath(save_path))
        os.makedirs(dirpath, exist_ok=True)
        fig.savefig(save_path, bbox_inches="tight", dpi=150)
        plt.close(fig)
        print(f"  [Saved] {save_path}")
    else:
        plt.show()


def plot_grid_layout(
    env: OneWayArrowEnv,
    switch_state: int = 0,
    token_status: int = TOKEN_ON_GRID,
    title: Optional[str] = None,
    save_path: Optional[str] = None
):
    """
    Plots the grid layout showing walls, arrows, switch, token, start, and goal.
    """
    H, W = env.height, env.width
    fig, ax = plt.subplots(figsize=(max(5, W * 1.1 + 1), max(5, H * 1.1 + 1)))
    ax.set_xlim(-0.5, W - 0.5)
    ax.set_ylim(H - 0.5, -0.5)  # Invert y-axis so (0,0) is top-left
    ax.set_aspect("equal")

    # Grid background
    for r in range(H):
        for c in range(W):
            rect = patches.Rectangle(
                (c - 0.5, r - 0.5), 1, 1,
                linewidth=1, edgecolor="#ced4da", facecolor="white"
            )
            ax.add_patch(rect)

    # Walls
    for pos in env.walls:
        wr, wc = pos
        rect = patches.Rectangle(
            (wc - 0.5, wr - 0.5), 1, 1,
            linewidth=1, edgecolor=COLOR_WALL, facecolor=COLOR_WALL
        )
        ax.add_patch(rect)
        ax.text(wc, wr, "WALL", ha="center", va="center",
                color="white", fontsize=8, fontweight="bold")

    # Start and Goal
    sr, sc = env.start_pos
    gr, gc = env.goal_pos
    ax.add_patch(patches.Rectangle((sc - 0.5, sr - 0.5), 1, 1,
                                   facecolor=COLOR_START, alpha=0.35))
    ax.text(sc, sr, f"START\n({sr},{sc})", ha="center", va="center",
            color="#1d3557", fontsize=8, fontweight="bold")

    ax.add_patch(patches.Rectangle((gc - 0.5, gr - 0.5), 1, 1,
                                   facecolor=COLOR_GOAL, alpha=0.35))
    ax.text(gc, gr, f"GOAL\n+{int(env.goal_reward)}", ha="center", va="center",
            color="#9e2a2b", fontsize=9, fontweight="bold")

    # Switches
    for pos in env.switches:
        sw_r, sw_c = pos
        ax.add_patch(patches.Rectangle((sw_c - 0.5, sw_r - 0.5), 1, 1,
                                       facecolor=COLOR_SWITCH, alpha=0.25))
        ax.text(sw_c, sw_r, "SWITCH\n(Toggle)", ha="center", va="center",
                color=COLOR_SWITCH, fontsize=8, fontweight="bold")

    # Token
    if env.token_pos is not None:
        tr, tc = env.token_pos
        ax.add_patch(patches.Rectangle((tc - 0.5, tr - 0.5), 1, 1,
                                       facecolor=COLOR_TOKEN, alpha=0.25))
        ax.text(tc, tr, "TOKEN\n(1-use)", ha="center", va="center",
                color="#0077b6", fontsize=8, fontweight="bold")

    # Fixed and Dynamic Arrows
    for r in range(H):
        for c in range(W):
            pos = (r, c)
            if pos in env.walls or pos == env.goal_pos:
                continue
            is_dynamic = pos in env.dynamic_arrows
            allowed = env.get_allowed_arrows_at(pos, switch_state)
            if allowed:
                arrow_color = COLOR_DYNAMIC_ARROW if is_dynamic else COLOR_ARROW
                for a in allowed:
                    dr, dc = ACTION_DELTAS[a]
                    ax.annotate(
                        "",
                        xy=(c + dc * 0.35, r + dr * 0.35),
                        xytext=(c - dc * 0.2, r - dr * 0.2),
                        arrowprops=dict(
                            arrowstyle="->,head_width=0.4,head_length=0.6",
                            lw=2.5,
                            color=arrow_color
                        )
                    )
                label = "Dyn" if is_dynamic else "OneWay"
                ax.text(c, r + 0.38, label, ha="center", va="center",
                        color=arrow_color, fontsize=6, fontweight="bold")

    ax.set_xticks(range(W))
    ax.set_yticks(range(H))
    ax.set_xlabel("Columns", fontsize=10)
    ax.set_ylabel("Rows", fontsize=10)
    plot_title = title or f"{env.name} (Switch State: {switch_state})"
    ax.set_title(plot_title, fontsize=12, fontweight="bold", pad=12)
    plt.tight_layout()
    _save_or_show(fig, save_path)


def plot_policy_and_values(
    env: OneWayArrowEnv,
    V: np.ndarray,
    policy: np.ndarray,
    switch_state: int = 0,
    token_status: int = TOKEN_ON_GRID,
    title: Optional[str] = None,
    save_path: Optional[str] = None
):
    """
    Visualizes the optimal Value Function heatmap and Policy vector field on the grid.
    """
    H, W = env.height, env.width
    value_grid = np.zeros((H, W), dtype=np.float64)
    action_grid = np.zeros((H, W), dtype=int)

    for r in range(H):
        for c in range(W):
            s = (r, c, token_status, switch_state)
            s_idx = env.encode_state(s)
            value_grid[r, c] = V[s_idx]
            action_grid[r, c] = policy[s_idx]

    fig, ax = plt.subplots(figsize=(max(6, W * 1.1 + 1.5), max(6, H * 1.1 + 1)))
    ax.set_xlim(-0.5, W - 0.5)
    ax.set_ylim(H - 0.5, -0.5)
    ax.set_aspect("equal")

    # Mask walls in heatmap
    wall_mask = np.zeros((H, W), dtype=bool)
    for (wr, wc) in env.walls:
        wall_mask[wr, wc] = True

    masked_values = np.ma.masked_where(wall_mask, value_grid)
    cmap = plt.cm.viridis.copy()
    cmap.set_bad(color=COLOR_WALL)

    im = ax.imshow(masked_values, cmap=cmap, origin="upper",
                   extent=(-0.5, W - 0.5, H - 0.5, -0.5))
    cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("State Value $V^*(s)$", fontsize=10)

    # Draw walls explicitly
    for (wr, wc) in env.walls:
        rect = patches.Rectangle((wc - 0.5, wr - 0.5), 1, 1, facecolor=COLOR_WALL)
        ax.add_patch(rect)
        ax.text(wc, wr, "WALL", ha="center", va="center",
                color="white", fontsize=8, fontweight="bold")

    # Special positions: goal, start, switch, token
    gr, gc = env.goal_pos
    ax.text(gc, gr, "GOAL", ha="center", va="center",
            color="#e63946", fontsize=9, fontweight="bold")

    sr, sc = env.start_pos
    ax.text(sc, sr, "S", ha="center", va="top",
            color="lime", fontsize=9, fontweight="bold")

    for (sw_r, sw_c) in env.switches:
        ax.text(sw_c, sw_r, "K", ha="left", va="bottom",
                color="cyan", fontsize=8, fontweight="bold")

    if env.token_pos is not None:
        tr, tc = env.token_pos
        ax.text(tc, tr, "T", ha="right", va="bottom",
                color="yellow", fontsize=8, fontweight="bold")

    # Policy arrows and value labels
    for r in range(H):
        for c in range(W):
            if (r, c) in env.walls:
                continue
            val = value_grid[r, c]
            # Value label
            text_color = "white" if val < np.nanpercentile(value_grid[~wall_mask], 60) else "black"
            ax.text(c, r - 0.3, f"{val:.1f}", ha="center", va="center",
                    color=text_color, fontsize=7, fontweight="bold")

            if (r, c) == env.goal_pos:
                continue  # No policy arrow at goal

            a = action_grid[r, c]
            dc, dr = ACTION_DELTA_DISPLAY[a]
            ax.annotate(
                "",
                xy=(c + dc, r + dr),
                xytext=(c, r + 0.1),
                arrowprops=dict(
                    arrowstyle="->,head_width=0.35,head_length=0.45",
                    lw=2.0,
                    color="red"
                )
            )

    ax.set_xticks(range(W))
    ax.set_yticks(range(H))
    ax.set_xlabel("Columns", fontsize=10)
    ax.set_ylabel("Rows", fontsize=10)

    tok_names = {TOKEN_ON_GRID: "No Token", TOKEN_HELD: "Holding Token", TOKEN_USED: "Token Used"}
    plot_title = title or (
        f"Optimal Policy & Value Function "
        f"[{tok_names.get(token_status, '?')} | Switch={switch_state}]"
    )
    ax.set_title(plot_title, fontsize=11, fontweight="bold", pad=12)
    plt.tight_layout()
    _save_or_show(fig, save_path)


def plot_learning_curves(
    experiments_data: Dict[str, Dict[str, np.ndarray]],
    title: str = "Training Learning Curves",
    save_path: Optional[str] = None
):
    """
    Plots mean return and steps per episode with standard deviation shaded bands.

    experiments_data format:
    {
       'Label': {
           'returns': 2D array (num_seeds, num_episodes),
           'steps': 2D array (num_seeds, num_episodes)
       }
    }
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]

    for idx, (label, metrics) in enumerate(experiments_data.items()):
        returns = np.array(metrics["returns"])
        steps = np.array(metrics["steps"])
        num_episodes = returns.shape[1]
        color = colors[idx % len(colors)]

        # Smooth with moving average
        window = max(1, num_episodes // 20)

        def moving_avg(arr: np.ndarray) -> np.ndarray:
            """Apply moving average with mode='valid' to each row."""
            kernel = np.ones(window) / window
            result = np.array([np.convolve(row, kernel, mode="valid") for row in arr])
            return result

        smoothed_returns = moving_avg(returns)
        mean_ret = np.mean(smoothed_returns, axis=0)
        std_ret = np.std(smoothed_returns, axis=0)
        x_ret = np.arange(window, num_episodes + 1)

        smoothed_steps = moving_avg(steps)
        mean_steps = np.mean(smoothed_steps, axis=0)
        std_steps = np.std(smoothed_steps, axis=0)

        ax1.plot(x_ret, mean_ret, label=label, lw=2, color=color)
        ax1.fill_between(x_ret, mean_ret - std_ret, mean_ret + std_ret,
                         alpha=0.18, color=color)

        ax2.plot(x_ret, mean_steps, label=label, lw=2, color=color)
        ax2.fill_between(x_ret, mean_steps - std_steps, mean_steps + std_steps,
                         alpha=0.18, color=color)

    ax1.set_title("Episode Cumulative Return", fontsize=11, fontweight="bold")
    ax1.set_xlabel("Episode", fontsize=10)
    ax1.set_ylabel("Undiscounted Return", fontsize=10)
    ax1.grid(True, linestyle="--", alpha=0.6)
    ax1.legend(loc="lower right", fontsize=9)

    ax2.set_title("Episode Length (Steps to Goal)", fontsize=11, fontweight="bold")
    ax2.set_xlabel("Episode", fontsize=10)
    ax2.set_ylabel("Steps", fontsize=10)
    ax2.grid(True, linestyle="--", alpha=0.6)
    ax2.legend(loc="upper right", fontsize=9)

    fig.suptitle(title, fontsize=13, fontweight="bold", y=1.02)
    plt.tight_layout()
    _save_or_show(fig, save_path)


def plot_trajectory(
    env: OneWayArrowEnv,
    trajectory: List[Tuple[int, int]],
    title: str = "Agent Trajectory",
    save_path: Optional[str] = None
):
    """
    Plots the path taken by the agent on the grid during a demo episode.
    """
    H, W = env.height, env.width
    fig, ax = plt.subplots(figsize=(max(5, W * 1.1 + 1), max(5, H * 1.1 + 1)))
    ax.set_xlim(-0.5, W - 0.5)
    ax.set_ylim(H - 0.5, -0.5)
    ax.set_aspect("equal")

    for r in range(H):
        for c in range(W):
            rect = patches.Rectangle((c - 0.5, r - 0.5), 1, 1,
                                     edgecolor="#ced4da", facecolor="white")
            ax.add_patch(rect)

    for pos in env.walls:
        wr, wc = pos
        ax.add_patch(patches.Rectangle((wc - 0.5, wr - 0.5), 1, 1, facecolor=COLOR_WALL))
        ax.text(wc, wr, "WALL", ha="center", va="center",
                color="white", fontsize=8, fontweight="bold")

    sr, sc = env.start_pos
    gr, gc = env.goal_pos
    ax.add_patch(patches.Rectangle((sc - 0.5, sr - 0.5), 1, 1,
                                   facecolor=COLOR_START, alpha=0.3))
    ax.text(sc, sr, "START", ha="center", va="center",
            color=COLOR_START, fontsize=8, fontweight="bold")

    ax.add_patch(patches.Rectangle((gc - 0.5, gr - 0.5), 1, 1,
                                   facecolor=COLOR_GOAL, alpha=0.3))
    ax.text(gc, gr, "GOAL", ha="center", va="center",
            color=COLOR_GOAL, fontsize=8, fontweight="bold")

    # Draw trajectory line
    rows = [p[0] for p in trajectory]
    cols = [p[1] for p in trajectory]
    ax.plot(cols, rows, color=COLOR_AGENT, lw=3, marker="o", markersize=6,
            zorder=4, label="Agent Path", alpha=0.85)

    # Step labels along path
    for step_num, (r, c) in enumerate(trajectory):
        ax.text(c, r, str(step_num), ha="center", va="center",
                color="white", fontsize=6, fontweight="bold",
                bbox=dict(boxstyle="circle,pad=0.2",
                          facecolor=COLOR_AGENT, edgecolor="none", alpha=0.85))

    ax.set_xticks(range(W))
    ax.set_yticks(range(H))
    ax.set_xlabel("Columns", fontsize=10)
    ax.set_ylabel("Rows", fontsize=10)
    ax.set_title(title, fontsize=12, fontweight="bold", pad=12)
    ax.legend(loc="upper left")
    plt.tight_layout()
    _save_or_show(fig, save_path)

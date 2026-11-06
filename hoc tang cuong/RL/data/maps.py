"""
maps.py - Map configurations for One-Way Arrow Grid.
Contains 3 maps with increasing difficulty as specified:
1. Map 1: Basic One-Way Arrows with Cycles (5x5)
2. Map 2: Dynamic Switch & Dual Arrow Cycles (6x6)
3. Map 3: Master Challenge with Cycles, Switch, and Override Token (7x7)
"""

from typing import Dict, Any, List, Tuple

# Actions definition
# 0: UP, 1: DOWN, 2: LEFT, 3: RIGHT
ACTION_UP = 0
ACTION_DOWN = 1
ACTION_LEFT = 2
ACTION_RIGHT = 3

ACTION_NAMES = {0: "UP", 1: "DOWN", 2: "LEFT", 3: "RIGHT"}
ACTION_DELTAS = {
    0: (-1, 0),  # UP
    1: (1, 0),   # DOWN
    2: (0, -1),  # LEFT
    3: (0, 1)    # RIGHT
}
ACTION_ARROWS = {0: "^", 1: "v", 2: "<", 3: ">"}

# Inverse directions for dynamic arrow inversion
INVERSE_ACTION = {
    ACTION_UP: ACTION_DOWN,
    ACTION_DOWN: ACTION_UP,
    ACTION_LEFT: ACTION_RIGHT,
    ACTION_RIGHT: ACTION_LEFT
}

# Map 1: Introductory 5x5 Grid
# Features: Fixed one-way arrows and a trap cycle.
# The agent must learn to bypass or navigate around the cycle to reach the Goal.
MAP_1_CONFIG: Dict[str, Any] = {
    "name": "Map 1: Basic One-Way & Cycles (5x5)",
    "height": 5,
    "width": 5,
    "start": (0, 0),
    "goal": (4, 4),
    "walls": [(1, 4), (3, 3)],
    # arrows: {(r, c): [allowed_actions]}
    # Cycle at (1,1)->(1,2)->(2,2)->(2,1)->(1,1)
    # Plus arrows guiding or diverting agent
    "arrows": {
        (0, 1): [ACTION_RIGHT],
        (0, 2): [ACTION_DOWN],
        (1, 1): [ACTION_RIGHT],  # Cycle: Right
        (1, 2): [ACTION_DOWN],   # Cycle: Down
        (2, 2): [ACTION_LEFT],   # Cycle: Left
        (2, 1): [ACTION_UP],     # Cycle: Up (Creates strict loop!)
        (2, 3): [ACTION_DOWN],
        (3, 1): [ACTION_DOWN],
        (3, 2): [ACTION_RIGHT],
        (4, 2): [ACTION_RIGHT],
    },
    "dynamic_arrows": {},  # No dynamic arrows in Map 1
    "switches": [],        # No switches
    "token_pos": None,     # No override token
    "initial_token": 0,
    "max_steps": 100
}

# Map 2: Dynamic Switch & Dual Arrow Cycles (6x6)
# Features: Two cycle traps, and dynamic arrows that reverse orientation when the switch is stepped on.
# The gate at (3, 4) initially points UP (blocking entry to Goal area).
# Once the agent steps on the switch at (4, 0), dynamic arrows invert, allowing access to the Goal!
MAP_2_CONFIG: Dict[str, Any] = {
    "name": "Map 2: Dynamic Switch & Dual Cycles (6x6)",
    "height": 6,
    "width": 6,
    "start": (0, 0),
    "goal": (5, 5),
    "walls": [(1, 2), (4, 4)],
    # Fixed arrows
    "arrows": {
        # Cycle 1 (top): (0, 3) -> (0, 4) -> (1, 4) -> (1, 3) -> (0, 3)
        (0, 3): [ACTION_RIGHT],
        (0, 4): [ACTION_DOWN],
        (1, 4): [ACTION_LEFT],
        (1, 3): [ACTION_UP],
        # Cycle 2 (middle): (2, 2) -> (2, 3) -> (3, 3) -> (3, 2) -> (2, 2)
        (2, 2): [ACTION_RIGHT],
        (2, 3): [ACTION_DOWN],
        (3, 3): [ACTION_LEFT],
        (3, 2): [ACTION_UP],
        # Guiding arrow down towards switch
        (1, 0): [ACTION_DOWN],
    },
    # Dynamic arrows: gate direction flips when switch is activated (switch_state = 1)
    # Default (switch_state=0) points LEFT (blocks path to goal).
    # When switch is pressed (switch_state=1), inverts to RIGHT, opening path to goal!
    "dynamic_arrows": {
        (5, 3): [ACTION_LEFT],
    },
    "switches": [(5, 0)],
    "token_pos": None,
    "initial_token": 0,
    "max_steps": 150
}

# Map 3: Master Challenge: Cycles, Switch & Override Token (7x7)
# Features:
# - Complex maze with multiple cycles.
# - A Switch at (6, 0) that inverts gate arrows.
# - An Override Token at (0, 4) that allows violating an arrow exactly ONCE.
# - Strategic choice:
#   Path A (Long Way): Go left/down to Switch (6,0) -> Invert arrows -> Traverse bottom corridor -> Reach Goal.
#   Path B (Token Shortcut): Pick up Override Token at (0, 4) -> Move directly through one-way barrier at (3, 6)
#                          (which strictly points UP, requiring Override Token to cross DOWN towards Goal at (6, 6)).
MAP_3_CONFIG: Dict[str, Any] = {
    "name": "Map 3: Cycles, Switch & Override Token (7x7)",
    "height": 7,
    "width": 7,
    "start": (0, 0),
    "goal": (6, 6),
    "walls": [
        (1, 1), (1, 2), (1, 3),
        (3, 2), (3, 3), (3, 4),
        (5, 2), (5, 4)
    ],
    # Fixed arrows
    "arrows": {
        # Cycle 1: (0, 1) -> (0, 2) -> (0, 3)
        (0, 1): [ACTION_RIGHT],
        (0, 2): [ACTION_RIGHT],
        # Cycle 2 trap around (4, 1):
        (4, 0): [ACTION_RIGHT],
        (4, 1): [ACTION_DOWN],
        (5, 1): [ACTION_LEFT],
        (5, 0): [ACTION_UP],
        # Strict shortcut barrier: arrow points strictly UP.
        # Moving DOWN through (3, 6) requires consuming the Override Token!
        (3, 6): [ACTION_UP],
        (4, 6): [ACTION_DOWN],
        (5, 6): [ACTION_DOWN],
    },
    # Dynamic arrows: gate opened via switch
    "dynamic_arrows": {
        # Gate at (6, 3): initially points LEFT (away from goal), inverts to RIGHT!
        (6, 3): [ACTION_LEFT],
        (6, 4): [ACTION_RIGHT],
        (2, 4): [ACTION_DOWN],
    },
    "switches": [(6, 0)],
    "token_pos": (0, 4),   # Override token location
    "initial_token": 0,    # Pick up token when visiting (0, 4)
    "max_steps": 200
}

MAPS = {
    "map1": MAP_1_CONFIG,
    "map2": MAP_2_CONFIG,
    "map3": MAP_3_CONFIG
}

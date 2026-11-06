"""
env.py - Gymnasium environment for One-Way Arrow Grid.
Implements:
1. Fixed one-way arrows.
2. Cycles/loops in arrow configurations.
3. Switch mechanism that toggles/inverts dynamic arrow directions.
4. Override token that permits moving against arrow directions exactly once.
5. Two invalid action handling modes:
   - 'penalty_stay': Agent stays in place and incurs a penalty.
   - 'action_mask': Invalid actions are excluded from the available action set.
6. Full transition model P(s' | s, a) for Value Iteration.
7. Strict Markov state representation: (row, col, token_status, switch_state).
"""

from typing import Dict, Any, List, Tuple, Optional
import gymnasium as gym
from gymnasium import spaces
import numpy as np

from maps import (
    ACTION_UP, ACTION_DOWN, ACTION_LEFT, ACTION_RIGHT,
    ACTION_DELTAS, ACTION_NAMES, ACTION_ARROWS, INVERSE_ACTION, MAPS
)

# Token status constants
TOKEN_ON_GRID = 0   # Token is still on grid, agent does not have it
TOKEN_HELD = 1      # Agent possesses the token
TOKEN_USED = 2      # Token has been consumed


class OneWayArrowEnv(gym.Env):
    """
    One-Way Arrow Grid Gymnasium Environment.

    Observation space:
        Discrete space representing the encoded state index.
        Use decode_state() to recover (row, col, token_status, switch_state).
    Action space:
        Discrete(4): 0: UP, 1: DOWN, 2: LEFT, 3: RIGHT

    State tuple: (r, c, token_status, switch_state)
    - token_status ∈ {TOKEN_ON_GRID=0, TOKEN_HELD=1, TOKEN_USED=2}
    - switch_state ∈ {0: normal, 1: inverted}
    """
    metadata = {"render_modes": ["ansi", "human"]}

    def __init__(
        self,
        config: Dict[str, Any] = None,
        invalid_action_mode: str = "penalty_stay",
        step_cost: float = -1.0,
        goal_reward: float = 100.0,
        invalid_penalty: float = -10.0,
        token_pickup_reward: float = 5.0,
        render_mode: Optional[str] = None
    ):
        super().__init__()
        if config is None:
            config = MAPS["map1"]
        self.config = config
        self.name = config.get("name", "OneWayArrowGrid")
        self.height = config["height"]
        self.width = config["width"]
        self.start_pos = config["start"]
        self.goal_pos = config["goal"]
        self.walls = set(map(tuple, config.get("walls", [])))
        self.fixed_arrows: Dict[Tuple[int, int], List[int]] = {
            tuple(k): v for k, v in config.get("arrows", {}).items()
        }
        self.dynamic_arrows: Dict[Tuple[int, int], List[int]] = {
            tuple(k): v for k, v in config.get("dynamic_arrows", {}).items()
        }
        self.switches: set = set(map(tuple, config.get("switches", [])))
        self.token_pos: Optional[Tuple[int, int]] = (
            tuple(config["token_pos"]) if config.get("token_pos") is not None else None
        )
        self.max_steps: int = config.get("max_steps", 100)

        # Rewards and penalties
        self.step_cost = step_cost
        self.goal_reward = goal_reward
        self.invalid_penalty = invalid_penalty
        self.token_pickup_reward = token_pickup_reward
        self.invalid_action_mode = invalid_action_mode  # 'penalty_stay' or 'action_mask'
        self.render_mode = render_mode

        # Action space: 4 directions
        self.action_space = spaces.Discrete(4)

        # Number of possible token statuses:
        # If map has token: 3 states (ON_GRID, HELD, USED). If not, 1 state (USED/0).
        self.num_token_states = 3 if self.token_pos is not None else 1
        # Number of switch states:
        # If map has switches: 2 states (0: normal, 1: inverted). If not, 1 state (0).
        self.num_switch_states = 2 if len(self.switches) > 0 else 1

        # Total number of states
        self.num_states = self.height * self.width * self.num_token_states * self.num_switch_states
        self.observation_space = spaces.Discrete(self.num_states)

        # Internal state: (r, c, token_status, switch_state)
        self.state: Tuple[int, int, int, int] = (
            self.start_pos[0], self.start_pos[1], 0, 0
        )
        self.steps = 0

    def encode_state(self, s: Tuple[int, int, int, int]) -> int:
        """Encode (r, c, token_status, switch_state) to a unique integer index."""
        r, c, tok, sw = s
        tok_idx = min(tok, self.num_token_states - 1)
        sw_idx = min(sw, self.num_switch_states - 1)
        idx = ((r * self.width + c) * self.num_token_states + tok_idx) * self.num_switch_states + sw_idx
        return idx

    def decode_state(self, idx: int) -> Tuple[int, int, int, int]:
        """Decode integer index back to (r, c, token_status, switch_state)."""
        sw = idx % self.num_switch_states
        idx //= self.num_switch_states
        tok = idx % self.num_token_states
        idx //= self.num_token_states
        c = idx % self.width
        r = idx // self.width
        return (r, c, tok, sw)

    def get_allowed_arrows_at(
        self, pos: Tuple[int, int], switch_state: int
    ) -> Optional[List[int]]:
        """Return list of allowed actions at position, or None if regular cell."""
        if pos in self.fixed_arrows:
            return self.fixed_arrows[pos]
        if pos in self.dynamic_arrows:
            base_arrows = self.dynamic_arrows[pos]
            if switch_state == 0:
                return base_arrows
            else:
                # Dynamic arrows are inverted when switch is active
                return [INVERSE_ACTION[a] for a in base_arrows]
        return None

    def get_action_mask(
        self, state: Optional[Tuple[int, int, int, int]] = None
    ) -> np.ndarray:
        """
        Returns boolean mask of valid actions for the given state (or current state).
        Shape: (4,), True if action is legal, False otherwise.
        """
        if state is None:
            state = self.state
        r, c, tok, sw = state
        mask = np.zeros(4, dtype=bool)

        # If already at goal, episode is done - no further moves are meaningful.
        # Return all-True so agent can still be queried without crashing,
        # but terminated flag should prevent further stepping.
        if (r, c) == self.goal_pos:
            mask[:] = True
            return mask

        allowed_arrows = self.get_allowed_arrows_at((r, c), sw)

        for a in range(4):
            dr, dc = ACTION_DELTAS[a]
            nr, nc = r + dr, c + dc

            # Boundary check
            if not (0 <= nr < self.height and 0 <= nc < self.width):
                continue
            # Wall check
            if (nr, nc) in self.walls:
                continue

            # Arrow constraint check
            if allowed_arrows is not None:
                if a in allowed_arrows:
                    mask[a] = True
                elif tok == TOKEN_HELD:
                    # Token allows overriding arrow constraint
                    mask[a] = True
            else:
                # Regular cell: any non-wall, in-bound move is legal
                mask[a] = True

        return mask

    def action_masks(self) -> np.ndarray:
        """Gymnasium convention for action masking."""
        return self.get_action_mask(self.state)

    def get_transition_prob(
        self, state: Tuple[int, int, int, int], action: int
    ) -> List[Tuple[float, Tuple[int, int, int, int], float, bool]]:
        """
        Transition model for MDP: P(s' | s, a).
        Returns list of tuples: [(probability, next_state, reward, terminated)]
        Since environment dynamics are deterministic, probability is always 1.0.
        """
        r, c, tok, sw = state

        # Terminal state: goal already reached
        if (r, c) == self.goal_pos:
            return [(1.0, state, 0.0, True)]

        mask = self.get_action_mask(state)
        is_legal = bool(mask[action])

        # Case 1: Action is illegal
        if not is_legal:
            # Both modes: stay in place, incur penalty
            reward = self.invalid_penalty
            next_state = state
            return [(1.0, next_state, reward, False)]

        # Case 2: Legal action
        dr, dc = ACTION_DELTAS[action]
        nr, nc = r + dr, c + dc
        allowed_arrows = self.get_allowed_arrows_at((r, c), sw)

        next_tok = tok
        next_sw = sw
        reward = self.step_cost

        # Check if override token was used to bypass an arrow
        if allowed_arrows is not None and action not in allowed_arrows:
            if tok == TOKEN_HELD:
                next_tok = TOKEN_USED  # Consume token

        # Check if agent stepped on token tile
        if self.token_pos is not None and (nr, nc) == self.token_pos:
            if next_tok == TOKEN_ON_GRID:
                next_tok = TOKEN_HELD
                reward += self.token_pickup_reward

        # Check if agent stepped on switch tile -> toggle switch
        if (nr, nc) in self.switches:
            next_sw = 1 - next_sw

        # Check goal
        terminated = ((nr, nc) == self.goal_pos)
        if terminated:
            reward += self.goal_reward

        next_state = (nr, nc, next_tok, next_sw)
        return [(1.0, next_state, reward, terminated)]

    def get_all_states(self) -> List[Tuple[int, int, int, int]]:
        """Returns all non-wall state tuples (r, c, token_status, switch_state)."""
        states = []
        tok_range = range(self.num_token_states)
        sw_range = range(self.num_switch_states)
        for r in range(self.height):
            for c in range(self.width):
                if (r, c) in self.walls:
                    continue
                for tok in tok_range:
                    for sw in sw_range:
                        states.append((r, c, tok, sw))
        return states

    def reset(
        self,
        *,
        seed: Optional[int] = None,
        options: Optional[Dict[str, Any]] = None
    ) -> Tuple[int, Dict[str, Any]]:
        super().reset(seed=seed)
        self.steps = 0
        init_tok = TOKEN_ON_GRID if self.token_pos is not None else 0
        init_sw = 0
        self.state = (self.start_pos[0], self.start_pos[1], init_tok, init_sw)
        obs = self.encode_state(self.state)
        info = {
            "state_tuple": self.state,
            "action_mask": self.get_action_mask(self.state)
        }
        return obs, info

    def step(
        self, action: int
    ) -> Tuple[int, float, bool, bool, Dict[str, Any]]:
        self.steps += 1
        transitions = self.get_transition_prob(self.state, action)
        # Deterministic environment: single transition
        _, next_state, reward, terminated = transitions[0]
        self.state = next_state

        # Truncate only if max_steps exceeded and not already terminated
        truncated = (self.steps >= self.max_steps) and not terminated

        obs = self.encode_state(self.state)
        info = {
            "state_tuple": self.state,
            "steps": self.steps,
            "action_mask": self.get_action_mask(self.state)
        }

        if self.render_mode == "human":
            self.render()

        return obs, reward, terminated, truncated, info

    def render(self) -> str:
        """Render ASCII representation of current grid state."""
        r_agent, c_agent, tok, sw = self.state
        lines = [
            f"\n--- {self.name} | Steps: {self.steps} | "
            f"Token: {['On Grid', 'Held', 'Used'][tok]} | Switch: {sw} ---"
        ]
        for r in range(self.height):
            row_str = []
            for c in range(self.width):
                pos = (r, c)
                if pos == (r_agent, c_agent):
                    row_str.append("[A]")
                elif pos == self.goal_pos:
                    row_str.append(" G ")
                elif pos in self.walls:
                    row_str.append("###")
                elif pos in self.switches:
                    row_str.append(" S ")
                elif self.token_pos is not None and pos == self.token_pos and tok == TOKEN_ON_GRID:
                    row_str.append(" T ")
                elif pos in self.fixed_arrows or pos in self.dynamic_arrows:
                    allowed = self.get_allowed_arrows_at(pos, sw)
                    if allowed:
                        arrows = "".join(ACTION_ARROWS[a] for a in allowed)
                        row_str.append(f" {arrows:^1} ")
                    else:
                        row_str.append(" . ")
                else:
                    row_str.append(" . ")
            lines.append(" ".join(row_str))
        lines.append("--------------------------------------------------")
        output = "\n".join(lines)
        print(output)
        return output

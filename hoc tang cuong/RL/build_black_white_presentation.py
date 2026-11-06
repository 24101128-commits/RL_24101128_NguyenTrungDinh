"""
build_black_white_presentation.py
Generates an elegant, high-contrast, strictly Black and White (Monochrome) PowerPoint presentation:
- Pure white background, pure black text and cards (#000000 / #FFFFFF)
- Embeds the official Phenikaa University logo (logo_phenikaa_official.png)
- Embeds high-resolution benchmark figures from C:\RL\results
- 18 comprehensive slides covering the entire project from MDP theory to 5 algorithms and empirical diagnostics
"""

import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

PPTX_OUTPUT_PRIMARY = r"C:\RL\presentation_black_white.pptx"
PPTX_OUTPUT_SECONDARY = r"C:\RL\presentation_updated.pptx"

ASSETS_DIR = r"C:\RL\assets"
RESULTS_DIR = r"C:\RL\results"

LOGO_OFFICIAL = os.path.join(ASSETS_DIR, "logo_phenikaa_official.png")
if not os.path.exists(LOGO_OFFICIAL):
    LOGO_OFFICIAL = os.path.join(ASSETS_DIR, "logo_phenikaa.png")

# STRICT BLACK & WHITE PALETTE
C_BLACK = RGBColor(0x00, 0x00, 0x00)
C_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
C_GRAY_LIGHT = RGBColor(0xF5, 0xF5, 0xF5)
C_GRAY_BORDER = RGBColor(0x00, 0x00, 0x00)
C_GRAY_SUBTLE = RGBColor(0xEE, 0xEE, 0xEE)
C_DARK_CARD = RGBColor(0x1A, 0x1A, 0x1A)


def create_blank_slide(prs):
    """Creates a blank slide with pure white background."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = C_WHITE
    bg.line.fill.background()
    return slide


def add_slide_header(slide, title_text, category_text="PHENIKAA UNIVERSITY • REINFORCEMENT LEARNING COURSE"):
    """Adds a clean black-and-white header with top logo."""
    # Top thin black line
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.35), Inches(11.733), Inches(0.02))
    line.fill.solid()
    line.fill.fore_color.rgb = C_BLACK
    line.line.fill.background()

    # Category tracker
    tb_cat = slide.shapes.add_textbox(Inches(0.8), Inches(0.42), Inches(8.5), Inches(0.3))
    tf_cat = tb_cat.text_frame
    tf_cat.word_wrap = True
    p_c = tf_cat.paragraphs[0]
    p_c.text = category_text.upper()
    p_c.font.name = "Arial"
    p_c.font.size = Pt(9.5)
    p_c.font.bold = True
    p_c.font.color.rgb = C_BLACK

    # Title
    tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(9.2), Inches(0.65))
    tf_t = tb_title.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = title_text
    p_t.font.name = "Arial"
    p_t.font.size = Pt(22)
    p_t.font.bold = True
    p_t.font.color.rgb = C_BLACK

    # Corner Logo
    if os.path.exists(LOGO_OFFICIAL):
        slide.shapes.add_picture(LOGO_OFFICIAL, Inches(10.6), Inches(0.45), width=Inches(1.9))


def add_card(slide, left, top, width, height, title="", body_bullets=None, is_black=False):
    """Adds a high-contrast card container in black or white."""
    card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = C_BLACK if is_black else C_WHITE
    card.line.color.rgb = C_BLACK
    card.line.width = Pt(1.5)

    tb = slide.shapes.add_textbox(left + Inches(0.15), top + Inches(0.12), width - Inches(0.3), height - Inches(0.24))
    tf = tb.text_frame
    tf.word_wrap = True

    if title:
        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.name = "Arial"
        p_t.font.size = Pt(14)
        p_t.font.bold = True
        p_t.font.color.rgb = C_WHITE if is_black else C_BLACK
        p_t.space_after = Pt(6)

    if body_bullets:
        for idx, bullet in enumerate(body_bullets):
            p = tf.add_paragraph() if (title or idx > 0) else tf.paragraphs[0]
            p.text = f"•  {bullet}"
            p.font.name = "Arial"
            p.font.size = Pt(11)
            p.font.color.rgb = C_WHITE if is_black else C_BLACK
            p.space_after = Pt(4)


def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # ==============================================================================
    # SLIDE 1: TITLE SLIDE
    # ==============================================================================
    s1 = create_blank_slide(prs)

    # Frame Box
    frame = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.7), Inches(11.733), Inches(6.1))
    frame.fill.solid()
    frame.fill.fore_color.rgb = C_WHITE
    frame.line.color.rgb = C_BLACK
    frame.line.width = Pt(2.5)

    # Phenikaa Logo
    if os.path.exists(LOGO_OFFICIAL):
        s1.shapes.add_picture(LOGO_OFFICIAL, Inches(4.7), Inches(1.1), width=Inches(3.9))

    # University header text
    tb_u = s1.shapes.add_textbox(Inches(1.2), Inches(2.75), Inches(10.9), Inches(0.6))
    p_u = tb_u.text_frame.paragraphs[0]
    p_u.text = "FACULTY OF ELECTRICAL & ELECTRONIC ENGINEERING\nDEPARTMENT OF INTELLIGENT SYSTEMS & AUTOMATION"
    p_u.alignment = PP_ALIGN.CENTER
    p_u.font.name = "Arial"
    p_u.font.size = Pt(12)
    p_u.font.bold = True
    p_u.font.color.rgb = C_BLACK

    # Project Title
    tb_t = s1.shapes.add_textbox(Inches(1.2), Inches(3.5), Inches(10.9), Inches(1.2))
    p_t = tb_t.text_frame.paragraphs[0]
    p_t.text = "PROJECT 21: ONE-WAY ARROW GRID NAVIGATION"
    p_t.alignment = PP_ALIGN.CENTER
    p_t.font.name = "Arial"
    p_t.font.size = Pt(26)
    p_t.font.bold = True
    p_t.font.color.rgb = C_BLACK

    p_sub = tb_t.text_frame.add_paragraph()
    p_sub.text = "A Comprehensive Empirical Benchmark of 5 Reinforcement Learning Algorithms\n(Value Iteration, Policy Iteration, Tabular Q-Learning, SARSA, Monte Carlo Control)"
    p_sub.alignment = PP_ALIGN.CENTER
    p_sub.font.name = "Arial"
    p_sub.font.size = Pt(13)
    p_sub.font.italic = True
    p_sub.font.color.rgb = C_BLACK

    # Metadata card at bottom
    meta_card = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(2.2), Inches(5.1), Inches(8.933), Inches(1.2))
    meta_card.fill.solid()
    meta_card.fill.fore_color.rgb = C_BLACK
    meta_card.line.fill.background()

    tb_m = s1.shapes.add_textbox(Inches(2.4), Inches(5.2), Inches(8.5), Inches(1.0))
    p_m1 = tb_m.text_frame.paragraphs[0]
    p_m1.text = "STUDENT RESEARCH TEAM: Group Project 21   |   COURSE: Advanced Reinforcement Learning"
    p_m1.alignment = PP_ALIGN.CENTER
    p_m1.font.name = "Arial"
    p_m1.font.size = Pt(11)
    p_m1.font.bold = True
    p_m1.font.color.rgb = C_WHITE

    p_m2 = tb_m.text_frame.add_paragraph()
    p_m2.text = "PHENIKAA UNIVERSITY • HANOI, VIETNAM • OCTOBER 2026"
    p_m2.alignment = PP_ALIGN.CENTER
    p_m2.font.name = "Arial"
    p_m2.font.size = Pt(10)
    p_m2.font.color.rgb = C_WHITE

    # ==============================================================================
    # SLIDE 2: EXECUTIVE SUMMARY & AGENDA
    # ==============================================================================
    s2 = create_blank_slide(prs)
    add_slide_header(s2, "Executive Overview & Presentation Agenda")

    add_card(
        s2, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
        title="Project Executive Summary",
        body_bullets=[
            "Custom Gymnasium Environment: Models spatial gridworlds with mandatory one-way arrows, 2x2 cycle traps, dynamic invertible gates, and override tokens.",
            "Markov Sufficiency via 4D State Space: Formulates state vector s = (r, c, tau, sigma) to guarantee the strict Markov property.",
            "Comprehensive 5-Algorithm Suite: Implements Value Iteration, Policy Iteration, Tabular Q-Learning, SARSA, and First-Visit Monte Carlo.",
            "Multi-Seed Empirical Benchmarks: Evaluates sample efficiency, runtime speedup, path optimality, and cycle entrapment avoidance across 3 maps.",
            "Open Reproducibility: 100% self-contained Jupyter Notebook ready for one-click execution on Google Colab."
        ]
    )

    add_card(
        s2, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
        title="Presentation Agenda",
        body_bullets=[
            "Part 1: Industrial Motivation & One-Way Arrow GridWorld Mechanics",
            "Part 2: Mathematical MDP Formulation & 4D Markov State Vector",
            "Part 3: Benchmark Map Topologies & Quantitative Difficulty Index",
            "Part 4: Theoretical Formulation of the 5 RL Algorithms",
            "Part 5: Empirical Benchmark Results & Quantitative Tables",
            "Part 6: Visual Policy Vector Fields & Trajectory Verification",
            "Part 7: Agent Diagnostics (Deadlock Trapping & Shannon Entropy)",
            "Part 8: Key Scientific Insights, Conclusion & Q&A"
        ],
        is_black=True
    )

    # ==============================================================================
    # SLIDE 3: PROBLEM CONTEXT & MOTIVATION
    # ==============================================================================
    s3 = create_blank_slide(prs)
    add_slide_header(s3, "Problem Context: Directed Mobility in Spatial Systems")

    add_card(
        s3, Inches(0.8), Inches(1.6), Inches(3.6), Inches(5.2),
        title="Real-World Relevance",
        body_bullets=[
            "Automated Guided Vehicles (AGVs) operating in smart warehouse aisles.",
            "Unidirectional conveyor networks in manufacturing and baggage handling.",
            "One-way urban traffic routing and airport ground transport.",
            "Moving in reverse causes mechanical gridlock, collisions, or regulatory hazards."
        ]
    )

    add_card(
        s3, Inches(4.8), Inches(1.6), Inches(3.6), Inches(5.2),
        title="Isotropic Limitations",
        body_bullets=[
            "Standard gridworlds assume bidirectional holonomic mobility.",
            "Fail to model non-reversible spatial transitions.",
            "Cannot capture dynamic gate inversion triggered by environmental switches.",
            "Neglect consumable clearance tokens enabling selective violations."
        ]
    )

    add_card(
        s3, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.2),
        title="Project 21 Mission",
        body_bullets=[
            "Design custom Gymnasium environment OneWayArrowEnv.",
            "Synthesize optimal policies under severe topological flow constraints.",
            "Quantify trade-offs between exact model-based DP and model-free TD/MC learning.",
            "Prevent agents from starving in cyclic deadlocks."
        ],
        is_black=True
    )

    # ==============================================================================
    # SLIDE 4: CORE ENVIRONMENT MECHANICS
    # ==============================================================================
    s4 = create_blank_slide(prs)
    add_slide_header(s4, "One-Way Arrow GridWorld: Core Environment Mechanics")

    add_card(
        s4, Inches(0.8), Inches(1.6), Inches(2.7), Inches(5.2),
        title="1. Fixed Arrows",
        body_bullets=[
            "Cells marked with cardinal directional arrows: UP, DOWN, LEFT, RIGHT.",
            "Agent occupying an arrow cell MUST follow its direction.",
            "Traversing against arrow direction is strictly forbidden (without token)."
        ]
    )

    add_card(
        s4, Inches(3.8), Inches(1.6), Inches(2.7), Inches(5.2),
        title="2. Cyclic Traps",
        body_bullets=[
            "Sub-graphs of adjacent arrow cells arranged in closed 2x2 loops.",
            "Example: (0,1)->(0,2)->(1,2)->(1,1)->(0,1).",
            "Naive exploration causes infinite looping and agent starvation."
        ]
    )

    add_card(
        s4, Inches(6.8), Inches(1.6), Inches(2.7), Inches(5.2),
        title="3. Dynamic Switch",
        body_bullets=[
            "Floor switch cell at special coordinates.",
            "Visiting the switch toggles gate direction by 180 degrees.",
            "Unlocks impassable barriers protecting the goal sector."
        ]
    )

    add_card(
        s4, Inches(9.8), Inches(1.6), Inches(2.7), Inches(5.2),
        title="4. Override Token",
        body_bullets=[
            "Special consumable token located on the grid.",
            "Permits moving against an arrow direction exactly once.",
            "Enables strategic shortcuts that drastically shorten path length."
        ],
        is_black=True
    )

    # ==============================================================================
    # SLIDE 5: 4D MARKOV STATE SPACE FORMULATION
    # ==============================================================================
    s5 = create_blank_slide(prs)
    add_slide_header(s5, "Mathematical MDP Formulation & 4D Markov State Space")

    add_card(
        s5, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
        title="Why 2D Fails the Markov Property",
        body_bullets=[
            "Markov Property: P(s_{t+1} | s_t, a_t) must depend ONLY on current state and action.",
            "Failure Mode 1 (Switch): Direction of dynamic arrows depends on whether switch has been visited an odd or even number of times.",
            "Failure Mode 2 (Token): Permission to violate arrows depends on whether the token has been picked up AND whether it was already consumed.",
            "Conclusion: Spatial coordinate (r, c) alone is fundamentally non-Markovian!"
        ]
    )

    add_card(
        s5, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
        title="The 4D State Space Vector: s = (r, c, tau, sigma)",
        body_bullets=[
            "r in {0, ..., H-1}: Vertical row grid index.",
            "c in {0, ..., W-1}: Horizontal column grid index.",
            "tau in {0, 1, 2}: Token status (0 = On grid, 1 = Possessed by agent, 2 = Consumed/used).",
            "sigma in {0, 1}: Dynamic switch orientation (0 = Normal, 1 = Inverted).",
            "Total State Cardinality: |S| = H * W * |T| * |Sigma|.",
            "Map 1 (5x5): |S| = 25 states.",
            "Map 2 (6x6 with switch): |S| = 72 states.",
            "Map 3 (7x7 master challenge): |S| = 294 states."
        ],
        is_black=True
    )

    # ==============================================================================
    # SLIDE 6: OPERATIONAL MECHANICS & REWARDS
    # ==============================================================================
    s6 = create_blank_slide(prs)
    add_slide_header(s6, "Operational Modes & Multi-Objective Reward Design")

    add_card(
        s6, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
        title="Dual Invalid Action Modes",
        body_bullets=[
            "Mode 1: Action Masking ('action_mask'):",
            "  - Environment computes boolean vector M(s) in {0, 1}^4.",
            "  - Invalid actions (walls, boundaries, arrows without token) are filtered.",
            "  - The agent never wastes samples colliding into obstacles.",
            "Mode 2: Penalty Stay ('penalty_stay'):",
            "  - All 4 actions physically selectable.",
            "  - Illegal actions incur R_invalid = -10.0 penalty with state retention.",
            "  - Empirically increases sample complexity by >350%."
        ]
    )

    add_card(
        s6, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
        title="Reward Structure R(s, a, s')",
        body_bullets=[
            "R_step = -1.0: Incurred on every valid move to drive shortest path discovery.",
            "R_goal = +100.0: Terminal absorbing reward upon reaching (r_goal, c_goal).",
            "R_token = +5.0: Immediate positive bonus upon stepping on uncollected token.",
            "R_invalid = -10.0: Penalty incurred in penalty_stay mode for illegal moves.",
            "Objective: Maximize expected discounted return G_t = sum gamma^k r_{t+k} with gamma = 0.99."
        ]
    )

    # ==============================================================================
    # SLIDE 7: MAP TOPOLOGIES & DIFFICULTY METRICS
    # ==============================================================================
    s7 = create_blank_slide(prs)
    add_slide_header(s7, "Benchmark Map Topologies & Quantitative Difficulty Index")

    add_card(
        s7, Inches(0.8), Inches(1.6), Inches(4.8), Inches(5.2),
        title="Environmental Difficulty Index D",
        body_bullets=[
            "Mathematical Formulation:",
            "  D = 1.8 * log10(|S|) + 2.5 * rho_arrow + 1.5 * rho_wall + 1.5 * I_sw + 1.2 * I_tok + 1.5 * (N_cyc / 8)",
            "Map 1: D = 3.72 / 10 (25 states, 4-node cycle, 25% arrows).",
            "Map 2: D = 5.66 / 10 (72 states, switch-inverted gate).",
            "Map 3: D = 8.12 / 10 (294 states, token shortcut bifurcation vs safe detour)."
        ]
    )

    fig_diff = os.path.join(RESULTS_DIR, "fig_map_difficulty_metrics.png")
    if os.path.exists(fig_diff):
        s7.shapes.add_picture(fig_diff, Inches(5.9), Inches(1.6), width=Inches(6.6))

    # ==============================================================================
    # SLIDE 8: 5 REINFORCEMENT LEARNING ALGORITHMS OVERVIEW
    # ==============================================================================
    s8 = create_blank_slide(prs)
    add_slide_header(s8, "Algorithmic Suite: 5 Reinforcement Learning Paradigms")

    add_card(
        s8, Inches(0.8), Inches(1.6), Inches(3.6), Inches(5.2),
        title="Model-Based DP",
        body_bullets=[
            "1. Value Iteration:",
            "  - Computes V*(s) via Bellman optimality operator.",
            "  - Stopping rule: delta < 1e-6.",
            "2. Policy Iteration:",
            "  - Decoupled Policy Evaluation + Greedy Policy Improvement.",
            "  - Exact finite convergence."
        ]
    )

    add_card(
        s8, Inches(4.8), Inches(1.6), Inches(3.6), Inches(5.2),
        title="Model-Free TD Control",
        body_bullets=[
            "3. Tabular Q-Learning:",
            "  - Off-policy 1-step TD.",
            "  - Update target: r + gamma * max_{a'} Q(s', a').",
            "4. Tabular SARSA:",
            "  - On-policy 1-step TD.",
            "  - Update target: r + gamma * Q(s', a').",
            "  - Cautious exploration near deadlocks."
        ]
    )

    add_card(
        s8, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.2),
        title="Model-Free MC Control",
        body_bullets=[
            "5. First-Visit Monte Carlo:",
            "  - Pure episodic rollouts.",
            "  - No transition model.",
            "  - No bootstrapping (true returns G_t).",
            "  - Updates Q(s, a) on first state-action visit.",
            "  - High sample variance in loops."
        ],
        is_black=True
    )

    # ==============================================================================
    # SLIDE 9: DYNAMIC PROGRAMMING: VALUE & POLICY ITERATION
    # ==============================================================================
    s9 = create_blank_slide(prs)
    add_slide_header(s9, "Dynamic Programming: Value Iteration & Policy Iteration")

    add_card(
        s9, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
        title="Algorithm 1: Value Iteration",
        body_bullets=[
            "Bellman Optimality Operator:",
            "  V_{k+1}(s) = max_a sum_{s'} P(s'|s,a) [ R(s,a,s') + gamma * V_k(s') ]",
            "Extraction of Optimal Policy pi*(s):",
            "  pi*(s) = argmax_a sum_{s'} P(s'|s,a) [ R(s,a,s') + gamma * V*(s') ]",
            "Convergence: Exactly 72 sweeps on Map 3 in 0.089 seconds.",
            "Guaranteed globally optimal policy with zero variance."
        ]
    )

    add_card(
        s9, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
        title="Algorithm 2: Policy Iteration",
        body_bullets=[
            "Phase 1: Policy Evaluation (Iterative Bellman Expectation):",
            "  V^{pi}(s) = sum_{s'} P(s'|s,pi(s)) [ R(s,pi(s),s') + gamma * V^{pi}(s') ]",
            "Phase 2: Greedy Policy Improvement:",
            "  pi'(s) = argmax_a sum_{s'} P(s'|s,a) [ R(s,a,s') + gamma * V^{pi}(s') ]",
            "Finite Convergence: Only 4 policy improvement iterations on Map 3!",
            "Fastest wall-clock runtime: 0.038 seconds (56x faster than MC)."
        ],
        is_black=True
    )

    # ==============================================================================
    # SLIDE 10: TEMPORAL DIFFERENCE: Q-LEARNING VS SARSA
    # ==============================================================================
    s10 = create_blank_slide(prs)
    add_slide_header(s10, "Temporal Difference Control: Q-Learning vs SARSA")

    add_card(
        s10, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
        title="Algorithm 3: Tabular Q-Learning (Off-Policy)",
        body_bullets=[
            "Update Equation:",
            "  Q(s, a) <- Q(s, a) + alpha * [ r + gamma * max_{a'} Q(s', a') - Q(s, a) ]",
            "Target Policy: Deterministic greedy policy wrt Q.",
            "Behavioral Policy: Epsilon-greedy with exponential decay.",
            "Key Characteristic: Learns the optimal shortcut route aggressively even while exploring suboptimally.",
            "Convergence: 118 episodes on Map 3."
        ]
    )

    add_card(
        s10, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
        title="Algorithm 4: Tabular SARSA (On-Policy)",
        body_bullets=[
            "Update Equation:",
            "  Q(s, a) <- Q(s, a) + alpha * [ r + gamma * Q(s', a') - Q(s, a) ]",
            "Target Policy: Identical to behavioral policy (uses actual a').",
            "Safety Inductive Bias: Penalizes states near arrow deadlocks because exploration might trigger cycle traps.",
            "Convergence: 142 episodes on Map 3 (safer early trajectory learning)."
        ]
    )

    # ==============================================================================
    # SLIDE 11: MONTE CARLO CONTROL
    # ==============================================================================
    s11 = create_blank_slide(prs)
    add_slide_header(s11, "Algorithm 5: First-Visit Monte Carlo Control")

    add_card(
        s11, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
        title="First-Visit Episodic Update",
        body_bullets=[
            "Rollout Generation: Simulates complete episodes to termination or truncation.",
            "Backward Return Computation: G_t = sum_{k=0}^{T-t-1} gamma^k * r_{t+k}.",
            "First-Visit Check: Updates Q(s_t, a_t) only on the first time (s, a) appears in trajectory.",
            "Update Rule: Q(s_t, a_t) <- Q(s_t, a_t) + alpha * [ G_t - Q(s_t, a_t) ].",
            "No Bootstrapping: Relies on true environmental returns rather than estimates."
        ]
    )

    add_card(
        s11, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
        title="Strengths & Weaknesses in Cyclic Domains",
        body_bullets=[
            "Strength: Completely unbiased estimate of returns; no model assumptions.",
            "Weakness: High variance in wandering trajectories; requires episodes to terminate before updating.",
            "Cyclic Deadlock Penalty: If an agent wanders in a loop until step-limit truncation, zero goal credit is assigned.",
            "Empirical Result: Required 225 episodes on Map 3 (2x more environment interactions than Q-Learning)."
        ],
        is_black=True
    )

    # ==============================================================================
    # SLIDE 12: THEORETICAL COMPARISON TABLE
    # ==============================================================================
    s12 = create_blank_slide(prs)
    add_slide_header(s12, "Theoretical Comparison: The 5 RL Paradigms")

    rows = 6
    cols = 6
    t_shape = s12.shapes.add_table(rows, cols, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.2))
    tbl = t_shape.table

    headers = ["Algorithm", "Model Required", "Policy Type", "Bootstrapping", "Update Operator", "Guarantee"]
    for i, h in enumerate(headers):
        c = tbl.cell(0, i)
        c.text = h
        c.fill.solid()
        c.fill.fore_color.rgb = C_BLACK
        p = c.text_frame.paragraphs[0]
        p.font.name = "Arial"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_WHITE

    t_data = [
        ("Value Iteration", "Model P(s'|s,a)", "Exact Bellman", "Yes (Full sweep)", "max_a sum P [R + gamma V]", "Exact V* (theta-tolerance)"),
        ("Policy Iteration", "Model P(s'|s,a)", "Exact Policy Eval", "Yes (Full sweep)", "sum P [R + gamma V^pi]", "Exact pi* (Finite iters)"),
        ("Tabular Q-Learning", "Model-Free", "Off-Policy", "Yes (1-step TD)", "r + gamma max_a' Q(s', a')", "Asymptotic to Q*"),
        ("SARSA", "Model-Free", "On-Policy", "Yes (1-step TD)", "r + gamma Q(s', a')", "Asymptotic to Q^pi"),
        ("Monte Carlo Control", "Model-Free", "On-Policy (First-Visit)", "No (Empirical G_t)", "Return G_t = sum gamma^k r", "Asymptotic (GLIE)")
    ]

    for r_idx, row in enumerate(t_data, start=1):
        for c_idx, val in enumerate(row):
            c = tbl.cell(r_idx, c_idx)
            c.text = val
            c.fill.solid()
            c.fill.fore_color.rgb = C_GRAY_LIGHT if r_idx % 2 == 1 else C_WHITE
            p = c.text_frame.paragraphs[0]
            p.font.name = "Arial"
            p.font.size = Pt(9.5)
            p.font.color.rgb = C_BLACK

    # ==============================================================================
    # SLIDE 13: EMPIRICAL BENCHMARK: LEARNING CURVES
    # ==============================================================================
    s13 = create_blank_slide(prs)
    add_slide_header(s13, "Empirical Benchmark: Learning Curves & Sample Efficiency")

    add_card(
        s13, Inches(0.8), Inches(1.6), Inches(4.2), Inches(5.2),
        title="Multi-Seed Training Dynamics",
        body_bullets=[
            "Evaluated across 3 independent random seeds (42, 101, 2024).",
            "Map 1 (5x5): All algorithms rapidly reach optimal reward (+92.0) within 70 episodes.",
            "Map 3 (7x7 Master Challenge):",
            "  - Q-Learning reaches 95% optimality at Episode 118.",
            "  - SARSA converges smoothly at Episode 142.",
            "  - Monte Carlo exhibits high variance, reaching plateau at Episode 225."
        ]
    )

    fig_curves = os.path.join(RESULTS_DIR, "curve_all_5_algorithms.png")
    if os.path.exists(fig_curves):
        s13.shapes.add_picture(fig_curves, Inches(5.3), Inches(1.6), width=Inches(7.2))

    # ==============================================================================
    # SLIDE 14: RUNTIME & PATH QUALITY
    # ==============================================================================
    s14 = create_blank_slide(prs)
    add_slide_header(s14, "Empirical Benchmark: Wall-Clock Runtime vs Path Optimality")

    add_card(
        s14, Inches(0.8), Inches(1.6), Inches(4.2), Inches(5.2),
        title="Quantitative Trade-Offs",
        body_bullets=[
            "Analytical Speed of Dynamic Programming:",
            "  - Policy Iteration: 0.038 s (56x faster than MC).",
            "  - Value Iteration: 0.089 s (24x faster than MC).",
            "Model-Free Sample Costs (400 episodes):",
            "  - SARSA: 1.580 s   |   Q-Learning: 1.650 s.",
            "  - Monte Carlo: 2.140 s.",
            "Path Optimality on Map 3:",
            "  - All DP and TD algorithms discover the 12-step optimal shortcut path.",
            "  - Monte Carlo averages 13.4 steps."
        ]
    )

    fig_bars = os.path.join(RESULTS_DIR, "bar_steps_runtime_5_algos.png")
    if os.path.exists(fig_bars):
        s14.shapes.add_picture(fig_bars, Inches(5.3), Inches(1.6), width=Inches(7.2))

    # ==============================================================================
    # SLIDE 15: VISUAL POLICY & TRAJECTORY VERIFICATION
    # ==============================================================================
    s15 = create_blank_slide(prs)
    add_slide_header(s15, "Optimal Policy Vector Fields & Executed Trajectories")

    fig_m1 = os.path.join(RESULTS_DIR, "map1_optimal_policy_5_algos.png")
    fig_m3 = os.path.join(RESULTS_DIR, "map3_optimal_policy_5_algos.png")

    if os.path.exists(fig_m1):
        s15.shapes.add_picture(fig_m1, Inches(0.8), Inches(1.6), width=Inches(5.7))
    if os.path.exists(fig_m3):
        s15.shapes.add_picture(fig_m3, Inches(6.8), Inches(1.6), width=Inches(5.7))

    # Bottom caption box
    add_card(
        s15, Inches(0.8), Inches(5.9), Inches(11.733), Inches(1.0),
        title="Visual Policy Insights",
        body_bullets=[
            "Map 1: Policy directs agent south around the obstacle, avoiding the 2x2 arrow deadlock cycle completely.",
            "Map 3: Agent picks up Override Token at (0,4), travels down column 6, and breaks through arrow barrier at (3,6) to reach Goal in 12 steps."
        ]
    )

    # ==============================================================================
    # SLIDE 16: AGENT DIAGNOSTICS: DEADLOCK & ENTROPY
    # ==============================================================================
    s16 = create_blank_slide(prs)
    add_slide_header(s16, "Agent Diagnostics: Deadlock Trapping & Exploration Entropy")

    add_card(
        s16, Inches(0.8), Inches(1.6), Inches(4.2), Inches(5.2),
        title="Action Masking Impact",
        body_bullets=[
            "Cycle Entrapment Reduction:",
            "  - Unmasked penalty mode spends 65 steps/ep in deadlock loops.",
            "  - Action masking suppresses cycle trapping to 0% after 60 episodes.",
            "Exploration Diversity (Shannon Entropy):",
            "  - Action masking maintains elevated state visitation entropy across productive corridors.",
            "  - Yields 3.6x faster empirical convergence."
        ]
    )

    fig_diag = os.path.join(RESULTS_DIR, "fig_agent_diagnostics_deadlock_entropy.png")
    if os.path.exists(fig_diag):
        s16.shapes.add_picture(fig_diag, Inches(5.3), Inches(1.6), width=Inches(7.2))

    # ==============================================================================
    # SLIDE 17: SCIENTIFIC FINDINGS & ENGINEERING LESSONS
    # ==============================================================================
    s17 = create_blank_slide(prs)
    add_slide_header(s17, "Key Scientific Findings & Practical Recommendations")

    add_card(
        s17, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
        title="Key Scientific Findings",
        body_bullets=[
            "1. 4D State Space is Indispensable: Modeling token and switch states is strictly required to preserve the Markov property and guarantee convergence.",
            "2. Policy Iteration Superiority: Solves known MDPs in fractions of a second (4 policy improvement iterations).",
            "3. Off-Policy Exploration Advantage: Q-learning discovers high-reward token shortcuts faster than SARSA due to max-operator bootstrapping.",
            "4. Bootstrapping vs True Returns: Without 1-step TD bootstrapping, Monte Carlo suffers high variance in cyclic gridworlds."
        ]
    )

    add_card(
        s17, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
        title="Practical Recommendations",
        body_bullets=[
            "• Use Action Masking as an Inductive Safety Bias: Dramatically reduces exploratory collisions and accelerates learning by >350%.",
            "• Prefer Model-Based Methods when Dynamics are Accessible: DP produces zero-variance, mathematically exact policies.",
            "• Future Extensions:",
            "  - Deep RL (DQN / PPO) with invalid action masking for continuous domains.",
            "  - Multi-agent one-way routing networks with decentralized token negotiation.",
            "  - Stochastic slippery transition dynamics."
        ],
        is_black=True
    )

    # ==============================================================================
    # SLIDE 18: CONCLUSION & Q&A
    # ==============================================================================
    s18 = create_blank_slide(prs)

    # Big Frame Box
    f18 = s18.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.7), Inches(11.733), Inches(6.1))
    f18.fill.solid()
    f18.fill.fore_color.rgb = C_BLACK
    f18.line.fill.background()

    # Logo
    if os.path.exists(LOGO_OFFICIAL):
        s18.shapes.add_picture(LOGO_OFFICIAL, Inches(4.7), Inches(1.2), width=Inches(3.9))

    tb_end = s18.shapes.add_textbox(Inches(1.2), Inches(3.0), Inches(10.9), Inches(1.6))
    p_e1 = tb_end.text_frame.paragraphs[0]
    p_e1.text = "THANK YOU FOR YOUR ATTENTION!"
    p_e1.alignment = PP_ALIGN.CENTER
    p_e1.font.name = "Arial"
    p_e1.font.size = Pt(28)
    p_e1.font.bold = True
    p_e1.font.color.rgb = C_WHITE

    p_e2 = tb_end.text_frame.add_paragraph()
    p_e2.text = "PROJECT 21: ONE-WAY ARROW GRID NAVIGATION\nA Comprehensive Benchmark of 5 Reinforcement Learning Algorithms"
    p_e2.alignment = PP_ALIGN.CENTER
    p_e2.font.name = "Arial"
    p_e2.font.size = Pt(14)
    p_e2.font.italic = True
    p_e2.font.color.rgb = C_WHITE

    p_e3 = tb_end.text_frame.add_paragraph()
    p_e3.text = "\nFaculty of Electrical & Electronic Engineering • Phenikaa University\nQuestions & Answers"
    p_e3.alignment = PP_ALIGN.CENTER
    p_e3.font.name = "Arial"
    p_e3.font.size = Pt(13)
    p_e3.font.bold = True
    p_e3.font.color.rgb = C_WHITE

    # Save to primary and secondary outputs
    for p_out in [PPTX_OUTPUT_PRIMARY, PPTX_OUTPUT_SECONDARY]:
        try:
            prs.save(p_out)
            print(f"[SUCCESS] Black-and-white PowerPoint generated: {p_out}")
        except PermissionError:
            print(f"[WARNING] Could not save to {p_out} (file locked).")


if __name__ == "__main__":
    build_presentation()

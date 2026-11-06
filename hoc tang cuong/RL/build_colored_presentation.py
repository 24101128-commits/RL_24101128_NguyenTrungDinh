"""
build_colored_presentation.py
Generates a modern, beautifully color-distributed PowerPoint presentation (18 slides)
using a harmonious academic palette inspired by Phenikaa University:
- Deep Navy Blue (#003366), Cobalt Blue (#1D4ED8), Phenikaa Amber/Orange (#EA580C),
  Emerald Green (#059669), and Crimson Accent (#DC2626).
- Official Phenikaa University Logo (logo_phenikaa_official.png) on title, section, and closing slides.
- Rich visual cards with colored accent headers, badges, metric callouts, and clean borders.
- Embedded high-resolution technical charts from C:\RL\results.
- Saves to C:\RL\presentation_colored.pptx and C:\RL\presentation_updated.pptx.
"""

import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

PPTX_OUTPUT_PRIMARY = r"C:\RL\presentation_colored.pptx"
PPTX_OUTPUT_SECONDARY = r"C:\RL\presentation_updated.pptx"

ASSETS_DIR = r"C:\RL\assets"
RESULTS_DIR = r"C:\RL\results"

LOGO_OFFICIAL = os.path.join(ASSETS_DIR, "logo_phenikaa_official.png")
if not os.path.exists(LOGO_OFFICIAL):
    LOGO_OFFICIAL = os.path.join(ASSETS_DIR, "logo_phenikaa.png")

# ==============================================================================
# HARMONIOUS COLOR PALETTE (Phenikaa Brand + Modern UI Accents)
# ==============================================================================
COLOR_NAVY = RGBColor(0x00, 0x33, 0x66)       # Primary Deep Navy
COLOR_BLUE = RGBColor(0x1D, 0x4E, 0xD8)       # Royal Cobalt Blue
COLOR_BLUE_LIGHT = RGBColor(0xEF, 0xF6, 0xFF) # Soft Blue Tint
COLOR_AMBER = RGBColor(0xEA, 0x58, 0x0C)      # Phenikaa Warm Orange / Amber
COLOR_AMBER_LIGHT = RGBColor(0xFF, 0xF7, 0xED)# Soft Amber Tint
COLOR_GREEN = RGBColor(0x05, 0x96, 0x69)      # Emerald Success Green
COLOR_GREEN_LIGHT = RGBColor(0xEC, 0xFD, 0xF5)# Soft Green Tint
COLOR_RED = RGBColor(0xDC, 0x26, 0x26)        # Danger / Penalty Red
COLOR_RED_LIGHT = RGBColor(0xFE, 0xF2, 0xF2)  # Soft Red Tint
COLOR_SLATE_DARK = RGBColor(0x0F, 0x17, 0x2A) # Charcoal Dark Text
COLOR_SLATE_MUTED = RGBColor(0x47, 0x55, 0x69)# Neutral Muted Body Text
COLOR_BG = RGBColor(0xF8, 0xFA, 0xFC)         # Crisp Off-White / Slate Background
COLOR_WHITE = RGBColor(0xFF, 0xFF, 0xFF)      # Pure White Card Fill
COLOR_BORDER = RGBColor(0xE2, 0xE8, 0xF0)     # Clean Card Border


def create_base_slide(prs, bg_color=COLOR_BG):
    """Creates a blank slide with customized background fill."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = bg_color
    bg.line.fill.background()
    return slide


def add_slide_header(
    slide,
    title_text,
    category_text="PHENIKAA UNIVERSITY • ADVANCED REINFORCEMENT LEARNING",
    badge_text=None,
    badge_color=COLOR_BLUE
):
    """Adds a modern, beautifully structured slide header with category tracker and logo."""
    # Top accent bar
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.35), Inches(11.733), Inches(0.04))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = COLOR_NAVY
    top_bar.line.fill.background()

    # Category tracker line
    tb_cat = slide.shapes.add_textbox(Inches(0.8), Inches(0.44), Inches(8.5), Inches(0.28))
    tf_c = tb_cat.text_frame
    tf_c.word_wrap = True
    p_c = tf_c.paragraphs[0]
    p_c.text = category_text.upper()
    p_c.font.name = "Arial"
    p_c.font.size = Pt(9.5)
    p_c.font.bold = True
    p_c.font.color.rgb = COLOR_AMBER

    # Title & Optional Badge
    tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(9.4), Inches(0.65))
    tf_t = tb_title.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = title_text
    p_t.font.name = "Arial"
    p_t.font.size = Pt(22)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_NAVY

    # Corner Official Logo
    if os.path.exists(LOGO_OFFICIAL):
        slide.shapes.add_picture(LOGO_OFFICIAL, Inches(10.6), Inches(0.42), width=Inches(1.95))


def add_modern_card(
    slide,
    left,
    top,
    width,
    height,
    title="",
    body_bullets=None,
    accent_color=COLOR_NAVY,
    bg_color=COLOR_WHITE,
    border_color=COLOR_BORDER,
    pill_text=None
):
    """
    Renders a modern container card with colored top accent border,
    optional category pill, title, and formatted bullet points.
    """
    # Card Background shape
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = border_color
    card.line.width = Pt(1.2)

    # Accent top border indicator strip
    strip = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left + Inches(0.08), top + Inches(0.02), width - Inches(0.16), Inches(0.06))
    strip.fill.solid()
    strip.fill.fore_color.rgb = accent_color
    strip.line.fill.background()

    # Text content frame
    tb = slide.shapes.add_textbox(left + Inches(0.18), top + Inches(0.12), width - Inches(0.36), height - Inches(0.24))
    tf = tb.text_frame
    tf.word_wrap = True

    if pill_text:
        p_pill = tf.paragraphs[0]
        p_pill.text = f"[{pill_text.upper()}]"
        p_pill.font.name = "Arial"
        p_pill.font.size = Pt(8.5)
        p_pill.font.bold = True
        p_pill.font.color.rgb = accent_color
        p_pill.space_after = Pt(2)

    if title:
        p_t = tf.add_paragraph() if pill_text else tf.paragraphs[0]
        p_t.text = title
        p_t.font.name = "Arial"
        p_t.font.size = Pt(13.5)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_NAVY
        p_t.space_after = Pt(6)

    if body_bullets:
        for idx, bullet in enumerate(body_bullets):
            p = tf.add_paragraph() if (title or pill_text or idx > 0) else tf.paragraphs[0]
            p.text = f"•  {bullet}"
            p.font.name = "Arial"
            p.font.size = Pt(10.5)
            p.font.color.rgb = COLOR_SLATE_DARK
            p.space_after = Pt(3.5)


def add_metric_callout_box(slide, left, top, width, height, value_text, label_text, sublabel="", accent_color=COLOR_BLUE):
    """Creates a high-impact numerical metric stat card."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = COLOR_WHITE
    card.line.color.rgb = accent_color
    card.line.width = Pt(1.5)

    tb = slide.shapes.add_textbox(left + Inches(0.1), top + Inches(0.1), width - Inches(0.2), height - Inches(0.2))
    tf = tb.text_frame
    tf.word_wrap = True

    p_val = tf.paragraphs[0]
    p_val.text = value_text
    p_val.alignment = PP_ALIGN.CENTER
    p_val.font.name = "Arial"
    p_val.font.size = Pt(24)
    p_val.font.bold = True
    p_val.font.color.rgb = accent_color

    p_lbl = tf.add_paragraph()
    p_lbl.text = label_text
    p_lbl.alignment = PP_ALIGN.CENTER
    p_lbl.font.name = "Arial"
    p_lbl.font.size = Pt(10)
    p_lbl.font.bold = True
    p_lbl.font.color.rgb = COLOR_NAVY

    if sublabel:
        p_sub = tf.add_paragraph()
        p_sub.text = sublabel
        p_sub.alignment = PP_ALIGN.CENTER
        p_sub.font.name = "Arial"
        p_sub.font.size = Pt(8.5)
        p_sub.font.color.rgb = COLOR_SLATE_MUTED


def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # ==============================================================================
    # SLIDE 1: TITLE SLIDE (Hero Navy Background with Gold/White Accents)
    # ==============================================================================
    s1 = create_base_slide(prs, bg_color=COLOR_NAVY)

    # White Hero Container
    container = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.6), Inches(11.733), Inches(6.3))
    container.fill.solid()
    container.fill.fore_color.rgb = COLOR_WHITE
    container.line.color.rgb = COLOR_AMBER
    container.line.width = Pt(2.5)

    # Official Phenikaa University Logo
    if os.path.exists(LOGO_OFFICIAL):
        s1.shapes.add_picture(LOGO_OFFICIAL, Inches(4.7), Inches(0.95), width=Inches(3.9))

    # University header subtitle
    tb_u = s1.shapes.add_textbox(Inches(1.2), Inches(2.65), Inches(10.9), Inches(0.6))
    p_u = tb_u.text_frame.paragraphs[0]
    p_u.text = "FACULTY OF ELECTRICAL & ELECTRONIC ENGINEERING\nDEPARTMENT OF INTELLIGENT SYSTEMS & AUTOMATION"
    p_u.alignment = PP_ALIGN.CENTER
    p_u.font.name = "Arial"
    p_u.font.size = Pt(12.5)
    p_u.font.bold = True
    p_u.font.color.rgb = COLOR_NAVY

    # Project Title
    tb_t = s1.shapes.add_textbox(Inches(1.2), Inches(3.45), Inches(10.9), Inches(1.3))
    p_t = tb_t.text_frame.paragraphs[0]
    p_t.text = "PROJECT 21: ONE-WAY ARROW GRID NAVIGATION"
    p_t.alignment = PP_ALIGN.CENTER
    p_t.font.name = "Arial"
    p_t.font.size = Pt(26)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_NAVY

    p_sub = tb_t.text_frame.add_paragraph()
    p_sub.text = "A Comprehensive Empirical Benchmark of 5 Reinforcement Learning Algorithms\n(Value Iteration, Policy Iteration, Tabular Q-Learning, SARSA, Monte Carlo Control)"
    p_sub.alignment = PP_ALIGN.CENTER
    p_sub.font.name = "Arial"
    p_sub.font.size = Pt(13)
    p_sub.font.italic = True
    p_sub.font.color.rgb = COLOR_BLUE

    # Colored Metadata Banner at Bottom
    meta_banner = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.5), Inches(5.25), Inches(10.333), Inches(1.25))
    meta_banner.fill.solid()
    meta_banner.fill.fore_color.rgb = COLOR_NAVY
    meta_banner.line.color.rgb = COLOR_AMBER
    meta_banner.line.width = Pt(1.5)

    tb_m = s1.shapes.add_textbox(Inches(1.6), Inches(5.35), Inches(10.1), Inches(1.0))
    p_m1 = tb_m.text_frame.paragraphs[0]
    p_m1.text = "STUDENT RESEARCH TEAM: Group Project 21   •   COURSE: Advanced Reinforcement Learning (ECE-RL401)"
    p_m1.alignment = PP_ALIGN.CENTER
    p_m1.font.name = "Arial"
    p_m1.font.size = Pt(11)
    p_m1.font.bold = True
    p_m1.font.color.rgb = COLOR_WHITE

    p_m2 = tb_m.text_frame.add_paragraph()
    p_m2.text = "PHENIKAA UNIVERSITY • HANOI, VIETNAM • ACADEMIC YEAR 2026-2027"
    p_m2.alignment = PP_ALIGN.CENTER
    p_m2.font.name = "Arial"
    p_m2.font.size = Pt(10)
    p_m2.font.bold = True
    p_m2.font.color.rgb = COLOR_AMBER

    # ==============================================================================
    # SLIDE 2: EXECUTIVE SUMMARY & AGENDA
    # ==============================================================================
    s2 = create_base_slide(prs)
    add_slide_header(s2, "Executive Overview & Presentation Blueprint", category_text="Project 21 • Blueprint")

    # 4 Colored Summary Cards
    add_modern_card(
        s2, Inches(0.8), Inches(1.6), Inches(2.7), Inches(5.2),
        title="1. Challenge",
        pill_text="Problem Domain",
        accent_color=COLOR_RED,
        bg_color=COLOR_WHITE,
        body_bullets=[
            "Non-isotropic spatial navigation with mandatory one-way corridors.",
            "Closed cyclic deadlocks trapping naive exploration.",
            "Dynamic invertible arrow gates toggled via floor switches.",
            "Override token granting single-use arrow rule violation."
        ]
    )

    add_modern_card(
        s2, Inches(3.8), Inches(1.6), Inches(2.7), Inches(5.2),
        title="2. MDP Solution",
        pill_text="Formulation",
        accent_color=COLOR_BLUE,
        bg_color=COLOR_WHITE,
        body_bullets=[
            "Spatial 2D coordinates violate the Markov property due to history memory.",
            "Augmented 4D state vector: s = (r, c, tau, sigma) in S.",
            "State space scaling: 25 -> 72 -> 294 discrete states.",
            "Action masking eliminates illegal explorations."
        ]
    )

    add_modern_card(
        s2, Inches(6.8), Inches(1.6), Inches(2.7), Inches(5.2),
        title="3. 5 Algorithms",
        pill_text="Suite",
        accent_color=COLOR_AMBER,
        bg_color=COLOR_WHITE,
        body_bullets=[
            "Model-Based DP: Value Iteration & Policy Iteration.",
            "Model-Free TD: Tabular Q-Learning (Off-policy) & SARSA (On-policy).",
            "Model-Free MC: First-Visit Monte Carlo Control.",
            "Tested across 3 maps & 3 independent seeds."
        ]
    )

    add_modern_card(
        s2, Inches(9.8), Inches(1.6), Inches(2.7), Inches(5.2),
        title="4. Key Results",
        pill_text="Empirical Insights",
        accent_color=COLOR_GREEN,
        bg_color=COLOR_WHITE,
        body_bullets=[
            "Policy Iteration converges in 0.038 s (56x faster than MC).",
            "Q-Learning discovers 12-step optimal shortcut in 118 episodes.",
            "Action masking accelerates sample learning by >350%.",
            "100% self-contained notebook runs on Colab."
        ]
    )

    # ==============================================================================
    # SLIDE 3: PROBLEM CONTEXT & MOTIVATION
    # ==============================================================================
    s3 = create_base_slide(prs)
    add_slide_header(s3, "Industrial Motivation: Flow Constraints in Autonomous Systems")

    add_modern_card(
        s3, Inches(0.8), Inches(1.6), Inches(3.6), Inches(5.2),
        title="Real-World Industrial Systems",
        pill_text="Engineering Context",
        accent_color=COLOR_NAVY,
        body_bullets=[
            "Automated Guided Vehicles (AGVs): Operating in narrow warehouse aisles where reverse motion creates gridlock.",
            "Semiconductor & Baggage Conveyors: Strict unidirectional transport flow.",
            "Urban Logistics & Traffic Networks: Regulated one-way street corridors.",
            "Air Traffic Corridors: Directional altitude lanes and mandatory flight vectors."
        ]
    )

    add_modern_card(
        s3, Inches(4.8), Inches(1.6), Inches(3.6), Inches(5.2),
        title="Limitations of Classical GridWorlds",
        pill_text="Research Gap",
        accent_color=COLOR_RED,
        body_bullets=[
            "Standard benchmarks assume bidirectional isotropic mobility.",
            "Fail to model non-reversible flow dynamics and topological deadlocks.",
            "Neglect dynamic gate inversion mechanisms triggered by remote switches.",
            "Ignore clearance tokens enabling single-use override privileges."
        ]
    )

    add_modern_card(
        s3, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.2),
        title="Project 21 Objective",
        pill_text="Core Deliverable",
        accent_color=COLOR_GREEN,
        body_bullets=[
            "Construct Gymnasium-compliant OneWayArrowEnv.",
            "Formulate strictly Markovian 4D state representation.",
            "Implement, benchmark, and contrast 5 RL paradigms across 3 difficulty maps.",
            "Synthesize safe, cycle-avoiding optimal path navigation."
        ]
    )

    # ==============================================================================
    # SLIDE 4: THE ONE-WAY ARROW GRIDWORLD
    # ==============================================================================
    s4 = create_base_slide(prs)
    add_slide_header(s4, "One-Way Arrow GridWorld: 4 Core Environmental Mechanics")

    add_modern_card(
        s4, Inches(0.8), Inches(1.6), Inches(2.7), Inches(5.2),
        title="Fixed Arrows",
        pill_text="Constraint 1",
        accent_color=COLOR_BLUE,
        body_bullets=[
            "Cells marked with cardinal directional arrows: ^, v, <, >.",
            "Agent occupying an arrow cell MUST move in the designated direction.",
            "Moving backwards is strictly forbidden unless using an override token."
        ]
    )

    add_modern_card(
        s4, Inches(3.8), Inches(1.6), Inches(2.7), Inches(5.2),
        title="Cyclic Deadlocks",
        pill_text="Constraint 2",
        accent_color=COLOR_RED,
        body_bullets=[
            "Sub-graphs of adjacent arrow cells arranged in closed 2x2 loops.",
            "Example: (0,1)->(0,2)->(1,2)->(1,1)->(0,1).",
            "Agents entering cycles starve in infinite loops unless guided by global value gradients."
        ]
    )

    add_modern_card(
        s4, Inches(6.8), Inches(1.6), Inches(2.7), Inches(5.2),
        title="Dynamic Switches",
        pill_text="Constraint 3",
        accent_color=COLOR_AMBER,
        body_bullets=[
            "Special switch coordinates on the grid.",
            "Visiting a switch toggles dynamic arrow corridors by 180 degrees.",
            "Unblocks impassable barrier passages leading directly to the goal."
        ]
    )

    add_modern_card(
        s4, Inches(9.8), Inches(1.6), Inches(2.7), Inches(5.2),
        title="Override Tokens",
        pill_text="Constraint 4",
        accent_color=COLOR_GREEN,
        body_bullets=[
            "Single-use clearance token placed on the grid.",
            "Grants permission to violate an arrow constraint exactly once.",
            "Enables high-reward shortcut routes that bypass lengthy detours."
        ]
    )

    # ==============================================================================
    # SLIDE 5: 4D MARKOV STATE SPACE FORMULATION
    # ==============================================================================
    s5 = create_base_slide(prs)
    add_slide_header(s5, "Mathematical MDP Formulation: Restoring the Markov Property")

    add_modern_card(
        s5, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
        title="The Markov Property Dilemma",
        pill_text="Theoretical Foundation",
        accent_color=COLOR_RED,
        body_bullets=[
            "Markov Axiom: P(s_{t+1} | s_t, a_t) = P(s_{t+1} | s_t, a_t, s_{t-1}, ...).",
            "Non-Markovian Breakdown in 2D Grid:",
            "  - Dynamic arrows depend on whether the switch was visited an odd or even number of times.",
            "  - Arrow override depends on whether the token has been picked up AND whether it was already consumed.",
            "Conclusion: Spatial coordinate (r, c) alone creates non-Markovian history dependency, causing classical tabular RL to fail!"
        ]
    )

    add_modern_card(
        s5, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
        title="The 4D Augmented State Vector: s = (r, c, tau, sigma)",
        pill_text="Exact Solution",
        accent_color=COLOR_BLUE,
        body_bullets=[
            "r in {0, ..., H-1}: Vertical row grid coordinate.",
            "c in {0, ..., W-1}: Horizontal column grid coordinate.",
            "tau in {0, 1, 2}: Token status (0 = On grid, 1 = Held by agent, 2 = Consumed/used).",
            "sigma in {0, 1}: Dynamic switch orientation (0 = Normal, 1 = Inverted).",
            "State Space Dimensionality:",
            "  - |S| = H * W * |T| * |Sigma|.",
            "  - Map 1 (5x5): 25 states   |   Map 2 (6x6): 72 states.",
            "  - Map 3 (7x7 Master Challenge): 294 discrete Markov states."
        ]
    )

    # ==============================================================================
    # SLIDE 6: OPERATIONAL MECHANICS & REWARD DESIGN
    # ==============================================================================
    s6 = create_base_slide(prs)
    add_slide_header(s6, "Operational Modes & Multi-Objective Reward Design")

    add_modern_card(
        s6, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
        title="Dual Invalid Action Modes",
        pill_text="Safety Mechanics",
        accent_color=COLOR_BLUE,
        body_bullets=[
            "Mode 1: Action Masking ('action_mask'):",
            "  - Environment computes boolean validity mask M(s) in {0, 1}^4.",
            "  - Illegal moves (boundaries, walls, arrows without token) are filtered.",
            "  - Prevents wasted exploratory samples; enforces 100% collision safety.",
            "Mode 2: Penalty Stay ('penalty_stay'):",
            "  - All 4 actions selectable physically.",
            "  - Illegal actions trigger R_invalid = -10.0 penalty with state retention.",
            "  - Requires >350% more training episodes to learn boundary constraints."
        ]
    )

    add_modern_card(
        s6, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
        title="Multi-Objective Reward Function R(s, a, s')",
        pill_text="Incentive Design",
        accent_color=COLOR_GREEN,
        body_bullets=[
            "R_step = -1.0: Incurred on every valid step to drive shortest path discovery.",
            "R_goal = +100.0: Absorbing terminal reward upon reaching (r_goal, c_goal).",
            "R_token = +5.0: Immediate positive incentive upon stepping on uncollected token.",
            "R_invalid = -10.0: Punitive cost applied in penalty_stay mode.",
            "Optimization Target: Maximize expected discounted return G_t = sum gamma^k r_{t+k} with gamma = 0.99."
        ]
    )

    # ==============================================================================
    # SLIDE 7: MAP TOPOLOGIES & DIFFICULTY INDEX
    # ==============================================================================
    s7 = create_base_slide(prs)
    add_slide_header(s7, "Benchmark Topologies & Environmental Difficulty Index")

    add_modern_card(
        s7, Inches(0.8), Inches(1.6), Inches(4.7), Inches(5.2),
        title="Quantitative Difficulty Score D",
        pill_text="Complexity Metric",
        accent_color=COLOR_AMBER,
        body_bullets=[
            "Formula Integrating Spatial & Topological Factors:",
            "  D = 1.8 log10(|S|) + 2.5 rho_arrow + 1.5 rho_wall + 1.5 I_sw + 1.2 I_tok + 1.5 (N_cyc / 8)",
            "Map 1: D = 3.72 / 10 (5x5, 25 states, 4-node deadlock cycle).",
            "Map 2: D = 5.66 / 10 (6x6, 72 states, switch-inverted gate).",
            "Map 3: D = 8.12 / 10 (7x7, 294 states, token shortcut vs safe detour bifurcation)."
        ]
    )

    fig_diff = os.path.join(RESULTS_DIR, "fig_map_difficulty_metrics.png")
    if os.path.exists(fig_diff):
        s7.shapes.add_picture(fig_diff, Inches(5.8), Inches(1.6), width=Inches(6.7))

    # ==============================================================================
    # SLIDE 8: THE 5 REINFORCEMENT LEARNING ALGORITHMS
    # ==============================================================================
    s8 = create_base_slide(prs)
    add_slide_header(s8, "Algorithmic Suite: 5 Reinforcement Learning Paradigms")

    add_modern_card(
        s8, Inches(0.8), Inches(1.6), Inches(3.6), Inches(5.2),
        title="Model-Based DP",
        pill_text="Analytical Solutions",
        accent_color=COLOR_BLUE,
        body_bullets=[
            "Accesses transition model P(s'|s,a) and reward model R.",
            "1. Value Iteration:",
            "  - Computes V*(s) via Bellman optimality operator.",
            "  - Convergence tolerance theta = 1e-6.",
            "2. Policy Iteration:",
            "  - Alternating Policy Evaluation & Policy Improvement.",
            "  - Exact finite convergence."
        ]
    )

    add_modern_card(
        s8, Inches(4.8), Inches(1.6), Inches(3.6), Inches(5.2),
        title="Model-Free TD Control",
        pill_text="Temporal Difference",
        accent_color=COLOR_AMBER,
        body_bullets=[
            "Learns from experience tuples (s, a, r, s') with 1-step bootstrapping.",
            "3. Tabular Q-Learning:",
            "  - Off-policy max operator target.",
            "  - Aggressive shortcut discovery.",
            "4. Tabular SARSA:",
            "  - On-policy actual action target.",
            "  - Cautious exploration near cycles."
        ]
    )

    add_modern_card(
        s8, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.2),
        title="Model-Free MC Control",
        pill_text="Episodic Rollouts",
        accent_color=COLOR_GREEN,
        body_bullets=[
            "Learns from complete episodic trajectories without a transition model.",
            "5. First-Visit Monte Carlo:",
            "  - Pure empirical return G_t.",
            "  - No bootstrapping assumptions.",
            "  - Updates Q(s, a) on first visit.",
            "  - Higher sample variance in wandering cycles."
        ]
    )

    # ==============================================================================
    # SLIDE 9: DYNAMIC PROGRAMMING: VALUE & POLICY ITERATION
    # ==============================================================================
    s9 = create_base_slide(prs)
    add_slide_header(s9, "Dynamic Programming: Value Iteration & Policy Iteration")

    add_modern_card(
        s9, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
        title="Algorithm 1: Value Iteration",
        pill_text="Bellman Optimality",
        accent_color=COLOR_BLUE,
        body_bullets=[
            "Bellman Optimality Operator:",
            "  V_{k+1}(s) = max_a sum_{s'} P(s'|s,a) [ R(s,a,s') + gamma * V_k(s') ]",
            "Optimal Policy Extraction:",
            "  pi*(s) = argmax_a sum_{s'} P(s'|s,a) [ R(s,a,s') + gamma * V*(s') ]",
            "Stopping Criterion: max_s |V_{k+1}(s) - V_k(s)| < 1e-6.",
            "Empirical Performance on Map 3:",
            "  - Converges in exactly 72 Bellman sweeps.",
            "  - Execution time: 0.089 seconds.",
            "  - Zero variance, globally optimal 12-step shortcut."
        ]
    )

    add_modern_card(
        s9, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
        title="Algorithm 2: Policy Iteration",
        pill_text="Policy Eval + Improvement",
        accent_color=COLOR_BLUE,
        body_bullets=[
            "Phase 1: Policy Evaluation (Iterative Bellman Expectation):",
            "  V^{pi}(s) = sum_{s'} P(s'|s,pi(s)) [ R(s,pi(s),s') + gamma * V^{pi}(s') ]",
            "Phase 2: Greedy Policy Improvement:",
            "  pi_{k+1}(s) = argmax_a sum_{s'} P(s'|s,a) [ R(s,a,s') + gamma * V^{pi_k}(s') ]",
            "Exact Finite Convergence:",
            "  - Terminated in only 4 policy iterations on Map 3!",
            "  - Fastest wall-clock runtime: 0.038 seconds (56x speedup vs MC).",
            "  - Produces identical mathematical global optimum."
        ]
    )

    # ==============================================================================
    # SLIDE 10: TEMPORAL DIFFERENCE: Q-LEARNING VS SARSA
    # ==============================================================================
    s10 = create_base_slide(prs)
    add_slide_header(s10, "Temporal Difference Control: Q-Learning vs SARSA")

    add_modern_card(
        s10, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
        title="Algorithm 3: Tabular Q-Learning",
        pill_text="Off-Policy TD",
        accent_color=COLOR_AMBER,
        body_bullets=[
            "TD(0) Update Equation:",
            "  Q(s, a) <- Q(s, a) + alpha * [ r + gamma * max_{a'} Q(s', a') - Q(s, a) ]",
            "Target Policy: Greedy wrt Q; Behavioral Policy: Epsilon-greedy.",
            "Aggressive Optimization:",
            "  - Bootstraps from max valid Q-value in successor state.",
            "  - Discovers the 12-step override token shortcut rapidly.",
            "Convergence: Episode 118 on Map 3 (Sample efficient)."
        ]
    )

    add_modern_card(
        s10, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
        title="Algorithm 4: Tabular SARSA",
        pill_text="On-Policy TD",
        accent_color=COLOR_AMBER,
        body_bullets=[
            "TD(0) Update Equation:",
            "  Q(s, a) <- Q(s, a) + alpha * [ r + gamma * Q(s', a') - Q(s, a) ]",
            "Target Policy: Same as executing behavioral policy (uses actual a').",
            "Safety Inductive Bias:",
            "  - Considers exploratory probability when evaluating s'.",
            "  - Avoids corridors near arrow deadlocks during training.",
            "Convergence: Episode 142 on Map 3 (safer early trajectory learning)."
        ]
    )

    # ==============================================================================
    # SLIDE 11: MONTE CARLO CONTROL
    # ==============================================================================
    s11 = create_base_slide(prs)
    add_slide_header(s11, "Algorithm 5: First-Visit Monte Carlo Control")

    add_modern_card(
        s11, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
        title="First-Visit Episodic Update",
        pill_text="True Returns (No Bootstrapping)",
        accent_color=COLOR_GREEN,
        body_bullets=[
            "Trajectory Generation: Simulates full episode until goal or max steps.",
            "Backward Return Calculation: G_t = sum_{k=0}^{T-t-1} gamma^k * r_{t+k}.",
            "First-Visit Update Rule:",
            "  Q(s_t, a_t) <- Q(s_t, a_t) + alpha * [ G_t - Q(s_t, a_t) ]",
            "Unbiased Property:",
            "  - Directly estimates expectation E[G_t | s, a] without bootstrapping assumptions.",
            "  - Independent of transition model dynamics."
        ]
    )

    add_modern_card(
        s11, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
        title="Credit Assignment Penalty in Loops",
        pill_text="Trade-offs & Limitations",
        accent_color=COLOR_RED,
        body_bullets=[
            "High Variance in Trajectories:",
            "  - Wandering in cycles delays episode completion.",
            "  - If truncated without reaching the goal, G_t = -max_steps, providing no credit towards the terminal reward.",
            "Empirical Convergence on Map 3:",
            "  - Requires 225 episodes (almost 2x more environment steps than Q-Learning).",
            "  - Slightly higher path step variance (13.4 steps vs 12.0 steps)."
        ]
    )

    # ==============================================================================
    # SLIDE 12: THEORETICAL COMPARISON TABLE
    # ==============================================================================
    s12 = create_base_slide(prs)
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
        c.fill.fore_color.rgb = COLOR_NAVY
        p = c.text_frame.paragraphs[0]
        p.font.name = "Arial"
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE

    t_data = [
        ("Value Iteration", "Model P(s'|s,a)", "Exact Bellman", "Yes (Full sweep)", "max_a sum P [R + gamma V]", "Exact V* (theta-tolerance)"),
        ("Policy Iteration", "Model P(s'|s,a)", "Exact Policy Eval", "Yes (Full sweep)", "sum P [R + gamma V^pi]", "Exact pi* (Finite iters)"),
        ("Tabular Q-Learning", "Model-Free", "Off-Policy", "Yes (1-step TD)", "r + gamma max_a' Q(s', a')", "Asymptotic to Q*"),
        ("SARSA", "Model-Free", "On-Policy", "Yes (1-step TD)", "r + gamma Q(s', a')", "Asymptotic to Q^pi"),
        ("Monte Carlo Control", "Model-Free", "On-Policy (First-Visit)", "No (Empirical G_t)", "Return G_t = sum gamma^k r", "Asymptotic (GLIE)")
    ]

    row_colors = [COLOR_BLUE_LIGHT, COLOR_BLUE_LIGHT, COLOR_AMBER_LIGHT, COLOR_AMBER_LIGHT, COLOR_GREEN_LIGHT]
    for r_idx, row in enumerate(t_data, start=1):
        for c_idx, val in enumerate(row):
            c = tbl.cell(r_idx, c_idx)
            c.text = val
            c.fill.solid()
            c.fill.fore_color.rgb = row_colors[r_idx - 1]
            p = c.text_frame.paragraphs[0]
            p.font.name = "Arial"
            p.font.size = Pt(9.5)
            p.font.color.rgb = COLOR_SLATE_DARK

    # ==============================================================================
    # SLIDE 13: EMPIRICAL BENCHMARK: LEARNING CURVES
    # ==============================================================================
    s13 = create_base_slide(prs)
    add_slide_header(s13, "Empirical Benchmark: Learning Curves & Sample Efficiency")

    add_modern_card(
        s13, Inches(0.8), Inches(1.6), Inches(4.2), Inches(5.2),
        title="Multi-Seed Training Dynamics",
        pill_text="Sample Efficiency",
        accent_color=COLOR_BLUE,
        body_bullets=[
            "Evaluated across 3 independent random seeds (42, 101, 2024).",
            "Map 1 (5x5 Basic):",
            "  - All algorithms reach optimal reward (+92.0) within 70 episodes.",
            "Map 3 (7x7 Master Challenge):",
            "  - Q-Learning reaches 95% optimality at Episode 118.",
            "  - SARSA stabilizes at Episode 142.",
            "  - Monte Carlo exhibits early variance, reaching plateau at Episode 225."
        ]
    )

    fig_curves = os.path.join(RESULTS_DIR, "curve_all_5_algorithms.png")
    if os.path.exists(fig_curves):
        s13.shapes.add_picture(fig_curves, Inches(5.3), Inches(1.6), width=Inches(7.2))

    # ==============================================================================
    # SLIDE 14: RUNTIME & PATH QUALITY
    # ==============================================================================
    s14 = create_base_slide(prs)
    add_slide_header(s14, "Empirical Benchmark: Wall-Clock Runtime vs Path Optimality")

    add_modern_card(
        s14, Inches(0.8), Inches(1.6), Inches(4.2), Inches(5.2),
        title="Quantitative Trade-Offs",
        pill_text="Runtime vs Quality",
        accent_color=COLOR_GREEN,
        body_bullets=[
            "Analytical Speed of Dynamic Programming:",
            "  - Policy Iteration: 0.038 s (56x speedup vs MC).",
            "  - Value Iteration: 0.089 s (24x speedup vs MC).",
            "Model-Free Sample Costs (400 episodes):",
            "  - SARSA: 1.580 s   |   Q-Learning: 1.650 s.",
            "  - Monte Carlo: 2.140 s.",
            "Path Optimality on Map 3:",
            "  - Both DP methods, Q-Learning, and SARSA discover the 12-step optimal shortcut.",
            "  - Monte Carlo averages 13.4 steps."
        ]
    )

    fig_bars = os.path.join(RESULTS_DIR, "bar_steps_runtime_5_algos.png")
    if os.path.exists(fig_bars):
        s14.shapes.add_picture(fig_bars, Inches(5.3), Inches(1.6), width=Inches(7.2))

    # ==============================================================================
    # SLIDE 15: VISUAL POLICY & TRAJECTORY VERIFICATION
    # ==============================================================================
    s15 = create_base_slide(prs)
    add_slide_header(s15, "Optimal Policy Vector Fields & Executed Trajectories")

    fig_m1 = os.path.join(RESULTS_DIR, "map1_optimal_policy_5_algos.png")
    fig_m3 = os.path.join(RESULTS_DIR, "map3_optimal_policy_5_algos.png")

    if os.path.exists(fig_m1):
        s15.shapes.add_picture(fig_m1, Inches(0.8), Inches(1.6), width=Inches(5.7))
    if os.path.exists(fig_m3):
        s15.shapes.add_picture(fig_m3, Inches(6.8), Inches(1.6), width=Inches(5.7))

    add_modern_card(
        s15, Inches(0.8), Inches(5.9), Inches(11.733), Inches(1.05),
        title="Visual Trajectory Insights",
        pill_text="Execution Verification",
        accent_color=COLOR_NAVY,
        body_bullets=[
            "Map 1: Policy directs agent south around the obstacle, completely avoiding the 2x2 arrow deadlock cycle.",
            "Map 3: Agent picks up Override Token at (0,4), descends column 6, and breaks through arrow barrier at (3,6) to reach Goal in exactly 12 steps."
        ]
    )

    # ==============================================================================
    # SLIDE 16: AGENT DIAGNOSTICS: DEADLOCK & ENTROPY
    # ==============================================================================
    s16 = create_base_slide(prs)
    add_slide_header(s16, "Agent Diagnostics: Deadlock Trapping & Exploration Entropy")

    add_modern_card(
        s16, Inches(0.8), Inches(1.6), Inches(4.2), Inches(5.2),
        title="Action Masking Impact",
        pill_text="Diagnostic Evidence",
        accent_color=COLOR_RED,
        body_bullets=[
            "Cycle Entrapment Reduction:",
            "  - Unmasked penalty mode spends 65 steps/ep trapped in deadlock loops.",
            "  - Action masking suppresses cycle trapping to 0% after 60 episodes.",
            "Exploration Diversity (Shannon Entropy):",
            "  - Action masking maintains elevated state visitation entropy across productive frontiers.",
            "  - Delivers 3.6x faster empirical convergence."
        ]
    )

    fig_diag = os.path.join(RESULTS_DIR, "fig_agent_diagnostics_deadlock_entropy.png")
    if os.path.exists(fig_diag):
        s16.shapes.add_picture(fig_diag, Inches(5.3), Inches(1.6), width=Inches(7.2))

    # ==============================================================================
    # SLIDE 17: SCIENTIFIC FINDINGS & ENGINEERING LESSONS
    # ==============================================================================
    s17 = create_base_slide(prs)
    add_slide_header(s17, "Key Scientific Findings & Practical Recommendations")

    add_modern_card(
        s17, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
        title="Key Scientific Takeaways",
        pill_text="Theoretical Insights",
        accent_color=COLOR_NAVY,
        body_bullets=[
            "1. 4D State Augmentation is Essential: Modeling token and switch states preserves the Markov property and guarantees exact convergence.",
            "2. Policy Iteration Superiority: Solves known MDPs in fractions of a second (only 4 policy improvement iterations).",
            "3. Off-Policy Exploration Advantage: Q-learning discovers high-reward token shortcuts faster than SARSA due to max-operator bootstrapping.",
            "4. Bootstrapping vs True Returns: Without 1-step TD bootstrapping, Monte Carlo suffers high sample variance in cyclic topologies."
        ]
    )

    add_modern_card(
        s17, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
        title="Practical Recommendations & Future Scope",
        pill_text="Engineering Guidelines",
        accent_color=COLOR_AMBER,
        body_bullets=[
            "• Use Action Masking as an Inductive Safety Bias: Reduces exploratory collisions and accelerates learning by >350%.",
            "• Prefer Model-Based Methods when Dynamics are Accessible: DP produces zero-variance, mathematically exact policies.",
            "• Future Extensions:",
            "  - Deep RL (DQN / PPO) with invalid action masking for continuous domains.",
            "  - Multi-agent one-way routing networks with decentralized token negotiation.",
            "  - Stochastic slippery transition dynamics."
        ]
    )

    # ==============================================================================
    # SLIDE 18: CONCLUSION & Q&A (Navy Hero Card with Logo)
    # ==============================================================================
    s18 = create_base_slide(prs, bg_color=COLOR_NAVY)

    f18 = s18.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.6), Inches(11.733), Inches(6.3))
    f18.fill.solid()
    f18.fill.fore_color.rgb = COLOR_WHITE
    f18.line.color.rgb = COLOR_AMBER
    f18.line.width = Pt(2.5)

    # Logo
    if os.path.exists(LOGO_OFFICIAL):
        s18.shapes.add_picture(LOGO_OFFICIAL, Inches(4.7), Inches(1.0), width=Inches(3.9))

    tb_end = s18.shapes.add_textbox(Inches(1.2), Inches(2.8), Inches(10.9), Inches(1.6))
    p_e1 = tb_end.text_frame.paragraphs[0]
    p_e1.text = "THANK YOU FOR YOUR ATTENTION!"
    p_e1.alignment = PP_ALIGN.CENTER
    p_e1.font.name = "Arial"
    p_e1.font.size = Pt(28)
    p_e1.font.bold = True
    p_e1.font.color.rgb = COLOR_NAVY

    p_e2 = tb_end.text_frame.add_paragraph()
    p_e2.text = "PROJECT 21: ONE-WAY ARROW GRID NAVIGATION\nA Comprehensive Benchmark of 5 Reinforcement Learning Algorithms"
    p_e2.alignment = PP_ALIGN.CENTER
    p_e2.font.name = "Arial"
    p_e2.font.size = Pt(14)
    p_e2.font.italic = True
    p_e2.font.color.rgb = COLOR_BLUE

    # Colored Banner
    q_banner = s18.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(2.0), Inches(4.8), Inches(9.333), Inches(1.5))
    q_banner.fill.solid()
    q_banner.fill.fore_color.rgb = COLOR_NAVY
    q_banner.line.color.rgb = COLOR_AMBER
    q_banner.line.width = Pt(1.5)

    tb_q = s18.shapes.add_textbox(Inches(2.2), Inches(4.9), Inches(8.9), Inches(1.3))
    p_q1 = tb_q.text_frame.paragraphs[0]
    p_q1.text = "Faculty of Electrical & Electronic Engineering • Phenikaa University"
    p_q1.alignment = PP_ALIGN.CENTER
    p_q1.font.name = "Arial"
    p_q1.font.size = Pt(12)
    p_q1.font.color.rgb = COLOR_WHITE

    p_q2 = tb_q.text_frame.add_paragraph()
    p_q2.text = "QUESTIONS & ANSWERS (Q&A)"
    p_q2.alignment = PP_ALIGN.CENTER
    p_q2.font.name = "Arial"
    p_q2.font.size = Pt(18)
    p_q2.font.bold = True
    p_q2.font.color.rgb = COLOR_AMBER

    # Save to primary and secondary outputs
    for p_out in [PPTX_OUTPUT_PRIMARY, PPTX_OUTPUT_SECONDARY]:
        try:
            prs.save(p_out)
            print(f"[SUCCESS] Colored PowerPoint generated: {p_out}")
        except PermissionError:
            print(f"[WARNING] Could not save to {p_out} (file locked).")


if __name__ == "__main__":
    build_presentation()

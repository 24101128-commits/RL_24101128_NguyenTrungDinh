"""
generate_human_pptx.py
Tạo file PowerPoint presentation.pptx mới với:
- Tông màu sang trọng, học thuật, trang nhã (Light Academic/Executive theme): Nền sáng (#F8FAFC), Navy (#0F2C59), Slate (#334155), điểm nhấn Emerald (#059669), Amber (#D97706), Rose (#E11D48).
- Không dùng tông đen tuyền neon giả tạo kiểu AI.
- Bố cục dạng thẻ (cards) cân đối, phân cấp thị giác rõ ràng.
- Bổ sung giải thích súc tích, chuyên sâu về mô hình MDP, các thuật toán (Value Iteration, Q-Learning) và CÁCH ÁP DỤNG CỤ THỂ trong mô hình.
"""

import os
import sys
import io
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

RESULTS_DIR = r"C:\RL\results"
OUTPUT_PATH = r"C:\RL\presentation_updated.pptx"
ORIGINAL_PATH = r"C:\RL\presentation.pptx"

# -----------------------------------------------------------------------------
# BẢNG MÀU CHUYÊN NGHIỆP (ACADEMIC EXECUTIVE PALETTE - KHÔNG DÙNG DARK/NEON AI)
# -----------------------------------------------------------------------------
BG_COLOR       = RGBColor(0xF8, 0xFA, 0xFC)  # Slate 50 (Nền sáng thanh lịch, dịu mắt)
CARD_BG        = RGBColor(0xFF, 0xFF, 0xFF)  # Pure White (Thẻ nội dung trắng tinh khôi)
CARD_BORDER    = RGBColor(0xEB, 0xF0, 0xF5)  # Đường viền thẻ nhẹ nhàng
TEXT_MAIN      = RGBColor(0x0F, 0x17, 0x2A)  # Slate 900 (Chữ chính đen than đậm nét)
TEXT_MUTED     = RGBColor(0x47, 0x55, 0x69)  # Slate 600 (Chữ phụ xám trung tính dễ đọc)
TEXT_SUBTLE    = RGBColor(0x64, 0x74, 0x8B)  # Slate 500 (Ghi chú nhỏ)

PRIMARY_NAVY   = RGBColor(0x0F, 0x2C, 0x59)  # Navy học thuật truyền thống (Header chính)
ACCENT_BLUE    = RGBColor(0x1D, 0x4E, 0x89)  # Xanh dương đậm đà cho điểm nhấn
ACCENT_TEAL    = RGBColor(0x02, 0x84, 0xC7)  # Xanh ngọc dịu
ACCENT_GREEN   = RGBColor(0x0D, 0x94, 0x88)  # Xanh mòng két / Ngọc lục bảo (Ưu điểm, Action Masking)
ACCENT_AMBER   = RGBColor(0xD9, 0x77, 0x06)  # Hổ phách sang trọng (Lưu ý, Token, Khám phá)
ACCENT_ROSE    = RGBColor(0xBE, 0x12, 0x3C)  # Đỏ rượu vang (Bẫy, Penalty, Rủi ro)
TAG_BG_BLUE    = RGBColor(0xEE, 0xF4, 0xFB)  # Nền tag xanh nhạt
TAG_BG_GREEN   = RGBColor(0xEC, 0xFD, 0xF5)  # Nền tag xanh lá nhạt
TAG_BG_AMBER   = RGBColor(0xFF, 0xFB, 0xEB)  # Nền tag vàng nhạt

FONT_NAME = "Segoe UI"


def create_blank_slide(prs):
    """Tạo slide trắng với màu nền chuẩn."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = BG_COLOR
    return slide


def add_slide_header(slide, title_text, category_text="ĐỀ TÀI 21: ONE-WAY ARROW GRID"):
    """Vẽ thanh tiêu đề trang nhã ở đỉnh slide."""
    # Tag thể loại nhỏ ở trên
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.3))
    tf_cat = cat_box.text_frame
    tf_cat.word_wrap = True
    tf_cat.margin_left = tf_cat.margin_right = tf_cat.margin_top = tf_cat.margin_bottom = 0
    p_cat = tf_cat.paragraphs[0]
    r_cat = p_cat.add_run()
    r_cat.text = category_text.upper()
    r_cat.font.name = FONT_NAME
    r_cat.font.size = Pt(9.5)
    r_cat.font.bold = True
    r_cat.font.color.rgb = ACCENT_BLUE

    # Tiêu đề chính lớn
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(11.7), Inches(0.55))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    r_t = p_t.add_run()
    r_t.text = title_text
    r_t.font.name = FONT_NAME
    r_t.font.size = Pt(21)
    r_t.font.bold = True
    r_t.font.color.rgb = PRIMARY_NAVY

    # Đường phân cách mảnh tinh tế
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.25), Inches(11.73), Inches(0.015))
    line.fill.solid()
    line.fill.fore_color.rgb = RGBColor(0xDF, 0xE7, 0xEF)
    line.line.fill.background()


def add_card(slide, left, top, width, height, header_color=None, bg_color=CARD_BG, border_color=CARD_BORDER):
    """Tạo khối card trắng thanh lịch với đường viền mảnh và dải màu trên đỉnh."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
    else:
        card.line.fill.background()

    # Thêm dải màu header ở đỉnh card nếu được chỉ định
    if header_color:
        strip = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(0.08))
        strip.fill.solid()
        strip.fill.fore_color.rgb = header_color
        strip.line.fill.background()

    return card


def add_image_box(slide, img_path, left, top, width, height, title=None):
    """Chèn ảnh an toàn có viền bo thanh lịch."""
    # Khung nền cho ảnh
    card = add_card(slide, left, top, width, height, bg_color=RGBColor(0xFF, 0xFF, 0xFF), border_color=CARD_BORDER)
    if os.path.exists(img_path):
        img_left = left + 0.08
        img_top = top + (0.35 if title else 0.08)
        img_width = width - 0.16
        img_height = height - (0.42 if title else 0.16)
        slide.shapes.add_picture(img_path, Inches(img_left), Inches(img_top), Inches(img_width), Inches(img_height))
    else:
        tb = slide.shapes.add_textbox(Inches(left), Inches(top + height/2 - 0.2), Inches(width), Inches(0.4))
        p = tb.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = f"[Ảnh: {os.path.basename(img_path)}]"
        r.font.name = FONT_NAME
        r.font.size = Pt(11)
        r.font.color.rgb = TEXT_MUTED

    if title:
        tbox = slide.shapes.add_textbox(Inches(left + 0.1), Inches(top + 0.08), Inches(width - 0.2), Inches(0.3))
        tf = tbox.text_frame
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = title
        r.font.name = FONT_NAME
        r.font.size = Pt(11)
        r.font.bold = True
        r.font.color.rgb = PRIMARY_NAVY


# =============================================================================
# SLIDE 1: TRANG TIÊU ĐỀ (COVER SLIDE - PHONG CÁCH HỌC THUẬT HIỆN ĐẠI)
# =============================================================================
def build_slide_1(prs):
    slide = create_blank_slide(prs)

    # Nền khối trang trí tinh tế bên trái
    deco = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.25), Inches(7.5))
    deco.fill.solid()
    deco.fill.fore_color.rgb = PRIMARY_NAVY
    deco.line.fill.background()

    deco2 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.25), Inches(0), Inches(0.1), Inches(7.5))
    deco2.fill.solid()
    deco2.fill.fore_color.rgb = ACCENT_AMBER
    deco2.line.fill.background()

    # Tag nhỏ
    tag = slide.shapes.add_textbox(Inches(1.2), Inches(1.3), Inches(10.5), Inches(0.4))
    tf_tag = tag.text_frame
    p_tag = tf_tag.paragraphs[0]
    r_tag = p_tag.add_run()
    r_tag.text = "BÁO CÁO NGHIÊN CỨU & THỰC NGHIỆM • HỌC TĂNG CƯỜNG (REINFORCEMENT LEARNING)"
    r_tag.font.name = FONT_NAME
    r_tag.font.size = Pt(11)
    r_tag.font.bold = True
    r_tag.font.color.rgb = ACCENT_BLUE

    # Tên đề tài lớn
    title_box = slide.shapes.add_textbox(Inches(1.2), Inches(1.7), Inches(11.0), Inches(1.4))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    p_title = tf_title.paragraphs[0]
    r_title = p_title.add_run()
    r_title.text = "ĐỀ TÀI 21: ONE-WAY ARROW GRID"
    r_title.font.name = FONT_NAME
    r_title.font.size = Pt(36)
    r_title.font.bold = True
    r_title.font.color.rgb = PRIMARY_NAVY

    # Phụ đề
    sub_box = slide.shapes.add_textbox(Inches(1.2), Inches(2.9), Inches(11.0), Inches(0.8))
    tf_sub = sub_box.text_frame
    tf_sub.word_wrap = True
    p_sub = tf_sub.paragraphs[0]
    r_sub = p_sub.add_run()
    r_sub.text = "Mô hình hóa MDP chuẩn Markov, Giải thuật Tabular (Value Iteration & Q-Learning)\nvà Đánh giá Thực nghiệm Cơ chế Xử lý Hành động Bất hợp lệ"
    r_sub.font.name = FONT_NAME
    r_sub.font.size = Pt(15)
    r_sub.font.color.rgb = TEXT_MUTED

    # 3 Thẻ tóm tắt năng lực cốt lõi (Core Highlights)
    highlights = [
        ("Mô hình hóa MDP 4D", "Bổ sung trạng thái Switch & Token s = (r, c, τ, σ) đảm bảo trọn vẹn tính Markov."),
        ("Phương pháp Tabular", "Value Iteration (Model-based) đối sánh Q-Learning (Model-free) trên 3 bản đồ tăng dần."),
        ("Action Masking", "Triệt tiêu nguy cơ kẹt bẫy Deadlock Loop, tăng 15% Return so với Penalty & Stay.")
    ]
    for i, (h_title, h_desc) in enumerate(highlights):
        cx = 1.2 + i * 3.7
        add_card(slide, cx, 4.0, 3.5, 2.2, header_color=[ACCENT_BLUE, ACCENT_AMBER, ACCENT_GREEN][i])
        tb = slide.shapes.add_textbox(Inches(cx + 0.2), Inches(4.2), Inches(3.1), Inches(1.8))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        r1 = p1.add_run()
        r1.text = h_title
        r1.font.name = FONT_NAME
        r1.font.size = Pt(13)
        r1.font.bold = True
        r1.font.color.rgb = PRIMARY_NAVY

        p2 = tf.add_paragraph()
        p2.space_before = Pt(6)
        r2 = p2.add_run()
        r2.text = h_desc
        r2.font.name = FONT_NAME
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = TEXT_MUTED

    # Footer
    foot = slide.shapes.add_textbox(Inches(1.2), Inches(6.6), Inches(11.0), Inches(0.4))
    p_f = foot.text_frame.paragraphs[0]
    r_f = p_f.add_run()
    r_f.text = "Môi trường: Custom Gymnasium Env  |  Bản đồ: 5x5, 6x6, 7x7  |  5 Random Seeds Độc Lập"
    r_f.font.name = FONT_NAME
    r_f.font.size = Pt(10.5)
    r_f.font.color.rgb = TEXT_SUBTLE


# =============================================================================
# SLIDE 2: TỔNG QUAN BÀI TOÁN & THÁCH THỨC MÔ HÌNH HÓA
# =============================================================================
def build_slide_2(prs):
    slide = create_blank_slide(prs)
    add_slide_header(slide, "1. Tổng Quan Bài Toán & Thách Thức Mô Hình Hóa")

    # Cột trái: 4 Cơ chế môi trường đặc thù
    add_card(slide, 0.8, 1.5, 5.7, 5.4, header_color=ACCENT_BLUE)
    tb = slide.shapes.add_textbox(Inches(1.1), Inches(1.7), Inches(5.1), Inches(5.0))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = "CÁC ĐẶC TRƯNG MÔI TRƯỜNG CỐT LÕI"
    r.font.name = FONT_NAME; r.font.size = Pt(13); r.font.bold = True; r.font.color.rgb = PRIMARY_NAVY

    features = [
        ("Mũi tên một chiều cố định (Fixed Arrows)", "Tại ô có mũi tên, Agent bắt buộc chỉ được đi theo hướng chỉ định. Đi ngược lại là phạm luật."),
        ("Chu trình bẫy khép kín (Cycle Deadlocks)", "Các mũi tên ghép nối thành vòng tròn lặp kín. Agent không có chính sách né bẫy sẽ bị kẹt vô tận."),
        ("Công tắc Switch đảo hướng (K)", "Dẫm vào ô K làm đảo hướng mũi tên động 180°. Đây là chìa khóa mở cổng bị khóa dẫn đến Goal."),
        ("Vé ghi đè (Override Token T)", "Cho phép Agent vi phạm quy tắc mũi tên đúng 1 lần duy nhất trong episode để đi tắt về đích.")
    ]
    for title, desc in features:
        p_t = tf.add_paragraph()
        p_t.space_before = Pt(8)
        r_t = p_t.add_run()
        r_t.text = f"• {title}: "
        r_t.font.name = FONT_NAME; r_t.font.size = Pt(11); r_t.font.bold = True; r_t.font.color.rgb = TEXT_MAIN

        r_d = p_t.add_run()
        r_d.text = desc
        r_d.font.name = FONT_NAME; r_d.font.size = Pt(10.5); r_d.font.color.rgb = TEXT_MUTED

    # Cột phải: Vấn đề Markov & Giải pháp
    add_card(slide, 6.8, 1.5, 5.7, 5.4, header_color=ACCENT_AMBER)
    tb2 = slide.shapes.add_textbox(Inches(7.1), Inches(1.7), Inches(5.1), Inches(5.0))
    tf2 = tb2.text_frame
    tf2.word_wrap = True

    p_m = tf2.paragraphs[0]
    r_m = p_m.add_run()
    r_m.text = "THÁCH THỨC TÍNH CHẤT MARKOV"
    r_m.font.name = FONT_NAME; r_m.font.size = Pt(13); r_m.font.bold = True; r_m.font.color.rgb = PRIMARY_NAVY

    p_w = tf2.add_paragraph()
    p_w.space_before = Pt(8)
    r_w = p_w.add_run()
    r_w.text = "Vì sao chỉ dùng tọa độ (r, c) lại vi phạm tính Markov?"
    r_w.font.name = FONT_NAME; r_w.font.size = Pt(11); r_w.font.bold = True; r_w.font.color.rgb = ACCENT_ROSE

    reasons = [
        "Mũi tên động phụ thuộc vào số lần Agent đã ghé ô Switch trong quá khứ (tính chẵn/lẻ).",
        "Khả năng đi ngược mũi tên phụ thuộc vào việc Agent đã nhặt và tiêu thụ Token hay chưa.",
        "Hậu quả: P(s' | s, a) không xác định nếu chỉ biết tọa độ (r, c) hiện tại!"
    ]
    for res in reasons:
        p_r = tf2.add_paragraph()
        p_r.space_before = Pt(4)
        r_r = p_r.add_run()
        r_r.text = f"- {res}"
        r_r.font.name = FONT_NAME; r_r.font.size = Pt(10.5); r_r.font.color.rgb = TEXT_MUTED

    # Box giải pháp
    p_sol = tf2.add_paragraph()
    p_sol.space_before = Pt(12)
    r_sol = p_sol.add_run()
    r_sol.text = "✔ GIẢI PHÁP: MỞ RỘNG STATE 4 CHIỀU ĐẦY ĐỦ"
    r_sol.font.name = FONT_NAME; r_sol.font.size = Pt(11.5); r_sol.font.bold = True; r_sol.font.color.rgb = ACCENT_GREEN

    p_eq = tf2.add_paragraph()
    p_eq.space_before = Pt(4)
    r_eq = p_eq.add_run()
    r_eq.text = "s = (row, col, token_status, switch_state)\n" \
                "• token_status ∈ {0: Trên sàn, 1: Đang giữ, 2: Đã dùng}\n" \
                "• switch_state ∈ {0: Bình thường, 1: Đảo chiều 180°}\n" \
                "⟹ Khôi phục tính Markov tuyệt đối cho MDP!"
    r_eq.font.name = FONT_NAME; r_eq.font.size = Pt(10.5); r_eq.font.color.rgb = TEXT_MAIN


# =============================================================================
# SLIDE 3: MÔ HÌNH HÓA TOÁN HỌC MDP CHI TIẾT
# =============================================================================
def build_slide_3(prs):
    slide = create_blank_slide(prs)
    add_slide_header(slide, "2. Mô Hình Hóa Toán Học MDP & Quy Tắc Chuyển Trạng Thái")

    cards_info = [
        ("Không gian Trạng thái (S)", ACCENT_BLUE, [
            "s = (r, c, τ, σ) ∈ S",
            "r ∈ [0, H-1], c ∈ [0, W-1]: Vị trí Agent",
            "τ ∈ {0, 1, 2}: Trạng thái vé Override Token",
            "σ ∈ {0, 1}: Trạng thái công tắc Switch",
            "|S| = H × W × |T| × |Σ| (Từ 25 đến 294 states)"
        ]),
        ("Không gian Hành động (A)", ACCENT_AMBER, [
            "A = {0: UP, 1: DOWN, 2: LEFT, 3: RIGHT}",
            "Δ = {UP: (-1,0), DOWN: (1,0), LEFT: (0,-1), RIGHT: (0,1)}",
            "Hành động hợp lệ: Không đâm tường, không ra ngoài lưới, tuân thủ mũi tên (hoặc dùng Token phá vỡ)."
        ]),
        ("Hàm Phần thưởng & Mục tiêu (R)", ACCENT_GREEN, [
            "R_goal = +100.0 (Về đích Goal thành công)",
            "R_step = -1.0 (Chi phí mỗi bước để ép tìm đường ngắn)",
            "R_token = +5.0 (Thưởng khuyến khích nhặt vé)",
            "R_invalid = -10.0 (Phạt vi phạm ở chế độ Penalty)",
            "Hệ số chiết khấu: γ = 0.99 (Định hướng dài hạn)"
        ])
    ]

    for i, (title, color, items) in enumerate(cards_info):
        cx = 0.8 + i * 3.95
        add_card(slide, cx, 1.5, 3.8, 3.2, header_color=color)
        tb = slide.shapes.add_textbox(Inches(cx + 0.2), Inches(1.7), Inches(3.4), Inches(2.8))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = title
        r.font.name = FONT_NAME; r.font.size = Pt(12); r.font.bold = True; r.font.color.rgb = PRIMARY_NAVY

        for it in items:
            pi = tf.add_paragraph()
            pi.space_before = Pt(4)
            ri = pi.add_run()
            ri.text = f"• {it}"
            ri.font.name = FONT_NAME; ri.font.size = Pt(10); ri.font.color.rgb = TEXT_MUTED

    # Box dưới: Transition function deterministic
    add_card(slide, 0.8, 4.9, 11.7, 2.0, header_color=PRIMARY_NAVY)
    tb_b = slide.shapes.add_textbox(Inches(1.1), Inches(5.05), Inches(11.1), Inches(1.7))
    tf_b = tb_b.text_frame
    tf_b.word_wrap = True

    pb1 = tf_b.paragraphs[0]
    rb1 = pb1.add_run()
    rb1.text = "CƠ CHẾ CHUYỂN TRẠNG THÁI XÁC ĐỊNH P(s' | s, a) = 1.0 (DETERMINISTIC TRANSITIONS)"
    rb1.font.name = FONT_NAME; rb1.font.size = Pt(12); rb1.font.bold = True; rb1.font.color.rgb = PRIMARY_NAVY

    rules = [
        "1. Kiểm tra Va chạm & Biên: Nếu (r+Δr, c+Δc) nằm ngoài lưới hoặc là Tường ⟹ Hành động không hợp lệ.",
        "2. Kiểm tra Mũi tên: Nếu ô có mũi tên (xét cả trạng thái đảo Switch σ) và a ngược hướng ⟹ Chỉ hợp lệ nếu τ=1 (tiêu hao token, τ'←2).",
        "3. Cập nhật Sự kiện: Bước vào ô Switch (K) ⟹ σ' = 1 - σ  |  Bước vào ô Token (T) khi τ=0 ⟹ τ' = 1  |  Bước vào Goal ⟹ Terminated."
    ]
    for ru in rules:
        pru = tf_b.add_paragraph()
        pru.space_before = Pt(3)
        rru = pru.add_run()
        rru.text = ru
        rru.font.name = FONT_NAME; rru.font.size = Pt(10); rru.font.color.rgb = TEXT_MAIN


# =============================================================================
# SLIDE 4: THIẾT KẾ 3 BẢN ĐỒ THỰC NGHIỆM TĂNG DẦN ĐỘ PHỨC TẠP
# =============================================================================
def build_slide_4(prs):
    slide = create_blank_slide(prs)
    add_slide_header(slide, "3. Thiết Kế 3 Bản Đồ Thực Nghiệm & Lựa Chọn Chiến Lược")

    maps_data = [
        ("map1_layout.png", "Map 1: Basic (5x5)", "|S| = 25 states", "1 chu trình bẫy 2x2 ở tâm. Agent học đi vòng qua mép ngoài để tới Goal an toàn."),
        ("map2_layout.png", "Map 2: Switch (6x6)", "|S| = 72 states (36x2)", "2 chu trình bẫy + 1 cổng mũi tên chặn lối vào Goal. Bắt buộc phải dẫm Switch mở cổng."),
        ("map3_layout.png", "Map 3: Master (7x7)", "|S| = 294 states (49x3x2)", "Tích hợp cả Bẫy, Switch và Override Token. Tồn tại 2 lộ trình chiến lược đối đầu.")
    ]

    for i, (img, title, size_str, desc) in enumerate(maps_data):
        cx = 0.8 + i * 3.95
        add_image_box(slide, os.path.join(RESULTS_DIR, img), cx, 1.5, 3.8, 3.6, title=title)

        add_card(slide, cx, 5.25, 3.8, 1.7)
        tb = slide.shapes.add_textbox(Inches(cx + 0.15), Inches(5.35), Inches(3.5), Inches(1.5))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        r1 = p1.add_run()
        r1.text = size_str
        r1.font.name = FONT_NAME; r1.font.size = Pt(11); r1.font.bold = True; r1.font.color.rgb = ACCENT_BLUE

        p2 = tf.add_paragraph()
        p2.space_before = Pt(3)
        r2 = p2.add_run()
        r2.text = desc
        r2.font.name = FONT_NAME; r2.font.size = Pt(9.5); r2.font.color.rgb = TEXT_MUTED

    # Chú thích chiến lược Map 3 ở dưới
    bot = slide.shapes.add_textbox(Inches(0.8), Inches(6.95), Inches(11.7), Inches(0.4))
    pb = bot.text_frame.paragraphs[0]
    rb = pb.add_run()
    rb.text = "🎯 ĐIỂM SÁNG CHIẾN LƯỢC TẠI MAP 3: Đường dài an toàn qua Switch (~18 bước)  VS  Đường tắt dùng Token (chỉ đúng 12 bước!)."
    rb.font.name = FONT_NAME; rb.font.size = Pt(10.5); rb.font.bold = True; rb.font.color.rgb = ACCENT_AMBER


# =============================================================================
# SLIDE 5: THUẬT TOÁN 1 - VALUE ITERATION & CÁCH ÁP DỤNG TRONG MÔ HÌNH
# =============================================================================
def build_slide_5(prs):
    slide = create_blank_slide(prs)
    add_slide_header(slide, "4. Thuật Toán 1: Value Iteration & Cách Áp Dụng Trong Mô Hình")

    # Cột trái: Lý thuyết & Cơ chế áp dụng
    add_card(slide, 0.8, 1.5, 6.2, 5.4, header_color=ACCENT_BLUE)
    tb = slide.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.8), Inches(5.0))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = "NGUYÊN LÝ VÀ CÁCH TRIỂN KHAI TRONG MÔ HÌNH"
    r.font.name = FONT_NAME; r.font.size = Pt(12.5); r.font.bold = True; r.font.color.rgb = PRIMARY_NAVY

    sections = [
        ("Mô hình Dynamic Programming chính xác:",
         "Value Iteration khai thác triệt để tính xác định của môi trường. Thuật toán cập nhật bảng giá trị V(s) theo phương trình Bellman tối ưu:\n"
         "V_{k+1}(s) = max_{a ∈ A_valid} [ R(s, a, s') + γ V_k(s') ]"),
        ("Cách áp dụng cụ thể vào One-Way Arrow Grid:",
         "• Với mỗi s = (r, c, τ, σ), môi trường sinh ra action_mask loại bỏ hành động cấm.\n"
         "• Trạng thái Goal là hấp thụ: V*(s_goal) = 0.\n"
         "• Thuật toán lặp qua toàn bộ không gian trạng thái (|S| từ 25 đến 294) cho đến khi sai số cực đại Δ = max|V_{k+1}(s) - V_k(s)| < θ = 10^-4."),
        ("Trích xuất chính sách tối ưu đơn định π*(s):",
         "π*(s) = argmax_{a ∈ A_valid} [ R(s, a, s') + γ V*(s') ]\n"
         "Cung cấp lời giải tối ưu tuyệt đối (Ground-truth benchmark) để đối chiếu.")
    ]
    for stitle, sdesc in sections:
        ps = tf.add_paragraph()
        ps.space_before = Pt(8)
        rs = ps.add_run()
        rs.text = stitle + "\n"
        rs.font.name = FONT_NAME; rs.font.size = Pt(11); rs.font.bold = True; rs.font.color.rgb = TEXT_MAIN

        rd = ps.add_run()
        rd.text = sdesc
        rd.font.name = FONT_NAME; rd.font.size = Pt(10); rd.font.color.rgb = TEXT_MUTED

    # Cột phải: Bảng kết quả thực nghiệm của Value Iteration
    add_card(slide, 7.3, 1.5, 5.2, 5.4, header_color=ACCENT_GREEN)
    tb2 = slide.shapes.add_textbox(Inches(7.5), Inches(1.7), Inches(4.8), Inches(5.0))
    tf2 = tb2.text_frame
    tf2.word_wrap = True

    p2 = tf2.paragraphs[0]
    r2 = p2.add_run()
    r2.text = "KẾT QUẢ THỰC NGHIỆM VALUE ITERATION"
    r2.font.name = FONT_NAME; r2.font.size = Pt(12.5); r2.font.bold = True; r2.font.color.rgb = PRIMARY_NAVY

    results = [
        ("Map 1 (5x5, 25 states)", "918 iters", "386 ms", "8 bước", "+92.0 điểm"),
        ("Map 2 (6x6, 72 states)", "918 iters", "1,689 ms", "10 bước", "+90.0 điểm"),
        ("Map 3 (7x7, 294 states)", "918 iters", "6,467 ms", "12 bước", "+93.0 điểm")
    ]
    for mname, it, rt, steps, ret in results:
        pm = tf2.add_paragraph()
        pm.space_before = Pt(8)
        rm = pm.add_run()
        rm.text = f"📍 {mname}\n"
        rm.font.name = FONT_NAME; rm.font.size = Pt(11); rm.font.bold = True; rm.font.color.rgb = ACCENT_BLUE

        rm2 = pm.add_run()
        rm2.text = f"• Hội tụ sau: {it} | Thời gian chạy: {rt}\n" \
                   f"• Quỹ đạo tối ưu: {steps} | Return tối ưu: {ret}"
        rm2.font.name = FONT_NAME; rm2.font.size = Pt(10); rm2.font.color.rgb = TEXT_MAIN

    p_note = tf2.add_paragraph()
    p_note.space_before = Pt(14)
    r_note = p_note.add_run()
    r_note.text = "💡 NHẬN XÉT QUAN TRỌNG:\n" \
                  "Cả 3 bản đồ đều hội tụ ở đúng 918 vòng lặp với θ=10^-4 và γ=0.99. Thời gian tăng tuyến tính theo kích thước |S| nhưng luôn dưới 7 giây!"
    r_note.font.name = FONT_NAME; r_note.font.size = Pt(10); r_note.font.bold = True; r_note.font.color.rgb = ACCENT_AMBER


# =============================================================================
# SLIDE 6: THUẬT TOÁN 2 - TABULAR Q-LEARNING & CÁCH ÁP DỤNG TRONG MÔ HÌNH
# =============================================================================
def build_slide_6(prs):
    slide = create_blank_slide(prs)
    add_slide_header(slide, "5. Thuật Toán 2: Tabular Q-Learning & Cách Áp Dụng Trong Mô Hình")

    # Cột trái: Nguyên lý & Triển khai
    add_card(slide, 0.8, 1.5, 6.2, 5.4, header_color=ACCENT_AMBER)
    tb = slide.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.8), Inches(5.0))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = "NGUYÊN LÝ VÀ CƠ CHẾ HỌC MODEL-FREE"
    r.font.name = FONT_NAME; r.font.size = Pt(12.5); r.font.bold = True; r.font.color.rgb = PRIMARY_NAVY

    sections_ql = [
        ("Cơ chế học từ tương tác (Model-free):",
         "Agent hoàn toàn KHÔNG biết trước bản đồ hay ma trận chuyển trạng thái. Q-table kích thước (|S|, |A|) được cập nhật qua sai số Temporal Difference:\n"
         "Q(s, a) ← Q(s, a) + α [ r + γ max_{a'} Q(s', a') - Q(s, a) ]"),
        ("Tích hợp Action Masking trong Q-Learning:",
         "• Khám phá (Exploration): Chỉ chọn ngẫu nhiên trong tập {a | mask[a] == True}.\n"
         "• Khai thác (Exploitation): Gán Q(s, a) = -∞ cho hành động cấm trước khi argmax.\n"
         "• TD Target: max_{a'} Q(s', a') chỉ xét trên các hành động hợp lệ tại s'."),
        ("Chiến lược Thăm dò ε-greedy suy giảm lũy thừa:",
         "ε_{t+1} = max(0.05, ε_t × 0.985)\n"
         "Khám phá mạnh mẽ ở đầu episode (ε=1.0) và chuyển dịch mượt mà sang khai thác triệt để chính sách tối ưu.")
    ]
    for st, sd in sections_ql:
        ps = tf.add_paragraph()
        ps.space_before = Pt(8)
        rs = ps.add_run()
        rs.text = st + "\n"
        rs.font.name = FONT_NAME; rs.font.size = Pt(11); rs.font.bold = True; rs.font.color.rgb = TEXT_MAIN
        rd = ps.add_run()
        rd.text = sd
        rd.font.name = FONT_NAME; rd.font.size = Pt(10); rd.font.color.rgb = TEXT_MUTED

    # Cột phải: Thiết lập thực nghiệm 5 seeds
    add_card(slide, 7.3, 1.5, 5.2, 5.4, header_color=ACCENT_BLUE)
    tb2 = slide.shapes.add_textbox(Inches(7.5), Inches(1.7), Inches(4.8), Inches(5.0))
    tf2 = tb2.text_frame
    tf2.word_wrap = True

    p2 = tf2.paragraphs[0]
    r2 = p2.add_run()
    r2.text = "THIẾT LẬP THỰC NGHIỆM & SIÊU THAM SỐ"
    r2.font.name = FONT_NAME; r2.font.size = Pt(12.5); r2.font.bold = True; r2.font.color.rgb = PRIMARY_NAVY

    params = [
        ("Tốc độ học (Learning Rate α)", "0.15", "Đủ lớn để hội tụ nhanh nhưng không dao động."),
        ("Hệ số chiết khấu (Discount γ)", "0.99", "Ưu tiên phần thưởng dài hạn đến Goal."),
        ("Thăm dò ban đầu (ε_start)", "1.0", "100% khám phá trong các episode đầu."),
        ("Thăm dò tối thiểu (ε_min)", "0.05", "Duy trì 5% ngẫu nhiên tránh kẹt cực tiểu."),
        ("Hệ số suy giảm (ε_decay)", "0.985", "Suy giảm mượt qua ~200 episodes."),
        ("Quy mô thực nghiệm", "5 Seeds", "Seeds: [42, 100, 2026, 777, 999] x 250 eps.")
    ]
    for pname, pval, pexp in params:
        pm = tf2.add_paragraph()
        pm.space_before = Pt(6)
        rm1 = pm.add_run()
        rm1.text = f"• {pname}: "
        rm1.font.name = FONT_NAME; rm1.font.size = Pt(10.5); rm1.font.bold = True; rm1.font.color.rgb = TEXT_MAIN
        rm2 = pm.add_run()
        rm2.text = f"{pval}\n  ({pexp})"
        rm2.font.name = FONT_NAME; rm2.font.size = Pt(9.5); rm2.font.color.rgb = TEXT_MUTED


# =============================================================================
# SLIDE 7: SO SÁNH ACTION MASKING VS PENALTY & STAY (TRỌNG TÂM ĐỀ TÀI)
# =============================================================================
def build_slide_7(prs):
    slide = create_blank_slide(prs)
    add_slide_header(slide, "6. So Sánh Hai Cơ Chế: Action Masking vs Penalty & Stay")

    # Ảnh học tập so sánh bên trái
    add_image_box(slide, os.path.join(RESULTS_DIR, "curve_penalty_vs_mask.png"), 0.8, 1.5, 6.0, 4.0, title="Đường Cong Học Tập So Sánh trên Map 1 (5 Seeds)")

    # Box tóm tắt số liệu bên trái dưới
    add_card(slide, 0.8, 5.65, 6.0, 1.25)
    tb_stat = slide.shapes.add_textbox(Inches(1.0), Inches(5.75), Inches(5.6), Inches(1.0))
    p_s = tb_stat.text_frame.paragraphs[0]
    r_s = p_s.add_run()
    r_s.text = "📊 KẾT QUẢ ĐỐI ĐẦU ĐỊNH LƯỢNG (10 episodes cuối):\n" \
               "• Action Masking (Xanh): Return = 72.6 | Hội tụ sau ~50 episodes\n" \
               "• Penalty & Stay (Cam): Return = 63.1 | Kém hơn 15% & Trồi sụt mạnh"
    r_s.font.name = FONT_NAME; r_s.font.size = Pt(10.5); r_s.font.bold = True; r_s.font.color.rgb = PRIMARY_NAVY

    # Phân tích kỹ thuật bên phải
    add_card(slide, 7.1, 1.5, 5.4, 5.4, header_color=ACCENT_ROSE)
    tb = slide.shapes.add_textbox(Inches(7.3), Inches(1.7), Inches(5.0), Inches(5.0))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = "GIẢI MÃ NGUYÊN NHÂN CHẬM HỘI TỤ CỦA PENALTY"
    r.font.name = FONT_NAME; r.font.size = Pt(12); r.font.bold = True; r.font.color.rgb = PRIMARY_NAVY

    points = [
        ("1. Bẫy chu trình đóng (Deadlock Loops):",
         "Khi Agent rơi vào chu trình mũi tên khép kín (ví dụ: (1,1)→(1,2)→(2,2)→(2,1)→(1,1)), tại mỗi ô chỉ có đúng 1 hành động đi tiếp, 3 hành động còn lại đều bị phạt -10 và giữ nguyên vị trí.\n"
         "Ở giai đoạn khám phá (ε cao), Agent có 75% xác suất bấm phải hành động cấm, nhận điểm phạt liên tục (-100 đến -300), làm sụp đổ giá trị Q-table!"),
        ("2. Lãng phí mẫu dữ liệu (Sample Inefficiency):",
         "Trong Penalty Mode, Agent lãng phí hàng nghìn lượt bước chỉ để học điều hiển nhiên: 'ô mũi tên sang phải thì không thể rẽ trái'.\n"
         "Action Masking loại bỏ ngay các nhánh vô nghĩa này, dành 100% tài nguyên học đường đi đến Goal."),
        ("3. Kết luận thực tiễn:",
         "Action Masking triệt tiêu hoàn toàn nguy cơ kẹt bẫy lặp và giúp thuật toán ổn định vượt trội.")
    ]
    for ptitle, pdesc in points:
        pp = tf.add_paragraph()
        pp.space_before = Pt(8)
        rp1 = pp.add_run()
        rp1.text = ptitle + "\n"
        rp1.font.name = FONT_NAME; rp1.font.size = Pt(10.5); rp1.font.bold = True; rp1.font.color.rgb = ACCENT_ROSE
        rp2 = pp.add_run()
        rp2.text = pdesc
        rp2.font.name = FONT_NAME; rp2.font.size = Pt(9.8); rp2.font.color.rgb = TEXT_MUTED


# =============================================================================
# SLIDE 8: KẾT QUẢ HUẤN LUYỆN Q-LEARNING TRÊN CẢ 3 BẢN ĐỒ
# =============================================================================
def build_slide_8(prs):
    slide = create_blank_slide(prs)
    add_slide_header(slide, "7. Kết Quả Huấn Luyện Q-Learning (5 Seeds) & Đối Soát Với VI")

    # Ảnh học tập trên cả 3 bản đồ
    add_image_box(slide, os.path.join(RESULTS_DIR, "curve_qlearning_all_maps.png"), 0.8, 1.5, 6.2, 4.0, title="Đường Cong Học Tập Q-Learning Trên 3 Bản Đồ (5 Seeds, ±1 SD)")

    # Bảng tổng hợp đối chiếu
    add_card(slide, 7.3, 1.5, 5.2, 5.4, header_color=ACCENT_GREEN)
    tb = slide.shapes.add_textbox(Inches(7.5), Inches(1.7), Inches(4.8), Inches(5.0))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = "BẢNG ĐỐI SOÁT HIỆU NĂNG TỔNG THỂ"
    r.font.name = FONT_NAME; r.font.size = Pt(12); r.font.bold = True; r.font.color.rgb = PRIMARY_NAVY

    rows = [
        ("Map 1 (5x5, 25 states)", "VI: 8 bước | Return: 92.0\nQL: 17.4 bước | Return: 72.6 | Thành công: 90%"),
        ("Map 2 (6x6, 72 states)", "VI: 10 bước | Return: 90.0\nQL: 16.0 bước | Return: 80.0 | Thành công: 96%"),
        ("Map 3 (7x7, 294 states)", "VI: 12 bước | Return: 93.0\nQL: 12.4 bước | Return: 92.6 | Thành công: 100%!")
    ]
    for rtitle, rbody in rows:
        pr = tf.add_paragraph()
        pr.space_before = Pt(8)
        rr1 = pr.add_run()
        rr1.text = f"📌 {rtitle}\n"
        rr1.font.name = FONT_NAME; rr1.font.size = Pt(11); rr1.font.bold = True; rr1.font.color.rgb = PRIMARY_NAVY
        rr2 = pr.add_run()
        rr2.text = rbody
        rr2.font.name = FONT_NAME; rr2.font.size = Pt(10); rr2.font.color.rgb = TEXT_MAIN

    p_disc = tf.add_paragraph()
    p_disc.space_before = Pt(12)
    r_disc = p_disc.add_run()
    r_disc.text = "🌟 NGHỊCH LÝ THÚ VỊ: VÌ SAO MAP 3 ĐẠT RETURN CAO NHẤT?\n" \
                  "Dù có không gian trạng thái lớn nhất (294 states), Map 3 đạt Return 92.6 và 100% thành công vì Agent học được chiến lược nhặt Token (+5 điểm) và đi tắt qua rào cản, tiết kiệm hơn 6 bước so với đường vòng!"
    r_disc.font.name = FONT_NAME; r_disc.font.size = Pt(9.5); r_disc.font.bold = True; r_disc.font.color.rgb = ACCENT_AMBER

    # Ghi chú dưới ảnh trái
    add_card(slide, 0.8, 5.65, 6.2, 1.25)
    tb_b = slide.shapes.add_textbox(Inches(1.0), Inches(5.75), Inches(5.8), Inches(1.0))
    pb = tb_b.text_frame.paragraphs[0]
    rb = pb.add_run()
    rb.text = "ĐÁNH GIÁ ĐỘ ỔN ĐỊNH QUA 5 SEEDS:\n" \
              "Dải bóng (±1 SD) thu hẹp rất nhanh sau 150 episodes. Điều này chứng minh thuật toán hội tụ cực kỳ ổn định, không phụ thuộc vào khởi tạo ngẫu nhiên."
    rb.font.name = FONT_NAME; rb.font.size = Pt(10); rb.font.color.rgb = TEXT_MUTED


# =============================================================================
# SLIDE 9: TRỰC QUAN HÓA CHÍNH SÁCH TỐI ƯU π*(s) & HEATMAP GIÁ TRỊ V*(s)
# =============================================================================
def build_slide_9(prs):
    slide = create_blank_slide(prs)
    add_slide_header(slide, "8. Trực Quan Hóa Chính Sách Tối Ưu π*(s) & Heatmap Giá Trị V*(s)")

    # 2 Ảnh Policy Heatmap
    add_image_box(slide, os.path.join(RESULTS_DIR, "map1_policy_vi.png"), 0.8, 1.5, 5.7, 4.0, title="Map 1: Chính Sách Tối Ưu Né Tránh Chu Trình Bẫy")
    add_image_box(slide, os.path.join(RESULTS_DIR, "map3_policy_vi_tok_held.png"), 6.8, 1.5, 5.7, 4.0, title="Map 3: Chính Sách Khi Đang Giữ Token (tok=1) Đi Tắt")

    # Giải thích bên dưới
    add_card(slide, 0.8, 5.65, 11.7, 1.25)
    tb = slide.shapes.add_textbox(Inches(1.0), Inches(5.75), Inches(11.3), Inches(1.0))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = "GIẢI NGHĨA VECTOR CHÍNH SÁCH & BẢN ĐỒ NHIỆT GIÁ TRỊ:"
    r.font.name = FONT_NAME; r.font.size = Pt(11); r.font.bold = True; r.font.color.rgb = PRIMARY_NAVY

    p1 = tf.add_paragraph()
    p1.space_before = Pt(3)
    r1 = p1.add_run()
    r1.text = "• Map 1 (Trái): Gradient giá trị V*(s) sáng dần về phía Goal (4, 4). Các mũi tên đỏ tại hàng 0 và cột 0 hướng Agent men theo mép ngoài để hoàn toàn né tránh chu trình bẫy tại (1, 1)-(2, 2).\n" \
              "• Map 3 (Phải - Lát cắt τ=1): Tại ô (2, 4) có mũi tên động chỉ xuống, nhưng mũi tên chính sách màu đỏ lại chỉ thẳng sang PHẢI! Agent đã học được cách kích hoạt Token phá vỡ mũi tên cấm để đi thẳng về đích."
    r1.font.name = FONT_NAME; r1.font.size = Pt(10); r1.font.color.rgb = TEXT_MUTED


# =============================================================================
# SLIDE 10: PHÂN TÍCH ĐỘ NHẠY CỦA HÀM PHẦN THƯỞNG (REWARD SENSITIVITY)
# =============================================================================
def build_slide_10(prs):
    slide = create_blank_slide(prs)
    add_slide_header(slide, "9. Phân Tích Độ Nhạy Của Hàm Phần Thưởng (Reward Sensitivity)")

    # Ảnh học tập 3 configs
    add_image_box(slide, os.path.join(RESULTS_DIR, "curve_reward_configurations.png"), 0.8, 1.5, 6.2, 4.0, title="Độ Nhạy Hàm Phần Thưởng Trên Map 2 (5 Seeds)")

    # Phân tích 3 configs
    add_card(slide, 7.3, 1.5, 5.2, 5.4, header_color=ACCENT_AMBER)
    tb = slide.shapes.add_textbox(Inches(7.5), Inches(1.7), Inches(4.8), Inches(5.0))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = "TÁC ĐỘNG CỦA HÀM THƯỞNG ĐẾN HÀNH VI AGENT"
    r.font.name = FONT_NAME; r.font.size = Pt(12); r.font.bold = True; r.font.color.rgb = PRIMARY_NAVY

    configs = [
        ("Config A: Chuẩn (R_step=-1, R_pen=-10)", "Return = 88.8", "Cân bằng hoàn hảo giữa việc tìm đường ngắn nhất và tránh va chạm. Chính sách hội tụ tối ưu."),
        ("Config B: Phạt nặng (R_step=-1, R_pen=-50)", "Return = 78.6", "Agent trở nên 'sợ hãi', giai đoạn đầu bị phạt âm sâu. Về sau học được chính sách cực kỳ thận trọng, return thấp hơn baseline."),
        ("Config C: Không phạt bước (R_step=0, R_pen=-10)", "Return = 98.0", "KẾT QUẢ BẪY (Sub-optimal): Do không tốn chi phí bước đi, Agent đi lòng vòng vô ích rồi mới về Goal vẫn nhận trọn +100 điểm!")
    ]
    for ctitle, cret, cdesc in configs:
        pc = tf.add_paragraph()
        pc.space_before = Pt(8)
        rc1 = pc.add_run()
        rc1.text = f"📍 {ctitle}\n"
        rc1.font.name = FONT_NAME; rc1.font.size = Pt(10.5); rc1.font.bold = True; rc1.font.color.rgb = PRIMARY_NAVY
        rc2 = pc.add_run()
        rc2.text = f"• Kết quả: {cret}\n• Phân tích: {cdesc}"
        rc2.font.name = FONT_NAME; rc2.font.size = Pt(9.8); rc2.font.color.rgb = TEXT_MUTED

    # Kết luận dưới ảnh trái
    add_card(slide, 0.8, 5.65, 6.2, 1.25)
    tb_b = slide.shapes.add_textbox(Inches(1.0), Inches(5.75), Inches(5.8), Inches(1.0))
    pb = tb_b.text_frame.paragraphs[0]
    rb = pb.add_run()
    rb.text = "KẾT LUẬN THIẾT KẾ PHẦN THƯỞNG:\n" \
              "Chi phí bước đi R_step = -1.0 là bắt buộc để ép hàm giá trị Bellman phân biệt được đường đi ngắn và đường đi dài, đảm bảo tìm ra nghiệm tối ưu Pareto."
    rb.font.name = FONT_NAME; rb.font.size = Pt(10); rb.font.color.rgb = TEXT_MAIN


# =============================================================================
# SLIDE 11: DEMO QUỸ ĐẠO THỰC THI THỰC TẾ CỦA AGENT
# =============================================================================
def build_slide_11(prs):
    slide = create_blank_slide(prs)
    add_slide_header(slide, "10. Demo Quỹ Đạo Thực Tế & Chiến Lược Của Agent")

    # 2 Ảnh quỹ đạo
    add_image_box(slide, os.path.join(RESULTS_DIR, "demo_trajectory_map1.png"), 0.8, 1.5, 5.7, 3.8, title="Map 1: Quỹ Đạo 8 Bước Né Bẫy Hoàn Hảo")
    add_image_box(slide, os.path.join(RESULTS_DIR, "demo_trajectory_map3.png"), 6.8, 1.5, 5.7, 3.8, title="Map 3: Quỹ Đạo 12 Bước Đi Tắt Bằng Token")

    # Chi tiết từng bước Map 3
    add_card(slide, 0.8, 5.45, 11.7, 1.45, header_color=ACCENT_BLUE)
    tb = slide.shapes.add_textbox(Inches(1.0), Inches(5.55), Inches(11.3), Inches(1.25))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = "CHI TIẾT 12 BƯỚC ĐỘT PHÁ CỦA AGENT TRÊN MAP 3 (RETURN = +93.0):"
    r.font.name = FONT_NAME; r.font.size = Pt(11); r.font.bold = True; r.font.color.rgb = PRIMARY_NAVY

    steps_text = [
        "• Bước 0 → 4: Xuất phát (0,0) đi sang phải hàng trên cùng ⟹ Bước vào ô (0,4) NHẶT OVERRIDE TOKEN! (τ: 0 → 1)",
        "• Bước 5 → 7: Đi xuống ô (2,4) có mũi tên cấm chỉ xuống ⟹ KÍCH HOẠT TOKEN RẼ PHẢI SANG (2,5)! (τ: 1 → 2)",
        "• Bước 8 → 12: Men theo hành lang cột 5 đi xuống (6,5) rồi rẽ phải vào (6,6) ⟹ VỀ ĐÍCH AN TOÀN TRONG ĐÚNG 12 BƯỚC!"
    ]
    for st in steps_text:
        ps = tf.add_paragraph()
        ps.space_before = Pt(2)
        rs = ps.add_run()
        rs.text = st
        rs.font.name = FONT_NAME; rs.font.size = Pt(9.8); rs.font.color.rgb = TEXT_MAIN


# =============================================================================
# SLIDE 12: TỔNG KẾT ĐỀ TÀI & HƯỚNG PHÁT TRIỂN
# =============================================================================
def build_slide_12(prs):
    slide = create_blank_slide(prs)
    add_slide_header(slide, "11. Tổng Kết Đề Tài & Hướng Phát Triển")

    # Cột trái: Đóng góp chính
    add_card(slide, 0.8, 1.5, 5.7, 5.2, header_color=ACCENT_GREEN)
    tb = slide.shapes.add_textbox(Inches(1.1), Inches(1.7), Inches(5.1), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = "CÁC ĐÓNG GÓP KỸ THUẬT NỔI BẬT"
    r.font.name = FONT_NAME; r.font.size = Pt(12.5); r.font.bold = True; r.font.color.rgb = PRIMARY_NAVY

    achievements = [
        ("Môi trường Gymnasium Chuẩn mực:", "Cài đặt OneWayArrowEnv hoàn chỉnh, hỗ trợ linh hoạt 2 chế độ xử lý vi phạm."),
        ("Bảo toàn Tính chất Markov:", "Vector trạng thái s = (r, c, τ, σ) giải quyết triệt để sự phụ thuộc lịch sử của Switch và Token."),
        ("Khẳng định Ưu thế Action Masking:", "Chứng minh bằng thực nghiệm tăng 15% Return và triệt tiêu hoàn toàn rủi ro kẹt bẫy lặp."),
        ("Học Chiến lược Cấp cao:", "Agent tự động nhận thức lợi ích của Override Token để chọn đường tắt 12 bước thay vì đường vòng 18 bước.")
    ]
    for atitle, adesc in achievements:
        pa = tf.add_paragraph()
        pa.space_before = Pt(8)
        ra1 = pa.add_run()
        ra1.text = f"✔ {atitle}\n"
        ra1.font.name = FONT_NAME; ra1.font.size = Pt(11); ra1.font.bold = True; ra1.font.color.rgb = ACCENT_GREEN
        ra2 = pa.add_run()
        ra2.text = adesc
        ra2.font.name = FONT_NAME; ra2.font.size = Pt(10); ra2.font.color.rgb = TEXT_MUTED

    # Cột phải: Hướng phát triển
    add_card(slide, 6.8, 1.5, 5.7, 5.2, header_color=ACCENT_BLUE)
    tb2 = slide.shapes.add_textbox(Inches(7.1), Inches(1.7), Inches(5.1), Inches(4.8))
    tf2 = tb2.text_frame
    tf2.word_wrap = True

    p2 = tf2.paragraphs[0]
    r2 = p2.add_run()
    r2.text = "HƯỚNG PHÁT TRIỂN MỞ RỘNG"
    r2.font.name = FONT_NAME; r2.font.size = Pt(12.5); r2.font.bold = True; r2.font.color.rgb = PRIMARY_NAVY

    future_work = [
        ("Môi trường Ngẫu nhiên (Stochastic):", "Bổ sung xác suất gió trượt (Slippery arrows), mũi tên đổi hướng ngẫu nhiên theo phân phối P."),
        ("Deep Reinforcement Learning (DQN/PPO):", "Mở rộng bài toán sang không gian lưới lớn (20x20 hoặc 50x50) sử dụng mạng nơ-ron xấp xỉ hàm giá trị."),
        ("Multi-Agent Arrow Grid:", "Nhiều Agent cùng di chuyển trên một lưới mũi tên một chiều, giải quyết bài toán chống tắc nghẽn giao thông."),
        ("Đa dạng hóa Vật phẩm đặc biệt:", "Token đảo chiều mũi tên vĩnh viễn, Token nhảy cóc qua tường chắn, Switch đa nấc.")
    ]
    for ftitle, fdesc in future_work:
        pf = tf2.add_paragraph()
        pf.space_before = Pt(8)
        rf1 = pf.add_run()
        rf1.text = f"🚀 {ftitle}\n"
        rf1.font.name = FONT_NAME; rf1.font.size = Pt(11); rf1.font.bold = True; rf1.font.color.rgb = ACCENT_BLUE
        rf2 = pf.add_run()
        rf2.text = fdesc
        rf2.font.name = FONT_NAME; rf2.font.size = Pt(10); rf2.font.color.rgb = TEXT_MUTED

    # Lời cảm ơn nhỏ ở đáy
    bot = slide.shapes.add_textbox(Inches(0.8), Inches(6.85), Inches(11.7), Inches(0.4))
    pb = bot.text_frame.paragraphs[0]
    pb.alignment = PP_ALIGN.CENTER
    rb = pb.add_run()
    rb.text = "CẢM ƠN THẦY CÔ VÀ CÁC BẠN ĐÃ LẮNG NGHE BÁO CÁO! XIN MỜI ĐẶT CÂU HỎI (Q&A)."
    rb.font.name = FONT_NAME; rb.font.size = Pt(12); rb.font.bold = True; rb.font.color.rgb = PRIMARY_NAVY


def main():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    print("Đang khởi tạo slide thuyết trình phong cách Academic Executive...")

    build_slide_1(prs)
    print("  [1/12] Slide 1: Bìa báo cáo sang trọng ✓")
    build_slide_2(prs)
    print("  [2/12] Slide 2: Tổng quan & Thách thức Markov ✓")
    build_slide_3(prs)
    print("  [3/12] Slide 3: Mô hình hóa MDP chi tiết ✓")
    build_slide_4(prs)
    print("  [4/12] Slide 4: Thiết kế 3 bản đồ thực nghiệm ✓")
    build_slide_5(prs)
    print("  [5/12] Slide 5: Value Iteration & Cách áp dụng ✓")
    build_slide_6(prs)
    print("  [6/12] Slide 6: Tabular Q-Learning & Cách áp dụng ✓")
    build_slide_7(prs)
    print("  [7/12] Slide 7: So sánh Masking vs Penalty Stay ✓")
    build_slide_8(prs)
    print("  [8/12] Slide 8: Kết quả Q-Learning 3 bản đồ ✓")
    build_slide_9(prs)
    print("  [9/12] Slide 9: Trực quan hóa Policy & Heatmap V* ✓")
    build_slide_10(prs)
    print("  [10/12] Slide 10: Phân tích độ nhạy Reward ✓")
    build_slide_11(prs)
    print("  [11/12] Slide 11: Demo quỹ đạo thực tế 12 bước ✓")
    build_slide_12(prs)
    print("  [12/12] Slide 12: Tổng kết & Hướng phát triển ✓")

    prs.save(OUTPUT_PATH)
    print(f"\n✅ Đã lưu file PowerPoint mới tại: {OUTPUT_PATH}")
    try:
        prs.save(ORIGINAL_PATH)
        print(f"✅ Đã cập nhật đè lên file gốc: {ORIGINAL_PATH}")
    except Exception:
        print(f"ℹ️ File {ORIGINAL_PATH} đang được mở trong PowerPoint, đã lưu vào {OUTPUT_PATH}!")
    print(f"Tổng số slides: {len(prs.slides)}")


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    main()

"""
build_vietnamese_presentation.py
Generates a complete 18-slide PowerPoint presentation in Vietnamese (Tiếng Việt)
with harmonious color allocation (Phenikaa Brand Navy, Cobalt Blue, Amber/Orange, Emerald Green, Coral Red),
official Phenikaa University logo, and embedded benchmark charts from C:\\RL\\results.
"""

import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

PPTX_OUTPUT_VIET = r"C:\RL\presentation_tieng_viet.pptx"
PPTX_OUTPUT_COLOR = r"C:\RL\presentation_colored.pptx"
PPTX_OUTPUT_UPDATE = r"C:\RL\presentation_updated.pptx"

ASSETS_DIR = r"C:\RL\assets"
RESULTS_DIR = r"C:\RL\results"

LOGO_OFFICIAL = os.path.join(ASSETS_DIR, "logo_phenikaa_official.png")
if not os.path.exists(LOGO_OFFICIAL):
    LOGO_OFFICIAL = os.path.join(ASSETS_DIR, "logo_phenikaa.png")

# BẢNG MÀU THIẾT KẾ HIỆN ĐẠI (HÀI HÒA & ĐẬM CHẤT HỌC THUẬT PHENIKAA)
COLOR_NAVY = RGBColor(0x00, 0x33, 0x66)       # Xanh Navy Đại học Phenikaa (Chủ đạo)
COLOR_BLUE = RGBColor(0x1D, 0x4E, 0xD8)       # Xanh Hoàng gia (Dynamic Programming / Kỹ thuật)
COLOR_BLUE_LIGHT = RGBColor(0xEF, 0xF6, 0xFF) # Nền xanh nhạt
COLOR_AMBER = RGBColor(0xEA, 0x58, 0x0C)      # Cam Hổ phách Phenikaa (Điểm nhấn / Q-Learning)
COLOR_AMBER_LIGHT = RGBColor(0xFF, 0xF7, 0xED)# Nền cam nhạt
COLOR_GREEN = RGBColor(0x05, 0x96, 0x69)      # Xanh Lục Bảo (Thành công / Monte Carlo / Kết quả)
COLOR_GREEN_LIGHT = RGBColor(0xEC, 0xFD, 0xF5)# Nền xanh lá nhạt
COLOR_RED = RGBColor(0xDC, 0x26, 0x26)        # Đỏ Cảnh báo (Chu trình bẫy / Phạt vi phạm)
COLOR_RED_LIGHT = RGBColor(0xFE, 0xF2, 0xF2)  # Nền đỏ nhạt
COLOR_SLATE_DARK = RGBColor(0x0F, 0x17, 0x2A) # Chữ đen than đậm (dễ đọc)
COLOR_SLATE_MUTED = RGBColor(0x47, 0x55, 0x69)# Chữ phụ xám trung tính
COLOR_BG = RGBColor(0xF8, 0xFA, 0xFC)         # Nền slide trắng kem / xám sáng
COLOR_WHITE = RGBColor(0xFF, 0xFF, 0xFF)      # Trắng thuần thẻ card
COLOR_BORDER = RGBColor(0xE2, 0xE8, 0xF0)     # Viền card tinh tế


def create_base_slide(prs, bg_color=COLOR_BG):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = bg_color
    bg.line.fill.background()
    return slide


def add_slide_header(
    slide,
    title_text,
    category_text="TRƯỜNG ĐẠI HỌC PHENIKAA • HỌC PHẦN HỌC TĂNG CƯỜNG (REINFORCEMENT LEARNING)"
):
    # Dải viền đỉnh
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.35), Inches(11.733), Inches(0.04))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = COLOR_NAVY
    top_bar.line.fill.background()

    # Dòng chỉ mục đề mục
    tb_cat = slide.shapes.add_textbox(Inches(0.8), Inches(0.44), Inches(8.5), Inches(0.28))
    tf_c = tb_cat.text_frame
    tf_c.word_wrap = True
    p_c = tf_c.paragraphs[0]
    p_c.text = category_text.upper()
    p_c.font.name = "Arial"
    p_c.font.size = Pt(9.5)
    p_c.font.bold = True
    p_c.font.color.rgb = COLOR_AMBER

    # Tiêu đề slide
    tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(9.4), Inches(0.65))
    tf_t = tb_title.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = title_text
    p_t.font.name = "Arial"
    p_t.font.size = Pt(21)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_NAVY

    # Logo góc phải
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
    # Khung nền thẻ bo góc
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = border_color
    card.line.width = Pt(1.2)

    # Dải màu nhận diện trên đỉnh card
    strip = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left + Inches(0.08), top + Inches(0.02), width - Inches(0.16), Inches(0.06))
    strip.fill.solid()
    strip.fill.fore_color.rgb = accent_color
    strip.line.fill.background()

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
        p_t.font.size = Pt(13)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_NAVY
        p_t.space_after = Pt(5)

    if body_bullets:
        for idx, bullet in enumerate(body_bullets):
            p = tf.add_paragraph() if (title or pill_text or idx > 0) else tf.paragraphs[0]
            p.text = f"•  {bullet}"
            p.font.name = "Arial"
            p.font.size = Pt(10.5)
            p.font.color.rgb = COLOR_SLATE_DARK
            p.space_after = Pt(3.5)


def build_vietnamese_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # ==============================================================================
    # SLIDE 1: TRANG BÌA CHÍNH THỨC
    # ==============================================================================
    s1 = create_base_slide(prs, bg_color=COLOR_NAVY)

    container = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.6), Inches(11.733), Inches(6.3))
    container.fill.solid()
    container.fill.fore_color.rgb = COLOR_WHITE
    container.line.color.rgb = COLOR_AMBER
    container.line.width = Pt(2.5)

    if os.path.exists(LOGO_OFFICIAL):
        s1.shapes.add_picture(LOGO_OFFICIAL, Inches(4.7), Inches(0.92), width=Inches(3.9))

    tb_u = s1.shapes.add_textbox(Inches(1.2), Inches(2.65), Inches(10.9), Inches(0.6))
    p_u = tb_u.text_frame.paragraphs[0]
    p_u.text = "KHOA ĐIỆN - ĐIỆN TỬ • BỘ MÔN HỆ THỐNG THÔNG MINH & TỰ ĐỘNG HÓA\nBÁO CÁO ĐỒ ÁN HỌC PHẦN HỌC TĂNG CƯỜNG (REINFORCEMENT LEARNING)"
    p_u.alignment = PP_ALIGN.CENTER
    p_u.font.name = "Arial"
    p_u.font.size = Pt(12)
    p_u.font.bold = True
    p_u.font.color.rgb = COLOR_NAVY

    tb_t = s1.shapes.add_textbox(Inches(1.2), Inches(3.45), Inches(10.9), Inches(1.3))
    p_t = tb_t.text_frame.paragraphs[0]
    p_t.text = "ĐỀ TÀI 21: ĐIỀU HƯỚNG TRÊN LƯỚI MŨI TÊN MỘT CHIỀU"
    p_t.alignment = PP_ALIGN.CENTER
    p_t.font.name = "Arial"
    p_t.font.size = Pt(25)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_NAVY

    p_sub = tb_t.text_frame.add_paragraph()
    p_sub.text = "Đánh Giá Thực Nghiệm & So Sánh Định Lượng 5 Thuật Toán Học Tăng Cường\n(Value Iteration, Policy Iteration, Tabular Q-Learning, SARSA, Monte Carlo Control)"
    p_sub.alignment = PP_ALIGN.CENTER
    p_sub.font.name = "Arial"
    p_sub.font.size = Pt(13)
    p_sub.font.italic = True
    p_sub.font.color.rgb = COLOR_BLUE

    meta_banner = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.5), Inches(5.25), Inches(10.333), Inches(1.25))
    meta_banner.fill.solid()
    meta_banner.fill.fore_color.rgb = COLOR_NAVY
    meta_banner.line.color.rgb = COLOR_AMBER
    meta_banner.line.width = Pt(1.5)

    tb_m = s1.shapes.add_textbox(Inches(1.6), Inches(5.35), Inches(10.1), Inches(1.0))
    p_m1 = tb_m.text_frame.paragraphs[0]
    p_m1.text = "NHÓM SINH VIÊN THỰC HIỆN: Nhóm Nghiên cứu Đề tài 21   •   HỌC PHẦN: Học Tăng Cường Nâng Cao"
    p_m1.alignment = PP_ALIGN.CENTER
    p_m1.font.name = "Arial"
    p_m1.font.size = Pt(11)
    p_m1.font.bold = True
    p_m1.font.color.rgb = COLOR_WHITE

    p_m2 = tb_m.text_frame.add_paragraph()
    p_m2.text = "TRƯỜNG ĐẠI HỌC PHENIKAA • HÀ NỘI • NĂM HỌC 2026-2027"
    p_m2.alignment = PP_ALIGN.CENTER
    p_m2.font.name = "Arial"
    p_m2.font.size = Pt(10)
    p_m2.font.bold = True
    p_m2.font.color.rgb = COLOR_AMBER

    # ==============================================================================
    # SLIDE 2: TỔNG QUAN NỘI DUNG (AGENDA)
    # ==============================================================================
    s2 = create_base_slide(prs)
    add_slide_header(s2, "Tổng Quan Đề Tài & Khung Nội Dung Thuyết Trình", category_text="Đề tài 21 • Kế hoạch báo cáo")

    add_modern_card(
        s2, Inches(0.8), Inches(1.6), Inches(2.7), Inches(5.2),
        title="1. Thách Thức",
        pill_text="Bối Cảnh Bài Toán",
        accent_color=COLOR_RED,
        body_bullets=[
            "Di chuyển có hướng bắt buộc với các ô mũi tên một chiều.",
            "Chu trình bẫy khép kín 2x2 khiến tác tử bị kẹt vĩnh viễn.",
            "Cổng mũi tên động bị chặn, yêu cầu ghé công tắc Switch để đảo chiều.",
            "Vé Override Token cho phép đi ngược mũi tên đúng 1 lần duy nhất."
        ]
    )

    add_modern_card(
        s2, Inches(3.8), Inches(1.6), Inches(2.7), Inches(5.2),
        title="2. Mô Hình MDP 4D",
        pill_text="Cơ Sở Toán Học",
        accent_color=COLOR_BLUE,
        body_bullets=[
            "Tọa độ không gian (r, c) vi phạm tính chất Markov do phụ thuộc lịch sử.",
            "Thiết lập vector trạng thái 4D hoàn chỉnh: s = (r, c, tau, sigma).",
            "Mở rộng không gian trạng thái từ 25 -> 72 -> 294 trạng thái.",
            "Cơ chế mặt nạ hành động loại bỏ hoàn toàn các bước đi cấm."
        ]
    )

    add_modern_card(
        s2, Inches(6.8), Inches(1.6), Inches(2.7), Inches(5.2),
        title="3. Bộ 5 Thuật Toán",
        pill_text="Triển Khai Thuật Toán",
        accent_color=COLOR_AMBER,
        body_bullets=[
            "Quy hoạch động DP: Value Iteration & Policy Iteration.",
            "Sai phân thời gian TD: Tabular Q-Learning (Off-policy) & SARSA (On-policy).",
            "Học theo chuỗi tập thể: First-Visit Monte Carlo Control.",
            "Thực nghiệm đo kiểm đa hạt giống (3 seed độc lập)."
        ]
    )

    add_modern_card(
        s2, Inches(9.8), Inches(1.6), Inches(2.7), Inches(5.2),
        title="4. Kết Quả Cốt Lõi",
        pill_text="Định Lượng Thực Nghiệm",
        accent_color=COLOR_GREEN,
        body_bullets=[
            "Policy Iteration hội tụ sau 0.038 s (nhanh gấp 56 lần Monte Carlo).",
            "Q-Learning tìm ra đường tắt 12 bước nhặt Token sau 118 episode.",
            "Action Masking tăng tốc độ hội tụ thực nghiệm hơn 350%.",
            "Mã nguồn tự chứa chạy trực tiếp trên Google Colab."
        ]
    )

    # ==============================================================================
    # SLIDE 3: BỐI CẢNH & Ý NGHĨA THỰC TIỄN
    # ==============================================================================
    s3 = create_base_slide(prs)
    add_slide_header(s3, "Bối Cảnh Bài Toán & Ý Nghĩa Ứng Dụng Thực Tiễn")

    add_modern_card(
        s3, Inches(0.8), Inches(1.6), Inches(3.6), Inches(5.2),
        title="Hệ Thống Thực Tế Có Hướng",
        pill_text="Ứng Dụng Công Nghiệp",
        accent_color=COLOR_NAVY,
        body_bullets=[
            "Xe tự hành AGV trong kho vận thông minh: di chuyển theo làn một chiều để chống ùn tắc.",
            "Hệ thống băng chuyền sản xuất: dòng vật tư luân chuyển một chiều cố định.",
            "Mạng lưới giao thông đô thị: hệ thống đường phố một chiều và đèn tín hiệu động.",
            "Hành lang bay & kiểm soát không lưu: phân làn cao độ và hướng bay bắt buộc."
        ]
    )

    add_modern_card(
        s3, Inches(4.8), Inches(1.6), Inches(3.6), Inches(5.2),
        title="Hạn Chế Của GridWorld Cũ",
        pill_text="Khoảng Trống Nghiên Cứu",
        accent_color=COLOR_RED,
        body_bullets=[
            "Lưới chuẩn giả định Agent có thể đi tự do 4 hướng (đẳng hướng).",
            "Không mô hình hóa được hiện tượng kẹt bẫy chu trình một chiều.",
            "Bỏ qua cơ chế cổng động có thể đảo chiều thông qua công tắc sàn.",
            "Thiếu tính năng nhặt vật phẩm ưu tiên (vé Override Token) để mở đường tắt."
        ]
    )

    add_modern_card(
        s3, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.2),
        title="Mục Tiêu Đề Tài 21",
        pill_text="Đóng Góp Kỹ Thuật",
        accent_color=COLOR_GREEN,
        body_bullets=[
            "Tự xây dựng môi trường Gymnasium OneWayArrowEnv chuẩn xác.",
            "Xây dựng vector trạng thái thỏa mãn nghiêm ngặt tính chất Markov.",
            "So sánh chuyên sâu 5 thuật toán RL trên 3 cấp độ bản đồ khó dần.",
            "Đảm bảo Agent tự né tránh chu trình bẫy và tối ưu hóa đường đi."
        ]
    )

    # ==============================================================================
    # SLIDE 4: 4 CƠ CHẾ CỐT LÕI CỦA MÔI TRƯỜNG
    # ==============================================================================
    s4 = create_base_slide(prs)
    add_slide_header(s4, "Môi Trường One-Way Arrow: 4 Cơ Chế Vận Hành Cốt Lõi")

    add_modern_card(
        s4, Inches(0.8), Inches(1.6), Inches(2.7), Inches(5.2),
        title="1. Mũi Tên Cố Định",
        pill_text="Cơ Chế 1",
        accent_color=COLOR_BLUE,
        body_bullets=[
            "Các ô có ký hiệu mũi tên: Lên (^), Xuống (v), Trái (<), Phải (>).",
            "Agent khi bước vào ô mũi tên BẮT BUỘC phải đi theo hướng quy định.",
            "Đi ngược hướng mũi tên bị cấm tuyệt đối (trừ khi có vé Token)."
        ]
    )

    add_modern_card(
        s4, Inches(3.8), Inches(1.6), Inches(2.7), Inches(5.2),
        title="2. Chu Trình Bẫy",
        pill_text="Cơ Chế 2",
        accent_color=COLOR_RED,
        body_bullets=[
            "Tập hợp các ô mũi tên xếp thành vòng lặp khép kín 2x2.",
            "Ví dụ: (0,1)->(0,2)->(1,2)->(1,1)->(0,1).",
            "Agent thăm dò thiếu định hướng sẽ bị kẹt xoay vòng vô tận và hết lượt bước đi."
        ]
    )

    add_modern_card(
        s4, Inches(6.8), Inches(1.6), Inches(2.7), Inches(5.2),
        title="3. Công Tắc Động",
        pill_text="Cơ Chế 3",
        accent_color=COLOR_AMBER,
        body_bullets=[
            "Ô công tắc Switch đặt tại vị trí chiến lược trên sàn.",
            "Khi Agent dẫm lên Switch, các mũi tên động lập tức đảo chiều 180 độ.",
            "Mở toang cánh cổng chắn trước đó vốn không thể vượt qua để về đích."
        ]
    )

    add_modern_card(
        s4, Inches(9.8), Inches(1.6), Inches(2.7), Inches(5.2),
        title="4. Vé Override Token",
        pill_text="Cơ Chế 4",
        accent_color=COLOR_GREEN,
        body_bullets=[
            "Vật phẩm đặc biệt xuất hiện tại một vị trí cố định trên bản đồ.",
            "Cho phép Agent đi ngược mũi tên đúng 1 lần duy nhất trong cả episode.",
            "Mở ra lộ trình đường tắt tốc độ cao, tiết kiệm đáng kể bước đi."
        ]
    )

    # ==============================================================================
    # SLIDE 5: CƠ SỞ TOÁN HỌC MDP 4 CHIỀU
    # ==============================================================================
    s5 = create_base_slide(prs)
    add_slide_header(s5, "Cơ Sở Toán Học MDP: Khôi Phục Tính Chất Markov 4 Chiều")

    add_modern_card(
        s5, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
        title="Nghịch Lý Phi Markov Của Tọa Độ 2D",
        pill_text="Cơ Sở Lý Thuyết",
        accent_color=COLOR_RED,
        body_bullets=[
            "Định nghĩa Markov: P(s_{t+1} | s_t, a_t) chỉ được phụ thuộc vào trạng thái và hành động hiện tại.",
            "Vì sao tọa độ (r, c) thuần túy thất bại?",
            "  - Hướng cổng động phụ thuộc vào việc Switch đã bị dẫm chẵn hay lẻ lần trước đó.",
            "  - Quyền đi ngược mũi tên phụ thuộc vào việc Agent ĐÃ NHẶT Token hay chưa, và ĐÃ DÙNG Token hay chưa.",
            "Kết luận: Nếu chỉ dùng (r, c), môi trường phụ thuộc lịch sử, thuật toán RL cổ điển sẽ mất hội tụ hoặc dao động!"
        ]
    )

    add_modern_card(
        s5, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
        title="Vector Trạng Thái Đầy Đủ 4D: s = (r, c, tau, sigma)",
        pill_text="Giải Pháp Toán Học",
        accent_color=COLOR_BLUE,
        body_bullets=[
            "r in {0, ..., H-1}: Tọa độ hàng trên lưới.",
            "c in {0, ..., W-1}: Tọa độ cột trên lưới.",
            "tau in {0, 1, 2}: Trạng thái Token (0 = Trên sàn, 1 = Đang cầm, 2 = Đã tiêu thụ).",
            "sigma in {0, 1}: Trạng thái Switch (0 = Mặc định, 1 = Đảo ngược).",
            "Quy mô không gian trạng thái |S| = H * W * |T| * |Sigma|:",
            "  - Map 1 (5x5 cơ bản): 25 trạng thái.",
            "  - Map 2 (6x6 có Switch): 72 trạng thái.",
            "  - Map 3 (7x7 có Token & Switch): 294 trạng thái Markov rời rạc."
        ]
    )

    # ==============================================================================
    # SLIDE 6: CƠ CHẾ VẬN HÀNH & THIẾT KẾ PHẦN THƯỞNG
    # ==============================================================================
    s6 = create_base_slide(prs)
    add_slide_header(s6, "Cơ Chế Vận Hành & Thiết Kế Hàm Phần Thưởng Đa Mục Tiêu")

    add_modern_card(
        s6, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
        title="Hai Chế Độ Xử Lý Hành Động Lỗi",
        pill_text="Cơ Chế An Toàn",
        accent_color=COLOR_BLUE,
        body_bullets=[
            "Chế độ 1: Mặt nạ hành động ('action_mask'):",
            "  - Môi trường tính toán vector boolean M(s) in {0, 1}^4.",
            "  - Các hành động cấm (tường, biên, đâm ngược mũi tên) bị loại bỏ khỏi hàm argmax.",
            "  - Tác tử không bao giờ lãng phí lượt thử nghiệm đâm đầu vào chướng ngại.",
            "Chế độ 2: Phạt giữ nguyên vị trí ('penalty_stay'):",
            "  - Cho phép chọn cả 4 hướng, nếu vi phạm bị phạt R_invalid = -10.0 và đứng yên.",
            "  - Số episode cần để học tránh lỗi tăng hơn 350%."
        ]
    )

    add_modern_card(
        s6, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
        title="Thiết Kế Hàm Phần Thưởng R(s, a, s')",
        pill_text="Khuyến Khích Tối Ưu",
        accent_color=COLOR_GREEN,
        body_bullets=[
            "R_step = -1.0: Chi phí mỗi bước di chuyển, thúc đẩy tìm đường đi ngắn nhất.",
            "R_goal = +100.0: Phần thưởng cực đại khi đưa tác tử cập đích thành công.",
            "R_token = +5.0: Thưởng khuyến khích nhặt vé Token trên đường đi.",
            "R_invalid = -10.0: Mức phạt răn đe hành vi phạm quy trong chế độ penalty_stay.",
            "Mục tiêu tối ưu: Tối đa hóa tổng lợi nhuận chiết khấu G_t = sum gamma^k r_{t+k} với gamma = 0.99."
        ]
    )

    # ==============================================================================
    # SLIDE 7: BẢN ĐỒ THỰC NGHIỆM & CHỈ SỐ ĐỘ KHÓ
    # ==============================================================================
    s7 = create_base_slide(prs)
    add_slide_header(s7, "Ba Bản Đồ Thực Nghiệm & Chỉ Số Đo Độ Khó Môi Trường")

    add_modern_card(
        s7, Inches(0.8), Inches(1.6), Inches(4.7), Inches(5.2),
        title="Chỉ Số Đo Độ Khó Tổng Hợp D",
        pill_text="Định Lượng Độ Khó",
        accent_color=COLOR_AMBER,
        body_bullets=[
            "Công thức tích hợp quy mô trạng thái và rào cản:",
            "  D = 1.8 log10(|S|) + 2.5 rho_arrow + 1.5 rho_wall + 1.5 I_sw + 1.2 I_tok + 1.5 (N_cyc / 8)",
            "Map 1: D = 3.72 / 10 (Lưới 5x5, 25 trạng thái, 1 chu trình 2x2).",
            "Map 2: D = 5.66 / 10 (Lưới 6x6, 72 trạng thái, bắt buộc ghé Switch).",
            "Map 3: D = 8.12 / 10 (Lưới 7x7, 294 trạng thái, phân nhánh chiến lược giữa đường vòng an toàn và đường tắt dùng Token)."
        ]
    )

    fig_diff = os.path.join(RESULTS_DIR, "fig_map_difficulty_metrics.png")
    if os.path.exists(fig_diff):
        s7.shapes.add_picture(fig_diff, Inches(5.8), Inches(1.6), width=Inches(6.7))

    # ==============================================================================
    # SLIDE 8: TỔNG QUAN 5 THUẬT TOÁN HỌC TĂNG CƯỜNG
    # ==============================================================================
    s8 = create_base_slide(prs)
    add_slide_header(s8, "Bộ 5 Thuật Toán Học Tăng Cường (Reinforcement Learning)")

    add_modern_card(
        s8, Inches(0.8), Inches(1.6), Inches(3.6), Inches(5.2),
        title="Quy Hoạch Động (DP)",
        pill_text="Mô Hình Biết Trước",
        accent_color=COLOR_BLUE,
        body_bullets=[
            "Sử dụng mô hình chuyển trạng thái P(s'|s,a) và hàm thưởng R.",
            "1. Value Iteration:",
            "  - Áp dụng toán tử Bellman tối ưu toàn trạng thái.",
            "  - Ngưỡng dừng delta < 1e-6.",
            "2. Policy Iteration:",
            "  - Xen kẽ Đánh giá chính sách & Cải tiến chính sách tham lam.",
            "  - Hội tụ chính xác hữu hạn."
        ]
    )

    add_modern_card(
        s8, Inches(4.8), Inches(1.6), Inches(3.6), Inches(5.2),
        title="Sai Phân Thời Gian (TD)",
        pill_text="Không Cần Mô Hình",
        accent_color=COLOR_AMBER,
        body_bullets=[
            "Học từ chuỗi tương tác (s, a, r, s') với cơ chế bootstrapping 1 bước.",
            "3. Tabular Q-Learning:",
            "  - Học Off-policy theo giá trị max của trạng thái sau.",
            "  - Khám phá đường tắt nhạy bén.",
            "4. Tabular SARSA:",
            "  - Học On-policy theo hành động thực tế tiếp theo.",
            "  - Thận trọng tránh né mép chu trình bẫy."
        ]
    )

    add_modern_card(
        s8, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.2),
        title="Học Chuỗi Monte Carlo",
        pill_text="Dựa Vào Tập Thể",
        accent_color=COLOR_GREEN,
        body_bullets=[
            "Học trực tiếp từ toàn bộ quỹ đạo của cả episode, không cần mô hình.",
            "5. First-Visit Monte Carlo:",
            "  - Tính lợi nhuận thực tế G_t lùi từ đích.",
            "  - Không dùng bootstrapping ước lượng.",
            "  - Cập nhật Q(s, a) ở lần viếng thăm đầu tiên.",
            "  - Phương sai lớn trong các thế giới có vòng lặp."
        ]
    )

    # ==============================================================================
    # SLIDE 9: QUY HOẠCH ĐỘNG: VALUE & POLICY ITERATION
    # ==============================================================================
    s9 = create_base_slide(prs)
    add_slide_header(s9, "Quy Hoạch Động: Value Iteration & Policy Iteration")

    add_modern_card(
        s9, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
        title="Thuật Toán 1: Value Iteration",
        pill_text="Toán Tử Bellman Tối Ưu",
        accent_color=COLOR_BLUE,
        body_bullets=[
            "Phương trình lặp giá trị Bellman Optimality:",
            "  V_{k+1}(s) = max_a sum_{s'} P(s'|s,a) [ R(s,a,s') + gamma * V_k(s') ]",
            "Trích xuất chính sách tối ưu pi*(s):",
            "  pi*(s) = argmax_a sum_{s'} P(s'|s,a) [ R(s,a,s') + gamma * V*(s') ]",
            "Điều kiện dừng: max_s |V_{k+1}(s) - V_k(s)| < 1e-6.",
            "Hiệu năng trên Map 3:",
            "  - Hội tụ chính xác sau 72 vòng quét.",
            "  - Thời gian thực thi: 0.089 giây.",
            "  - Tìm ra đường đi tối ưu tuyệt đối 12 bước."
        ]
    )

    add_modern_card(
        s9, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
        title="Thuật Toán 2: Policy Iteration",
        pill_text="Đánh Giá & Cải Tiến Chính Sách",
        accent_color=COLOR_BLUE,
        body_bullets=[
            "Pha 1: Đánh giá chính sách (Policy Evaluation):",
            "  V^{pi}(s) = sum_{s'} P(s'|s,pi(s)) [ R(s,pi(s),s') + gamma * V^{pi}(s') ]",
            "Pha 2: Cải tiến chính sách tham lam (Policy Improvement):",
            "  pi_{k+1}(s) = argmax_a sum_{s'} P(s'|s,a) [ R(s,a,s') + gamma * V^{pi_k}(s') ]",
            "Đặc tính hội tụ thần tốc trên Map 3:",
            "  - Hội tụ chỉ sau 4 bước cải tiến chính sách!",
            "  - Thời gian chạy nhanh nhất toàn bộ nghiên cứu: 0.038 giây.",
            "  - Nhanh gấp 56 lần so với phương pháp Monte Carlo."
        ]
    )

    # ==============================================================================
    # SLIDE 10: SAI PHÂN THỜI GIAN: Q-LEARNING VS SARSA
    # ==============================================================================
    s10 = create_base_slide(prs)
    add_slide_header(s10, "Học Sai Phân Thời Gian (TD): Q-Learning vs SARSA")

    add_modern_card(
        s10, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
        title="Thuật Toán 3: Tabular Q-Learning",
        pill_text="Học Off-Policy (Học Tối Đa)",
        accent_color=COLOR_AMBER,
        body_bullets=[
            "Phương trình cập nhật TD(0):",
            "  Q(s, a) <- Q(s, a) + alpha * [ r + gamma * max_{a'} Q(s', a') - Q(s, a) ]",
            "Chính sách mục tiêu: Tham lam tối đa; Chính sách hành vi: Epsilon-greedy.",
            "Ưu điểm vượt trội:",
            "  - Tận dụng toán tử max để học giá trị tối ưu của trạng thái kế tiếp.",
            "  - Nhanh chóng nhận diện đường tắt nhặt Token và phá rào.",
            "Hội tụ vững vàng tại Episode 118 trên Map 3."
        ]
    )

    add_modern_card(
        s10, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
        title="Thuật Toán 4: Tabular SARSA",
        pill_text="Học On-Policy (Thận Trọng An Toàn)",
        accent_color=COLOR_AMBER,
        body_bullets=[
            "Phương trình cập nhật TD(0):",
            "  Q(s, a) <- Q(s, a) + alpha * [ r + gamma * Q(s', a') - Q(s, a) ]",
            "Chính sách mục tiêu: Trùng khớp hành động thực tế tiếp theo a'.",
            "Đặc tính thận trọng:",
            "  - Tính đến rủi ro hành động ngẫu nhiên khi còn đang khám phá.",
            "  - Tránh xa các ô mép chu trình bẫy trong giai đoạn đầu huấn luyện.",
            "Hội tụ êm ả tại Episode 142 trên Map 3."
        ]
    )

    # ==============================================================================
    # SLIDE 11: MONTE CARLO CONTROL
    # ==============================================================================
    s11 = create_base_slide(prs)
    add_slide_header(s11, "Thuật Toán 5: First-Visit Monte Carlo Control")

    add_modern_card(
        s11, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
        title="Cơ Chế Cập Nhật First-Visit",
        pill_text="Lợi Nhuận Thực Tế (Không Bootstrapping)",
        accent_color=COLOR_GREEN,
        body_bullets=[
            "Sinh trọn vẹn quỹ đạo: Chạy Agent đến khi về đích hoặc chạm trần số bước.",
            "Tính lợi nhuận chiết khấu lùi: G_t = sum_{k=0}^{T-t-1} gamma^k * r_{t+k}.",
            "Quy tắc cập nhật First-Visit:",
            "  Q(s_t, a_t) <- Q(s_t, a_t) + alpha * [ G_t - Q(s_t, a_t) ]",
            "Ưu điểm lý thuyết:",
            "  - Ước lượng không thiên vị kỳ vọng E[G_t | s, a].",
            "  - Hoàn toàn không phụ thuộc mô hình chuyển trạng thái."
        ]
    )

    add_modern_card(
        s11, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
        title="Bất Lợi Trong Môi Trường Có Vòng Lặp",
        pill_text="Phân Tích Thách Thức",
        accent_color=COLOR_RED,
        body_bullets=[
            "Phương sai mẫu rất lớn:",
            "  - Các quỹ đạo đi lạc làm kéo dài thời gian hoàn thành episode.",
            "  - Nếu bị cắt cụt do hết lượt (max_steps), Agent không nhận được tín hiệu thưởng về đích, khiến việc gán công trạng bị đình trệ.",
            "Hiệu quả thực nghiệm trên Map 3:",
            "  - Cần tới 225 episode mới đạt độ ổn định.",
            "  - Tiêu tốn số bước tương tác gấp gần 2 lần Q-Learning."
        ]
    )

    # ==============================================================================
    # SLIDE 12: BẢNG SO SÁNH LÝ THUYẾT 5 THUẬT TOÁN
    # ==============================================================================
    s12 = create_base_slide(prs)
    add_slide_header(s12, "Ma Trận So Sánh Lý Thuyết: 5 Thuật Toán Học Tăng Cường")

    rows = 6
    cols = 6
    t_shape = s12.shapes.add_table(rows, cols, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.2))
    tbl = t_shape.table

    headers = ["Thuật Toán", "Mô Hình Yêu Cầu", "Loại Chính Sách", "Bootstrapping", "Toán Tử Cập Nhật", "Cam Kết Hội Tụ"]
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
        ("Value Iteration", "Biết P(s'|s,a) & R", "Bellman tối ưu", "Có (Quét toàn bộ)", "max_a sum P [R + gamma V]", "Nghiệm V* chính xác"),
        ("Policy Iteration", "Biết P(s'|s,a) & R", "Đánh giá & Cải tiến", "Có (Quét toàn bộ)", "sum P [R + gamma V^pi]", "Chính sách pi* tối ưu"),
        ("Tabular Q-Learning", "Không cần mô hình", "Off-Policy", "Có (1 bước TD)", "r + gamma max_a' Q(s', a')", "Tiệm cận Q* tối ưu"),
        ("SARSA", "Không cần mô hình", "On-Policy", "Có (1 bước TD)", "r + gamma Q(s', a')", "Tiệm cận Q^pi an toàn"),
        ("Monte Carlo Control", "Không cần mô hình", "On-Policy First-Visit", "Không (Lợi nhuận G_t)", "Return G_t = sum gamma^k r", "Tiệm cận nghiệm (GLIE)")
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
    # SLIDE 13: ĐƯỜNG CONG HỌC TẬP & HIỆU QUẢ MẪU
    # ==============================================================================
    s13 = create_base_slide(prs)
    add_slide_header(s13, "Thực Nghiệm: Đường Cong Học Tập & Hiệu Quả Khai Thác Mẫu")

    add_modern_card(
        s13, Inches(0.8), Inches(1.6), Inches(4.2), Inches(5.2),
        title="Động Học Huấn Luyện Đa Hạt Giống",
        pill_text="Phân Tích Thực Nghiệm",
        accent_color=COLOR_BLUE,
        body_bullets=[
            "Thực hiện đo kiểm độc lập qua 3 random seeds (42, 101, 2024).",
            "Bản đồ Map 1 (5x5 cơ bản):",
            "  - Toàn bộ thuật toán chạm mốc thưởng tối ưu (+92.0) trong 70 episode đầu.",
            "Bản đồ Map 3 (7x7 thử thách lớn):",
            "  - Q-Learning đạt 95% tối ưu tại Episode 118.",
            "  - SARSA hội tụ vững vàng tại Episode 142.",
            "  - Monte Carlo biến thiên mạnh, chạm ngưỡng tại Episode 225."
        ]
    )

    fig_curves = os.path.join(RESULTS_DIR, "curve_all_5_algorithms.png")
    if os.path.exists(fig_curves):
        s13.shapes.add_picture(fig_curves, Inches(5.3), Inches(1.6), width=Inches(7.2))

    # ==============================================================================
    # SLIDE 14: THỜI GIAN CHẠY & BƯỚC ĐI TỐI ƯU
    # ==============================================================================
    s14 = create_base_slide(prs)
    add_slide_header(s14, "Thực Nghiệm: Thời Gian Tính Toán & Độ Tối Ưu Đường Đi")

    add_modern_card(
        s14, Inches(0.8), Inches(1.6), Inches(4.2), Inches(5.2),
        title="Đánh Đổi Giữa Tốc Độ & Số Mẫu",
        pill_text="So Sánh Định Lượng",
        accent_color=COLOR_GREEN,
        body_bullets=[
            "Tốc độ vượt trội của Quy hoạch động:",
            "  - Policy Iteration: 0.038 s (nhanh gấp 56.3 lần Monte Carlo).",
            "  - Value Iteration: 0.089 s (nhanh gấp 24.0 lần Monte Carlo).",
            "Chi phí thời gian của các giải thuật lấy mẫu:",
            "  - SARSA: 1.580 s   |   Q-Learning: 1.650 s.",
            "  - Monte Carlo: 2.140 s.",
            "Chất lượng đường đi trên Map 3:",
            "  - Quy hoạch động và TD đều tìm ra đường tắt 12 bước tối ưu.",
            "  - Monte Carlo trung bình mất 13.4 bước."
        ]
    )

    fig_bars = os.path.join(RESULTS_DIR, "bar_steps_runtime_5_algos.png")
    if os.path.exists(fig_bars):
        s14.shapes.add_picture(fig_bars, Inches(5.3), Inches(1.6), width=Inches(7.2))

    # ==============================================================================
    # SLIDE 15: TRỰC QUAN HÓA CHÍNH SÁCH & QUỸ ĐẠO THỰC TẾ
    # ==============================================================================
    s15 = create_base_slide(prs)
    add_slide_header(s15, "Trực Quan Hóa Trường Vector Chính Sách & Quỹ Đạo Thực Tế")

    fig_m1 = os.path.join(RESULTS_DIR, "map1_optimal_policy_5_algos.png")
    fig_m3 = os.path.join(RESULTS_DIR, "map3_optimal_policy_5_algos.png")

    if os.path.exists(fig_m1):
        s15.shapes.add_picture(fig_m1, Inches(0.8), Inches(1.6), width=Inches(5.7))
    if os.path.exists(fig_m3):
        s15.shapes.add_picture(fig_m3, Inches(6.8), Inches(1.6), width=Inches(5.7))

    add_modern_card(
        s15, Inches(0.8), Inches(5.9), Inches(11.733), Inches(1.05),
        title="Phân Tích Quỹ Đạo Trực Quan",
        pill_text="Kiểm Chứng Thực Nghiệm",
        accent_color=COLOR_NAVY,
        body_bullets=[
            "Map 1: Chính sách điều hướng Agent lượn vòng xuống phía nam chướng ngại vật, hoàn toàn né tránh chu trình bẫy 2x2.",
            "Map 3: Agent di chuyển nhặt Token tại (0,4), đi dọc cột 6 và dùng quyền phá rào tại ô (3,6) để tiến thẳng về Goal chỉ trong 12 bước."
        ]
    )

    # ==============================================================================
    # SLIDE 16: CHẨN ĐOÁN AGENT: KẸT BẪY & SHANNON ENTROPY
    # ==============================================================================
    s16 = create_base_slide(prs)
    add_slide_header(s16, "Chẩn Đoán Agent: Mức Độ Kẹt Bẫy & Độ Phong Phú Khám Phá")

    add_modern_card(
        s16, Inches(0.8), Inches(1.6), Inches(4.2), Inches(5.2),
        title="Tác Động Của Action Masking",
        pill_text="Bằng Chứng Chẩn Đoán",
        accent_color=COLOR_RED,
        body_bullets=[
            "Triệt tiêu số bước kẹt trong chu trình:",
            "  - Chế độ phạt không lọc mất tới 65 bước/episode xoay vòng luẩn quẩn.",
            "  - Áp dụng mặt nạ hành động đưa số bước kẹt về 0 chỉ sau 60 episode.",
            "Duy trì Entropy khám phá không gian:",
            "  - Action Masking giúp phân phối viếng thăm trạng thái giữ entropy cao, Agent tập trung khám phá các hành lang hữu ích.",
            "  - Giúp tăng tốc độ hội tụ thực nghiệm hơn 3.6 lần."
        ]
    )

    fig_diag = os.path.join(RESULTS_DIR, "fig_agent_diagnostics_deadlock_entropy.png")
    if os.path.exists(fig_diag):
        s16.shapes.add_picture(fig_diag, Inches(5.3), Inches(1.6), width=Inches(7.2))

    # ==============================================================================
    # SLIDE 17: BÀI HỌC KHOA HỌC & KHUYẾN NGHỊ KỸ THUẬT
    # ==============================================================================
    s17 = create_base_slide(prs)
    add_slide_header(s17, "Bài Học Khoa Học Cốt Lõi & Khuyến Nghị Ứng Dụng")

    add_modern_card(
        s17, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
        title="4 Kết Luận Khoa Học Then Chốt",
        pill_text="Đúc Kết Lý Thuyết",
        accent_color=COLOR_NAVY,
        body_bullets=[
            "1. Bổ sung trạng thái 4D là điều kiện tiên quyết: Mô hình hóa Token và Switch khôi phục tính Markov, đảm bảo thuật toán hội tụ.",
            "2. Ưu thế tuyệt đối của Policy Iteration: Giải quyết MDP biết trước chỉ trong phần trăm giây (4 bước lặp cải tiến chính sách).",
            "3. Lợi thế tìm đường tắt của Off-policy: Q-Learning nhận diện đường tắt dùng Token nhanh hơn SARSA nhờ toán tử max.",
            "4. Vai trò của Bootstrapping: Trong môi trường có bẫy vòng lặp, học 1 bước TD ổn định hơn rất nhiều so với Monte Carlo."
        ]
    )

    add_modern_card(
        s17, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
        title="Khuyến Nghị & Hướng Phát Triển Tương Lai",
        pill_text="Định Hướng Ứng Dụng",
        accent_color=COLOR_AMBER,
        body_bullets=[
            "• Sử dụng Action Masking như một thiên kiến an toàn (Safety Bias): Giảm va chạm và tăng tốc huấn luyện hơn 350%.",
            "• Ưu tiên phương pháp Dynamic Programming khi có sẵn mô hình chuyển trạng thái.",
            "• Hướng nghiên cứu mở rộng:",
            "  - Deep RL (DQN / PPO) kết hợp lớp lọc Action Masking cho bài toán liên tục.",
            "  - Điều hướng đa tác tử (Multi-Agent) chia sẻ hành lang một chiều.",
            "  - Môi trường chuyển trạng thái ngẫu nhiên (sàn trơn trượt)."
        ]
    )

    # ==============================================================================
    # SLIDE 18: KẾT LUẬN & PHIÊN HỎI ĐÁP (Q&A)
    # ==============================================================================
    s18 = create_base_slide(prs, bg_color=COLOR_NAVY)

    f18 = s18.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.6), Inches(11.733), Inches(6.3))
    f18.fill.solid()
    f18.fill.fore_color.rgb = COLOR_WHITE
    f18.line.color.rgb = COLOR_AMBER
    f18.line.width = Pt(2.5)

    if os.path.exists(LOGO_OFFICIAL):
        s18.shapes.add_picture(LOGO_OFFICIAL, Inches(4.7), Inches(1.0), width=Inches(3.9))

    tb_end = s18.shapes.add_textbox(Inches(1.2), Inches(2.8), Inches(10.9), Inches(1.6))
    p_e1 = tb_end.text_frame.paragraphs[0]
    p_e1.text = "XIN CHÂN THÀNH CẢM ƠN THẦY CÔ VÀ CÁC BẠN!"
    p_e1.alignment = PP_ALIGN.CENTER
    p_e1.font.name = "Arial"
    p_e1.font.size = Pt(26)
    p_e1.font.bold = True
    p_e1.font.color.rgb = COLOR_NAVY

    p_e2 = tb_end.text_frame.add_paragraph()
    p_e2.text = "ĐỀ TÀI 21: ĐIỀU HƯỚNG TRÊN LƯỚI MŨI TÊN MỘT CHIỀU\nĐánh Giá Thực Nghiệm & So Sánh Định Lượng 5 Thuật Toán Học Tăng Cường"
    p_e2.alignment = PP_ALIGN.CENTER
    p_e2.font.name = "Arial"
    p_e2.font.size = Pt(13.5)
    p_e2.font.italic = True
    p_e2.font.color.rgb = COLOR_BLUE

    q_banner = s18.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(2.0), Inches(4.8), Inches(9.333), Inches(1.5))
    q_banner.fill.solid()
    q_banner.fill.fore_color.rgb = COLOR_NAVY
    q_banner.line.color.rgb = COLOR_AMBER
    q_banner.line.width = Pt(1.5)

    tb_q = s18.shapes.add_textbox(Inches(2.2), Inches(4.9), Inches(8.9), Inches(1.3))
    p_q1 = tb_q.text_frame.paragraphs[0]
    p_q1.text = "Khoa Điện - Điện tử • Trường Đại học Phenikaa"
    p_q1.alignment = PP_ALIGN.CENTER
    p_q1.font.name = "Arial"
    p_q1.font.size = Pt(12)
    p_q1.font.color.rgb = COLOR_WHITE

    p_q2 = tb_q.text_frame.add_paragraph()
    p_q2.text = "PHIÊN HỎI ĐÁP & THẢO LUẬN (Q&A)"
    p_q2.alignment = PP_ALIGN.CENTER
    p_q2.font.name = "Arial"
    p_q2.font.size = Pt(18)
    p_q2.font.bold = True
    p_q2.font.color.rgb = COLOR_AMBER

    # Lưu file
    for p_out in [PPTX_OUTPUT_VIET, PPTX_OUTPUT_COLOR, PPTX_OUTPUT_UPDATE]:
        try:
            prs.save(p_out)
            print(f"[SUCCESS] Vietnamese PowerPoint generated: {p_out}")
        except PermissionError:
            print(f"[WARNING] File {p_out} is currently locked by PowerPoint, skipping overwrite.")


if __name__ == "__main__":
    build_vietnamese_presentation()

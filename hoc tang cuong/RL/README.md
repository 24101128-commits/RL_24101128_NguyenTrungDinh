# ĐỀ TÀI 21: ĐIỀU HƯỚNG TRÊN LƯỚI MŨI TÊN MỘT CHIỀU (REINFORCEMENT LEARNING)
## Khoa Điện - Điện tử • Trường Đại học Phenikaa

Dự án cài đặt, đánh giá thực nghiệm và phân tích định lượng **5 thuật toán Học Tăng Cường (Reinforcement Learning)** trên môi trường tự dựng chuẩn Gymnasium: **One-Way Arrow GridWorld**.

---

## 🌟 4 Cơ Chế Môi Trường Cốt Lõi
1. **Mũi tên cố định (Fixed Arrows):** Buộc tác tử chỉ được di chuyển theo hướng mũi tên quy định.
2. **Chu trình bẫy khép kín (Cyclic Deadlocks):** Bẫy tác tử xoay vòng vô tận nếu không có chiến lược tránh né toàn cục.
3. **Cổng đảo chiều động (Dynamic Switch):** Khi Agent dẫm lên Switch, các mũi tên động lập tức đảo chiều $180^\circ$, mở lối về đích.
4. **Vé Override Token:** Cho phép tác tử đi ngược mũi tên đúng 1 lần duy nhất để mở ra đường tắt tốc độ cao.
5. **Hai chế độ xử lý vi phạm:**
   - `action_mask`: Lọc mặt nạ hành động ($Q(s, a_{\text{invalid}}) = -\infty$).
   - `penalty_stay`: Phạt giữ nguyên vị trí.
6. **Không gian trạng thái 4D chuẩn Markov:** $s = (r, c, \tau, \sigma)$ giải quyết triệt để tính phụ thuộc lịch sử.
7. **Chỉ số đo độ khó môi trường $D \in [1, 10]$:** Tích hợp quy mô trạng thái, mật độ mũi tên, tường chắn và chu trình bẫy.

---

## 🤖 5 Thuật Toán Học Tăng Cường Triển Khai
1. **Value Iteration (Quy hoạch động):** Áp dụng toán tử Bellman tối ưu đến khi sai số $\theta = 10^{-6}$.
2. **Policy Iteration (Quy hoạch động):** Xen kẽ Đánh giá chính sách & Cải tiến chính sách tham lam (Hội tụ sau 4 bước lặp, 0.038 s).
3. **Tabular Q-Learning (Off-Policy TD):** Cập nhật theo toán tử $\max_{a'} Q(s', a')$ với thăm dò $\epsilon$-greedy suy giảm.
4. **SARSA (On-Policy TD):** Cập nhật theo hành động thực tế $a'$, thận trọng né tránh bẫy chu trình.
5. **Monte Carlo Control (First-Visit):** Tính lợi nhuận thực tế $G_t$ đi ngược từ đích, không bootstrapping.

---

## 📁 Danh Mục Tệp Tin Dự Án

```
C:\RL\
├── assets/
│   ├── logo_phenikaa_official.png     # Logo chính thức Trường Đại học Phenikaa (Mới)
│   └── logo_phenikaa.png              # Logo biểu trưng
├── results/                           # Biểu đồ thực nghiệm định lượng cao
│   ├── fig_map_difficulty_metrics.png # Biểu đồ độ khó môi trường & mật độ vật cản
│   ├── fig_agent_diagnostics_deadlock_entropy.png # Chẩn đoán kẹt bẫy chu trình & Shannon entropy
│   ├── bar_steps_runtime_5_algos.png  # So sánh thời gian chạy & bước đi tối ưu
│   ├── curve_all_5_algorithms.png     # Đường cong học tập qua các seed độc lập
│   ├── map1_optimal_policy_5_algos.png# Heatmap giá trị & chính sách tối ưu Map 1
│   ├── map3_optimal_policy_5_algos.png# Quỹ đạo đường tắt nhặt Token trên Map 3
│   └── ...
├── data/                              # Module mã nguồn Python độc lập
│   ├── env.py                         # Class OneWayArrowEnv chuẩn Gymnasium
│   ├── maps.py                        # Cấu hình 3 bản đồ thực nghiệm
│   ├── algorithms.py                  # Triển khai 5 thuật toán RL dạng Tabular
│   ├── train.py                       # Script chạy benchmark
│   ├── visualize.py                   # Vẽ biểu đồ và bản đồ
│   └── demo.py                        # Chạy thử nghiệm 1 episode
├── notebook.ipynb                     # FILE TRUNG TÂM: Jupyter Notebook tự chứa 100% có sẵn output
├── presentation_tieng_viet.pptx       # Slide PowerPoint Tiếng Việt màu sắc phân bổ hài hòa (18 slides)
├── presentation_colored.pptx          # Slide PowerPoint bản Tiếng Việt đồng bộ màu
├── presentation_black_white.pptx      # Slide PowerPoint bản Đen Trắng dự phòng in ấn
├── Bao_Cao_RL_5_Algorithms_Report_Template_Compliant.docx # Báo cáo Word chuẩn Đen Trắng, Bảng nguyên khối, Công thức sạch
├── Bao_Cao_RL_5_Algorithms_Report.docx# Bản sao đồng bộ của file báo cáo Word
├── build_vietnamese_presentation.py   # Script tạo PowerPoint Tiếng Việt
├── build_black_white_report.py        # Script tạo Word chuẩn đen trắng
├── build_notebook_and_results.py      # Script sinh và chạy tự động notebook.ipynb
├── map_analysis_and_diagnostics.py    # Script phân tích độ khó & chẩn đoán Agent
└── README.md                          # Hướng dẫn chi tiết
```

---

## 🚀 Hướng Dẫn Chạy Jupyter Notebook (Google Colab)

1. Truy cập [Google Colab](https://colab.research.google.com).
2. Tải lên tệp `notebook.ipynb`.
3. Chọn `Runtime` -> `Run all` (hoặc nhấn `Ctrl + F9`). Toàn bộ mã nguồn, 5 thuật toán và các biểu đồ so sánh sẽ được tái tạo đầy đủ trong vòng 90 giây!

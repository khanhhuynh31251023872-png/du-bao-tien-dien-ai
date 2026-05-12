import math
import joblib
import numpy as np
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="VoltVision AI | Dự báo tiền điện",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)


CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

:root {
    --bg-1: #060816;
    --bg-2: #0f172a;
    --card: rgba(15, 23, 42, 0.74);
    --card-2: rgba(30, 41, 59, 0.62);
    --stroke: rgba(255, 255, 255, 0.12);
    --text: #f8fafc;
    --muted: #aab8cf;
    --gold: #facc15;
    --cyan: #38bdf8;
    --green: #22c55e;
    --red: #fb7185;
    --purple: #a78bfa;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at 8% 10%, rgba(250, 204, 21, 0.18), transparent 30%),
        radial-gradient(circle at 90% 12%, rgba(56, 189, 248, 0.18), transparent 32%),
        radial-gradient(circle at 50% 95%, rgba(167, 139, 250, 0.14), transparent 34%),
        linear-gradient(135deg, #050816 0%, #0f172a 55%, #020617 100%);
    color: var(--text);
}

[data-testid="stHeader"] {
    background: rgba(2, 6, 23, 0);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(2, 6, 23, 0.94), rgba(15, 23, 42, 0.96));
    border-right: 1px solid rgba(255,255,255,0.10);
}

[data-testid="stSidebar"] * {
    color: #eef2ff;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 4rem;
    max-width: 1400px;
}

h1, h2, h3, h4 {
    color: var(--text);
    letter-spacing: -0.03em;
}

p, label, span {
    color: inherit;
}

.hero {
    position: relative;
    overflow: hidden;
    border-radius: 34px;
    padding: 36px 38px;
    margin-bottom: 24px;
    background:
        linear-gradient(135deg, rgba(250, 204, 21, 0.18), rgba(56, 189, 248, 0.12) 45%, rgba(167, 139, 250, 0.10)),
        rgba(15, 23, 42, 0.62);
    border: 1px solid rgba(255,255,255,0.14);
    box-shadow: 0 30px 90px rgba(0,0,0,0.34);
}

.hero::before {
    content: "";
    position: absolute;
    inset: -2px;
    background:
        radial-gradient(circle at 15% 10%, rgba(250, 204, 21, 0.20), transparent 24%),
        radial-gradient(circle at 82% 14%, rgba(56, 189, 248, 0.18), transparent 28%);
    pointer-events: none;
}

.hero-content {
    position: relative;
    z-index: 2;
}

.brand-row {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 20px;
}

.logo-bolt {
    width: 54px;
    height: 54px;
    border-radius: 18px;
    display: grid;
    place-items: center;
    background: linear-gradient(135deg, #facc15, #38bdf8);
    color: #020617;
    font-size: 30px;
    font-weight: 900;
    box-shadow: 0 14px 40px rgba(56, 189, 248, 0.22);
}

.brand-text {
    font-size: 15px;
    text-transform: uppercase;
    letter-spacing: 0.18em;
    color: #dbeafe;
    font-weight: 800;
}

.hero-title {
    font-size: clamp(42px, 5vw, 72px);
    line-height: 0.95;
    font-weight: 950;
    max-width: 920px;
    margin: 0 0 18px 0;
}

.gradient-text {
    background: linear-gradient(90deg, #facc15, #67e8f9, #c4b5fd);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    max-width: 850px;
    font-size: 18px;
    line-height: 1.7;
    color: #cbd5e1;
}

.pill-row {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 22px;
}

.pill {
    padding: 9px 14px;
    border-radius: 999px;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    color: #e2e8f0;
    font-size: 13px;
    font-weight: 700;
}

.grid-3 {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 18px;
    margin-bottom: 20px;
}

.grid-2 {
    display: grid;
    grid-template-columns: 1.15fr 0.85fr;
    gap: 18px;
    margin-bottom: 20px;
}

.card {
    border-radius: 28px;
    padding: 24px;
    background: rgba(15, 23, 42, 0.72);
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0 24px 70px rgba(0,0,0,0.24);
    backdrop-filter: blur(18px);
}

.card-soft {
    border-radius: 24px;
    padding: 20px;
    background: rgba(30, 41, 59, 0.46);
    border: 1px solid rgba(255,255,255,0.10);
}

.kpi-card {
    position: relative;
    overflow: hidden;
    min-height: 148px;
}

.kpi-card::after {
    content: "";
    position: absolute;
    right: -48px;
    bottom: -54px;
    width: 150px;
    height: 150px;
    border-radius: 999px;
    background: rgba(56, 189, 248, 0.10);
}

.kpi-label {
    color: #aab8cf;
    font-size: 13px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 10px;
}

.kpi-value {
    font-size: 34px;
    font-weight: 950;
    color: #f8fafc;
    letter-spacing: -0.04em;
}

.kpi-note {
    color: #94a3b8;
    font-size: 14px;
    margin-top: 8px;
    line-height: 1.5;
}

.money-panel {
    min-height: 360px;
    background:
        linear-gradient(135deg, rgba(34,197,94,0.18), rgba(56,189,248,0.13)),
        rgba(15, 23, 42, 0.72);
}

.money-label {
    color: #cbd5e1;
    font-size: 15px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.12em;
}

.money-value {
    font-size: clamp(42px, 5vw, 68px);
    font-weight: 950;
    color: #facc15;
    letter-spacing: -0.06em;
    margin: 10px 0 2px 0;
}

.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    margin-top: 14px;
    padding: 10px 14px;
    border-radius: 999px;
    background: rgba(250,204,21,0.14);
    color: #fde68a;
    border: 1px solid rgba(250,204,21,0.24);
    font-weight: 800;
}

.range-box {
    margin-top: 22px;
    padding: 16px;
    border-radius: 20px;
    background: rgba(2, 6, 23, 0.42);
    border: 1px solid rgba(255,255,255,0.10);
}

.progress-wrap {
    width: 100%;
    height: 13px;
    border-radius: 999px;
    background: rgba(255,255,255,0.08);
    overflow: hidden;
    margin-top: 12px;
}

.progress-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #22c55e, #facc15, #fb7185);
}

.tip {
    padding: 16px 18px;
    border-radius: 20px;
    background: rgba(2, 6, 23, 0.40);
    border: 1px solid rgba(255,255,255,0.10);
    margin-bottom: 12px;
    color: #dbeafe;
    line-height: 1.65;
}

.tip strong {
    color: #facc15;
}

.bill-row {
    display: flex;
    justify-content: space-between;
    gap: 16px;
    padding: 12px 0;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    color: #cbd5e1;
}

.bill-row:last-child {
    border-bottom: none;
}

.bill-total {
    color: #facc15;
    font-size: 24px;
    font-weight: 950;
}

.chart-wrap {
    display: grid;
    grid-template-columns: repeat(25, 1fr);
    align-items: end;
    gap: 5px;
    height: 230px;
    padding: 18px 10px 6px 10px;
    border-radius: 22px;
    background: rgba(2, 6, 23, 0.32);
    border: 1px solid rgba(255,255,255,0.08);
}

.bar {
    min-height: 8px;
    border-radius: 999px 999px 6px 6px;
    background: linear-gradient(180deg, #facc15, #38bdf8);
    box-shadow: 0 8px 26px rgba(56, 189, 248, 0.18);
}

.legend-row {
    display: flex;
    justify-content: space-between;
    color: #94a3b8;
    font-size: 12px;
    margin-top: 8px;
}

.score-ring {
    width: 170px;
    height: 170px;
    border-radius: 50%;
    display: grid;
    place-items: center;
    margin: 6px auto 16px auto;
    background:
        radial-gradient(circle at center, #0f172a 0 57%, transparent 58%),
        conic-gradient(#22c55e 0deg, #facc15 150deg, #fb7185 260deg, rgba(255,255,255,0.10) 260deg 360deg);
    border: 1px solid rgba(255,255,255,0.10);
}

.score-inner {
    text-align: center;
}

.score-num {
    font-size: 36px;
    font-weight: 950;
    color: #facc15;
}

.score-label {
    color: #94a3b8;
    font-size: 12px;
    font-weight: 800;
    text-transform: uppercase;
}

.model-table {
    width: 100%;
    border-collapse: collapse;
    overflow: hidden;
    border-radius: 18px;
    font-size: 14px;
}

.model-table th {
    text-align: left;
    padding: 13px 14px;
    background: rgba(255,255,255,0.08);
    color: #e2e8f0;
    font-weight: 900;
}

.model-table td {
    padding: 13px 14px;
    border-top: 1px solid rgba(255,255,255,0.08);
    color: #cbd5e1;
}

.model-table tr:hover td {
    background: rgba(255,255,255,0.04);
}

.footer-note {
    text-align: center;
    color: #94a3b8;
    font-size: 13px;
    padding: 22px;
}

.stButton > button {
    border-radius: 18px;
    padding: 0.78rem 1rem;
    font-weight: 900;
    border: none;
    background: linear-gradient(135deg, #facc15, #38bdf8);
    color: #020617;
    box-shadow: 0 18px 36px rgba(56, 189, 248, 0.18);
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 22px 50px rgba(250, 204, 21, 0.20);
}

hr {
    border-color: rgba(255,255,255,0.10);
}

@media (max-width: 980px) {
    .grid-3, .grid-2 {
        grid-template-columns: 1fr;
    }
    .hero-title {
        font-size: 44px;
    }
}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)


def format_vnd(value):
    value = float(value)
    return f"{value:,.0f}".replace(",", ".") + " VNĐ"


def build_features_from_input(people, ac_units, ac_hours, fans, fan_hours, fridges, area):
    data = {
        "People": [people],
        "AC_Units": [ac_units],
        "AC_Hours": [ac_hours],
        "Fans": [fans],
        "Fan_Hours": [fan_hours],
        "Fridges": [fridges],
        "Area": [area],
    }

    X = pd.DataFrame(data)

    X["AC_Load"] = X["AC_Units"] * X["AC_Hours"]
    X["Fan_Load"] = X["Fans"] * X["Fan_Hours"]
    X["Total_Appliances"] = X["AC_Units"] + X["Fans"] + X["Fridges"]
    X["Cooling_Per_Person"] = X["AC_Load"] / (X["People"] + 0.5)
    X["Area_Per_Person"] = X["Area"] / X["People"].replace(0, np.nan)
    X["Device_Density"] = X["Total_Appliances"] / X["Area"].clip(lower=1)

    return X.replace([np.inf, -np.inf], np.nan).fillna(0)


@st.cache_resource
def load_model():
    return joblib.load("model_dien_pro.pkl")


def cost_level(vnd):
    if vnd < 350_000:
        return "Thấp", "Chi phí đang ở mức dễ kiểm soát.", 26
    if vnd < 800_000:
        return "Trung bình", "Chi phí khá phổ biến với phòng có thiết bị làm mát.", 48
    if vnd < 1_500_000:
        return "Cao", "Chi phí cao, nên tối ưu thời gian dùng máy lạnh.", 72
    return "Rất cao", "Chi phí rất cao, cần rà soát lại thiết bị tiêu thụ điện.", 92


def tips(people, area, ac_units, ac_hours, fans, fan_hours, fridges, predicted_vnd):
    output = []

    if ac_units > 0 and ac_hours >= 8:
        output.append(("Máy lạnh là điểm nóng", "Giảm 1 đến 2 giờ dùng máy lạnh mỗi ngày có thể tạo khác biệt lớn trong hóa đơn."))
    if ac_units > 0 and ac_hours <= 4:
        output.append(("Thói quen làm mát khá tốt", "Thời gian dùng máy lạnh đang vừa phải, nên duy trì và kết hợp quạt để giảm tải."))
    if fans >= 4 and fan_hours >= 9:
        output.append(("Quạt hoạt động nhiều", "Quạt tiêu thụ ít hơn máy lạnh nhưng nếu chạy lâu và nhiều cái vẫn tạo điện nền đáng kể."))
    if fridges >= 2:
        output.append(("Tủ lạnh chạy 24/24", "Nên kiểm tra gioăng tủ, nhiệt độ cài đặt và hạn chế mở tủ liên tục."))
    if area / max(people, 1) > 45:
        output.append(("Không gian khá rộng", "Diện tích lớn làm chi phí làm mát cao hơn, nên chia khu vực sử dụng khi bật máy lạnh."))
    if predicted_vnd >= 1_000_000:
        output.append(("Cảnh báo chi phí cao", "Nên lập lịch sử dụng máy lạnh và tắt thiết bị khi không dùng để giảm hóa đơn."))

    if not output:
        output.append(("Mức sử dụng cân đối", "Thông số hiện tại khá hợp lý. Chi phí chủ yếu đến từ thói quen dùng thiết bị hằng ngày."))

    return output[:4]


def estimate_breakdown(people, area, ac_units, ac_hours, fans, fan_hours, fridges):
    ac_score = ac_units * ac_hours * 1.9
    fan_score = fans * fan_hours * 0.35
    fridge_score = fridges * 24 * 0.5
    area_score = area * 0.18
    people_score = people * 4.0

    total = ac_score + fan_score + fridge_score + area_score + people_score
    if total <= 0:
        total = 1

    return {
        "Máy lạnh": ac_score / total,
        "Quạt": fan_score / total,
        "Tủ lạnh": fridge_score / total,
        "Diện tích": area_score / total,
        "Số người": people_score / total,
    }


def custom_bar_chart(values):
    max_val = max([v for _, v in values]) if values else 1
    bars = ""
    for hour, val in values:
        height = int(8 + (val / max_val) * 210)
        bars += f'<div title="{hour}h: {format_vnd(val)}" class="bar" style="height:{height}px;"></div>'
    return f"""
    <div class="chart-wrap">{bars}</div>
    <div class="legend-row"><span>0h</span><span>6h</span><span>12h</span><span>18h</span><span>24h</span></div>
    """


def table_html(df):
    if df.empty:
        return "<p style='color:#94a3b8'>Chưa có dữ liệu đánh giá.</p>"

    cols = list(df.columns)
    html = "<table class='model-table'><thead><tr>"
    for c in cols:
        html += f"<th>{c}</th>"
    html += "</tr></thead><tbody>"
    for _, row in df.iterrows():
        html += "<tr>"
        for c in cols:
            html += f"<td>{row[c]}</td>"
        html += "</tr>"
    html += "</tbody></table>"
    return html


try:
    artifact = load_model()
    model = artifact["model"]
    feature_columns = artifact["feature_columns"]
    metrics = artifact.get("metrics", {})
except Exception:
    st.error("Không tìm thấy file model_dien_pro.pkl. Hãy đặt model_dien_pro.pkl cùng thư mục với app_dien_ultra.py.")
    st.stop()


with st.sidebar:
    st.markdown("## ⚡ VoltVision AI")
    st.caption("Bảng điều khiển dự báo tiền điện")
    st.markdown("---")

    people = st.number_input("👥 Số người sử dụng", min_value=1, max_value=20, value=3, step=1)
    area = st.number_input("🏠 Diện tích phòng/nhà m²", min_value=5, max_value=300, value=25, step=1)

    st.markdown("### ❄️ Thiết bị làm mát")
    ac_units = st.number_input("Số máy lạnh", min_value=0, max_value=10, value=1, step=1)
    ac_hours = st.slider("Giờ dùng máy lạnh/ngày", min_value=0, max_value=24, value=6)

    st.markdown("### 🌬️ Thiết bị thường dùng")
    fans = st.number_input("Số quạt", min_value=0, max_value=20, value=2, step=1)
    fan_hours = st.slider("Giờ dùng quạt/ngày", min_value=0, max_value=24, value=10)
    fridges = st.number_input("Số tủ lạnh", min_value=0, max_value=6, value=1, step=1)

    st.markdown("---")
    st.button("🚀 Cập nhật dự báo", use_container_width=True)


X_input = build_features_from_input(
    people, ac_units, ac_hours, fans, fan_hours, fridges, area
)[feature_columns]

pred_thousand = float(np.maximum(model.predict(X_input)[0], 0))
pred_vnd = pred_thousand * 1000

level, level_text, score = cost_level(pred_vnd)

leaderboard = pd.DataFrame(metrics.get("leaderboard", []))
best_mae_thousand = 0.0
if not leaderboard.empty and "model" in leaderboard.columns:
    best_name = metrics.get("best_model")
    matched = leaderboard[leaderboard["model"] == best_name]
    if not matched.empty and "MAE_thousand_VND" in matched.columns:
        best_mae_thousand = float(matched.iloc[0]["MAE_thousand_VND"])

low_vnd = max((pred_thousand - best_mae_thousand) * 1000, 0)
high_vnd = (pred_thousand + best_mae_thousand) * 1000

st.markdown(
    """
    <div class="hero">
        <div class="hero-content">
            <div class="brand-row">
                <div class="logo-bolt">⚡</div>
                <div>
                    <div class="brand-text">VoltVision AI</div>
                    <div style="color:#94a3b8;font-weight:700;">Smart electricity forecasting dashboard</div>
                </div>
            </div>
            <div class="hero-title">
                Dự báo tiền điện <span class="gradient-text">thông minh</span><br>
                cho phòng trọ và hộ gia đình
            </div>
            <div class="hero-subtitle">
                Hệ thống mô phỏng quy trình Machine Learning hoàn chỉnh: làm sạch dữ liệu,
                tạo biến đặc trưng, dự báo chi phí, phân tích kịch bản và gợi ý tiết kiệm điện.
            </div>
            <div class="pill-row">
                <div class="pill">Machine Learning</div>
                <div class="pill">Feature Engineering</div>
                <div class="pill">Scenario Simulator</div>
                <div class="pill">Energy Insight</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

device_total = ac_units + fans + fridges
ac_load = ac_units * ac_hours
fan_load = fans * fan_hours
area_per_person = area / max(people, 1)

st.markdown(
    f"""
    <div class="grid-3">
        <div class="card kpi-card">
            <div class="kpi-label">Tải máy lạnh</div>
            <div class="kpi-value">{ac_load:.0f}</div>
            <div class="kpi-note">Số máy lạnh × số giờ sử dụng mỗi ngày.</div>
        </div>
        <div class="card kpi-card">
            <div class="kpi-label">Tải quạt</div>
            <div class="kpi-value">{fan_load:.0f}</div>
            <div class="kpi-note">Số quạt × số giờ sử dụng mỗi ngày.</div>
        </div>
        <div class="card kpi-card">
            <div class="kpi-label">Thiết bị chính</div>
            <div class="kpi-value">{device_total}</div>
            <div class="kpi-note">Tổng máy lạnh, quạt và tủ lạnh đang khai báo.</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

progress_width = min(max(score, 6), 96)

st.markdown('<div class="grid-2">', unsafe_allow_html=True)

left_col, right_col = st.columns([1.15, 0.85])

with left_col:
    st.markdown(
        f"""
        <div class="card money-panel">
            <div class="money-label">Số tiền điện ước tính trong tháng</div>
            <div class="money-value">{format_vnd(pred_vnd)}</div>
            <div class="status-badge">● Mức chi phí: {level}</div>
            <div style="color:#cbd5e1;line-height:1.7;margin-top:14px;">{level_text}</div>

            <div class="range-box">
                <div style="display:flex;justify-content:space-between;gap:12px;align-items:center;">
                    <div>
                        <div style="color:#94a3b8;font-size:13px;font-weight:800;text-transform:uppercase;">Khoảng tham khảo</div>
                        <div style="font-size:20px;font-weight:900;color:#f8fafc;margin-top:4px;">
                            {format_vnd(low_vnd)} - {format_vnd(high_vnd)}
                        </div>
                    </div>
                    <div style="text-align:right;color:#94a3b8;font-size:13px;">
                        Sai số tham khảo<br>theo tập kiểm tra
                    </div>
                </div>
                <div class="progress-wrap">
                    <div class="progress-fill" style="width:{progress_width}%;"></div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with right_col:
    st.markdown(
        f"""
        <div class="card">
            <div class="score-ring">
                <div class="score-inner">
                    <div class="score-num">{score}</div>
                    <div class="score-label">Energy score</div>
                </div>
            </div>
            <div class="card-soft">
                <div class="bill-row"><span>Số người</span><strong>{people}</strong></div>
                <div class="bill-row"><span>Diện tích/người</span><strong>{area_per_person:.1f} m²</strong></div>
                <div class="bill-row"><span>Máy lạnh/ngày</span><strong>{ac_hours} giờ</strong></div>
                <div class="bill-row"><span>Quạt/ngày</span><strong>{fan_hours} giờ</strong></div>
                <div class="bill-row"><span>Tổng dự báo</span><span class="bill-total">{format_vnd(pred_vnd)}</span></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown('</div>', unsafe_allow_html=True)

breakdown = estimate_breakdown(people, area, ac_units, ac_hours, fans, fan_hours, fridges)
breakdown_html = ""
for name, ratio in breakdown.items():
    width = max(4, int(ratio * 100))
    breakdown_html += f"""
    <div style="margin-bottom:14px;">
        <div style="display:flex;justify-content:space-between;color:#cbd5e1;font-weight:700;">
            <span>{name}</span><span>{ratio*100:.1f}%</span>
        </div>
        <div class="progress-wrap" style="height:10px;margin-top:7px;">
            <div class="progress-fill" style="width:{width}%;"></div>
        </div>
    </div>
    """

st.markdown('<div class="grid-2">', unsafe_allow_html=True)

left2, right2 = st.columns([0.95, 1.05])

with left2:
    st.markdown(
        f"""
        <div class="card">
            <h3>🧾 Hóa đơn mô phỏng</h3>
            <p style="color:#94a3b8;line-height:1.6;">
                Phân bổ bên dưới là mô phỏng để giải thích yếu tố nào đang ảnh hưởng mạnh đến chi phí.
            </p>
            {breakdown_html}
        </div>
        """,
        unsafe_allow_html=True
    )

with right2:
    tip_html = ""
    for title, body in tips(people, area, ac_units, ac_hours, fans, fan_hours, fridges, pred_vnd):
        tip_html += f"<div class='tip'><strong>{title}:</strong> {body}</div>"

    st.markdown(
        f"""
        <div class="card">
            <h3>💡 Trợ lý tiết kiệm điện</h3>
            <p style="color:#94a3b8;line-height:1.6;">
                Các gợi ý được tạo dựa trên thông số sử dụng hiện tại.
            </p>
            {tip_html}
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown('</div>', unsafe_allow_html=True)

scenario_values = []
for h in range(25):
    X_scenario = build_features_from_input(
        people, ac_units, h, fans, fan_hours, fridges, area
    )[feature_columns]
    scenario_pred = float(np.maximum(model.predict(X_scenario)[0], 0)) * 1000
    scenario_values.append((h, scenario_pred))

current_pred = scenario_values[ac_hours][1]
saving_pred = scenario_values[max(ac_hours - 2, 0)][1]
saving_amount = max(current_pred - saving_pred, 0)

st.markdown(
    f"""
    <div class="card">
        <h3>📈 Kịch bản chi phí theo giờ dùng máy lạnh</h3>
        <p style="color:#94a3b8;line-height:1.6;">
            Biểu đồ mô phỏng tiền điện thay đổi khi điều chỉnh số giờ dùng máy lạnh mỗi ngày.
        </p>
        {custom_bar_chart(scenario_values)}
        <div class="grid-3" style="margin-top:18px;margin-bottom:0;">
            <div class="card-soft">
                <div class="kpi-label">Hiện tại</div>
                <div class="kpi-value" style="font-size:24px;">{format_vnd(current_pred)}</div>
                <div class="kpi-note">{ac_hours} giờ máy lạnh mỗi ngày</div>
            </div>
            <div class="card-soft">
                <div class="kpi-label">Giảm 2 giờ/ngày</div>
                <div class="kpi-value" style="font-size:24px;">{format_vnd(saving_pred)}</div>
                <div class="kpi-note">{max(ac_hours - 2, 0)} giờ máy lạnh mỗi ngày</div>
            </div>
            <div class="card-soft">
                <div class="kpi-label">Có thể tiết kiệm</div>
                <div class="kpi-value" style="font-size:24px;color:#22c55e;">{format_vnd(saving_amount)}</div>
                <div class="kpi-note">Ước tính theo mô hình hiện tại</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="card">
        <h3>🧠 Thông tin mô hình</h3>
        <div class="grid-3" style="margin-bottom:18px;">
            <div class="card-soft">
                <div class="kpi-label">Mô hình chọn</div>
                <div class="kpi-value" style="font-size:25px;">{metrics.get("best_model", "N/A")}</div>
            </div>
            <div class="card-soft">
                <div class="kpi-label">Dòng dữ liệu</div>
                <div class="kpi-value" style="font-size:25px;">{metrics.get("rows_after_cleaning", "N/A")}</div>
            </div>
            <div class="card-soft">
                <div class="kpi-label">Đơn vị đầu ra</div>
                <div class="kpi-value" style="font-size:25px;">VNĐ/tháng</div>
            </div>
        </div>
        {table_html(leaderboard)}
        <div class="tip" style="margin-top:18px;">
            <strong>Ghi chú học thuật:</strong> dữ liệu hiện còn ít, vì vậy mô hình phù hợp để minh họa quy trình dự báo bằng Machine Learning.
            Muốn tăng độ chính xác thực tế, nên thu thập thêm dữ liệu và kiểm tra kỹ các giá trị bất thường.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="footer-note">
        VoltVision AI Dashboard • Demo sản phẩm học máy cho dự án dự báo tiền điện
    </div>
    """,
    unsafe_allow_html=True
)

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import time

st.set_page_config(page_title="바이오가스 발전 시뮬레이터", layout="wide")
st.title("🟢 바이오가스 발전 시뮬레이터: 폐기물에서 에너지까지")

# -------------------------
# 1. 입력: 폐기물 종류, 양, 발효 조건
# -------------------------
st.sidebar.header("입력 조건 설정")
waste_type = st.sidebar.selectbox("폐기물 종류", ["음식물 쓰레기", "농업 부산물"])
waste_amount = st.sidebar.slider("폐기물 양 (kg)", 1, 100, 10)
temperature = st.sidebar.slider("발효 온도 (℃)", 20, 60, 35)
time_days = st.sidebar.slider("발효 시간 (일)", 1, 30, 10)

st.markdown(f"**선택한 조건:** {waste_type}, {waste_amount}kg, {temperature}℃, {time_days}일")

# -------------------------
# 2. 산물 생성량 계산 (간단한 모델)
# -------------------------
# 폐기물 종류별 생성 비율 (임의 단순 모델)
waste_ratio = {
    "음식물 쓰레기": {"CH4": 0.05, "CO2": 0.08, "Ethanol": 0.02, "Butanol": 0.01},
    "농업 부산물": {"CH4": 0.03, "CO2": 0.10, "Ethanol": 0.015, "Butanol": 0.005}
}

# 시간에 따른 생성량 증가 (단순 선형 모델)
days = np.arange(1, time_days + 1)
CH4 = days * waste_amount * waste_ratio[waste_type]["CH4"] / time_days
CO2 = days * waste_amount * waste_ratio[waste_type]["CO2"] / time_days
Ethanol = days * waste_amount * waste_ratio[waste_type]["Ethanol"] / time_days
Butanol = days * waste_amount * waste_ratio[waste_type]["Butanol"] / time_days

df = pd.DataFrame({
    "Day": days,
    "CH4 (kg)": CH4,
    "CO2 (kg)": CO2,
    "Ethanol (kg)": Ethanol,
    "Butanol (kg)": Butanol
})

# -------------------------
# 3. 시각화: 바 차트 + 선 그래프
# -------------------------
st.subheader("💨 산물 생성량 변화 (시간에 따른 시뮬레이션)")

# 선택한 날 표시
selected_day = st.slider("시뮬레이션 일 선택", 1, time_days, 1)
day_data = df[df["Day"] == selected_day].melt(id_vars="Day", var_name="산물", value_name="양")

bar_chart = alt.Chart(day_data).mark_bar().encode(
    x="산물",
    y="양",
    color="산물",
    tooltip=["산물", "양"]
).properties(width=700, height=400)
st.altair_chart(bar_chart, use_container_width=True)

st.subheader("📈 전체 발효 기간 산물 생성 추이")
line_chart = alt.Chart(df.melt(id_vars="Day", var_name="산물", value_name="양")).mark_line(point=True).encode(
    x="Day",
    y="양",
    color="산물",
    tooltip=["Day", "산물", "양"]
).properties(width=700, height=400)
st.altair_chart(line_chart, use_container_width=True)

# -------------------------
# 4. 애니메이션: 발효 → 가스 생성 → 에너지 활용
# -------------------------
st.subheader("⚡ 발효 → 가스 생성 → 에너지 활용 애니메이션")
progress_bar = st.progress(0)
status_text = st.empty()

for i in range(time_days):
    status_text.text(f"Day {i+1}/{time_days}: 발효 진행 중...")
    progress_bar.progress((i+1)/time_days)
    time.sleep(0.1)  # 애니메이션 속도 조절

status_text.text("✅ 발효 완료! 바이오연료 생성 완료")


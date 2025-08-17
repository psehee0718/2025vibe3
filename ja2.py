import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import time
import matplotlib.pyplot as plt

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
# 2. 산물 생성량 계산 (단순 모델)
# -------------------------
waste_ratio = {
    "음식물 쓰레기": {"CH4": 0.05, "CO2": 0.08, "Ethanol": 0.02, "Butanol": 0.01},
    "농업 부산물": {"CH4": 0.03, "CO2": 0.10, "Ethanol": 0.015, "Butanol": 0.005}
}

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
st.subheader("💨 산물 생성량 변화 (선택일 기준)")
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
# 4. 애니메이션: 발효 진행
# -------------------------
st.subheader("⚡ 발효 → 가스 생성 → 에너지 활용 애니메이션")
progress_bar = st.progress(0)
status_text = st.empty()

for i in range(time_days):
    status_text.text(f"Day {i+1}/{time_days}: 발효 진행 중...")
    progress_bar.progress((i+1)/time_days)
    time.sleep(0.1)

status_text.text("✅ 발효 완료! 바이오연료 생성 완료")

# -------------------------
# 5. 바이오연료 에너지 환산
# -------------------------
st.subheader("🔋 생성된 바이오연료 에너지 환산")

heating_values = {
    "CH4": 13.9,      # kWh/kg
    "Ethanol": 7.8,
    "Butanol": 10.2
}

final_CH4 = CH4[-1]
final_Ethanol = Ethanol[-1]
final_Butanol = Butanol[-1]

energy_CH4 = final_CH4 * heating_values["CH4"]
energy_Ethanol = final_Ethanol * heating_values["Ethanol"]
energy_Butanol = final_Butanol * heating_values["Butanol"]
total_energy = energy_CH4 + energy_Ethanol + energy_Butanol

st.write(f"메탄(CH₄) 에너지: {energy_CH4:.2f} kWh")
st.write(f"에탄올(C₂H₅OH) 에너지: {energy_Ethanol:.2f} kWh")
st.write(f"부탄올(C₄H₉OH) 에너지: {energy_Butanol:.2f} kWh")
st.write(f"**총 에너지 생산량: {total_energy:.2f} kWh**")

# -------------------------
# 6. 원형 차트 시각화
# -------------------------
st.subheader("📊 산물별 에너지 비율 (원형 차트)")

energy_data = [energy_CH4, energy_Ethanol, energy_Butanol]
labels = ["CH₄", "Ethanol", "Butanol"]
colors = ["#1f77b4", "#ff7f0e", "#2ca02c"]

fig, ax = plt.subplots()
ax.pie(energy_data, labels=labels, autopct="%1.1f%%", startangle=90, colors=colors)
ax.set_title("산물별 에너지 비율")
st.pyplot(fig)



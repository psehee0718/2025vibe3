import streamlit as st
from streamlit_folium import st_folium
import folium
import math

st.set_page_config(page_title="방사능 영향 시각화", layout="wide")
st.title("☢️ 방사능 누출 거리별 영향 시각화")

# 방사능 누출 지점 (예: 후쿠시마 원전)
latitude = 37.4218
longitude = 141.0328

# 초기 방사선 세기 (예: 1000 μSv/h)
initial_dose = st.slider("초기 방사선 세기 (μSv/h)", 100, 5000, 1000)

# 거리별 감소 모델 (지수함수적 감소)
def dose_at_distance(r, r0=1):
    return initial_dose * math.exp(-r / 5)

# 지도 생성
m = folium.Map(location=[latitude, longitude], zoom_start=8)

# 거리별 원 그리기 + 방사선 세기 표시
distances_km = [1, 5, 10, 20, 30, 50, 100]
for dist in distances_km:
    dose = dose_at_distance(dist)
    folium.Circle(
        location=[latitude, longitude],
        radius=dist * 1000,
        color="red" if dose > 100 else "orange" if dose > 10 else "green",
        fill=True,
        fill_opacity=0.2,
        popup=f"{dist}km 거리<br>방사선: {dose:.2f} μSv/h",
    ).add_to(m)

st.subheader("🗺️ 시각화 지도")
st_folium(m, width=900, height=600)


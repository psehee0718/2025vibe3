import streamlit as st
from streamlit_folium import st_folium
import folium
import math

st.set_page_config(page_title="과학 재해 시각화 대시보드", layout="wide")
st.title("🧪 과학 재해/환경 현상 통합 시각화 대시보드")

# 주제 리스트
topics = [
    "☢️ 방사능의 영향과 안전거리 시각화",
    "🌋 화산 폭발 영향 범위 시각화",
    "☣️ 화학 유독가스 누출 반경 시각화",
    "💥 핵폭발 또는 지진의 충격파 거리별 영향",
    "🌫️ 미세먼지 확산 지도 시각화",
    "🌀 태풍 경로와 바람 세기 시각화",
    "📡 전파탑의 전자파 강도 분포 시각화",
    "🌊 해양 유출사고(기름 유출)의 확산 시뮬레이션"
]

selected_topic = st.selectbox("📌 시각화할 주제를 선택하세요:", topics)

# 사용자가 클릭할 수 있는 지도 표시
st.markdown("### 🧭 사고 발생 위치를 지도에서 클릭하세요")
click_map = folium.Map(location=[36.5, 127.5], zoom_start=7)
st_click = st_folium(click_map, height=400, width=700)

if not st_click or not st_click.get("last_clicked"):
    st.warning("지도를 클릭해 위치를 선택해주세요.")
    st.stop()

# 클릭된 위치 좌표 추출
center_lat = st_click["last_clicked"]["lat"]
center_lon = st_click["last_clicked"]["lng"]
st.success(f"선택된 위치: 위도 {center_lat:.4f}, 경도 {center_lon:.4f}")

# 본 지도에 재해 시각화 표시
m = folium.Map(location=[center_lat, center_lon], zoom_start=8)

# 주제별 표시
if "방사능" in selected_topic:
    st.subheader("☢️ 방사능 감쇠 시각화")
    initial_dose = st.slider("초기 방사선 세기 (μSv/h)", 100, 5000, 1000)
    def dose(r): return initial_dose * math.exp(-r / 5)
    for d in [1, 5, 10, 20, 30, 50, 100]:
        value = dose(d)
        folium.Circle(
            location=[center_lat, center_lon],
            radius=d * 1000,
            popup=f"{d}km / {value:.1f} μSv/h",
            color="red" if value > 100 else "orange" if value > 10 else "green",
            fill=True,
            fill_opacity=0.3
        ).add_to(m)

elif "화산" in selected_topic:
    st.subheader("🌋 화산 폭발 범위 시각화")
    for r, color, label in [(3, "red", "화쇄류"), (10, "orange", "화산재"), (30, "yellow", "진동권")]:
        folium.Circle(
            location=[center_lat, center_lon],
            radius=r * 1000,
            popup=f"{label} ({r}km)",
            color=color,
            fill=True,
            fill_opacity=0.3
        ).add_to(m)

elif "유독가스" in selected_topic:
    st.subheader("☣️ 유독가스 확산 시각화")
    wind_dir = st.slider("풍향 (북=0, 동=90)", 0, 360, 90)
    for r in [1, 3, 5, 10]:
        folium.Circle(
            location=[center_lat, center_lon],
            radius=r * 1000,
            popup=f"{r}km 가스 확산",
            color="purple",
            fill=True,
            fill_opacity=0.2
        ).add_to(m)

elif "핵폭발" in selected_topic or "지진" in selected_topic:
    st.subheader("💥 충격파 시각화")
    for r, color, label in [(1, "red", "전파"), (3, "orange", "붕괴"), (6, "yellow", "파손"), (10, "green", "진동")]:
        folium.Circle(
            location=[center_lat, center_lon],
            radius=r * 1000,
            popup=f"{label} ({r}km)",
            color=color,
            fill=True,
            fill_opacity=0.25
        ).add_to(m)

elif "미세먼지" in selected_topic:
    st.subheader("🌫️ 미세먼지 확산 시각화")
    for r, color in zip([5, 15, 30, 50], ["orange", "yellow", "green", "blue"]):
        folium.Circle(
            location=[center_lat, center_lon],
            radius=r * 1000,
            popup=f"{r}km 확산",
            color=color,
            fill=True,
            fill_opacity=0.2
        ).add_to(m)

elif "태풍" in selected_topic:
    st.subheader("🌀 태풍 바람 반경 시각화")
    for r, wind in zip([50, 30, 10], [50, 30, 10]):
        folium.Circle(
            location=[center_lat, center_lon],
            radius=r * 1000,
            popup=f"{r}km 바람권 / 풍속 {wind} m/s",
            color="blue",
            fill=True,
            fill_opacity=0.2
        ).add_to(m)

elif "전자파" in selected_topic:
    st.subheader("📡 전자파 세기 시각화")
    power = st.slider("기지국 출력(W)", 10, 1000, 100)
    def strength(r): return power / (r ** 2)
    for r in [1, 5, 10, 20]:
        val = strength(r)
        folium.Circle(
            location=[center_lat, center_lon],
            radius=r * 1000,
            popup=f"{r}km 거리 / 세기: {val:.2f}",
            color="teal",
            fill=True,
            fill_opacity=0.2
        ).add_to(m)

elif "기름 유출" in selected_topic:
    st.subheader("🌊 기름 유출 확산 시각화")
    for t in range(1, 6):
        folium.Circle(
            location=[center_lat, center_lon],
            radius=t * 3000,
            popup=f"{t*3}km 유출 범위",
            color="black",
            fill=True,
            fill_opacity=0.1
        ).add_to(m)

# 최종 지도 표시
st.subheader("🗺️ 시각화 결과")
st_folium(m, height=600, width=900)

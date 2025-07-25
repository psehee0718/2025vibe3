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

st.markdown("### 🧭 사고 발생 위치를 지도에서 클릭하여 설정하세요")
base_map = folium.Map(location=[36.5, 127.5], zoom_start=7)
marker = folium.Marker(location=[36.5, 127.5], popup="기본 위치", draggable=True)
marker.add_to(base_map)

location_data = st_folium(base_map, height=400, width=700)
clicked_location = location_data.get("last_clicked")

if clicked_location:
    center_lat = clicked_location["lat"]
    center_lon = clicked_location["lng"]
    st.success(f"선택된 위치: 위도 {center_lat:.4f}, 경도 {center_lon:.4f}")
else:
    st.info("지도를 클릭해 위치를 선택해주세요.")
    st.stop()

# 본 시각화 지도
m = folium.Map(location=[center_lat, center_lon], zoom_start=8)

# 주제별 시각화
if "방사능" in selected_topic:
    st.subheader("☢️ 방사능 거리별 감쇠 시각화")
    initial_dose = st.slider("초기 방사선 세기 (μSv/h)", 100, 5000, 1000)
    def dose(r): return initial_dose * math.exp(-r / 5)
    for d in [1, 5, 10, 20, 30, 50, 100]:
        val = dose(d)
        folium.Circle(
            location=[center_lat, center_lon],
            radius=d * 1000,
            popup=f"{d}km 거리 / {val:.1f} μSv/h",
            color="red" if val > 100 else "orange" if val > 10 else "green",
            fill=True, fill_opacity=0.3
        ).add_to(m)

elif "화산" in selected_topic:
    st.subheader("🌋 화산 폭발 반경 시각화")
    zones = [(3, "red", "화쇄류 위험"), (10, "orange", "화산재 낙하"), (30, "yellow", "소음/진동")]
    for r, color, label in zones:
        folium.Circle(
            location=[center_lat, center_lon],




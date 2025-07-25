streamlit
folium
streamlit-folium

import streamlit as st
from streamlit_folium import st_folium
import folium


st.set_page_config(page_title="나만의 북마크 지도", layout="wide")

st.title("📍 나만의 북마크 지도")
st.markdown("지도를 클릭해서 북마크를 추가하세요!")

# 세션 상태로 북마크 저장
if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = []

# 기본 지도 위치
start_lat, start_lon = 37.5665, 126.9780  # 서울

# folium 지도 객체
m = folium.Map(location=[start_lat, start_lon], zoom_start=12)

# 기존 북마크 마커 표시
for mark in st.session_state.bookmarks:
    folium.Marker(location=[mark["lat"], mark["lon"]], popup=mark["name"]).add_to(m)

# 지도 출력 및 클릭 이벤트 수집
map_data = st_folium(m, height=500, width=700)

# 클릭으로 위치 저장
if map_data and map_data.get("last_clicked"):
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]
    with st.form("bookmark_form", clear_on_submit=True):
        name = st.text_input("이 장소의 이름은?", placeholder="예: 맛집, 약속장소 등")
        submitted = st.form_submit_button("북마크 추가")
        if submitted and name:
            st.session_state.bookmarks.append({"name": name, "lat": lat, "lon": lon})
            st.success(f"✅ '{name}' 위치가 저장되었습니다!")

# 저장된 북마크 리스트 보여주기
st.subheader("📌 저장된 북마크 목록")
for i, mark in enumerate(st.session_state.bookmarks):
    st.write(f"{i+1}. {mark['name']} ({mark['lat']:.4f}, {mark['lon']:.4f})")

# 전체 리셋 기능
if st.button("🗑️ 전체 북마크 초기화"):
    st.session_state.bookmarks = []
    st.success("모든 북마크가 삭제되었습니다.")

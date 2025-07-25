

import streamlit as st
from streamlit_folium import st_folium
import folium

st.set_page_config(page_title="나만의 북마크 지도", layout="wide")

st.title("📍 나만의 북마크 지도")
st.markdown("지도를 클릭해서 북마크를 추가하세요!")

# 북마크 리스트 초기화
if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = []

# 지도 시작 위치 (서울)
start_lat, start_lon = 37.5665, 126.9780

# 지도 생성
m = folium.Map(location=[start_lat, start_lon], zoom_start=12)

# 저장된 북마크 표시
for mark in st.session_state.bookmarks:
    folium.Marker(
        location=[mark["lat"], mark["lon"]],
        popup=mark["name"],
        tooltip=mark["name"],
        icon=folium.Icon(color="blue", icon="bookmark")
    ).add_to(m)

# 지도 출력 (클릭 이벤트 감지 포함)
map_data = st_folium(m, height=500, width=800)

# 클릭했을 경우 북마크 추가 폼 표시
if map_data and map_data.get("last_clicked"):
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]

    with st.form("bookmark_form", clear_on_submit=True):
        name = st.text_input("📝 북마크 이름을 입력하세요:", placeholder="예: 우리집, 맛집, 약속 장소")
        submitted = st.form_submit_button("✅ 북마크 추가")
        if submitted and name:
            st.session_state.bookmarks.append({"name": name, "lat": lat, "lon": lon})
            st.success(f"✅ '{name}' 북마크가 저장되었습니다!")

# 저장된 북마크 목록 출력
st.subheader("📌 저장된 북마크 목록")
if st.session_state.bookmarks:
    for i, mark in enumerate(st.session_state.bookmarks):
        st.write(f"{i+1}. {mark['name']} ({mark['lat']:.4f}, {mark['lon']:.4f})")
else:
    st.info("아직 북마크가 없습니다. 지도를 클릭해 추가해보세요!")

# 초기화 버튼
if st.button("🗑️ 모든 북마크 초기화"):
    st.session_state.bookmarks = []
    st.success("❌ 모든 북마크가 삭제되었습니다.")

# 전체 리셋 기능
if st.button("🗑️ 전체 북마크 초기화"):
    st.session_state.bookmarks = []
    st.success("모든 북마크가 삭제되었습니다.")

import streamlit as st
from streamlit_folium import st_folium
import folium

st.set_page_config(page_title="위도/경도 입력 북마크 지도", layout="wide")

st.title("📍 나만의 북마크 지도")
st.markdown("위도와 경도를 직접 입력해서 북마크를 추가하세요!")

# 북마크 리스트 초기화
if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = []

# 지도 중심 좌표 (기본 서울)
start_lat, start_lon = 37.5665, 126.9780

# 지도 생성
m = folium.Map(location=[start_lat, start_lon], zoom_start=12)

# 저장된 북마크 마커 표시
for mark in st.session_state.bookmarks:
    folium.Marker(
        location=[mark["lat"], mark["lon"]],
        popup=mark["name"],
        tooltip=mark["name"],
        icon=folium.Icon(color="blue", icon="bookmark")
    ).add_to(m)

# 지도 출력
st_folium(m, height=500, width=800)

# 북마크 입력 폼
st.subheader("📝 북마크 추가하기")

with st.form("add_bookmark_form"):
    name = st.text_input("북마크 이름")
    lat = st.number_input("위도 (latitude)", format="%.6f")
    lon = st.number_input("경도 (longitude)", format="%.6f")
    submitted = st.form_submit_button("✅ 북마크 추가")

    if submitted:
        if name and (-90 <= lat <= 90) and (-180 <= lon <= 180):
            st.session_state.bookmarks.append({"name": name, "lat": lat, "lon": lon})
            st.success(f"✅ '{name}' 북마크가 추가되었습니다!")
        else:
            st.error("❗ 올바른 위도/경도를 입력해주세요.")

# 북마크 목록 표시
st.subheader("📌 저장된 북마크 목록")
if st.session_state.bookmarks:
    for i, mark in enumerate(st.session_state.bookmarks):
        st.write(f"{i+1}. {mark['name']} ({mark['lat']:.4f}, {mark['lon']:.4f})")
else:
    st.info("아직 북마크가 없습니다. 위도와 경도를 입력해 추가해보세요!")

# 전체 초기화 버튼
if st.button("🗑️ 모든 북마크 초기화"):
    st.session_state.bookmarks = []
    st.success("✅ 모든 북마크가 삭제되었습니다.")


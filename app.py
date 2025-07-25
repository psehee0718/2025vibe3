import streamlit as st
from streamlit_folium import st_folium
import folium
import requests
import json
import os

# 페이지 설정
st.set_page_config(page_title="📍 북마크 지도", layout="wide")

# 저장 파일 경로
BOOKMARK_FILE = "bookmarks.json"

# 북마크 불러오기
def load_bookmarks():
    if os.path.exists(BOOKMARK_FILE):
        with open(BOOKMARK_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# 북마크 저장하기
def save_bookmarks(bookmarks):
    with open(BOOKMARK_FILE, "w", encoding="utf-8") as f:
        json.dump(bookmarks, f, ensure_ascii=False, indent=2)

# 주소 → 위경도 변환 (OpenStreetMap)
def geocode(address):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": address, "format": "json"}
    headers = {"User-Agent": "streamlit-app"}
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200 and response.json():
        result = response.json()[0]
        return float(result["lat"]), float(result["lon"])
    return None, None

# 세션 초기화
if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = load_bookmarks()

# ───────────────────────── 사이드바 (입력창 및 북마크 목록) ─────────────────────────
with st.sidebar:
    st.header("📌 북마크 추가")
    name = st.text_input("북마크 이름")
    address = st.text_input("도로명 주소", placeholder="예: 광주광역시 북구 금호로 100")
    if st.button("➕ 추가"):
        if name and address:
            lat, lon = geocode(address)
            if lat and lon:
                st.session_state.bookmarks.append({
                    "name": name,
                    "address": address,
                    "lat": lat,
                    "lon": lon
                })
                save_bookmarks(st.session_state.bookmarks)
                st.success(f"✅ '{name}' 북마크가 추가되었습니다.")
            else:
                st.error("❌ 주소를 찾을 수 없습니다.")
        else:
            st.warning("⚠️ 이름과 주소를 모두 입력해주세요.")

    if st.button("🗑️ 모든 북마크 초기화"):
        st.session_state.bookmarks = []
        save_bookmarks([])
        st.success("🧹 북마크가 초기화되었습니다.")

    st.divider()
    st.subheader("📋 북마크 목록")
    if st.session_state.bookmarks:
        for bm in st.session_state.bookmarks:
            st.write(f"• **{bm['name']}**<br><small>{bm['address']}</small>", unsafe_allow_html=True)
    else:
        st.caption("등록된 북마크가 없습니다.")

# ───────────────────────── 지도 영역 ─────────────────────────
st.title("🗺️ 나만의 북마크 지도")

# 시작 위치 설정
if st.session_state.bookmarks:
    center = [st.session_state.bookmarks[-1]["lat"], st.session_state.bookmarks[-1]["lon"]]
else:
    center = [37.5665, 126.9780]  # 기본 서울

# 지도 생성
m = folium.Map(location=center, zoom_start=12)
for bm in st.session_state.bookmarks:
    folium.Marker(
        location=[bm["lat"], bm["lon"]],
        popup=f"{bm['name']}<br>{bm['address']}",
        tooltip=bm["name"],
        icon=folium.Icon(color="blue", icon="bookmark")
    ).add_to(m)

# 지도 출력
st_folium(m, width=900, height=600)



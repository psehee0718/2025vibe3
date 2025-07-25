import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Safecast 방사선 시각화", layout="wide")
st.title("📡 Safecast 방사선 측정값 지도 시각화")

# CSV 업로드
file = st.file_uploader("⚛️ Safecast 측정 데이터 CSV 업로드", type=["csv"])
if not file:
    st.info("Safecast 데이터 CSV 파일을 업로드하세요.")
    st.stop()

# 데이터 불러오기
df = pd.read_csv(file)
st.write("### 데이터 미리보기", df.head())

# 위도, 경도, 측정값 컬럼 선택
lat_col = st.selectbox("위도 컬럼 선택", df.columns)
lon_col = st.selectbox("경도 컬럼 선택", df.columns)
dose_col = st.selectbox("방사선량 컬럼 선택 (예: dose_rate)", df.columns)

df = df[[lat_col, lon_col, dose_col]].dropna()

# 지도 중심 설정 (첫 행 위치 기준)
center = [df[lat_col].iloc[0], df[lon_col].iloc[0]]
m = folium.Map(location=center, zoom_start=6)

# 측정 포인트 표시
for _, row in df.iterrows():
    dose = row[dose_col]
    color = "green" if dose < 0.2 else "orange" if dose < 0.5 else "red"
    folium.CircleMarker(
        location=[row[lat_col], row[lon_col]],
        radius=5,
        popup=f"{dose_col}: {dose:.3f}",
        color=color,
        fill=True,
        fill_opacity=0.6
    ).add_to(m)

st.subheader("📍 방사선 측정 위치")
st_folium(m, width=900, height=600)

# 시간 기반 변화가 있다면 Plotly 시각화
if "timestamp" in df.columns:
    import plotly.express as px
    df['time'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df_time = df.dropna(subset=['time'])
    fig = px.scatter(df_time.sort_values('time'),
                     x='time', y=dose_col,
                     title="⏳ 시간대별 방사선량 변화",
                     labels={dose_col:'Dose (µSv/h)'})
    st.plotly_chart(fig, use_container_width=True)


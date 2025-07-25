import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="나노융합제품 분석", layout="wide")
st.title("🧪 나노융합제품의 산업별·연도별 분석 대시보드")

# ✅ 파일 업로드 받기
uploaded_file = st.file_uploader("📂 나노융합제품 CSV 파일 업로드", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, encoding="cp949")

    # 헤더 설정
    df.columns = df.iloc[0]
    df = df[1:]

# 연도 및 관련 컬럼 정의
year_list = ['2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023']
cols_total_revenue = [f"{y}.3" for y in year_list]  # 총매출액
cols_share = [f"{y}.1" for y in year_list]  # 비중 (%)

# 숫자형 변환
for col in cols_total_revenue + cols_share:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# 제목 및 설명
st.set_page_config(page_title="나노융합제품 분석", layout="wide")
st.title("🧪 나노융합제품의 산업별·연도별 분석")
st.markdown("한국산 나노융합제품의 제품화 단계, 산업군, 연도별 매출액 및 비중(%)을 분석합니다.")

# 분석 선택
analysis_type = st.radio("🔍 분석 종류를 선택하세요", ["산업별 분석", "연도별 총매출액 추이", "연도별 비중(%) 추이"])
selected_stage = st.selectbox("📦 제품화 단계 선택", df["단계별"].unique())

# 선택된 제품화 단계 필터링
filtered_df = df[df["단계별"] == selected_stage]
industries = filtered_df["산업별"].unique()

# 1. 산업별 분석
if analysis_type == "산업별 분석":
    st.subheader("📊 선택 연도의 산업별 총매출액 비교")
    year = st.selectbox("연도 선택", year_list)
    col = f"{year}.3"
    plot_df = filtered_df[["산업별", col]].dropna()
    plot_df.columns = ["산업별", "총매출액"]

    fig = px.bar( plot_df, x="산업별", y="총매출액", title=f"{year}년 산업별 총매출액 (단위: 억원)", text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

# 2. 연도별 총매출액 추이
elif analysis_type == "연도별 총매출액 추이":
    st.subheader("📈 산업의 연도별 총매출액 추이")
    selected_industry = st.selectbox("산업 선택", industries)
    plot_df = filtered_df[filtered_df["산업별"] == selected_industry][cols_total_revenue]
    plot_df.columns = year_list
    plot_df = plot_df.T.reset_index()
    plot_df.columns = ["연도", "총매출액"]

    fig = px.line(plot_df, x="연도", y="총매출액", markers=True, title=f"{selected_industry} 산업의 총매출액 연도별 추이")
    st.plotly_chart(fig, use_container_width=True)

# 3. 연도별 비중(%) 추이
elif analysis_type == "연도별 비중(%) 추이":
    st.subheader("📈 산업의 연도별 비중(%) 추이")
    selected_industry = st.selectbox("산업 선택", industries)
    plot_df = filtered_df[filtered_df["산업별"] == selected_industry][cols_share]
    plot_df.columns = year_list
    plot_df = plot_df.T.reset_index()
    plot_df.columns = ["연도", "비중"]

    fig = px.line(plot_df, x="연도", y="비중", markers=True, title=f"{selected_industry} 산업의 전체 중 비중(%) 연도별 추이")
    st.plotly_chart(fig, use_container_width=True)

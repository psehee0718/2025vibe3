import streamlit as st
import pandas as pd
import plotly.express as px

# CSV 파일 불러오기
df = pd.read_csv("나노융합제품의_제품화단계_20250725133453.csv", encoding="cp949")

# 헤더 재설정
df.columns = df.iloc[0]
df = df[1:]

# 분석용 컬럼 변환
year_list = ['2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023']
cols_total_revenue = [f"{y}.3" for y in year_list]  # 총매출액
cols_share = [f"{y}.1" for y in year_list]  # 비중

# 숫자형으로 변환
for col in cols_total_revenue + cols_share:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Streamlit 구성
st.set_page_config(page_title="나노융합제품 분석 대시보드", layout="wide")
st.title("🧪 나노융합제품 산업별/연도별 분석 대시보드")

# 분석 종류 선택
analysis_type = st.radio("분석 유형 선택", ["산업별 분석", "연도별 총매출액 추이", "연도별 비중(%) 추이"])
selected_stage = st.selectbox("제품화 단계 선택", df["단계별"].unique())

# 필터링
filtered_df = df[df["단계별"] == selected_stage]
industries = filtered_df["산업별"].unique()

if analysis_type == "산업별 분석":
    st.subheader("📊 산업별 총매출액 비교")
    year = st.selectbox("연도 선택", year_list)
    col = f"{year}.3"
    plot_df = filtered_df[["산업별", col]].dropna()
    fig = px.bar(plot_df, x="산업별", y=col, title=f"{year}년 산업별 총매출액", labels={col: "총매출액 (억원)"})
    st.plotly_chart(fig, use_container_width=True)

elif analysis_type == "연도별 총매출액 추이":
    st.subheader("📈 연도별 총매출액 추이")
    selected_industry = st.selectbox("산업 선택", industries)
    plot_df = filtered_df[filtered_df["산업별"] == selected_industry][cols_total_revenue]
    plot_df.columns = year_list
    plot_df = plot_df.T.reset_index()
    plot_df.columns = ["연도", "총매출액"]
    fig = px.line(plot_df, x="연도", y="총매출액", markers=True, title=f"{selected_industry} 총매출액 변화")
    st.plotly_chart(fig, use_container_width=True)

elif analysis_type == "연도별 비중(%) 추이":
    st.subheader("📈 연도별 비중(%) 추이")
    selected_industry = st.selectbox("산업 선택", industries)
    plot_df = filtered_df[filtered_df["산업별"] == selected_industry][cols_share]
    plot_df.columns = year_list
    plot_df = plot_df.T.reset_index()
    plot_df.columns = ["연도", "비중"]
    fig = px.line(plot_df, x="연도", y="비중", markers=True, title=f"{selected_industry} 비중 (%) 변화")
    st.plotly_chart(fig, use_container_width=True)


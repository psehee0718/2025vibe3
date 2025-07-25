import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="나노융합제품 분석 대시보드", layout="wide")
st.title("🧪 나노융합제품 산업별·연도별 분석 대시보드")

# ✅ CSV 업로드
uploaded_file = st.file_uploader("📂 나노융합제품 CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file:
    # CSV 읽기
    df = pd.read_csv(uploaded_file, encoding="cp949")

    # 첫 번째 행을 컬럼명으로 지정
    df.columns = df.iloc[0]
    df = df[1:].reset_index(drop=True)

    # 컬럼 공백 제거
    df.columns = df.columns.str.strip()

    # 연도 및 컬럼 정의
    year_list = ['2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023']
    cols_total_revenue = [f"{y}.3" for y in year_list]
    cols_share = [f"{y}.1" for y in year_list]

    # 존재하는 컬럼만 숫자형으로 변환
    for col in cols_total_revenue + cols_share:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # 분석 유형 선택
    analysis_type = st.radio("🔍 분석 종류 선택", ["산업별 분석", "연도별 총매출액 추이", "연도별 비중(%) 추이"])
    selected_stage = st.selectbox("📦 제품화 단계 선택", df["단계별"].unique())

    filtered_df = df[df["단계별"] == selected_stage]
    industries = filtered_df["산업별"].unique()

    # 산업별 분석
    if analysis_type == "산업별 분석":
        st.subheader("📊 산업별 총매출액 (선택 연도)")
        year = st.selectbox("연도 선택", year_list)
        col = f"{year}.3"
        if col in filtered_df.columns:
            plot_df = filtered_df[["산업별", col]].dropna()
            plot_df.columns = ["산업별", "총매출액"]
            fig = px.bar(plot_df, x="산업별", y="총매출액",
                         title=f"{year}년 산업별 총매출액 (단위: 억원)", text_auto=True)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error(f"❗ '{col}' 컬럼이 존재하지 않습니다.")

    # 연도별 총매출액 추이
    elif analysis_type == "연도별 총매출액 추이":
        st.subheader("📈 연도별 총매출액 추이")
        selected_industry = st.selectbox("산업 선택", industries)
        plot_df = filtered_df[filtered_df["산업별"] == selected_industry]
        safe_cols = [col for col in cols_total_revenue if col in plot_df.columns]
        if safe_cols and not plot_df.empty:
            ydata = plot_df[safe_cols].copy()
            ydata.columns = [y.split('.')[0] for y in safe_cols]
            ydata = ydata.T.reset_index()
            ydata.columns = ["연도", "총매출액"]
            fig = px.line(ydata, x="연도", y="총매출액", markers=True,
                          title=f"{selected_industry} 산업의 연도별 총매출액 추이")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("❗ 연도별 총매출액 관련 컬럼이 누락되어 있거나 데이터가 없습니다.")

    # 연도별 비중(%) 추이
    elif analysis_type == "연도별 비중(%) 추이":
        st.subheader("📈 연도별 비중(%) 추이")
        selected_industry = st.selectbox("산업 선택", industries)
        plot_df = filtered_df[filtered_df["산업별"] == selected_industry]
        safe_cols = [col for col in cols_share if col in plot_df.columns]
        if safe_cols and not plot_df.empty:
            ydata = plot_df[safe_cols].copy()
            ydata.columns = [y.split('.')[0] for y in safe_cols]
            ydata = ydata.T.reset_index()
            ydata.columns = ["연도", "비중"]
            fig = px.line(ydata, x="연도", y="비중", markers=True,
                          title=f"{selected_industry} 산업의 연도별 비중(%) 추이")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("❗ 연도별 비중 관련 컬럼이 누락되어 있거나 데이터가 없습니다.")

else:
    st.info("먼저 CSV 파일을 업로드해주세요. 예: 나노융합제품의_제품화단계_20250725133453.csv")

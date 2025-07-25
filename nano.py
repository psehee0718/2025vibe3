import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="나노융합제품 분석", layout="wide")
st.title("🧪 나노융합제품 산업별/연도별 분석")

@st.cache_data
def load_data():
    df = pd.read_csv("나노융합제품의_제품화단계_20250725133453.csv", encoding="cp949")
    df.columns = df.iloc[0]
    df = df[1:].reset_index(drop=True)
    df.columns = df.columns.str.strip()
    return df

df = load_data()

year_list = ['2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023']
cols_total_revenue = [f"{y}.3" for y in year_list]
cols_share = [f"{y}.1" for y in year_list]

for col in cols_total_revenue + cols_share:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

analysis_type = st.radio("🔍 분석 선택", ["산업별 분석", "연도별 총매출액 추이", "연도별 비중 추이"])
selected_stage = st.selectbox("📦 제품화 단계 선택", df["단계별"].unique())
filtered_df = df[df["단계별"] == selected_stage]
industries = filtered_df["산업별"].unique()

if analysis_type == "산업별 분석":
    st.subheader("📊 산업별 총매출액")
    selected_year = st.selectbox("연도 선택", year_list)
    col = f"{selected_year}.3"
    if col in filtered_df.columns:
        plot_df = filtered_df[["산업별", col]].dropna()
        plot_df.columns = ["산업별", "총매출액"]
        fig = px.bar(plot_df, x="산업별", y="총매출액", text_auto=True,
                     title=f"{selected_year}년 산업별 총매출액")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(f"{selected_year} 총매출액 컬럼이 없습니다.")

elif analysis_type == "연도별 총매출액 추이":
    st.subheader("📈 연도별 총매출액 추이")
    selected_industry = st.selectbox("산업 선택", industries)
    plot_df = filtered_df[filtered_df["산업별"] == selected_industry]
    safe_cols = [c for c in cols_total_revenue if c in plot_df.columns]
    if safe_cols and not plot_df.empty:
        ydata = plot_df[safe_cols].copy()
        ydata.columns = [y.split(".")[0] for y in safe_cols]
        ydata = ydata.T.reset_index()
        ydata.columns = ["연도", "총매출액"]
        fig = px.line(ydata, x="연도", y="총매출액", markers=True,
                      title=f"{selected_industry} 산업의 연도별 총매출액")
        st.plotly_chart(fig, use_container_width=True)

elif analysis_type == "연도별 비중 추이":
    st.subheader("📈 연도별 비중(%) 추이")
    selected_industry = st.selectbox("산업 선택", industries)
    plot_df = filtered_df[filtered_df["산업별"] == selected_industry]
    safe_cols = [c for c in cols_share if c in plot_df.columns]
    if safe_cols and not plot_df.empty:
        ydata = plot_df[safe_cols].copy()
        ydata.columns = [y.split(".")[0] for y in safe_cols]
        ydata = ydata.T.reset_index()
        ydata.columns = ["연도", "비중"]
        fig = px.line(ydata, x="연도", y="비중", markers=True,
                      title=f"{selected_industry} 산업의 연도별 비중(%)")
        st.plotly_chart(fig, use_container_width=True)

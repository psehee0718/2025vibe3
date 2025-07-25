import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="나노융합제품 비중 분석", layout="wide")
st.title("📊 나노융합제품 산업별 / 연도별 비중 분석")

# CSV 파일 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("나노융합제품의_제품화단계_20250725133453.csv", encoding="cp949")
    df.columns = df.iloc[0]             # 첫 행을 컬럼으로 지정
    df = df[1:].reset_index(drop=True)  # 첫 행 제외하고 데이터 재정렬
    df.columns = df.columns.str.strip() # 공백 제거

    # 중복된 비중 컬럼명 자동 이름 변경 (2014~2023)
    base_cols = ["단계별", "산업별"]
    year_list = [str(y) for y in range(2014, 2024)]
    df.columns = base_cols + [f"{y} 비중 (%)" for y in year_list]
    
    # 숫자형으로 변환
    for y in year_list:
        col = f"{y} 비중 (%)"
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df, year_list

df, year_list = load_data()

# 사용자 분석 유형 선택
analysis_type = st.radio("🔍 분석 유형 선택", ["산업별 분석", "연도별 비중 추이"])

# 제품화 단계 선택
selected_stage = st.selectbox("📦 제품화 단계 선택", df["단계별"].unique())
filtered_df = df[df["단계별"] == selected_stage]
industries = filtered_df["산업별"].unique()

# ✅ 산업별 분석 (특정 연도의 산업별 비중 비교)
if analysis_type == "산업별 분석":
    selected_year = st.selectbox("📅 분석할 연도 선택", year_list)
    col = f"{selected_year} 비중 (%)"
    
    if col in filtered_df.columns:
        plot_df = filtered_df[["산업별", col]].dropna()
        plot_df.columns = ["산업별", "비중"]
        fig = px.bar(plot_df, x="산업별", y="비중", text_auto=True,
                     title=f"{selected_year}년 산업별 비중(%)")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error(f"{selected_year}년 비중 컬럼이 존재하지 않습니다.")

# ✅ 연도별 비중 추이 (특정 산업의 비중 변화 시각화)
elif analysis_type == "연도별 비중 추이":
    selected_industry = st.selectbox("🏭 분석할 산업 선택", industries)
    plot_df = filtered_df[filtered_df["산업별"] == selected_industry]

    y_cols = [f"{y} 비중 (%)" for y in year_list if f"{y} 비중 (%)" in plot_df.columns]

    if y_cols:
        ydata = plot_df[y_cols].copy()
        ydata.columns = year_list[:len(y_cols)]
        ydata = ydata.T.reset_index()
        ydata.columns = ["연도", "비중"]
        fig = px.line(ydata, x="연도", y="비중", markers=True,
                      title=f"{selected_industry} 산업의 연도별 비중(%) 추이")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("선택한 산업의 비중 데이터가 없습니다.")

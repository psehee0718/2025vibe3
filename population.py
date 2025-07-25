import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="📊 인구 통계 시각화", layout="wide")
st.title("👥 지역·성별·연령별 인구 시각화 대시보드")

# 파일 업로드
uploaded_file = st.file_uploader("📂 CSV 파일 업로드 (합계.csv 또는 남녀구분.csv)", type="csv")

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file, encoding="cp949")
    except:
        st.error("❌ CSV 파일을 CP949 인코딩으로 읽을 수 없습니다.")
        st.stop()

    # ------------------------- 성별 선택 -------------------------
    # 열 이름에 따라 성별 컬럼 추론
    all_columns = df.columns.tolist()
    if any("_남_" in col for col in all_columns):
        gender_mode = st.radio("성별 선택", ["전체 (합계)", "남", "여"], horizontal=True)
    else:
        gender_mode = "전체 (합계)"  # 남녀구분 데이터가 없을 경우 기본

    # ------------------------- 연령 컬럼 필터 -------------------------
    if gender_mode == "남":
        age_columns = [col for col in df.columns if "세" in col and "_남_" in col]
    elif gender_mode == "여":
        age_columns = [col for col in df.columns if "세" in col and "_여_" in col]
    else:
        age_columns = [col for col in df.columns if "세" in col and "계" in col]

    if not age_columns:
        st.warning("⚠️ 연령대 관련 컬럼을 찾을 수 없습니다.")
        st.stop()

    # 숫자형 처리
    df_filtered = df[["행정구역"] + age_columns].copy()
    for col in age_columns:
        df_filtered[col] = df_filtered[col].astype(str).str.replace(",", "").astype(int)

    # ------------------------- 지역 선택 -------------------------
    all_regions = df_filtered["행정구역"].unique().tolist()
    selected_regions = st.multiselect("📍 지역 선택 (다중 선택 가능)", options=all_regions, default=all_regions[:1])

    df_region = df_filtered[df_filtered["행정구역"].isin(selected_regions)]

    if df_region.empty:
        st.warning("선택한 지역의 데이터가 없습니다.")
        st.stop()

    # ------------------------- 연령 필터 -------------------------
    df_long = df_region.melt(id_vars="행정구역", var_name="연령", value_name="인구수")
    df_long["연령"] = df_long["연령"].str.extract(r"(\d+세)").fillna("100세 이상")
    df_long["연령순"] = df_long["연령"].str.replace("세", "").replace("100 이상", "100").astype(int)

    age_range = st.slider("🎚️ 연령 범위 선택", 0, 100, (0, 100))
    df_long = df_long[(df_long["연령순"] >= age_range[0]) & (df_long["연령순"] <= age_range[1])]

    # ------------------------- 그래프 -------------------------
    chart_type = st.selectbox("📊 차트 종류 선택", ["막대 그래프", "꺾은선 그래프"])

    if chart_type == "막대 그래프":
        fig = px.bar(
            df_long,
            x="연령",
            y="인구수",
            color="행정구역",
            barmode="group",
            title="📊 지역별 연령대 인구 비교",
        )
    else:
        fig = px.line(
            df_long,
            x="연령",
            y="인구수",
            color="행정구역",
            markers=True,
            title="📈 지역별 연령대 인구 추세",
        )

    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("CSV 파일을 업로드하면 시각화를 시작할 수 있어요.")

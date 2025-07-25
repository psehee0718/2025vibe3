import streamlit as st
import pandas as pd

try:
    import plotly.express as px
except ModuleNotFoundError:
    st.error("❌ Plotly가 설치되어 있지 않습니다. 아래 명령어로 설치하세요:\n\n`pip install plotly`")
    st.stop()

st.set_page_config(page_title="지역별 인구 시각화", layout="wide")

st.title("📍 지역별 연령대 인구 시각화")
st.markdown("업로드한 CSV 파일에서 **특정 지역**을 선택해 연령별 인구 분포를 시각화합니다.")

# CSV 업로드
uploaded_file = st.file_uploader("📂 CSV 파일 업로드 (예: 합계.csv)", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file, encoding="cp949")
    except:
        st.error("❌ CSV 파일을 CP949 인코딩으로 불러올 수 없습니다.")
        st.stop()

    # 연령 컬럼 추출
    age_columns = [col for col in df.columns if "세" in col and "계" in col]
    if not age_columns:
        st.error("⚠️ 연령대가 포함된 '계_세' 형식의 컬럼이 없습니다.")
        st.stop()

    # 숫자화
    df_age = df[["행정구역"] + age_columns].copy()
    for col in age_columns:
        df_age[col] = df_age[col].astype(str).str.replace(",", "").astype(int)

    # 선택 가능한 지역 리스트
    region_options = df_age["행정구역"].unique().tolist()
    region = st.selectbox("🏙️ 시각화할 지역 선택", region_options)

    # 선택된 지역의 데이터만 추출
    region_df = df_age[df_age["행정구역"] == region]

    if region_df.empty:
        st.warning("선택한 지역의 데이터가 없습니다.")
    else:
        # Long 형태로 변환
        df_long = region_df.melt(id_vars="행정구역", var_name="연령", value_name="인구수")
        df_long["연령"] = df_long["연령"].str.extract(r"(\d+세)").fillna("100세 이상")

        # 시각화
        fig = px.bar(
            df_long,
            x="연령",
            y="인구수",
            title=f"📊 {region}의 연령별 인구 분포",
            labels={"연령": "연령대", "인구수": "인구 수"},
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("왼쪽에 CSV 파일을 업로드하세요.")

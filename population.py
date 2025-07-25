import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="연령별 인구 시각화", layout="wide")

st.title("👥 연령별 인구 분포 시각화")
st.markdown("CSV 데이터를 기반으로 연령별 인구를 시각화합니다.")

# 파일 업로드
uploaded_file = st.file_uploader("📂 CSV 파일 업로드 (예: 합계.csv)", type=["csv"])
if uploaded_file:
    try:
        # CSV 읽기 (CP949 인코딩)
        df = pd.read_csv(uploaded_file, encoding="cp949")
        st.success("✅ 파일이 성공적으로 업로드되었습니다.")

        # 상위 행정구역만 필터링 (예: "서울특별시 " 만 추출)
        df_filtered = df[df["행정구역"].str.contains(r"^\s*서울특별시\s")].copy()

        # 연령별 컬럼만 선택
        age_columns = [col for col in df.columns if "세" in col and "계" in col]
        df_age = df_filtered[["행정구역"] + age_columns].copy()

        # 문자열 처리 및 숫자형 변환
        for col in age_columns:
            df_age[col] = df_age[col].astype(str).str.replace(",", "").astype(int)

        # 세로(long) 형태로 변환
        df_melted = df_age.melt(id_vars="행정구역", var_name="연령", value_name="인구수")
        df_melted["연령"] = df_melted["연령"].str.extract(r"(\d+세)").fillna("100세 이상")

        # 그래프 생성
        fig = px.line(
            df_melted,
            x="연령",
            y="인구수",
            color="행정구역",
            title="서울특별시 연령별 인구 분포",
            markers=True
        )
        fig.update_layout(xaxis_tickangle=-45)

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"❌ 오류 발생: {e}")
else:
    st.info("좌측 사이드바에서 CSV 파일을 업로드하세요.")


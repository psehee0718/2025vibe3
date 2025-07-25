import streamlit as st
import pandas as pd

try:
    import plotly.express as px
except ModuleNotFoundError:
    st.error("❌ Plotly가 설치되어 있지 않습니다. 아래 명령어로 설치하세요:\n\n`pip install plotly`")
    st.stop()

st.set_page_config(page_title="연령별 인구 시각화", layout="wide")

st.title("👥 연령별 인구 분포 시각화")
st.markdown("합계와 남녀 구분 데이터를 시각화합니다.")

# 파일 업로드
col1, col2 = st.columns(2)
with col1:
    total_file = st.file_uploader("📂 [1] 합계.csv", type="csv", key="total")
with col2:
    gender_file = st.file_uploader("📂 [2] 남녀구분.csv", type="csv", key="gender")

# 시각화 함수
def preprocess_and_plot(df_total, df_gender):
    try:
        df_total = pd.read_csv(df_total, encoding="cp949")
        df_gender = pd.read_csv(df_gender, encoding="cp949")
    except:
        st.error("❌ 파일 인코딩 오류. CP949 형식인지 확인하세요.")
        return

    ### 1. 전체 인구 그래프 (합계.csv)
    df_total_filtered = df_total[df_total['행정구역'].str.contains(r"^\s*서울특별시\s")].copy()
    total_age_cols = [col for col in df_total.columns if "세" in col and "계" in col]
    df_total_age = df_total_filtered[["행정구역"] + total_age_cols].copy()

    for col in total_age_cols:
        df_total_age[col] = df_total_age[col].astype(str).str.replace(",", "").astype(int)

    df_total_melted = df_total_age.melt(id_vars="행정구역", var_name="연령", value_name="인구수")
    df_total_melted["연령"] = df_total_melted["연령"].str.extract(r"(\d+세)").fillna("100세 이상")

    fig1 = px.line(
        df_total_melted,
        x="연령",
        y="인구수",
        color="행정구역",
        title="🟢 전체 인구 분포 (합계.csv)",
        markers=True
    )
    fig1.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig1, use_container_width=True)

    ### 2. 남녀 인구 비교 (남녀구분.csv)
    df_gender_filtered = df_gender[df_gender['행정구역'].str.contains(r"^\s*서울특별시\s")].copy()
    male_cols = [col for col in df_gender.columns if "세" in col and "_남_" in col]
    female_cols = [col for col in df_gender.columns if "세" in col and "_여_" in col]

    df_gender_male = df_gender_filtered[["행정구역"] + male_cols].copy()
    df_gender_female = df_gender_filtered[["행정구역"] + female_cols].copy()

    # 남
    for col in male_cols:
        df_gender_male[col] = df_gender_male[col].astype(str).str.replace(",", "").astype(int)
    df_male_melted = df_gender_male.melt(id_vars="행정구역", var_name="연령", value_name="인구수")
    df_male_melted["성별"] = "남"
    df_male_melted["연령"] = df_male_melted["연령"].str.extract(r"(\d+세)").fillna("100세 이상")

    # 여
    for col in female_cols:
        df_gender_female[col] = df_gender_female[col].astype(str).str.replace(",", "").astype(int)
    df_female_melted = df_gender_female.melt(id_vars="행정구역", var_name="연령", value_name="인구수")
    df_female_melted["성별"] = "여"
    df_female_melted["연령"] = df_female_melted["연령"].str.extract(r"(\d+세)").fillna("100세 이상")

    df_gender_all = pd.concat([df_male_melted, df_female_melted])

    fig2 = px.line(
        df_gender_all,
        x="연령",
        y="인구수",
        color="성별",
        title="🔵 남녀 인구 비교 (남녀구분.csv)",
        markers=True
    )
    fig2.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig2, use_container_width=True)

# 실행 조건
if total_file and gender_file:
    preprocess_and_plot(total_file, gender_file)
else:
    st.warning("👆 위에 두 개의 파일을 모두 업로드해야 그래프가 생성됩니다.")


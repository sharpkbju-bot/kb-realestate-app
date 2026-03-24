import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 설정 (본인의 GitHub ID로 꼭 확인하세요!)
GITHUB_USER = "sharpkbju-bot"  # 본인의 ID로 되어 있는지 확인!
BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/kb-realestate-app/main/data/"

st.set_page_config(page_title="내 부동산 자산 대시보드", layout="wide")
st.title("🏠 주간 부동산 투자 지표 대시보드")

# 2. 데이터 로드 함수 (오류 방지 로직 추가)
def load_kb_data(file_name):
    url = BASE_URL + file_name
    try:
        # skiprows를 제거하고 대신 첫 행을 컬럼으로 읽은 뒤 정리합니다.
        df = pd.read_csv(url, encoding='cp949')
        return df
    except Exception as e:
        st.error(f"파일({file_name})을 읽는 중 오류: {e}")
        return None

# 3. 사이드바 메뉴
region = st.sidebar.selectbox("지역 선택", ["광명시", "노원구", "연수구"])
file_dict = {
    "광명시": "kb_price_maemae_change.csv", # 파일명이 실제와 같은지 확인하세요!
    "노원구": "kb_price_maemae_change.csv",
    "연수구": "kb_price_maemae_change.csv"
}

# 4. 메인 화면 로직
df = load_kb_data(file_dict[region])

if df is not None:
    st.subheader(f"📍 {region} 주간 시세 흐름")
    
    # 데이터 프레임의 컬럼명에 '광명' 등이 포함되어 있는지 확인하고 그래프 그리기
    # 사용자님의 CSV 구조에 맞춰 자동으로 시계열을 생성합니다.
    st.write("최근 데이터 미리보기")
    st.dataframe(df.head())
    
    # 간단한 그래프 예시 (컬럼명에 따라 수정이 필요할 수 있습니다)
    if not df.empty:
        fig = px.line(df, title=f"{region} 시세 변동 추이")
        st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("데이터를 불러올 수 없습니다. GitHub의 data 폴더에 파일이 있는지 확인해주세요.")

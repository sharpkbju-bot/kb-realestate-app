import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 설정 (본인의 GitHub ID로 수정 필수!)
GITHUB_USER = "sharpkbju-bot" 
BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/kb-realestate-app/main/data/"

st.set_page_config(page_title="내 부동산 자산 대시보드", layout="wide")
st.title("🏠 주간 부동산 투자 지표 대시보드")

# 2. 데이터 로드 및 정제 함수
def load_kb_data(file_name):
    url = BASE_URL + file_name
    try:
        # 데이터 읽기 (인코딩 설정)
        df = pd.read_csv(url, encoding='cp949')
        
        # 데이터 정제: 숫자가 아닌 값이 섞인 열을 제외하거나 숫자로 강제 변환
        # 첫 번째 열을 인덱스(날짜 등)로 가정하고 나머지를 숫자로 변환합니다.
        df.iloc[:, 1:] = df.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')
        
        # 결측치가 많은 행이나 열 정리
        df = df.dropna(axis=0, how='all').dropna(axis=1, how='all')
        
        return df
    except Exception as e:
        st.error(f"데이터 처리 중 오류 발생: {e}")
        return None

# 3. 사이드바 메뉴
region = st.sidebar.selectbox("지역 선택", ["광명시", "노원구", "연수구"])
file_dict = {
    "광명시": "kb_price_maemae_change.csv",
    "노원구": "kb_price_maemae_change.csv",
    "연수구": "kb_price_maemae_change.csv"
}

# 4. 메인 화면 로직
df = load_kb_data(file_dict[region])

if df is not None:
    st.subheader(f"📍 {region} 주간 시세 흐름")
    
    # 데이터 미리보기
    with st.expander("데이터 원본 보기"):
        st.dataframe(df.head(10))
    
    # 그래프 그리기
    if not df.empty:
        # 첫 번째 열을 날짜(X축), 나머지를 데이터(Y축)로 지정
        date_col = df.columns[0]
        val_cols = df.columns[1:]
        
        fig = px.line(df, x=date_col, y=val_cols, 
                     title=f"{region} 시세 변동 추이",
                     labels={date_col: "날짜", "value": "증감률(%)", "variable": "지역"})
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("그래프를 표시할 데이터가 없습니다.")
else:
    st.warning("데이터를 불러올 수 없습니다. GitHub 설정을 확인해주세요.")

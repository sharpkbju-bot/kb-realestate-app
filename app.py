import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 설정 (본인의 GitHub ID 확인 필수!)
GITHUB_USER = "sharpkbju-bot" 
BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/kb-realestate-app/main/data/"

st.set_page_config(page_title="내 부동산 자산 관리 앱", layout="wide")
st.title("📊 KB 부동산 주간 지표 분석기")

# 2. 데이터 로드 및 정제 함수
@st.cache_data # 데이터를 매번 새로 받지 않고 캐시하여 속도를 높입니다.
def load_kb_data(file_name):
    url = BASE_URL + file_name
    try:
        df = pd.read_csv(url, encoding='cp949')
        # KB 특유의 상단 빈칸/제목 제거 (데이터가 2개 이상 있는 행부터)
        df = df.dropna(thresh=2) 
        # 첫 번째 열(날짜) 제외하고 모두 숫자로 강제 변환
        for col in df.columns[1:]:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        # 완전히 빈 행/열 삭제
        df = df.dropna(axis=0, how='all').dropna(axis=1, how='all')
        return df
    except Exception as e:
        st.error(f"파일({file_name}) 읽기 오류: {e}")
        return None

# 3. 사이드바: 데이터 파일 선택
st.sidebar.header("📁 데이터 설정")
file_list = [
    "kb_price_maemae_change.csv",   # 주간 매매 증감
    "kb_price_jeonse_change.csv",   # 주간 전세 증감
    "kb_price_maemae_index.csv",    # 매매 가격 지수
    "kb_price_jeonse_index.csv"     # 전세 가격 지수
    # 추가로 업로드한 파일명이 있다면 여기에 계속 적어주세요!
]
selected_file = st.sidebar.selectbox("보고 싶은 데이터 종류", file_list)

# 4. 데이터 로드 및 지역 선택 로직
df = load_kb_data(selected_file)

if df is not None and not df.empty:
    # 파일 내의 지역 목록 추출 (첫 열인 날짜 제외)
    all_regions = df.columns[1:].tolist()
    
    # 사이드바에서 지역 멀티 선택 가능하게 설정
    # 기본값으로 사용자님의 주요 자산 지역인 '광명', '노원', '연수' 등이 포함되도록 검색 시도
    default_selection = [r for r in all_regions if any(keyword in r for keyword in ["광명", "노원", "연수"])]
    
    selected_regions = st.sidebar.multiselect(
        "분석할 지역 선택 (여러 개 가능)", 
        options=all_regions,
        default=default_selection[:3] # 최대 3개까지만 기본 선택
    )

    # 5. 메인 화면: 그래프 출력
    st.subheader(f"📍 {selected_file} - 지역별 비교 분석")
    
    if selected_regions:
        date_col = df.columns[0]
        # 선택한 지역들만 필터링하여 그래프 생성
        fig = px.line(df, x=date_col, y=selected_regions, 
                     title="주간 시세 변동 추이 비교",
                     labels={date_col: "날짜", "value": "수치", "variable": "지역"})
        
        # 그래프 디자인 살짝 다듬기
        fig.update_layout(hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)
        
        # 데이터 수치 요약
        with st.expander("최신 데이터 수치 보기"):
            st.dataframe(df[[date_col] + selected_regions].tail(10))
    else:
        st.info("왼쪽 사이드바에서 분석할 지역을 선택해 주세요.")
else:
    st.warning("데이터를 불러오는 중입니다. 파일명을 다시 확인해 주세요.")

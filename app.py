import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 설정 (본인의 GitHub ID 확인 필수!)
GITHUB_USER = "sharpkbju-bot" 
BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/kb-realestate-app/main/data/"

st.set_page_config(page_title="내 부동산 자산 관리 앱", layout="wide")
st.title("📊 KB 부동산 주간 지표 분석기")

# 2. 데이터 로드 및 헤더 병합 함수
@st.cache_data
def load_kb_data(file_name):
    url = BASE_URL + file_name
    try:
        # 헤더 없이 원본 그대로 읽기
        df_raw = pd.read_csv(url, encoding='cp949', header=None)
        
        # 0행과 1행을 합쳐서 컬럼명 만들기
        h1_row = df_raw.iloc[0].fillna("").astype(str)
        h2_row = df_raw.iloc[1].fillna("").astype(str)
        
        new_cols = []
        current_h1 = ""
        for h1, h2 in zip(h1_row, h2_row):
            h1 = h1.strip()
            h2 = h2.strip()
            if h1 != "" and "Unnamed" not in h1:
                current_h1 = h1
            
            combined = f"{current_h1} {h2}".strip()
            if not combined or "Unnamed" in combined:
                combined = "날짜"
            new_cols.append(combined)
            
        # 데이터 본문 추출 (2행부터)
        df = df_raw.iloc[2:].copy()
        df.columns = new_cols
        
        # [핵심] 첫 번째 열(날짜)은 놔두고, 두 번째 열부터 숫자로 변환
        cols_to_fix = df.columns[1:]
        for col in cols_to_fix:
            # 개별 열(Series) 단위로 변환하여 에러 원천 차단
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
        # 날짜 열에 값이 없는 행 삭제
        df = df.dropna(subset=[df.columns[0]])
        
        return df
    except Exception as e:
        st.error(f"데이터 구조 분석 중 오류: {e}")
        return None

# 3. 사이드바 설정
st.sidebar.header("📁 데이터 설정")
file_list = [
    "kb_price_maemae_change.csv",
    "kb_price_jeonse_change.csv",
    "kb_price_maemae_index.csv",
    "kb_price_jeonse_index.csv"
]
selected_file = st.sidebar.selectbox("보고 싶은 데이터 종류", file_list)

# 4. 메인 실행 로직
df = load_kb_data(selected_file)

if df is not None and not df.empty:
    all_regions = df.columns[1:].tolist()
    
    # 광명, 노원, 연수 지역 자동 검색 및 기본 선택
    default_selection = [r for r in all_regions if any(k in r for k in ["광명", "노원", "연수"])]

    selected_regions = st.sidebar.multiselect(
        "분석할 지역 선택 (검색 가능)", 
        options=all_regions,
        default=default_selection[:3]
    )

    st.subheader(f"📍 {selected_file} 분석 결과")
    
    if selected_regions:
        date_col = df.columns[0]
        # 그래프 출력
        fig = px.line(df, x=date_col, y=selected_regions, 
                     title="주간 시세 변동 추이",
                     labels={date_col: "날짜", "value": "수치", "variable": "지역"})
        
        fig.update_layout(hovermode="x unified", legend_title_text="선택 지역")
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("최신 데이터 상세 보기"):
            st.dataframe(df[[date_col] + selected_regions].tail(10))
    else:
        st.info("왼쪽 사이드바에서 지역을 선택해 주세요.")
else:
    st.warning("데이터를 불러오는 중입니다. 파일명을 다시 확인해 주세요.")

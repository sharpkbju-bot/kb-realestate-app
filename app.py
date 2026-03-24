import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 설정 (본인의 GitHub ID 확인 필수!)
GITHUB_USER = "sharpkbju-bot" 
BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/kb-realestate-app/main/data/"

st.set_page_config(page_title="내 부동산 자산 관리 앱", layout="wide")
st.title("📊 KB 부동산 주간 지표 분석기")

# 2. 데이터 로드 및 헤더 병합 함수 (가장 안전한 방식)
@st.cache_data
def load_kb_data(file_name):
    url = BASE_URL + file_name
    try:
        # 일단 헤더 없이 읽어옵니다.
        df_raw = pd.read_csv(url, encoding='cp949', header=None)
        
        # 1행(시도)과 2행(시군구)을 가져와서 합칩니다.
        header_1 = df_raw.iloc[0].fillna("").astype(str)
        header_2 = df_raw.iloc[1].fillna("").astype(str)
        
        new_columns = []
        last_h1 = ""
        for h1, h2 in zip(header_1, header_2):
            # 상위 분류(시도)가 비어있으면 이전 분류를 사용 (병합된 셀 처리)
            if h1.strip() != "" and "Unnamed" not in h1:
                last_h1 = h1.strip()
            
            combined = f"{last_h1} {h2.strip()}".strip()
            if not combined or "Unnamed" in combined:
                combined = "날짜" # 첫 번째 열 처리
            new_columns.append(combined)
            
        # 실제 데이터만 남기고 컬럼명 적용
        df = df_raw.iloc[2:].copy()
        df.columns = new_columns
        
        # 첫 번째 열(날짜) 제외하고 모두 숫자로 변환
        for col in df.columns[1:]:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
        # 빈 데이터 정리
        df = df.dropna(subset=[df.columns[0]]) # 날짜 없는 행 삭제
        return df
    except Exception as e:
        st.error(f"데이터 구조 분석 중 오류: {e}")
        return None

# 3. 사이드바: 데이터 파일 선택
st.sidebar.header("📁 데이터 설정")
file_list = [
    "kb_price_maemae_change.csv",
    "kb_price_jeonse_change.csv",
    "kb_price_maemae_index.csv",
    "kb_price_jeonse_index.csv"
]
selected_file = st.sidebar.selectbox("보고 싶은 데이터 종류", file_list)

# 4. 메인 로직 실행
df = load_kb_data(selected_file)

if df is not None and not df.empty:
    all_regions = df.columns[1:].tolist()
    
    # 내 주요 자산 지역 기본 선택 (광명, 노원, 연수)
    default_selection = [r for r in all_regions if any(k in r for k in ["광명", "노원", "연수"])]

    selected_regions = st.sidebar.multiselect(
        "분석할 지역 선택 (검색 가능)", 
        options=all_regions,
        default=default_selection[:3]
    )

    st.subheader(f"📍 {selected_file} 분석 결과")
    
    if selected_regions:
        date_col = df.columns[0]
        # 그래프 생성
        fig = px.line(df, x=date_col, y=selected_regions, 
                     title="주간 시세 변동 추이",
                     labels={date_col: "날짜", "value": "수치", "variable": "지역"})
        
        fig.update_layout(hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("최신 데이터 상세 보기"):
            st.dataframe(df[[date_col] + selected_regions].tail(10))
    else:
        st.info("왼쪽 사이드바에서 지역을 선택해 주세요.")
else:
    st.warning("데이터를 불러오는 중입니다. 파일명을 다시 확인해 주세요.")

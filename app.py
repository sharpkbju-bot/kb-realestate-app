import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 설정 (본인의 GitHub ID 확인 필수!)
GITHUB_USER = "sharpkbju-bot" 
BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/kb-realestate-app/main/data/"

st.set_page_config(page_title="내 부동산 자산 관리 앱", layout="wide")
st.title("📊 KB 부동산 주간 지표 분석기")

# 2. 데이터 로드 및 정제
@st.cache_data
def load_kb_data(file_name):
    url = BASE_URL + file_name
    try:
        # 헤더 없이 로드 (가장 원시적인 형태)
        df_raw = pd.read_csv(url, encoding='cp949', header=None)
        
        # [안전장치 1] 컬럼명 직접 조립 (병합 셀 완벽 복구)
        new_cols = []
        last_h1 = ""
        for i in range(df_raw.shape[1]):
            h1 = str(df_raw.iloc[0, i]).strip()
            h2 = str(df_raw.iloc[1, i]).strip()
            
            if h1 != "" and "nan" not in h1.lower() and "unnamed" not in h1.lower():
                last_h1 = h1
            
            combined = f"{last_h1} {h2}".strip()
            if not combined or "nan" in combined.lower():
                combined = "날짜" if i == 0 else f"지역_{i}"
            new_cols.append(combined)
            
        # 데이터 본문 추출 (2행부터)
        df = df_raw.iloc[2:].copy()
        df.columns = new_cols
        
        # [안전장치 2] 숫자 변환 (DataFrame.str 에러 원천 차단)
        for col in df.columns[1:]:
            # .squeeze()를 사용해 강제로 '시리즈(Series)'로 변환합니다.
            # 그 후 모든 데이터를 문자열로 바꾸고 콤마를 제거한 뒤 숫자로 바꿉니다.
            target_series = df[col]
            if isinstance(target_series, pd.DataFrame):
                target_series = target_series.iloc[:, 0] # 중복 컬럼 발생 시 첫 번째 선택
            
            # 콤마 제거 및 숫자 변환
            clean_s = target_series.astype(str).str.replace(',', '').replace('nan', '')
            df[col] = pd.to_numeric(clean_s, errors='coerce')
        
        # 날짜 열 기준 정렬 및 빈 행 삭제
        df = df.dropna(subset=[df.columns[0]])
        return df
    except Exception as e:
        st.error(f"데이터 로드 중 오류 발생: {e}")
        return None

# 3. 사이드바 설정
file_list = [
    "kb_price_maemae_change.csv", 
    "kb_price_jeonse_change.csv", 
    "kb_price_maemae_index.csv", 
    "kb_price_jeonse_index.csv"
]
selected_file = st.sidebar.selectbox("파일 선택", file_list)

# 4. 실행
df = load_kb_data(selected_file)

if df is not None and not df.empty:
    all_regions = df.columns[1:].tolist()
    # 광명, 노원, 연수구 자동 검색 (사용자님 주요 자산 지역)
    default_sel = [r for r in all_regions if any(k in r for k in ["광명", "노원", "연수"])]
    
    selected_regions = st.sidebar.multiselect("분석할 지역 선택", options=all_regions, default=default_sel[:3])

    if selected_regions:
        # 그래프 출력
        fig = px.line(df, x=df.columns[0], y=selected_regions, 
                     title=f"{selected_file} 추이 비교",
                     labels={df.columns[0]: "날짜", "value": "수치", "variable": "지역"})
        fig.update_layout(hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)
        
        # 데이터 요약
        with st.expander("최신 데이터 보기"):
            st.dataframe(df[[df.columns[0]] + selected_regions].tail(10))
    else:
        st.info("왼쪽 사이드바에서 분석할 지역을 선택해주세요.")

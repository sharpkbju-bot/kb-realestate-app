import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 설정 (본인의 GitHub ID 확인 필수!)
GITHUB_USER = "sharpkbju-bot" 
BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/kb-realestate-app/main/data/"

st.set_page_config(page_title="내 부동산 자산 관리 앱", layout="wide")
st.title("📊 KB 부동산 주간 지표 분석기")

# 2. 데이터 로드 및 정제 (가장 안전한 방식)
@st.cache_data
def load_kb_data(file_name):
    url = BASE_URL + file_name
    try:
        # 헤더 없이 로드 (0, 1행은 이름, 2행부터 데이터)
        df_raw = pd.read_csv(url, encoding='cp949', header=None)
        
        # 1) 컬럼명 조립
        new_cols = []
        last_city = ""
        for i in range(df_raw.shape[1]):
            city = str(df_raw.iloc[0, i]).strip()
            dist = str(df_raw.iloc[1, i]).strip()
            
            # 시/도 이름이 비어있으면 이전 이름 사용 (병합 셀 처리)
            if city != "" and "nan" not in city.lower() and "unnamed" not in city.lower():
                last_city = city
            
            combined = f"{last_city} {dist}".strip()
            if not combined or "nan" in combined.lower():
                combined = "날짜" if i == 0 else f"지역_{i}"
            new_cols.append(combined)
            
        # 2) 데이터 본문만 추출 (2행부터)
        df = df_raw.iloc[2:].copy()
        df.columns = new_cols
        
        # 3) [핵심] 숫자 변환 (하나씩 확실하게)
        for col in df.columns[1:]:
            # 데이터를 먼저 시리즈(Series)로 추출한 뒤, 문자열 처리 후 숫자로 바꿉니다.
            s = df[col].astype(str).str.replace(',', '')
            df[col] = pd.to_numeric(s, errors='coerce')
        
        # 날짜 열에 값이 없는 행 삭제
        df = df.dropna(subset=[df.columns[0]])
        return df
    except Exception as e:
        st.error(f"데이터 로드 중 오류 발생: {e}")
        return None

# 3. 사이드바 설정
file_list = ["kb_price_maemae_change.csv", "kb_price_jeonse_change.csv", "kb_price_maemae_index.csv", "kb_price_jeonse_index.csv"]
selected_file = st.sidebar.selectbox("파일 선택", file_list)

# 4. 실행
df = load_kb_data(selected_file)

if df is not None and not df.empty:
    all_regions = df.columns[1:].tolist()
    # 광명, 노원, 연수구 자동 검색
    default_sel = [r for r in all_regions if any(k in r for k in ["광명", "노원", "연수"])]
    
    selected_regions = st.sidebar.multiselect("지역 선택", options=all_regions, default=default_sel[:3])

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

import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 설정
GITHUB_USER = "sharpkbju-bot" 
BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/kb-realestate-app/main/data/"

st.set_page_config(page_title="내 부동산 자산 관리 앱", layout="wide")
st.title("📊 KB 부동산 주간 지표 분석기")

# 2. 데이터 로드 및 정제 함수
@st.cache_data
def load_kb_data(file_name):
    url = BASE_URL + file_name
    try:
        df_raw = pd.read_csv(url, encoding='cp949', header=None)
        
        # 1) 컬럼명 조립
        new_cols = []
        last_h1 = ""
        for i in range(df_raw.shape[1]):
            h1 = str(df_raw.iloc[0, i]).strip()
            h2 = str(df_raw.iloc[1, i]).strip()
            if h1 != "" and "nan" not in h1.lower() and "unnamed" not in h1.lower():
                last_h1 = h1
            combined = f"{last_h1} {h2}".strip()
            if not combined or "nan" in combined.lower():
                combined = "날짜" if i == 0 else f"기타_{i}"
            new_cols.append(combined)
            
        # [핵심] 중복된 컬럼 이름 뒤에 번호 붙이기 (DuplicateError 해결)
        final_cols = []
        counts = {}
        for col in new_cols:
            if col in counts:
                counts[col] += 1
                final_cols.append(f"{col}.{counts[col]}")
            else:
                counts[col] = 0
                final_cols.append(col)
        
        df = df_raw.iloc[2:].copy()
        df.columns = final_cols
        
        # 2) 숫자 변환
        for col in df.columns[1:]:
            # 중복 체크 후 시리즈로 확실히 추출
            s = df[col]
            if isinstance(s, pd.DataFrame): # 만에 하나라도 데이터프레임이면 첫 열만 선택
                s = s.iloc[:, 0]
            df[col] = pd.to_numeric(s.astype(str).str.replace(',', '').replace('nan', ''), errors='coerce')
        
        df = df.dropna(subset=[df.columns[0]])
        return df
    except Exception as e:
        st.error(f"데이터 로드 중 오류 발생: {e}")
        return None

# 3. 사이드바 및 파일 선택
file_list = ["kb_price_maemae_change.csv", "kb_price_jeonse_change.csv", "kb_price_index_maemae.csv", "kb_price_index_jeonse.csv"]
selected_file = st.sidebar.selectbox("파일 선택", file_list)

# 4. 실행
df = load_kb_data(selected_file)

if df is not None and not df.empty:
    all_regions = df.columns[1:].tolist()
    # 광명, 노원, 연수구 자동 선택 로직
    default_sel = [r for r in all_regions if any(k in r for k in ["광명", "노원", "연수"])]
    
    selected_regions = st.sidebar.multiselect("분석할 지역 선택", options=all_regions, default=default_sel[:3])

    if selected_regions:
        # 5. 그래프 출력 (중복 없는 컬럼명 덕분에 이제 안전합니다)
        fig = px.line(df, x=df.columns[0], y=selected_regions, 
                     title=f"{selected_file} 추이 비교",
                     labels={df.columns[0]: "날짜", "value": "수치", "variable": "지역"})
        fig.update_layout(hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("최신 데이터 상세 보기"):
            st.dataframe(df[[df.columns[0]] + selected_regions].tail(10))
    else:
        st.info("왼쪽 사이드바에서 지역을 선택해주세요.")

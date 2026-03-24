import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 설정 (본인의 GitHub ID 확인 필수!)
GITHUB_USER = "sharpkbju-bot" 
BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/kb-realestate-app/main/data/"

st.set_page_config(page_title="내 부동산 자산 관리 앱", layout="wide")
st.title("📊 KB 부동산 주간 지표 분석기")

# 2. 데이터 로드 및 정제 (가장 단순화된 로직)
@st.cache_data
def load_kb_data(file_name):
    url = BASE_URL + file_name
    try:
        # 헤더 없이 로드
        df = pd.read_csv(url, encoding='cp949', header=None)
        
        # 1~2행의 이름을 합쳐서 컬럼명으로 만듦
        col_names = []
        prefix = ""
        for i in range(len(df.columns)):
            h1 = str(df.iloc[0, i]).strip()
            h2 = str(df.iloc[1, i]).strip()
            if h1 != "" and "nan" not in h1.lower() and "unnamed" not in h1.lower():
                prefix = h1
            name = f"{prefix} {h2}".strip()
            if not name or "nan" in name.lower():
                name = f"Column_{i}"
            col_names.append(name)
        
        # 데이터 본문 추출 및 컬럼명 적용
        df = df.iloc[2:].copy()
        df.columns = col_names
        
        # [핵심 수정] 첫 열(날짜)은 유지, 나머지는 하나씩 확실하게 숫자로 변환
        date_col = df.columns[0]
        for col in df.columns[1:]:
            # 이 부분이 에러를 해결하는 핵심 코드입니다.
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', ''), errors='coerce')
        
        # 날짜 데이터가 없는 행은 삭제
        df = df.dropna(subset=[date_col])
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
    # 지역 선택 (광명, 노원, 연수 키워드 포함된 지역 우선 검색)
    all_regions = df.columns[1:].tolist()
    default_sel = [r for r in all_regions if any(k in r for k in ["광명", "노원", "연수"])]
    
    selected_regions = st.sidebar.multiselect("지역 선택", options=all_regions, default=default_sel[:3])

    if selected_regions:
        # 그래프 그리기
        fig = px.line(df, x=df.columns[0], y=selected_regions, title=f"{selected_file} 추이")
        fig.update_layout(hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)
        
        # 데이터 표 출력
        st.write("### 최신 데이터 (최근 10주)")
        st.dataframe(df[[df.columns[0]] + selected_regions].tail(10))
    else:
        st.info("왼쪽에서 지역을 선택해주세요.")

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
        # 헤더가 2줄(0번, 1번행)인 경우를 대비해 2줄을 모두 읽습니다.
        df_raw = pd.read_csv(url, encoding='cp949', header=[0, 1])
        
        # 두 줄의 헤더를 하나로 합칩니다. (예: '경기도' + '광명' -> '경기도 광명')
        # Unnamed라고 표시된 상위 분류는 무시하고 합치는 로직입니다.
        new_columns = []
        for col in df_raw.columns:
            p1 = col[0] if "Unnamed" not in col[0] else ""
            p2 = col[1] if "Unnamed" not in col[1] else ""
            combined = f"{p1} {p2}".strip()
            # 만약 둘 다 이름이 없다면 원래 컬럼명 유지
            new_columns.append(combined if combined else f"Col_{df_raw.columns.get_loc(col)}")
        
        df_raw.columns = new_columns
        
        # 첫 번째 열(보통 날짜)을 제외하고 나머지를 숫자로 변환
        for col in df_raw.columns[1:]:
            df_raw[col] = pd.to_numeric(df_raw[col], errors='coerce')
            
        # 데이터가 아예 없는 행 삭제
        df_raw = df_raw.dropna(thresh=2)
        return df_raw
    except Exception as e:
        st.error(f"지역 이름 분석 중 오류: {e}")
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

# 4. 메인 로직
df = load_kb_data(selected_file)

if df is not None and not df.empty:
    all_regions = df.columns[1:].tolist()
    
    # 내 자산 지역(광명, 노원, 연수)을 기본으로 찾아서 보여주기
    default_selection = [r for r in all_regions if any(k in r for k in ["광명", "노원", "연수"])]

    selected_regions = st.sidebar.multiselect(
        "분석할 지역 선택 (검색 가능)", 
        options=all_regions,
        default=default_selection[:3]
    )

    st.subheader(f"📍 {selected_file} 분석 결과")
    
    if selected_regions:
        date_col = df.columns[0]
        fig = px.line(df, x=date_col, y=selected_regions, 
                     title="주간 시세 변동 추이",
                     labels={date_col: "날짜", "value": "수치", "variable": "지역"})
        
        fig.update_layout(hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("최신 데이터 상세 보기"):
            st.dataframe(df[[date_col] + selected_regions].tail(10))
    else:
        st.info("왼쪽 사이드바에서 지역을 선택해 주세요 (예: 광명, 노원, 연수 등 검색)")

import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 설정 및 페이지 레이아웃 (모바일 대응)
GITHUB_USER = "sharpkbju-bot" 
BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/kb-realestate-app/main/data/"

st.set_page_config(page_title="내 자산 대시보드", layout="wide")

# 모바일에서 글자가 너무 작지 않게 CSS 추가
st.markdown("""
    <style>
    .main { font-size: 1.1rem; }
    .stMultiSelect { margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏠 내 부동산 지표 분석")

# 2. 데이터 로드 및 정제 (자동 인코딩 및 중복 제거)
@st.cache_data
def load_kb_data(file_name):
    url = BASE_URL + file_name
    for enc in ['utf-8', 'cp949', 'euc-kr']:
        try:
            df_raw = pd.read_csv(url, encoding=enc, header=None)
            break
        except: continue
    if 'df_raw' not in locals(): return None

    # 컬럼명 조립
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

    # 중복 이름 처리
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

    # 숫자 변환
    for col in df.columns[1:]:
        s = df[col]
        if isinstance(s, pd.DataFrame): s = s.iloc[:, 0]
        df[col] = pd.to_numeric(s.astype(str).str.replace(',', '').replace('nan', ''), errors='coerce')
    
    return df.dropna(subset=[df.columns[0]])

# 3. 사이드바 (모바일에서는 접었다 폈다 가능)
st.sidebar.header("⚙️ 설정")
file_list = ["kb_price_maemae_change.csv", "kb_price_jeonse_change.csv", "kb_price_maemae_index.csv", "kb_price_jeonse_index.csv"]
selected_file = st.sidebar.selectbox("데이터 종류", file_list)

df = load_kb_data(selected_file)

if df is not None and not df.empty:
    all_regions = df.columns[1:].tolist()
    
    # 검색창과 선택창을 사이드바에 배치해 메인 화면 확보
    search_query = st.sidebar.text_input("🔍 지역명 검색 (관악, 광명 등)", "")
    matched = [r for r in all_regions if search_query and search_query in r]
    
    default_sel = matched if search_query else [r for r in all_regions if any(k in r for k in ["광명", "노원", "연수"])][:3]
    
    selected_regions = st.sidebar.multiselect("최종 분석 지역", options=all_regions, default=default_sel)

    # 4. 메인 화면 그래프 최적화
    if selected_regions:
        st.subheader(f"📍 {selected_file.split('.')[0]}")
        
        # 모바일 전용 그래프 설정
        fig = px.line(df, x=df.columns[0], y=selected_regions, 
                     render_mode="svg") # 모바일 터치 반응성 향상
        
        fig.update_layout(
            height=450, # 세로 길이를 충분히 확보
            margin=dict(l=10, r=10, t=30, b=10), # 여백 최소화
            legend=dict(orientation="h", yanchor="bottom", y=-0.5, xanchor="center", x=0.5), # 범례를 아래로
            hovermode="x unified",
            xaxis_title=None,
            yaxis_title=None
        )
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        # 데이터 표는 모바일에서 스크롤하기 편하게 넓게 표시
        with st.expander("📋 최신 데이터 수치"):
            st.dataframe(df[[df.columns[0]] + selected_regions].tail(5), use_container_width=True)
    else:
        st.info("왼쪽 상단의 '>' 아이콘을 눌러 지역을 검색해 주세요.")

import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 설정
st.set_page_config(page_title="내 부동산 자산 관리", layout="wide")

# 2. 데이터 로드 함수 (기존 로직 유지)
@st.cache_data
def load_kb_data(file_name):
    GITHUB_USER = "sharpkbju-bot" # 본인 ID로 확인!
    url = f"https://raw.githubusercontent.com/{GITHUB_USER}/kb-realestate-app/main/data/{file_name}"
    for enc in ['utf-8', 'cp949', 'euc-kr']:
        try:
            df_raw = pd.read_csv(url, encoding=enc, header=None)
            break
        except: continue
    if 'df_raw' not in locals(): return None

    # 헤더 조립 및 중복 제거
    new_cols = []
    last_h1 = ""
    for i in range(df_raw.shape[1]):
        h1 = str(df_raw.iloc[0, i]).strip()
        h2 = str(df_raw.iloc[1, i]).strip()
        if h1 != "" and "nan" not in h1.lower() and "unnamed" not in h1.lower():
            last_h1 = h1
        name = f"{last_h1} {h2}".strip()
        if not name or "nan" in name.lower(): name = "날짜" if i == 0 else f"기타_{i}"
        new_cols.append(name)

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
    for col in df.columns[1:]:
        s = df[col]
        if isinstance(s, pd.DataFrame): s = s.iloc[:, 0]
        df[col] = pd.to_numeric(s.astype(str).str.replace(',', '').replace('nan', ''), errors='coerce')
    return df.dropna(subset=[df.columns[0]])

# 3. 사이드바 구성 (입력 폼 적용)
st.sidebar.header("🚀 분석 설정")

file_list = ["kb_price_maemae_change.csv", "kb_price_jeonse_change.csv", "kb_price_maemae_index.csv", "kb_price_jeonse_index.csv"]
selected_file = st.sidebar.selectbox("데이터 종류", file_list)

df = load_kb_data(selected_file)

if df is not None and not df.empty:
    all_regions = df.columns[1:].tolist()
    
    # [핵심] 입력 폼 시작 - 버튼을 눌러야만 실행됨
    with st.sidebar.form("search_form"):
        st.write("🔍 지역 검색")
        query = st.text_input("지역명 입력 (예: 관악, 광명)", "")
        
        # 버튼 생성
        submitted = st.form_submit_button("그래프 적용하기")
        
        if submitted or "selected_regions" not in st.session_state:
            # 검색어가 있으면 해당 지역, 없으면 기본 관심 지역(광명, 노원, 연수)
            if query:
                st.session_state.selected_regions = [r for r in all_regions if query in r][:10]
            else:
                st.session_state.selected_regions = [r for r in all_regions if any(k in r for k in ["광명", "노원", "연수"])][:3]

    # 4. 메인 화면 출력
    if "selected_regions" in st.session_state and st.session_state.selected_regions:
        target = st.session_state.selected_regions
        st.subheader(f"📍 {selected_file.split('.')[0]} 분석")
        
        fig = px.line(df, x=df.columns[0], y=target, render_mode="svg")
        fig.update_layout(
            height=480,
            margin=dict(l=5, r=5, t=30, b=5),
            legend=dict(orientation="h", y=-0.2),
            hovermode="x unified"
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        with st.expander("📋 상세 데이터 (최근 5주)"):
            st.dataframe(df[[df.columns[0]] + target].tail(5), use_container_width=True)
    else:
        st.info("왼쪽 사이드바에서 검색어를 입력하고 [그래프 적용하기] 버튼을 눌러주세요.")

import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 설정
GITHUB_USER = "sharpkbju-bot" 
BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/kb-realestate-app/main/data/"

st.set_page_config(page_title="내 부동산 자산 관리 앱", layout="wide")
st.title("📊 KB 부동산 주간 지표 분석기")

# 2. 데이터 로드 및 정제 (인코딩 자동 감지)
@st.cache_data
def load_kb_data(file_name):
    url = BASE_URL + file_name
    encodings = ['utf-8', 'cp949', 'euc-kr']
    df_raw = None
    
    for enc in encodings:
        try:
            df_raw = pd.read_csv(url, encoding=enc, header=None)
            break
        except:
            continue
            
    if df_raw is None: return None

    try:
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
        
        df = df.dropna(subset=[df.columns[0]])
        return df
    except Exception as e:
        st.error(f"데이터 정제 중 오류 발생: {e}")
        return None

# 3. 사이드바 설정
st.sidebar.header("🔍 지역 검색 및 필터")
file_list = ["kb_price_maemae_change.csv", "kb_price_jeonse_change.csv", "kb_price_maemae_index.csv", "kb_price_jeonse_index.csv"]
selected_file = st.sidebar.selectbox("데이터 종류 선택", file_list)

df = load_kb_data(selected_file)

if df is not None and not df.empty:
    all_regions = df.columns[1:].tolist()
    
    # [개선] 검색어 입력 시 자동 매칭 로직
    search_query = st.sidebar.text_input("지역명 검색 (예: 관악, 광명, 노원)", "")
    
    # 검색어에 해당하는 지역들을 찾습니다.
    matched_regions = [r for r in all_regions if search_query and search_query in r]
    
    # 기본 노출 지역 (광명, 노원, 연수) - 검색어가 없을 때만 기본값으로 작동
    if not search_query:
        default_sel = [r for r in all_regions if any(k in r for k in ["광명", "노원", "연수"])]
    else:
        default_sel = matched_regions # 검색어가 있으면 검색된 지역을 기본 선택

    # 최종 선택 상자 (검색 결과가 자동으로 채워짐)
    selected_regions = st.sidebar.multiselect(
        "최종 분석 지역 선택", 
        options=all_regions, 
        default=default_sel[:10] # 너무 많아지지 않게 상위 10개만 자동 선택
    )

    # 4. 메인 화면 출력
    st.subheader(f"📍 {selected_file} 분석 결과")
    if selected_regions:
        fig = px.line(df, x=df.columns[0], y=selected_regions, title="주간 시세 변동 추이")
        fig.update_layout(hovermode="x unified", legend_title_text="지역명")
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("📊 상세 데이터 확인"):
            st.dataframe(df[[df.columns[0]] + selected_regions].tail(10))
    else:
        st.info("검색창에 '관악' 등을 입력하거나 목록에서 지역을 선택해 주세요.")

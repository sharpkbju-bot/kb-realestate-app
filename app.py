import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components

# 1. 페이지 설정
st.set_page_config(
    page_title="Dr.J의 부동산", 
    page_icon="🏠",
    layout="centered"
)

# 2. 디자인 및 버튼 커스텀 (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;500;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Noto+Sans+KR', sans-serif; }

    /* 타이틀 설정 */
    .title-container { padding: 45px 0 25px 0; text-align: center; }
    .brand-name { color: #006400; font-size: clamp(40px, 14vw, 56px); font-weight: 900; font-family: 'Arial Black'; letter-spacing: -3px; }
    .brand-suffix { color: #FF4500; font-size: clamp(20px, 6vw, 30px); font-weight: 900; }

    /* 랭킹 카드 */
    .rank-card {
        background-color: #fffaf0; padding: 10px 15px; border-radius: 10px;
        margin-bottom: 6px; border-left: 5px solid #FF4500;
        display: flex; justify-content: space-between; align-items: center;
    }
    .rank-num { font-weight: 900; color: #FF4500; width: 25px; }
    .rank-name { font-weight: 700; flex-grow: 1; font-size: 14px; }
    .rank-val { font-weight: 900; color: #e74c3c; font-size: 14px; }

    /* 섹션 타이틀 */
    .chart-title {
        font-size: 18px; font-weight: 800; margin: 35px 0 12px 0;
        color: #C71585; border-left: 6px solid #C71585; padding-left: 14px;
    }

    /* 버튼 컬러 커스텀 */
    .stButton>button { border-radius: 8px; font-weight: bold; width: 100%; }
    /* 초기화 버튼 (연한 파랑) */
    div[data-testid="stHorizontalBlock"] div:nth-child(1) button {
        background-color: #ADD8E6 !important; color: #333 !important; border: none;
    }
    /* 종료 버튼 (연한 그린) */
    div[data-testid="stHorizontalBlock"] div:nth-child(2) button {
        background-color: #90EE90 !important; color: #333 !important; border: none;
    }

    header {visibility: hidden;}
    .static-chart { pointer-events: none !important; }
    </style>
    
    <div class="title-container">
        <span class="brand-name">Dr.J</span><span class="brand-suffix">의 부동산</span>
    </div>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        df_m = pd.read_csv('maemae.csv', encoding='cp949')
        df_j = pd.read_csv('jeonse.csv', encoding='cp949')
    except:
        df_m = pd.read_csv('maemae.csv', encoding='utf-8')
        df_j = pd.read_csv('jeonse.csv', encoding='utf-8')
    
    common_cols = list(set(df_m.columns) & set(df_j.columns))
    df_m, df_j = df_m[common_cols], df_j[common_cols]
    
    for col in [c for c in df_m.columns if c != '날짜']:
        df_m[col] = pd.to_numeric(df_m[col], errors='coerce').fillna(0)
        df_j[col] = pd.to_numeric(df_j[col], errors='coerce').fillna(0)
    
    df_m['날짜'] = df_m['날짜'].astype(str)
    return df_m, df_j

def main():
    if "exit" in st.session_state:
        st.balloons()
        st.success("앱이 종료되었습니다. 브라우저 창을 닫아주세요.")
        components.html("<script>window.close();</script>")
        st.stop()

    try:
        df_maemae, df_jeonse = load_data()
        date_list = sorted(df_maemae['날짜'].unique().tolist())

        # 초기화 로직: 세션 상태 사용
        if "selected_date" not in st.session_state:
            st.session_state.selected_date = date_list[-1]
        if "selected_region" not in st.session_state:
            st.session_state.selected_region = "지역을 선택하세요."

        col_date, col_search = st.columns([1, 1.5])
        with col_date:
            sel_date = st.selectbox("📅 날짜 선택", date_list, 
                                    index=date_list.index(st.session_state.selected_date),
                                    key="date_box")
        with col_search:
            region_list = sorted([col for col in df_maemae.columns if col != '날짜'])
            sel_region = st.selectbox("🔍 지역 검색/선택", options=["지역을 선택하세요."] + region_list,
                                      index=0 if st.session_state.selected_region == "지역을 선택하세요." 
                                      else region_list.index(st.session_state.selected_region) + 1,
                                      key="region_box")

        # 랭킹 섹션 (주간/월간)
        r_col1, r_col2 = st.columns(2)
        
        with r_col1:
            st.markdown(f'<div class="chart-title">🔥 주간 상승 TOP 10</div>', unsafe_allow_html=True)
            week_data = df_maemae[df_maemae['날짜'] == sel_date].drop(columns=['날짜']).iloc[0]
            top_w = week_data[week_data > 0].sort_values(ascending=False).head(10)
            for i, (name, val) in enumerate(top_w.items()):
                st.markdown(f'<div class="rank-card"><span class="rank-num">{i+1}</span><span class="rank-name">{name}</span><span class="rank-val">+{val:.2f}%</span></div>', unsafe_allow_html=True)

        with r_col2:
            st.markdown(f'<div class="chart-title">📅 월간 상승 TOP 10</div>', unsafe_allow_html=True)
            curr_idx = date_list.index(sel_date)
            # 월간(최근 4주 합산) 계산
            if curr_idx >= 3:
                month_data = df_maemae.iloc[curr_idx-3 : curr_idx+1].drop(columns=['날짜']).sum()
                top_m = month_data[month_data > 0].sort_values(ascending=False).head(10)
                for i, (name, val) in enumerate(top_m.items()):
                    st.markdown(f'<div class="rank-card"><span class="rank-num">{i+1}</span><span class="rank-name">{name}</span><span class="rank-val">+{val:.2f}%</span></div>', unsafe_allow_html=True)
            else:
                st.caption("데이터가 부족합니다.")

        # 상세 시황 및 그래프 (기존 로직 동일)
        if sel_region != "지역을 선택하세요.":
            st.divider()
            st.markdown(f"#### 📍 <span style='color:#DB7093;'>{sel_region}</span> 시황", unsafe_allow_html=True)
            m_val = df_maemae.loc[df_maemae['날짜'] == sel_date, sel_region].values[0]
            j_val = df_jeonse.loc[df_jeonse['날짜'] == sel_date, sel_region].values[0]
            # ... (그래프 생성 코드 중략 - 이전과 동일) ...
            fig_m = px.line(df_maemae.iloc[max(0, curr_idx-3):curr_idx+1], x='날짜', y=sel_region, markers=True)
            fig_m.update_layout(height=200, margin=dict(l=10,r=10,t=10,b=10), hovermode=False, dragmode=False)
            st.plotly_chart(fig_m, use_container_width=True, config={'staticPlot': True})

        # 버튼 영역
        st.markdown("<br>", unsafe_allow_html=True)
        btn_col1, btn_col2 = st.columns(2)
        
        with btn_col1:
            if st.button("🔄 초기화"):
                st.session_state.selected_date = date_list[-1]
                st.session_state.selected_region = "지역을 선택하세요."
                st.rerun()

        with btn_col2:
            if st.button("🚪 종료"):
                st.session_state.exit = True
                st.rerun()

    except Exception as e:
        st.error(f"오류 발생: {e}")

if __name__ == "__main__":
    main()

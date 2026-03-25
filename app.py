import streamlit as st
import pandas as pd
import plotly.express as px

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
    .rank-name { font-weight: 700; flex-grow: 1; font-size: 13px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .rank-val { font-weight: 900; color: #e74c3c; font-size: 13px; }

    /* 섹션 타이틀 */
    .chart-title {
        font-size: 18px; font-weight: 800; margin: 35px 0 12px 0;
        color: #C71585; border-left: 6px solid #C71585; padding-left: 14px;
    }

    /* 버튼 스타일 (중앙 정렬 및 컬러) */
    .stButton>button {
        border-radius: 12px; font-weight: bold; height: 45px; border: none; font-size: 16px;
    }
    /* 초기화 버튼 (연한 파랑) */
    div[data-testid="column"]:nth-child(1) button {
        background-color: #D1E9F6 !important; color: #333 !important;
    }
    /* 종료 버튼 (연한 그린) */
    div[data-testid="column"]:nth-child(2) button {
        background-color: #D1F2D1 !important; color: #333 !important;
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
    
    # 공통 지역만 추출하여 에러 방지
    common_cols = ['날짜'] + sorted(list(set(df_m.columns) & set(df_j.columns) - {'날짜'}))
    df_m, df_j = df_m[common_cols], df_j[common_cols]
    
    for col in [c for c in df_m.columns if c != '날짜']:
        df_m[col] = pd.to_numeric(df_m[col], errors='coerce').fillna(0)
        df_j[col] = pd.to_numeric(df_j[col], errors='coerce').fillna(0)
    
    df_m['날짜'] = df_m['날짜'].astype(str)
    return df_m, df_j

def main():
    # 종료 로직
    if "exit_app" in st.session_state:
        st.markdown("<h2 style='text-align: center; color: #FF4500;'>앱이 종료되었습니다.<br>브라우저 창을 닫아주세요.</h2>", unsafe_allow_html=True)
        st.stop()

    df_maemae, df_jeonse = load_data()
    date_list = sorted(df_maemae['날짜'].unique().tolist())
    region_list = sorted([col for col in df_maemae.columns if col != '날짜'])

    # 세션 상태 초기화값 설정
    if "sel_date" not in st.session_state:
        st.session_state.sel_date = date_list[-1]
    if "sel_region" not in st.session_state:
        st.session_state.sel_region = "지역을 선택하세요."

    # 상단 입력 도구
    col_date, col_search = st.columns([1, 1.5])
    with col_date:
        # 초기화 버튼과 연동하기 위해 index를 세션 상태에서 가져옴
        current_date_idx = date_list.index(st.session_state.sel_date)
        selected_date = st.selectbox("📅 날짜 선택", date_list, index=current_date_idx, key="date_key")
        st.session_state.sel_date = selected_date

    with col_search:
        current_reg_options = ["지역을 선택하세요."] + region_list
        try:
            current_reg_idx = current_reg_options.index(st.session_state.sel_region)
        except:
            current_reg_idx = 0
        selected_region = st.selectbox("🔍 지역 검색/선택", options=current_reg_options, index=current_reg_idx, key="region_key")
        st.session_state.sel_region = selected_region

    # 1. 상승 TOP 10 (주간 / 월간)
    r_col1, r_col2 = st.columns(2)
    with r_col1:
        st.markdown(f'<div class="chart-title">🔥 주간 상승 TOP 10</div>', unsafe_allow_html=True)
        week_data = df_maemae[df_maemae['날짜'] == selected_date].drop(columns=['날짜']).iloc[0]
        top_w = week_data[week_data > 0].sort_values(ascending=False).head(10)
        for i, (name, val) in enumerate(top_w.items()):
            st.markdown(f'<div class="rank-card"><span class="rank-num">{i+1}</span><span class="rank-name">{name}</span><span class="rank-val">+{val:.2f}%</span></div>', unsafe_allow_html=True)

    with r_col2:
        st.markdown(f'<div class="chart-title">📅 월간 상승 TOP 10</div>', unsafe_allow_html=True)
        curr_idx = date_list.index(selected_date)
        if curr_idx >= 3:
            # 4주치 데이터 합산
            month_sum = df_maemae.iloc[curr_idx-3 : curr_idx+1].drop(columns=['날짜']).sum()
            top_m = month_sum[month_sum > 0].sort_values(ascending=False).head(10)
            for i, (name, val) in enumerate(top_m.items()):
                st.markdown(f'<div class="rank-card"><span class="rank-num">{i+1}</span><span class="rank-name">{name}</span><span class="rank-val">+{val:.2f}%</span></div>', unsafe_allow_html=True)
        else:
            st.caption("비교 데이터 부족")

    # 2. 개별 지역 시황 및 4주 그래프
    if selected_region != "지역을 선택하세요.":
        st.markdown("<hr style='border: 0.5px solid #eee;'>", unsafe_allow_html=True)
        st.markdown(f"#### 📍 <span style='color:#DB7093; font-weight:800;'>{selected_region}</span> 시황 분석", unsafe_allow_html=True)
        
        m_val = df_maemae.loc[df_maemae['날짜'] == selected_date, selected_region].values[0]
        j_val = df_jeonse.loc[df_jeonse['날짜'] == selected_date, selected_region].values[0]

        c_met1, c_met2 = st.columns(2)
        m_color = "#e74c3c" if m_val > 0 else "#000080" if m_val < 0 else "#333"
        j_color = "#e74c3c" if j_val > 0 else "#000080" if j_val < 0 else "#333"

        with c_met1:
            st.markdown(f'<div class="metric-container" style="text-align:center; padding:15px; border:1px solid #f0f0f0; border-radius:15px;"><div style="color:#4B0082; font-weight:800; font-size:14px;">전주 대비 매매 증감</div><div style="color:{m_color}; font-size:24px; font-weight:900;">{m_val:+.2f}%</div></div>', unsafe_allow_html=True)
        with c_met2:
            st.markdown(f'<div class="metric-container" style="text-align:center; padding:15px; border:1px solid #f0f0f0; border-radius:15px;"><div style="color:#4B0082; font-weight:800; font-size:14px;">전주 대비 전세 증감</div><div style="color:{j_color}; font-size:24px; font-weight:900;">{j_val:+.2f}%</div></div>', unsafe_allow_html=True)

        # 4주간 트렌드 그래프 출력 (중요 수정 포인트)
        start_idx = max(0, curr_idx - 3)
        chart_data = df_maemae.iloc[start_idx : curr_idx + 1]
        chart_data_j = df_jeonse.iloc[start_idx : curr_idx + 1]

        st.markdown('<div class="chart-title">📈 매매 지수 트렌드 (최근 4주)</div>', unsafe_allow_html=True)
        fig_m = px.line(chart_data, x='날짜', y=selected_region, markers=True)
        fig_m.update_traces(line_color='#e74c3c', line_width=4, marker=dict(size=10, color='white', line=dict(width=2, color='#e74c3c')))
        fig_m.update_layout(height=200, margin=dict(l=10,r=10,t=10,b=10), xaxis=dict(fixedrange=True), yaxis=dict(fixedrange=True), hovermode=False)
        st.plotly_chart(fig_m, use_container_width=True, config={'staticPlot': True})

        st.markdown('<div class="chart-title">📉 전세 지수 트렌드 (최근 4주)</div>', unsafe_allow_html=True)
        fig_j = px.line(chart_data_j, x='날짜', y=selected_region, markers=True)
        fig_j.update_traces(line_color='#000080', line_width=4, marker=dict(size=10, color='white', line=dict(width=2, color='#000080')))
        fig_j.update_layout(height=200, margin=dict(l=10,r=10,t=10,b=10), xaxis=dict(fixedrange=True), yaxis=dict(fixedrange=True), hovermode=False)
        st.plotly_chart(fig_j, use_container_width=True, config={'staticPlot': True})

    # 3. 하단 버튼 영역 (중앙 나란히 배치)
    st.markdown("<br><br>", unsafe_allow_html=True)
    btn_col1, btn_col2 = st.columns(2)
    
    with btn_col1:
        if st.button("🔄 초기화"):
            st.session_state.sel_date = date_list[-1]
            st.session_state.sel_region = "지역을 선택하세요."
            st.rerun()

    with btn_col2:
        if st.button("🚪 종료"):
            st.session_state.exit_app = True
            st.rerun()

if __name__ == "__main__":
    main()

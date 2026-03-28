import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components
import base64
import os

# 1. 페이지 설정
st.set_page_config(
    page_title="Dr.J의 부동산", 
    page_icon="🏠",
    layout="centered"
)

# 세션 상태 초기화 및 종료 로직
if "is_exit" not in st.session_state:
    st.session_state.is_exit = False

if st.session_state.is_exit:
    st.markdown("""
        <style>
        .stApp { background-color: white !important; background-image: none !important; }
        .exit-wrapper { position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 100%; text-align: center; }
        .brand-name { color: #006400; font-size: 45px; font-weight: 900; font-family: 'Arial Black'; }
        .brand-suffix { color: #FF4500; font-size: 24px; font-weight: 900; }
        .exit-msg { color: #006400; font-weight: 900; font-size: 32px; margin-top: 20px; }
        .created-by { font-family: 'Dancing Script', cursive !important; color: #000080 !important; font-size: 30px; margin-top: 10px; }
        .asset-info { font-weight: 900; color: #CC9900 !important; font-size: 20px; margin-top: 5px; }
        header { visibility: hidden; }
        </style>
        <div class="exit-wrapper">
            <div class="title-container"><span class="brand-name">Dr.J</span><span class="brand-suffix">의 부동산</span></div>
            <div class="exit-msg">모두 부자됩시다.</div>
            <div class="created-by">Created by Ju Kyung Bae</div>
            <div class="asset-info">with 70억 자산가 이승연</div>
        </div>
    """, unsafe_allow_html=True)
    st.stop()

# 배경 이미지 주입
def set_bg_from_local(image_file):
    if os.path.exists(image_file):
        with open(image_file, "rb") as f:
            encoded_string = base64.b64encode(f.read()).decode()
        st.markdown(f"""
            <style>
            .stApp {{ background-image: url("data:image/jpg;base64,{encoded_string}"); background-size: cover; background-attachment: fixed; background-position: center; }}
            </style>
        """, unsafe_allow_html=True)

set_bg_from_local('bg.jpg')

# UI 디자인 및 스타일 설정
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Noto+Sans+KR:wght@300;500;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }
    .title-container { width: 100%; padding: 30px 0 15px 0; text-align: center; }
    .brand-name { color: #006400; font-size: clamp(30px, 10vw, 45px); font-weight: 900; font-family: 'Arial Black'; letter-spacing: -2px; }
    .brand-suffix { color: #FF4500; font-size: clamp(16px, 5vw, 24px); font-weight: 900; }
    
    /* 카드 및 랭킹 스타일 */
    .summary-card { background: rgba(255, 255, 255, 0.92) !important; border-radius: 18px; padding: 20px; text-align: center; margin-bottom: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border: 1px solid #f0f0f0; }
    .rank-card { padding: 10px 15px; border-radius: 12px; margin-bottom: 8px; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 4px 10px rgba(0,0,0,0.2) !important; font-weight: 900 !important; }
    .rank-m { border-left: 7px solid #FF4500; background: rgba(255,240,240,0.95); }
    .rank-j { border-left: 7px solid #000080; background: rgba(240,240,255,0.95); }
    
    .chart-title { font-size: 19px; font-weight: 900; margin: 35px 0 15px 0; padding-left: 12px; color: #006400; border-bottom: 2px solid rgba(0,100,0,0.1); padding-bottom: 5px; }
    
    /* 탭 스타일 조정 */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { font-weight: 900 !important; color: #006400 !important; background-color: rgba(255,255,255,0.7); border-radius: 10px 10px 0 0; padding: 10px 20px; }

    div.stButton > button { width: 100% !important; height: 46px !important; border-radius: 12px !important; font-weight: 900 !important; font-size: 16px !important; color: #87CEEB !important; background: linear-gradient(135deg, rgba(60, 60, 60, 0.8), rgba(30, 30, 30, 0.9)) !important; margin-top: 20px !important; }
    header { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        df_m = pd.read_csv('maemae.csv', encoding='cp949')
        df_j = pd.read_csv('jeonse.csv', encoding='cp949')
    except:
        df_m = pd.read_csv('maemae.csv', encoding='utf-8')
        df_j = pd.read_csv('jeonse.csv', encoding='utf-8')
    common_cols = ['날짜'] + sorted(list(set(df_m.columns) & set(df_j.columns) - {'날짜'}))
    df_m, df_j = df_m[common_cols], df_j[common_cols]
    for col in [c for c in df_m.columns if c != '날짜']:
        df_m[col] = pd.to_numeric(df_m[col], errors='coerce').fillna(0)
        df_j[col] = pd.to_numeric(df_j[col], errors='coerce').fillna(0)
    return df_m, df_j

def main():
    st.markdown('<div class="title-container"><span class="brand-name">Dr.J</span><span class="brand-suffix">의 부동산</span></div>', unsafe_allow_html=True)

    df_maemae, df_jeonse = load_data()
    date_list = sorted(df_maemae['날짜'].unique().tolist())
    region_list = sorted([col for col in df_maemae.columns if col != '날짜'])

    # 메인 탭 구성
    tab1, tab2, tab3 = st.tabs(["📊 지역 분석", "🌡️ 시장 온도계", "🏆 랭킹 TOP 10"])

    # --- 탭 1: 지역 분석 (비교 분석 포함) ---
    with tab1:
        sel_date = st.selectbox("📅 기준 날짜", date_list, index=len(date_list)-1, key="date1")
        sel_regions = st.multiselect("🔍 비교할 지역을 선택하세요 (여러 개 가능)", region_list, default=[region_list[0]] if region_list else [])
        
        if sel_regions:
            curr_idx = date_list.index(sel_date)
            start_idx = max(0, curr_idx - 7) # 트렌드는 최근 8주 기준
            
            st.markdown(f'<div class="chart-title">📈 매매 증감 비교 (최근 8주)</div>', unsafe_allow_html=True)
            sub_m = df_maemae.iloc[start_idx : curr_idx + 1][['날짜'] + sel_regions]
            fig_m = px.line(sub_m, x='날짜', y=sel_regions, markers=True, color_discrete_sequence=px.colors.qualitative.Bold)
            fig_m.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
            st.plotly_chart(fig_m, use_container_width=True)

            st.markdown(f'<div class="chart-title">📉 전세 증감 비교 (최근 8주)</div>', unsafe_allow_html=True)
            sub_j = df_jeonse.iloc[start_idx : curr_idx + 1][['날짜'] + sel_regions]
            fig_j = px.line(sub_j, x='날짜', y=sel_regions, markers=True, color_discrete_sequence=px.colors.qualitative.Safe)
            fig_j.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
            st.plotly_chart(fig_j, use_container_width=True)

    # --- 탭 2: 시장 온도계 (Heatmap 스타일) ---
    with tab2:
        st.markdown('<div class="chart-title">🌡️ 지역별 시장 온도 (최근 8주 합산)</div>', unsafe_allow_html=True)
        
        # 최근 8주 합산 데이터 계산
        m_8w = df_maemae.iloc[max(0, len(date_list)-8):].drop(columns=['날짜']).sum().to_frame(name='매매합계')
        j_8w = df_jeonse.iloc[max(0, len(date_list)-8):].drop(columns=['날짜']).sum().to_frame(name='전세합계')
        heat_df = pd.concat([m_8w, j_8w], axis=1).sort_values(by='매매합계', ascending=False)
        
        # 스타일링된 표 출력
        st.dataframe(
            heat_df.style.background_gradient(cmap='RdYlBu_r', subset=['매매합계', '전세합계']),
            use_container_width=True,
            height=500
        )
        st.caption("※ 빨간색일수록 상승세가 강하고, 파란색일수록 하락세가 강함을 의미합니다.")

    # --- 탭 3: 랭킹 TOP 10 ---
    with tab3:
        sel_date_rank = st.selectbox("📅 날짜 선택", date_list, index=len(date_list)-1, key="date3")
        curr_idx = date_list.index(sel_date_rank)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'<p style="font-weight:900; color:#FF4500;">🔥 주간 매매 TOP 10</p>', unsafe_allow_html=True)
            m_w = df_maemae[df_maemae['날짜'] == sel_date_rank].drop(columns=['날짜']).iloc[0].sort_values(ascending=False).head(10)
            for i, (n, v) in enumerate(m_w.items()):
                if v > 0: st.markdown(f'<div class="rank-card rank-m"><span>{i+1}. {n}</span><span>+{v:.2f}</span></div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'<p style="font-weight:900; color:#000080;">💧 주간 전세 TOP 10</p>', unsafe_allow_html=True)
            j_w = df_jeonse[df_jeonse['날짜'] == sel_date_rank].drop(columns=['날짜']).iloc[0].sort_values(ascending=False).head(10)
            for i, (n, v) in enumerate(j_w.items()):
                if v > 0: st.markdown(f'<div class="rank-card rank-j"><span>{i+1}. {n}</span><span>+{v:.2f}</span></div>', unsafe_allow_html=True)

        st.markdown(f'<div class="chart-title" style="color:#8B4513;">📊 누적 상승 TOP 10 (최근 8주)</div>', unsafe_allow_html=True)
        m_8 = df_maemae.iloc[max(0, curr_idx-7) : curr_idx+1].drop(columns=['날짜']).sum().sort_values(ascending=False).head(10)
        for i, (n, v) in enumerate(m_8.items()):
            if v > 0: st.markdown(f'<div class="rank-card rank-m" style="background:rgba(255,235,200,0.9);"><span>{i+1}위. {n}</span><span>+{v:.2f}%</span></div>', unsafe_allow_html=True)

    # --- 공통 하단 종료 버튼 ---
    if st.button("🚪 앱 종료", key="exit_trigger", use_container_width=True):
        st.session_state.is_exit = True
        st.rerun()

if __name__ == "__main__":
    main()

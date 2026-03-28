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

# UI 디자인 및 스타일 설정 (CSS 업그레이드)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Noto+Sans+KR:wght@300;500;700;900&display=swap');
    
    /* 기본 폰트 설정 */
    html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; color: #1a1a1a; }

    /* 메인 타이틀 */
    .title-container { width: 100%; padding: 35px 0 20px 0; text-align: center; }
    .brand-name { color: #006400; font-size: clamp(35px, 11vw, 50px); font-weight: 900; font-family: 'Arial Black'; letter-spacing: -2px; text-shadow: 2px 2px 4px rgba(0,0,0,0.1); }
    .brand-suffix { color: #FF4500; font-size: clamp(18px, 6vw, 26px); font-weight: 900; }

    /* 드롭다운 및 입력 필드 글자 강화 */
    div[data-baseweb="select"] * { font-weight: 900 !important; font-size: 17px !important; color: #000000 !important; }
    label[data-testid="stWidgetLabel"] p { font-weight: 900 !important; font-size: 18px !important; color: #004d40 !important; margin-bottom: 8px; }

    /* 탭 디자인 강화 */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; border-bottom: 2px solid #006400; }
    .stTabs [data-baseweb="tab"] { 
        height: 50px; background-color: rgba(255,255,255,0.8); 
        border-radius: 12px 12px 0 0; font-weight: 900 !important; font-size: 16px !important; color: #333 !important;
        border: 1px solid transparent;
    }
    .stTabs [aria-selected="true"] { background-color: #006400 !important; color: white !important; border: 1px solid #006400 !important; }

    /* 섹션 타이틀 스타일 */
    .chart-title { 
        font-size: 21px; font-weight: 900; margin: 30px 0 15px 0; padding: 8px 15px;
        color: #ffffff; background: linear-gradient(90deg, #006400, rgba(0,100,0,0.6));
        border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }

    /* 랭킹 카드 */
    .rank-card { padding: 12px 18px; border-radius: 14px; margin-bottom: 10px; display: flex; align-items: center; justify-content: space-between; font-weight: 900 !important; font-size: 16px; border: 1px solid rgba(0,0,0,0.05); }
    .rank-m { border-left: 8px solid #FF4500; background: rgba(255,255,255,0.95); color: #8B0000; }
    .rank-j { border-left: 8px solid #000080; background: rgba(255,255,255,0.95); color: #00008b; }
    
    /* 종료 버튼 */
    div.stButton > button {
        width: 100% !important; height: 50px !important; border-radius: 15px !important;
        font-weight: 900 !important; font-size: 18px !important; color: #FFD700 !important;
        background: linear-gradient(135deg, #1a1a1a, #444) !important;
        border: 1px solid #FFD700 !important; margin-top: 30px !important;
    }
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

    tab1, tab2, tab3 = st.tabs(["📊 지역 비교 분석", "🌡️ 시장 온도계", "🏆 주간/8주 랭킹"])

    # 그래프 폰트 공통 설정
    graph_font = dict(family="Noto Sans KR", size=14, color="black", weight=900)

    # --- 탭 1: 지역 비교 분석 ---
    with tab1:
        sel_date = st.selectbox("📅 기준 날짜 선택", date_list, index=len(date_list)-1, key="tab1_date")
        sel_regions = st.multiselect("🔍 비교할 지역 선택 (복수 선택 가능)", region_list, default=[region_list[0]] if region_list else [])
        
        if sel_regions:
            curr_idx = date_list.index(sel_date)
            start_idx = max(0, curr_idx - 7)
            
            # 매매 그래프
            st.markdown(f'<div class="chart-title">📈 매매 증감 추이 (최근 8주)</div>', unsafe_allow_html=True)
            sub_m = df_maemae.iloc[start_idx : curr_idx + 1][['날짜'] + sel_regions]
            fig_m = px.line(sub_m, x='날짜', y=sel_regions, markers=True)
            fig_m.update_layout(
                height=380, margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,0.5)',
                font=graph_font,
                xaxis=dict(tickfont=dict(size=12, weight=900, color='black')),
                yaxis=dict(tickfont=dict(size=12, weight=900, color='black')),
                legend=dict(font=dict(size=13, weight=900), orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_m, use_container_width=True)

            # 전세 그래프
            st.markdown(f'<div class="chart-title">📉 전세 증감 추이 (최근 8주)</div>', unsafe_allow_html=True)
            sub_j = df_jeonse.iloc[start_idx : curr_idx + 1][['날짜'] + sel_regions]
            fig_j = px.line(sub_j, x='날짜', y=sel_regions, markers=True)
            fig_j.update_layout(
                height=380, margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,0.5)',
                font=graph_font,
                xaxis=dict(tickfont=dict(size=12, weight=900, color='black')),
                yaxis=dict(tickfont=dict(size=12, weight=900, color='black')),
                legend=dict(font=dict(size=13, weight=900), orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_j, use_container_width=True)

    # --- 탭 2: 시장 온도계 ---
    with tab2:
        st.markdown('<div class="chart-title">🌡️ 전국 시장 온도계 (8주 누적합산)</div>', unsafe_allow_html=True)
        m_sum = df_maemae.iloc[max(0, len(date_list)-8):].drop(columns=['날짜']).sum()
        j_sum = df_jeonse.iloc[max(0, len(date_list)-8):].drop(columns=['날짜']).sum()
        heat_df = pd.DataFrame({'매매누적': m_sum, '전세누적': j_sum}).sort_values(by='매매누적', ascending=False)
        
        # 표 내부 폰트 강화
        st.dataframe(
            heat_df.style.background_gradient(cmap='RdYlBu_r', subset=['매매누적', '전세누적'])
            .format("{:+.2f}%"),
            use_container_width=True, height=550
        )
        st.caption("※ 빨간색: 강한 상승, 파란색: 강한 하락 (최근 8주 합계 기준)")

    # --- 탭 3: 랭킹 TOP 10 ---
    with tab3:
        sel_date_rank = st.selectbox("📅 랭킹 기준일 선택", date_list, index=len(date_list)-1, key="tab3_date")
        curr_idx_rank = date_list.index(sel_date_rank)
        
        # 1. 주간 랭킹
        st.markdown('<div class="chart-title">🔥 주간 상승 지역 TOP 10</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<p style="font-weight:900; color:#FF4500; text-align:center; font-size:18px;">[매매]</p>', unsafe_allow_html=True)
            m_w = df_maemae[df_maemae['날짜'] == sel_date_rank].drop(columns=['날짜']).iloc[0].sort_values(ascending=False).head(10)
            for i, (n, v) in enumerate(m_w.items()):
                if v > 0: st.markdown(f'<div class="rank-card rank-m"><span>{i+1}. {n}</span><span>+{v:.2f}</span></div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<p style="font-weight:900; color:#000080; text-align:center; font-size:18px;">[전세]</p>', unsafe_allow_html=True)
            j_w = df_jeonse[df_jeonse['날짜'] == sel_date_rank].drop(columns=['날짜']).iloc[0].sort_values(ascending=False).head(10)
            for i, (n, v) in enumerate(j_w.items()):
                if v > 0: st.markdown(f'<div class="rank-card rank-j"><span>{i+1}. {n}</span><span>+{v:.2f}</span></div>', unsafe_allow_html=True)

        # 2. 8주 누적 랭킹
        st.markdown('<div class="chart-title">📊 8주 누적 상승 TOP 10</div>', unsafe_allow_html=True)
        c3, c4 = st.columns(2)
        with c3:
            st.markdown('<p style="font-weight:900; color:#8B4513; text-align:center; font-size:18px;">[매매 누적]</p>', unsafe_allow_html=True)
            m_8 = df_maemae.iloc[max(0, curr_idx_rank-7) : curr_idx_rank+1].drop(columns=['날짜']).sum().sort_values(ascending=False).head(10)
            for i, (n, v) in enumerate(m_8.items()):
                if v > 0: st.markdown(f'<div class="rank-card rank-m" style="background:#fffcf5;"><span>{i+1}. {n}</span><span>+{v:.2f}%</span></div>', unsafe_allow_html=True)
        with c4:
            st.markdown('<p style="font-weight:900; color:#008080; text-align:center; font-size:18px;">[전세 누적]</p>', unsafe_allow_html=True)
            j_8 = df_jeonse.iloc[max(0, curr_idx_rank-7) : curr_idx_rank+1].drop(columns=['날짜']).sum().sort_values(ascending=False).head(10)
            for i, (n, v) in enumerate(j_8.items()):
                if v > 0: st.markdown(f'<div class="rank-card rank-j" style="background:#f5ffff;"><span>{i+1}. {n}</span><span>+{v:.2f}%</span></div>', unsafe_allow_html=True)

    # 하단 종료 버튼
    if st.button("🚪 안전하게 앱 종료하기", key="exit_trigger", use_container_width=True):
        st.session_state.is_exit = True
        st.rerun()

if __name__ == "__main__":
    main()

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

# UI 디자인 및 스타일 설정 (탭 및 위젯 가독성 대폭 강화)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Noto+Sans+KR:wght@300;500;700;900&display=swap');
    
    html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; color: #000000; }

    /* 메인 타이틀 */
    .title-container { width: 100%; padding: 30px 0 15px 0; text-align: center; }
    .brand-name { color: #006400; font-size: clamp(35px, 11vw, 50px); font-weight: 900; font-family: 'Arial Black'; letter-spacing: -2px; }
    .brand-suffix { color: #FF4500; font-size: clamp(18px, 6vw, 26px); font-weight: 900; }

    /* 상단 탭 메뉴 버튼 스타일 강화 */
    .stTabs [data-baseweb="tab-list"] { 
        display: flex !important; justify-content: space-between !important; width: 100% !important; gap: 0px !important; 
        background-color: rgba(255,255,255,0.4) !important; border-radius: 15px 15px 0 0 !important;
    }
    .stTabs [data-baseweb="tab"] { 
        flex: 1 !important; text-align: center !important; height: 75px !important; 
        border: 1px solid rgba(0,0,0,0.1) !important; background-color: rgba(255,255,255,0.8) !important;
    }
    .stTabs [data-baseweb="tab"] div p { 
        font-size: 22px !important; font-weight: 900 !important; color: #1a1a1a !important; 
    }
    .stTabs [aria-selected="true"] { background-color: #006400 !important; border: 1px solid #006400 !important; }
    .stTabs [aria-selected="true"] div p { color: #ffffff !important; }

    /* ★ 랭킹 기준일 선택 레이블 및 리스트 박스 강화 ★ */
    label[data-testid="stWidgetLabel"] p { 
        font-weight: 900 !important; 
        font-size: 22px !important; /* 레이블 크기 확대 */
        color: #000000 !important; 
        margin-bottom: 10px !important;
    }
    /* 리스트 박스 내부 텍스트 및 선택된 항목 */
    div[data-baseweb="select"] div {
        font-weight: 900 !important;
        font-size: 20px !important; /* 날짜 숫자 크기 확대 */
        color: #000000 !important;
    }
    /* 드롭다운 메뉴 아이템 텍스트 */
    div[data-baseweb="popover"] li {
        font-weight: 900 !important;
        font-size: 18px !important;
    }

    /* 섹션 타이틀 스타일 */
    .chart-title { 
        font-size: 22px; font-weight: 900; margin: 30px 0 15px 0; padding: 12px 15px;
        color: #ffffff; background: #2c3e50; border-radius: 10px; text-align: center;
    }

    /* 카드 스타일 */
    .rank-card { padding: 12px 18px; border-radius: 14px; margin-bottom: 10px; display: flex; align-items: center; justify-content: space-between; font-weight: 900 !important; font-size: 18px; box-shadow: 0 4px 12px rgba(0,0,0,0.2); }
    .m-weekly { background: linear-gradient(135deg, #FFEFBA, #FFFFFF); border-left: 10px solid #FF4500; color: #D32F2F; } 
    .j-weekly { background: linear-gradient(135deg, #E0F7FA, #FFFFFF); border-left: 10px solid #01579B; color: #01579B; } 
    .m-accum { background: linear-gradient(135deg, #FFF9C4, #FFFFFF); border-left: 10px solid #FBC02D; color: #7F6000; }  
    .j-accum { background: linear-gradient(135deg, #E8F5E9, #FFFFFF); border-left: 10px solid #2E7D32; color: #1B5E20; }  

    /* 종료 버튼 (그레이 테마) */
    div.stButton > button {
        width: 100% !important; height: 60px !important; border-radius: 15px !important;
        font-weight: 900 !important; font-size: 22px !important; color: #FFD700 !important;
        background: linear-gradient(135deg, #555555, #222222) !important;
        border: 2px solid #FFD700 !important; margin-top: 40px !important;
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

    tab1, tab2, tab3 = st.tabs(["📊 지역분석", "🌡️ 시장온도", "🏆 랭킹TOP"])

    with tab1:
        # 기준 날짜 선택 박스 디자인 강화됨
        sel_date = st.selectbox("📅 기준 날짜 선택", date_list, index=len(date_list)-1, key="tab1_date")
        sel_regions = st.multiselect("🔍 비교 지역 선택", region_list, default=[region_list[0]] if region_list else [])
        if sel_regions:
            curr_idx = date_list.index(sel_date)
            start_idx = max(0, curr_idx - 7)
            st.markdown('<div class="chart-title">📈 매매 증감 추이 (최근 8주)</div>', unsafe_allow_html=True)
            sub_m = df_maemae.iloc[start_idx : curr_idx + 1][['날짜'] + sel_regions]
            fig_m = px.line(sub_m, x='날짜', y=sel_regions, markers=True)
            fig_m.update_traces(line_width=8, marker=dict(size=14))
            fig_m.update_layout(height=400, font=dict(size=15, color="black", weight=900), legend=dict(font=dict(size=14, weight=900), orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
            st.plotly_chart(fig_m, use_container_width=True)

            st.markdown('<div class="chart-title">📉 전세 증감 추이 (최근 8주)</div>', unsafe_allow_html=True)
            sub_j = df_jeonse.iloc[start_idx : curr_idx + 1][['날짜'] + sel_regions]
            fig_j = px.line(sub_j, x='날짜', y=sel_regions, markers=True)
            fig_j.update_traces(line_width=8, marker=dict(size=14))
            fig_j.update_layout(height=400, font=dict(size=15, color="black", weight=900), legend=dict(font=dict(size=14, weight=900), orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
            st.plotly_chart(fig_j, use_container_width=True)

    with tab2:
        st.markdown('<div class="chart-title">🌡️ 시장 온도계 (8주 합산)</div>', unsafe_allow_html=True)
        m_sum = df_maemae.iloc[max(0, len(date_list)-8):].drop(columns=['날짜']).sum()
        j_sum = df_jeonse.iloc[max(0, len(date_list)-8):].drop(columns=['날짜']).sum()
        heat_df = pd.DataFrame({'매매합계': m_sum, '전세합계': j_sum}).sort_values(by='매매합계', ascending=False)
        st.dataframe(heat_df.style.background_gradient(cmap='RdYlBu_r').format("{:+.2f}%"), use_container_width=True, height=600)

    with tab3:
        # ★ 랭킹 기준일 선택 디자인 강화 ★
        sel_date_rank = st.selectbox("📅 랭킹 기준일 선택", date_list, index=len(date_list)-1, key="tab3_date")
        curr_idx_rank = date_list.index(sel_date_rank)
        
        st.markdown('<div class="chart-title" style="background:#e67e22;">🔥 주간 상승 지역 TOP 10</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<p style="font-weight:900; text-align:center; color:#D32F2F; font-size:19px;">[매매 주간]</p>', unsafe_allow_html=True)
            m_w = df_maemae[df_maemae['날짜'] == sel_date_rank].drop(columns=['날짜']).iloc[0].sort_values(ascending=False).head(10)
            for i, (n, v) in enumerate(m_w.items()):
                if v > 0: st.markdown(f'<div class="rank-card m-weekly"><span>{i+1}. {n}</span><span>+{v:.2f}</span></div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<p style="font-weight:900; text-align:center; color:#01579B; font-size:19px;">[전세 주간]</p>', unsafe_allow_html=True)
            j_w = df_jeonse[df_jeonse['날짜'] == sel_date_rank].drop(columns=['날짜']).iloc[0].sort_values(ascending=False).head(10)
            for i, (n, v) in enumerate(j_w.items()):
                if v > 0: st.markdown(f'<div class="rank-card j-weekly"><span>{i+1}. {n}</span><span>+{v:.2f}</span></div>', unsafe_allow_html=True)

        st.markdown('<div class="chart-title" style="background:#f1c40f; color:#000;">📊 8주 누적 상승 TOP 10</div>', unsafe_allow_html=True)
        c3, c4 = st.columns(2)
        with c3:
            st.markdown('<p style="font-weight:900; text-align:center; color:#7F6000; font-size:19px;">[매매 누적]</p>', unsafe_allow_html=True)
            m_8 = df_maemae.iloc[max(0, curr_idx_rank-7) : curr_idx_rank+1].drop(columns=['날짜']).sum().sort_values(ascending=False).head(10)
            for i, (n, v) in enumerate(m_8.items()):
                if v > 0: st.markdown(f'<div class="rank-card m-accum"><span>{i+1}. {n}</span><span>+{v:.2f}%</span></div>', unsafe_allow_html=True)
        with c4:
            st.markdown('<p style="font-weight:900; text-align:center; color:#1B5E20; font-size:19px;">[전세 누적]</p>', unsafe_allow_html=True)
            j_8 = df_jeonse.iloc[max(0, curr_idx_rank-7) : curr_idx_rank+1].drop(columns=['날짜']).sum().sort_values(ascending=False).head(10)
            for i, (n, v) in enumerate(j_8.items()):
                if v > 0: st.markdown(f'<div class="rank-card j-accum"><span>{i+1}. {n}</span><span>+{v:.2f}%</span></div>', unsafe_allow_html=True)

    if st.button("🚪 안전하게 앱 종료하기", key="exit_trigger", use_container_width=True):
        st.session_state.is_exit = True
        st.rerun()

if __name__ == "__main__":
    main()

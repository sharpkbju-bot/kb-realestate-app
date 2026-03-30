import streamlit as st
import pandas as pd
import plotly.express as px
import base64
import os

# [이전 설정 코드 동일]
st.set_page_config(page_title="Dr.J의 부동산", page_icon="🏠", layout="centered")

if "is_exit" not in st.session_state:
    st.session_state.is_exit = False

if st.session_state.is_exit:
    st.markdown("""
        <style>
        .stApp { background-color: white !important; }
        .exit-wrapper { position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 100%; text-align: center; }
        .exit-title { font-size: 30px !important; font-weight: 900; color: #000080; }
        .exit-wishes { font-size: 20px !important; font-weight: 700; color: #333333; }
        header { visibility: hidden; }
        </style>
        <div class="exit-wrapper">
            <h1 class="exit-title">Dr.J의 부동산</h1>
            <h2 class="exit-wishes">모두 부자됩시다.</h2>
        </div>
    """, unsafe_allow_html=True)
    st.stop()

# [스타일 및 데이터 로드 로직 동일]
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }
    .brand-name { color: #006400; font-size: 35px; font-weight: 900; }
    .brand-suffix { color: #FF4500; font-size: 20px; font-weight: 900; }
    
    /* 하이라이트 애니메이션 */
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(255, 69, 0, 0.7); }
        70% { box-shadow: 0 0 0 15px rgba(255, 69, 0, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 69, 0, 0); }
    }
    .highlight-card { animation: pulse 2s infinite; border: 3px solid #FF4500 !important; }

    .stat-card { padding: 15px; border-radius: 12px; margin: 10px 0; display: flex; flex-direction: column; align-items: center; font-weight: 900; background: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .m-card { border-left: 10px solid #FF4500; color: #D32F2F; }
    .j-card { border-left: 10px solid #01579B; color: #01579B; }
    .chart-title { font-size: 18px; font-weight: 900; color: #ffffff; background: #2c3e50; border-radius: 8px; text-align: center; padding: 10px; margin: 20px 0; }
    header { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    def read_csv_safe(file):
        try: return pd.read_csv(file, encoding='cp949')
        except: return pd.read_csv(file, encoding='utf-8')
    df_m = read_csv_safe('maemae.csv')
    df_j = read_csv_safe('jeonse.csv')
    for df in [df_m, df_j]:
        for col in df.columns:
            if col != '날짜': df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    return df_m, df_j

def main():
    st.markdown('<div style="text-align:center; padding: 20px;"><span class="brand-name">Dr.J</span><span class="brand-suffix">의 부동산</span></div>', unsafe_allow_html=True)
    df_maemae, df_jeonse = load_data()
    date_list = sorted(df_maemae['날짜'].unique().tolist())
    region_list = sorted([col for col in df_maemae.columns if col != '날짜'])
    
    tab1, tab2, tab3 = st.tabs(["📊 지역 분석", "🌡️ 시장 온도", "🏆 누적 랭킹 TOP 10"])

    with tab1:
        sel_date = st.selectbox("📅 기준 날짜 선택", date_list, index=len(date_list)-1)
        sel_regions = st.multiselect("🔍 비교 지역 선택", region_list, default=[region_list[0]])
        
        if sel_regions:
            curr_idx = date_list.index(sel_date)
            # 누적 TOP 10 리스트 추출 (스포트라이트 기준)
            m_accum_top = df_maemae.iloc[max(0, curr_idx-7) : curr_idx+1].drop(columns=['날짜']).sum().sort_values(ascending=False).head(10).index.tolist()
            j_accum_top = df_jeonse.iloc[max(0, curr_idx-7) : curr_idx+1].drop(columns=['날짜']).sum().sort_values(ascending=False).head(10).index.tolist()

            for region in sel_regions:
                m_val = df_maemae[df_maemae['날짜'] == sel_date][region].values[0]
                j_val = df_jeonse[df_jeonse['날짜'] == sel_date][region].values[0]
                
                col1, col2 = st.columns(2)
                with col1:
                    m_style = "stat-card m-card highlight-card" if region in m_accum_top else "stat-card m-card"
                    st.markdown(f'<div class="{m_style}"><div>{region} 매매</div><div style="font-size:24px;">{m_val:+.2f}%</div></div>', unsafe_allow_html=True)
                with col2:
                    j_style = "stat-card j-card highlight-card" if region in j_accum_top else "stat-card j-card"
                    st.markdown(f'<div class="{j_style}"><div>{region} 전세</div><div style="font-size:24px;">{j_val:+.2f}%</div>{"<div style=\"color:#FF4500; font-size:12px;\">🔥 누적TOP</div>" if region in j_accum_top else ""}</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="chart-title">🌡️ 시장 온도계 (8주 합산)</div>', unsafe_allow_html=True)
        m_sum = df_maemae.iloc[-8:].drop(columns=['날짜']).sum()
        j_sum = df_jeonse.iloc[-8:].drop(columns=['날짜']).sum()
        heat_df = pd.DataFrame({'매매합계': m_sum, '전세합계': j_sum}).sort_values(by='매매합계', ascending=False)
        
        # ★ 표 중앙 정렬 및 글자 잘림 방지 수정 ★
        st.dataframe(
            heat_df.style.background_gradient(cmap='RdYlBu_r', axis=0)
            .format("{:+.2f}%")
            .set_properties(**{
                'text-align': 'center !important',
                'font-weight': '900',
                'white-space': 'nowrap' # 글자 잘림 방지
            }),
            use_container_width=True,
            height=500
        )

    # [tab3 및 종료 버튼 로직 동일]
    st.write("---")
    if st.button("🚪 안전하게 앱 종료하기", use_container_width=True):
        st.session_state.is_exit = True
        st.rerun()

if __name__ == "__main__":
    main()

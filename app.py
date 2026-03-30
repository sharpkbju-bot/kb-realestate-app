import streamlit as st
import pandas as pd
import plotly.express as px
import base64
import os

# 1. 페이지 설정
st.set_page_config(page_title="Dr.J의 부동산", page_icon="🏠", layout="centered")

# 세션 상태 초기화
if "is_exit" not in st.session_state: st.session_state.is_exit = False
if "active_tab" not in st.session_state: st.session_state.active_tab = "📊 지역 분석"
if "date_reset_key" not in st.session_state: st.session_state.date_reset_key = 0

# 종료 로직 (기존 디자인 유지)
if st.session_state.is_exit:
    st.markdown("""
        <style>
        .stApp { background-color: white !important; background-image: none !important; }
        .exit-wrapper { position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 100%; text-align: center; z-index: 1000; }
        .exit-logo-font { font-family: 'Noto Sans KR', sans-serif; font-weight: 900; line-height: 1.2; margin-bottom: 15px; }
        .exit-logo-drj { color: #006400; font-size: 50px; }
        .exit-logo-bds { color: #FF4500; font-size: 28px; }
        .exit-wishes { font-size: 20px !important; font-weight: 900; color: #333333; margin-bottom: 10px; }
        .exit-msg { font-size: 16px; color: #666; font-weight: 700; }
        header { visibility: hidden; }
        </style>
        <div class="exit-wrapper">
            <div class="exit-logo-font">
                <span class="exit-logo-drj">Dr.J</span><span class="exit-logo-bds">의 부동산</span>
            </div>
            <h2 class="exit-wishes">모두 부자됩시다.</h2>
            <p class="exit-msg">with by 70억 자산가 SY.LEE</p>
        </div>
    """, unsafe_allow_html=True)
    st.stop()

# 배경 이미지 주입
def set_bg(image_file):
    if os.path.exists(image_file):
        with open(image_file, "rb") as f:
            encoded_string = base64.b64encode(f.read()).decode()
        st.markdown(f'<style>.stApp {{ background-image: url("data:image/jpg;base64,{encoded_string}"); background-size: cover; background-attachment: fixed; background-position: center; }}</style>', unsafe_allow_html=True)
set_bg('bg.jpg')

# UI 스타일 통합 복구
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;500;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; color: #000000; }

    /* 브랜드 헤더 */
    .brand-container { text-align: center; padding: 20px; border: 3px solid #006400; border-radius: 15px; background-color: rgba(255,255,255,0.7); margin-bottom: 20px; }
    .brand-name { color: #006400; font-size: 35px; font-weight: 900; }
    .brand-suffix { color: #FF4500; font-size: 20px; font-weight: 900; }
    
    /* 커스텀 버튼 탭 스타일 복구 */
    .tab-container { display: flex; width: 100%; gap: 2px; background-color: rgba(255,255,255,0.4); border: 2px solid #2c3e50; border-radius: 12px 12px 0 0; overflow: hidden; }
    .stButton > button.tab-btn { 
        border-radius: 0px !important; border: none !important; height: 65px !important; font-weight: 900 !important; font-size: 16px !important;
        background-color: rgba(255,255,255,0.8) !important; color: #1a1a1a !important; margin: 0 !important;
    }
    .stButton > button.active-tab { background-color: #006400 !important; color: #ffffff !important; }

    /* 입력창 및 레이블 */
    label[data-testid="stWidgetLabel"] p { font-weight: 900 !important; font-size: 18px !important; color: #111111 !important; }
    div[data-baseweb="select"] > div:first-child { background-color: #f0f2f6 !important; border: 2px solid #4B0082 !important; border-radius: 10px !important; min-height: 48px !important; }
    div[data-baseweb="select"] span { color: #4B0082 !important; font-weight: 900 !important; font-size: 18px !important; }

    /* 통계 카드 */
    @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(255, 69, 0, 0.7); } 70% { box-shadow: 0 0 0 15px rgba(255, 69, 0, 0); } 100% { box-shadow: 0 0 0 0 rgba(255, 69, 0, 0); } }
    .highlight-card { animation: pulse 2s infinite !important; border: 4px solid #FF4500 !important; }
    .stat-card { padding: 15px; border-radius: 12px; margin: 10px 0; display: flex; flex-direction: column; align-items: center; font-weight: 900; font-size: 16px; background: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border: 1px solid #cccccc; }
    .m-card { border-left: 10px solid #FF4500; color: #D32F2F; }
    .j-card { border-left: 10px solid #01579B; color: #01579B; }

    /* 차트 타이틀 */
    .chart-title { font-size: 18px; font-weight: 900; color: #ffffff; background: #2c3e50; border-radius: 8px; text-align: center; padding: 10px; margin: 20px 0; border: 2px solid #FFD700; }
    
    /* 랭킹 카드 */
    .rank-card { padding: 10px 15px; border-radius: 12px; margin-bottom: 8px; display: flex; align-items: center; justify-content: space-between; font-weight: 900; border: 1.5px solid #333; font-size: 15px; }
    .m-weekly { background: linear-gradient(135deg, #FFEFBA, #FFFFFF); border-left: 8px solid #FF4500; color: #D32F2F; }
    .j-weekly { background: linear-gradient(135deg, #E0F7FA, #FFFFFF); border-left: 8px solid #01579B; color: #01579B; }
    .m-accum { background: linear-gradient(135deg, #FFF9C4, #FFFFFF); border-left: 8px solid #FBC02D; color: #7F6000; }
    .j-accum { background: linear-gradient(135deg, #E8F5E9, #FFFFFF); border-left: 8px solid #2E7D32; color: #1B5E20; }

    /* 종료 버튼 (요청 사항: 글자 BOLD 900) */
    .exit-btn-container > button { 
        width: 100% !important; height: 55px !important; border-radius: 12px !important; 
        font-weight: 900 !important; font-size: 18px !important; color: #FFD700 !important; 
        background: linear-gradient(135deg, #444444, #111111) !important; border: 3px solid #FFD700 !important; 
    }
    header { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    def read_csv_safe(file):
        try: return pd.read_csv(file, encoding='cp949')
        except UnicodeDecodeError: return pd.read_csv(file, encoding='utf-8')
    df_m = read_csv_safe('maemae.csv')
    df_j = read_csv_safe('jeonse.csv')
    for col in df_m.columns:
        if col != '날짜': 
            df_m[col] = pd.to_numeric(df_m[col], errors='coerce').fillna(0)
            df_j[col] = pd.to_numeric(df_j[col], errors='coerce').fillna(0)
    return df_m, df_j

def main():
    st.markdown('<div class="brand-container"><span class="brand-name">Dr.J</span><span class="brand-suffix">의 부동산</span></div>', unsafe_allow_html=True)
    df_maemae, df_jeonse = load_data()
    date_list = sorted(df_maemae['날짜'].unique().tolist())
    region_list = sorted([col for col in df_maemae.columns if col != '날짜'])
    
    # 탭 구현 (버튼 방식 + 디자인 복구)
    t_cols = st.columns(3)
    tabs = ["📊 지역 분석", "🌡️ 시장 온도", "🏆 누적 랭킹 TOP 10"]
    for i, t_label in enumerate(tabs):
        is_active = (st.session_state.active_tab == t_label)
        if t_cols[i].button(t_label, key=f"btn_{i}", use_container_width=True, 
                            type="secondary" if not is_active else "primary",
                            help=f"{t_label}로 이동"):
            st.session_state.active_tab = t_label
            st.session_state.date_reset_key += 1
            st.rerun()

    # 1. 지역 분석 탭
    if st.session_state.active_tab == "📊 지역 분석":
        sel_date = st.selectbox("📅 기준 날짜 선택", date_list, index=len(date_list)-1, key=f"sel_tab1_{st.session_state.date_reset_key}")
        sel_regions = st.multiselect("🔍 비교 지역 선택", region_list, default=[region_list[0]] if region_list else [])
        
        if sel_regions:
            curr_idx = date_list.index(sel_date)
            m_top = df_maemae.iloc[max(0, curr_idx-7) : curr_idx+1].drop(columns=['날짜']).sum().sort_values(ascending=False).head(10).index.tolist()
            j_top = df_jeonse.iloc[max(0, curr_idx-7) : curr_idx+1].drop(columns=['날짜']).sum().sort_values(ascending=False).head(10).index.tolist()

            for region in sel_regions:
                m_val = df_maemae[df_maemae['날짜'] == sel_date][region].values[0]
                j_val = df_jeonse[df_jeonse['날짜'] == sel_date][region].values[0]
                is_m_hot, is_j_hot = region in m_top, region in j_top
                c1, c2 = st.columns(2)
                with c1:
                    m_cls = "stat-card m-card highlight-card" if is_m_hot else "stat-card m-card"
                    st.markdown(f'<div class="{m_cls}"><div>{region} 매매 증감({sel_date})</div><div style="font-size:24px;">{m_val:+.2f}%</div>{"<div style=\'color:#FF4500; font-size:12px;\'>🔥 누적 TOP</div>" if is_m_hot else ""}</div>', unsafe_allow_html=True)
                with c2:
                    j_cls = "stat-card j-card highlight-card" if is_j_hot else "stat-card j-card"
                    st.markdown(f'<div class="{j_cls}"><div>{region} 전세 증감({sel_date})</div><div style="font-size:24px;">{j_val:+.2f}%</div>{"<div style=\'color:#01579B; font-size:12px;\'>🔥 누적 TOP</div>" if is_j_hot else ""}</div>', unsafe_allow_html=True)
            
            start_idx = max(0, curr_idx - 7)
            sub_m = df_maemae.iloc[start_idx : curr_idx + 1][['날짜'] + sel_regions]
            sub_j = df_jeonse.iloc[start_idx : curr_idx + 1][['날짜'] + sel_regions]
            
            # 그래프 컬러(첫번째 짙은 그린) & 터치방지
            c_palette = ['#006400'] + px.colors.qualitative.Plotly
            st.markdown('<div class="chart-title">📈 매매 증감 추이 (최근 8주)</div>', unsafe_allow_html=True)
            st.plotly_chart(px.line(sub_m, x='날짜', y=sel_regions, markers=True, color_discrete_sequence=c_palette).update_layout(height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'), use_container_width=True, config={'staticPlot': True})
            
            st.markdown('<div class="chart-title">📉 전세 증감 추이 (최근 8주)</div>', unsafe_allow_html=True)
            st.plotly_chart(px.line(sub_j, x='날짜', y=sel_regions, markers=True, color_discrete_sequence=c_palette).update_layout(height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'), use_container_width=True, config={'staticPlot': True})

    # 2. 시장 온도 탭
    elif st.session_state.active_tab == "🌡️ 시장 온도":
        st.markdown('<div class="chart-title">🌡️ 시장 온도계 (8주 합산)</div>', unsafe_allow_html=True)
        m_sum = df_maemae.iloc[-8:].drop(columns=['날짜']).sum()
        j_sum = df_jeonse.iloc[-8:].drop(columns=['날짜']).sum()
        heat_df = pd.DataFrame({'매매합계': m_sum, '전세합계': j_sum}).sort_values(by='매매합계', ascending=False)
        st.dataframe(heat_df.style.background_gradient(cmap='RdYlBu_r').format("{:+.2f}%"), use_container_width=True, height=500)

    # 3. 누적 랭킹 탭
    elif st.session_state.active_tab == "🏆 누적 랭킹 TOP 10":
        sel_date_rank = st.selectbox("📅 랭킹 기준일 선택", date_list, index=len(date_list)-1, key=f"sel_tab3_{st.session_state.date_reset_key}")
        curr_idx_rank = date_list.index(sel_date_rank)
        
        st.markdown('<div class="chart-title" style="background:#e67e22;">🔥 주간 상승 지역 TOP 10</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            m_w = df_maemae[df_maemae['날짜'] == sel_date_rank].drop(columns=['날짜']).iloc[0].sort_values(ascending=False).head(10)
            for i, (n, v) in enumerate(m_w.items()):
                if v > 0: st.markdown(f'<div class="rank-card m-weekly"><span>{i+1}. {n}</span><span>+{v:.2f}</span></div>', unsafe_allow_html=True)
        with c2:
            j_w = df_jeonse[df_jeonse['날짜'] == sel_date_rank].drop(columns=['날짜']).iloc[0].sort_values(ascending=False).head(10)
            for i, (n, v) in enumerate(j_w.items()):
                if v > 0: st.markdown(f'<div class="rank-card j-weekly"><span>{i+1}. {n}</span><span>+{v:.2f}</span></div>', unsafe_allow_html=True)

        st.markdown('<div class="chart-title" style="background:#f1c40f; color:#000;">📊 8주 누적 상승 TOP 10</div>', unsafe_allow_html=True)
        c3, c4 = st.columns(2)
        with c3:
            m_8 = df_maemae.iloc[max(0, curr_idx_rank-7) : curr_idx_rank+1].drop(columns=['날짜']).sum().sort_values(ascending=False).head(10)
            for i, (n, v) in enumerate(m_8.items()):
                if v > 0: st.markdown(f'<div class="rank-card m-accum"><span>{i+1}. {n}</span><span>+{v:.2f}%</span></div>', unsafe_allow_html=True)
        with c4:
            j_8 = df_jeonse.iloc[max(0, curr_idx_rank-7) : curr_idx_rank+1].drop(columns=['날짜']).sum().sort_values(ascending=False).head(10)
            for i, (n, v) in enumerate(j_8.items()):
                if v > 0: st.markdown(f'<div class="rank-card j-accum"><span>{i+1}. {n}</span><span>+{v:.2f}%</span></div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    # 종료 버튼 컨테이너 스타일 적용
    st.markdown('<div class="exit-btn-container">', unsafe_allow_html=True)
    if st.button("🚪 **안전하게 앱 종료하기**", key="exit_trigger", use_container_width=True):
        st.session_state.is_exit = True
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()

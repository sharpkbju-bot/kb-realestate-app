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

# 종료 로직
if st.session_state.is_exit:
    st.markdown("""
        <style>
        .stApp { background-color: white !important; background-image: none !important; }
        .exit-wrapper { position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 100%; text-align: center; z-index: 1000; }
        .exit-logo-font { font-family: 'Noto Sans KR', sans-serif; font-weight: 900; line-height: 1.2; margin-bottom: 15px; }
        .exit-logo-drj { color: #006400; font-size: 50px; }
        .exit-logo-bds { color: #FF4500; font-size: 28px; }
        .exit-wishes { font-size: 24px !important; font-weight: 900; color: #333333; margin-bottom: 10px; }
        header { visibility: hidden; }
        </style>
        <div class="exit-wrapper">
            <div class="exit-logo-font"><span class="exit-logo-drj">Dr.J</span><span class="exit-logo-bds">의 부동산</span></div>
            <h2 class="exit-wishes">모두 부자됩시다.</h2>
            <p style="font-weight:900; color:#666;">with by 70억 자산가 SY.LEE</p>
        </div>
    """, unsafe_allow_html=True)
    st.stop()

# 배경 이미지
def set_bg(image_file):
    if os.path.exists(image_file):
        with open(image_file, "rb") as f:
            encoded_string = base64.b64encode(f.read()).decode()
        st.markdown(f'<style>.stApp {{ background-image: url("data:image/jpg;base64,{encoded_string}"); background-size: cover; background-attachment: fixed; background-position: center; }}</style>', unsafe_allow_html=True)
set_bg('bg.jpg')

# UI 디자인 통합 스타일시트 (화면 잘림 유발 코드 완벽 제거)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;500;700;900&display=swap');
    
    * { font-family: 'Noto Sans KR', sans-serif !important; }
    p, span, div, label { font-weight: 900 !important; }

    .brand-container { text-align: center; padding: 20px; border: 3px solid #006400; border-radius: 15px; background-color: rgba(255,255,255,0.7); margin-bottom: 25px; }
    .brand-name { color: #006400; font-size: 40px; }
    .brand-suffix { color: #FF4500; font-size: 22px; }
    
    .stButton > button { 
        width: 100% !important; height: 60px !important; border-radius: 12px !important; 
        border: 2.5px solid #2c3e50 !important; font-weight: 900 !important; font-size: 16px !important;
        background-color: rgba(255,255,255,0.9) !important; color: #1a1a1a !important;
        margin-bottom: 5px !important;
    }
    .stButton > button[kind="primary"] { background-color: #006400 !important; color: #ffffff !important; border: 2.5px solid #2c3e50 !important; }

    label[data-testid="stWidgetLabel"] p { font-size: 17px !important; color: #111111 !important; }
    
    /* 드롭다운 기본 디자인 */
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:first-child { 
        border-radius: 12px !important; min-height: 50px !important; 
    }
    div[data-testid="stSelectbox"] div[data-baseweb="select"] span, 
    div[data-testid="stSelectbox"] div[data-baseweb="select"] div { 
        font-weight: 900 !important; font-size: 18px !important; 
    }

    /* 첫 번째 열(시작일) 컬러 적용 */
    div[data-testid="column"]:nth-child(1) div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:first-child {
        border: 3px solid #01579B !important; background-color: #E1F5FE !important;
    }
    div[data-testid="column"]:nth-child(1) div[data-testid="stSelectbox"] div[data-baseweb="select"] * { color: #01579B !important; }

    /* 두 번째 열(종료일) 컬러 적용 */
    div[data-testid="column"]:nth-child(2) div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:first-child {
        border: 3px solid #D32F2F !important; background-color: #FFEBEE !important;
    }
    div[data-testid="column"]:nth-child(2) div[data-testid="stSelectbox"] div[data-baseweb="select"] * { color: #D32F2F !important; }

    /* 멀티셀렉트(비교 지역 선택) 디자인 */
    div[data-testid="stMultiSelect"] div[data-baseweb="select"] > div:first-child {
        background-color: #E6E6FA !important; border: 3px solid #4B0082 !important; border-radius: 12px !important; min-height: 50px !important;
    }
    div[data-testid="stMultiSelect"] span { color: #4B0082 !important; font-size: 18px !important; }

    /* 스포트라이트 애니메이션 복구 */
    @keyframes spotlight_m { 
        0% { box-shadow: 0 0 0 0 rgba(255, 69, 0, 0.7); transform: scale(1); } 
        50% { box-shadow: 0 0 0 15px rgba(255, 69, 0, 0); transform: scale(1.02); } 
        100% { box-shadow: 0 0 0 0 rgba(255, 69, 0, 0); transform: scale(1); } 
    }
    @keyframes spotlight_j { 
        0% { box-shadow: 0 0 0 0 rgba(1, 87, 155, 0.7); transform: scale(1); } 
        50% { box-shadow: 0 0 0 15px rgba(1, 87, 155, 0); transform: scale(1.02); } 
        100% { box-shadow: 0 0 0 0 rgba(1, 87, 155, 0); transform: scale(1); } 
    }
    .highlight-m { animation: spotlight_m 2s infinite !important; border: 3px solid #FF4500 !important; border-left: 12px solid #FF4500 !important; z-index: 10; }
    .highlight-j { animation: spotlight_j 2s infinite !important; border: 3px solid #01579B !important; border-left: 12px solid #01579B !important; z-index: 10; }

    .stat-card { padding: 15px; border-radius: 12px; margin: 10px 0; display: flex; flex-direction: column; align-items: center; background: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border: 2px solid #cccccc; font-size: 15px; }
    .m-card { border-left: 12px solid #FF4500; color: #D32F2F; }
    .j-card { border-left: 12px solid #01579B; color: #01579B; }
    .stat-value { font-size: 24px !important; }

    .chart-title { font-size: 17px; font-weight: 900; color: #ffffff !important; background: #2c3e50; border-radius: 12px; text-align: center; padding: 10px; margin: 20px 0; border: 2.5px solid #FFD700; }
    
    .rank-card { padding: 10px 15px; border-radius: 12px; margin-bottom: 8px; display: flex; align-items: center; justify-content: space-between; border: 2.5px solid #333; font-size: 14px; font-weight: 900 !important; }
    .m-weekly { background: linear-gradient(135deg, #FFEFBA, #FFFFFF) !important; border-left: 10px solid #FF4500 !important; color: #D32F2F !important; }
    .j-weekly { background: linear-gradient(135deg, #E0F7FA, #FFFFFF) !important; border-left: 10px solid #01579B !important; color: #01579B !important; }
    .m-accum { background: linear-gradient(135deg, #FFF9C4, #FFFFFF) !important; border-left: 10px solid #FBC02D !important; color: #7F6000 !important; }
    .j-accum { background: linear-gradient(135deg, #E8F5E9, #FFFFFF) !important; border-left: 10px solid #2E7D32 !important; color: #1B5E20 !important; }

    .exit-btn-wrap > button { 
        width: 100% !important; height: 55px !important; border-radius: 15px !important; 
        font-weight: 900 !important; font-size: 18px !important; color: #FFFFFF !important; 
        background: linear-gradient(135deg, #A7C7E7, #749BC2) !important;
        border: 3px solid #FFFFFF !important; 
    }
    
    /* 심층분석 테이블 스타일 (가로 스크롤 추가하여 모바일 잘림 방지) */
    .table-wrapper { width: 100%; overflow-x: auto; border-radius: 10px; border: 2px solid #2c3e50; margin-top: 15px; background: rgba(255,255,255,0.85); -webkit-overflow-scrolling: touch; }
    .analysis-table { width: 100%; border-collapse: collapse; min-width: max-content; }
    .analysis-table th { background: #2c3e50; color: white; padding: 8px; font-size: 14px; text-align: center; }
    .analysis-table td { padding: 10px; border-bottom: 1px solid #ddd; font-size: 13px; text-align: center; color: #333; }
    .analysis-table tr:last-child td { border-bottom: none; }

    .stDataFrame div { font-size: 13px !important; }
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
    
    t_cols = st.columns(3)
    tabs = ["📊 지역 분석", "🌡️ 시장 온도", "🏆 누적 랭킹 TOP 10"]
    for i, t_label in enumerate(tabs):
        is_active = (st.session_state.active_tab == t_label)
        if t_cols[i].button(t_label, key=f"t_btn_fix_{i}", use_container_width=True, 
                            type="primary" if is_active else "secondary"):
            st.session_state.active_tab = t_label
            st.session_state.date_reset_key += 1
            st.rerun()

    def get_2026_start_idx(dates, current_idx):
        start = next((i for i, d in enumerate(dates) if str(d).startswith('2026')), 0)
        return min(start, current_idx)

    # 1. 지역 분석 탭
    if st.session_state.active_tab == "📊 지역 분석":
        
        c_date1, c_date2 = st.columns(2)
        with c_date1:
            start_date = st.selectbox("📅 기준 시작일", date_list, index=max(0, len(date_list)-9), key=f"st_d_{st.session_state.date_reset_key}")
        with c_date2:
            end_date = st.selectbox("📅 기준 종료일", date_list, index=len(date_list)-1, key=f"en_d_{st.session_state.date_reset_key}")
            
        sel_regions = st.multiselect("🔍 비교 지역 선택", region_list, default=[region_list[0]] if region_list else [])
        
        if sel_regions:
            s_idx, e_idx = date_list.index(start_date), date_list.index(end_date)
            
            # 날짜 역전 방지
            if s_idx > e_idx: 
                s_idx, e_idx = e_idx, s_idx
                start_date, end_date = end_date, start_date
            
            # 선택된 기간 누적 TOP 10 추출 (스포트라이트용)
            m_top = df_maemae.iloc[s_idx:e_idx+1].drop(columns=['날짜']).sum().sort_values(ascending=False).head(10).index.tolist()
            j_top = df_jeonse.iloc[s_idx:e_idx+1].drop(columns=['날짜']).sum().sort_values(ascending=False).head(10).index.tolist()

            for region in sel_regions:
                m_val = df_maemae.iloc[s_idx:e_idx+1][region].sum()
                j_val = df_jeonse.iloc[s_idx:e_idx+1][region].sum()
                is_m_hot, is_j_hot = region in m_top, region in j_top
                c1, c2 = st.columns(2)
                d_label = f"{start_date[5:]}~{end_date[5:]}"
                
                with c1:
                    m_cls = "stat-card m-card highlight-m" if is_m_hot else "stat-card m-card"
                    st.markdown(f'<div class="{m_cls}"><div>{region} 매매({d_label})</div><div class="stat-value">{m_val:+.2f}%</div>{"<div style=\'color:#FF4500; font-size:12px;\'>🔥 기간 TOP</div>" if is_m_hot else ""}</div>', unsafe_allow_html=True)
                with c2:
                    j_cls = "stat-card j-card highlight-j" if is_j_hot else "stat-card j-card"
                    st.markdown(f'<div class="{j_cls}"><div>{region} 전세({d_label})</div><div class="stat-value">{j_val:+.2f}%</div>{"<div style=\'color:#01579B; font-size:12px;\'>🔥 기간 TOP</div>" if is_j_hot else ""}</div>', unsafe_allow_html=True)
            
            c_palette = ['#006400'] + px.colors.qualitative.Plotly
            
            st.markdown(f'<div class="chart-title">📈 매매 증감 추이 ({start_date} ~ {end_date})</div>', unsafe_allow_html=True)
            st.plotly_chart(px.line(df_maemae.iloc[s_idx:e_idx+1][['날짜']+sel_regions], x='날짜', y=sel_regions, markers=True, color_discrete_sequence=c_palette).update_layout(height=320, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'), use_container_width=True, config={'staticPlot': True})
            
            # 심층 분석 테이블 추가
            st.markdown(f'<div class="chart-title" style="background:#4B0082; border-color:#E6E6FA;">🧐 {start_date[5:]} ~ {end_date[5:]} 기간 심층 분석</div>', unsafe_allow_html=True)
            
            analysis_html = "<div class='table-wrapper'><table class='analysis-table'><tr><th style='white-space:nowrap;'>지역명</th><th style='white-space:nowrap;'>구분</th><th style='white-space:nowrap;'>누적증감</th><th style='white-space:nowrap;'>최고상승(주)</th><th style='white-space:nowrap;'>최저하락(주)</th></tr>"
            
            for region in sel_regions:
                m_series = df_maemae.iloc[s_idx:e_idx+1][region]
                j_series = df_jeonse.iloc[s_idx:e_idx+1][region]
                
                m_max_date = df_maemae.iloc[s_idx:e_idx+1].loc[m_series.idxmax(), '날짜']
                m_min_date = df_maemae.iloc[s_idx:e_idx+1].loc[m_series.idxmin(), '날짜']
                j_max_date = df_jeonse.iloc[s_idx:e_idx+1].loc[j_series.idxmax(), '날짜']
                j_min_date = df_jeonse.iloc[s_idx:e_idx+1].loc[j_series.idxmin(), '날짜']
                
                analysis_html += (
                    f"<tr><td rowspan='2' style='background:#f9f9f9; font-weight:900; white-space:nowrap;'>{region}</td>"
                    f"<td style='color:#D32F2F; white-space:nowrap;'>매매</td>"
                    f"<td style='font-weight:900; white-space:nowrap;'>{m_series.sum():+.2f}%</td>"
                    f"<td>{m_max_date[5:]}<br>{m_series.max():+.2f}%</td>"
                    f"<td>{m_min_date[5:]}<br>{m_series.min():+.2f}%</td></tr>"
                    f"<tr><td style='color:#01579B; white-space:nowrap;'>전세</td>"
                    f"<td style='font-weight:900; white-space:nowrap;'>{j_series.sum():+.2f}%</td>"
                    f"<td>{j_max_date[5:]}<br>{j_series.max():+.2f}%</td>"
                    f"<td>{j_min_date[5:]}<br>{j_series.min():+.2f}%</td></tr>"
                )
            analysis_html += "</table></div>"
            st.markdown(analysis_html, unsafe_allow_html=True)

            st.markdown(f'<div class="chart-title" style="margin-top:30px;">📉 전세 증감 추이 ({start_date} ~ {end_date})</div>', unsafe_allow_html=True)
            st.plotly_chart(px.line(df_jeonse.iloc[s_idx:e_idx+1][['날짜']+sel_regions], x='날짜', y=sel_regions, markers=True, color_discrete_sequence=c_palette).update_layout(height=320, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'), use_container_width=True, config={'staticPlot': True})

    # 2. 시장 온도 탭 (2026년 기준)
    elif st.session_state.active_tab == "🌡️ 시장 온도":
        st.markdown('<div class="chart-title">🌡️ 시장 온도계 (2026년 누적)</div>', unsafe_allow_html=True)
        df_m_2026 = df_maemae[df_maemae['날짜'].astype(str).str.startswith('2026')]
        df_j_2026 = df_jeonse[df_jeonse['날짜'].astype(str).str.startswith('2026')]
        m_sum = df_m_2026.drop(columns=['날짜']).sum()
        j_sum = df_j_2026.drop(columns=['날짜']).sum()
        heat_df = pd.DataFrame({'매매합계': m_sum, '전세합계': j_sum}).sort_values(by='매매합계', ascending=False)
        st.dataframe(heat_df.style.background_gradient(cmap='RdYlBu_r').format("{:+.2f}%"), use_container_width=True, height=450)

    # 3. 누적 랭킹 탭 (2026년 기준)
    elif st.session_state.active_tab == "🏆 누적 랭킹 TOP 10":
        sel_date_rank = st.selectbox("📅 랭킹 기준일 선택", date_list, index=len(date_list)-1, key=f"rk_d_{st.session_state.date_reset_key}")
        curr_idx_rank = date_list.index(sel_date_rank)
        start_idx_rank = get_2026_start_idx(date_list, curr_idx_rank)
        
        st.markdown('<div class="chart-title" style="background:#e67e22; border-color:#d35400;">🔥 주간 상승 지역 TOP 10</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<p style="text-align:center; color:#D32F2F; font-size:14px;">[매매 주간 상승]</p>', unsafe_allow_html=True)
            m_w = df_maemae[df_maemae['날짜'] == sel_date_rank].drop(columns=['날짜']).iloc[0].sort_values(ascending=False).head(10)
            for i, (n, v) in enumerate(m_w.items()):
                if v > 0: st.markdown(f'<div class="rank-card m-weekly"><span>{i+1}. {n}</span><span>+{v:.2f}</span></div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<p style="text-align:center; color:#01579B; font-size:14px;">[전세 주간 상승]</p>', unsafe_allow_html=True)
            j_w = df_jeonse[df_jeonse['날짜'] == sel_date_rank].drop(columns=['날짜']).iloc[0].sort_values(ascending=False).head(10)
            for i, (n, v) in enumerate(j_w.items()):
                if v > 0: st.markdown(f'<div class="rank-card j-weekly"><span>{i+1}. {n}</span><span>+{v:.2f}</span></div>', unsafe_allow_html=True)

        st.markdown('<div class="chart-title" style="background:#f1c40f; color:#000; border-color:#b7950b;">📊 2026년 누적 상승 TOP 10</div>', unsafe_allow_html=True)
        c3, c4 = st.columns(2)
        with c3:
            st.markdown('<p style="text-align:center; color:#7F6000; font-size:14px;">[매매 누적 상승률]</p>', unsafe_allow_html=True)
            m_8 = df_maemae.iloc[start_idx_rank:curr_idx_rank+1].drop(columns=['날짜']).sum().sort_values(ascending=False).head(10)
            for i, (n, v) in enumerate(m_8.items()):
                if v > 0: st.markdown(f'<div class="rank-card m-accum"><span>{i+1}. {n}</span><span>+{v:.2f}%</span></div>', unsafe_allow_html=True)
        with c4:
            st.markdown('<p style="text-align:center; color:#1B5E20; font-size:14px;">[전세 누적 상승률]</p>', unsafe_allow_html=True)
            j_8 = df_jeonse.iloc[start_idx_rank:curr_idx_rank+1].drop(columns=['날짜']).sum().sort_values(ascending=False).head(10)
            for i, (n, v) in enumerate(j_8.items()):
                if v > 0: st.markdown(f'<div class="rank-card j-accum"><span>{i+1}. {n}</span><span>+{v:.2f}%</span></div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<div class="exit-btn-wrap">', unsafe_allow_html=True)
    if st.button("🚪 **안전하게 앱 종료하기**", key="exit_v_final", use_container_width=True):
        st.session_state.is_exit = True
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()

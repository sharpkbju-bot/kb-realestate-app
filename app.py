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

# UI 디자인 통합 스타일시트
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
    div[data-baseweb="select"] > div:first-child { 
        background-color: #E6E6FA !important; border: 3px solid #4B0082 !important; border-radius: 12px !important; min-height: 50px !important; 
    }
    div[data-baseweb="select"] span, div[data-baseweb="select"] div { 
        color: #4B0082 !important; font-weight: 900 !important; font-size: 18px !important; 
    }

    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stSelectbox"]) {
        display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important; gap: 8px !important;
    }
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stSelectbox"]) > div[data-testid="column"] {
        flex: 1 1 0% !important; min-width: 0 !important;
    }

    @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(255, 69, 0, 0.7); } 70% { box-shadow: 0 0 0 15px rgba(255, 69, 0, 0); } 100% { box-shadow: 0 0 0 0 rgba(255, 69, 0, 0); } }
    .highlight-card { animation: pulse 2s infinite !important; border: 4px solid #FF4500 !important; }
    .stat-card { padding: 15px; border-radius: 12px; margin: 10px 0; display: flex; flex-direction: column; align-items: center; background: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border: 2px solid #cccccc; font-size: 17px; }
    .m-card { border-left: 12px solid #FF4500; color: #D32F2F; }
    .j-card { border-left: 12px solid #01579B; color: #01579B; }
    .stat-value { font-size: 24px !important; }

    .chart-title { font-size: 15px; font-weight: 900; color: #ffffff !important; background: #2c3e50; border-radius: 12px; text-align: center; padding: 10px; margin: 20px 0; border: 2.5px solid #FFD700; }
    
    .rank-card { padding: 10px 15px; border-radius: 12px; margin-bottom: 8px; display: flex; align-items: center; justify-content: space-between; border: 2.5px solid #333; font-size: 14px; font-weight: 900 !important; }
    .m-weekly { background: linear-gradient(135deg, #FFEFBA, #FFFFFF) !important; border-left: 10px solid #FF4500 !important; color: #D32F2F !important; }
    .j-weekly { background: linear-gradient(135deg, #E0F7FA, #FFFFFF) !important; border-left: 10px solid #01579B !important; color: #01579B !important; }
    .m-accum { background: linear-gradient(135deg, #FFF9C4, #FFFFFF) !important; border-left: 10px solid #FBC02D !important; color: #7F6000 !important; }
    .j-accum { background: linear-gradient(135deg, #E8F5E9, #FFFFFF) !important; border-left: 10px solid #2E7D32 !important; color: #1B5E20 !important; }

    .analysis-table { width: 100%; border-collapse: collapse; background: rgba(255,255,255,0.9); border-radius: 10px; overflow: hidden; margin-top: 15px; border: 2px solid #2c3e50; table-layout: fixed; }
    .analysis-table th { background: #2c3e50; color: white; padding: 6px 2px; font-size: 11px; text-align: center; white-space: nowrap; }
    .analysis-table td { padding: 8px 2px; border-bottom: 1px solid #ddd; font-size: 11px; text-align: center; color: #333; line-height: 1.3; overflow: hidden; }
    .analysis-table tr:last-child td { border-bottom: none; }
    .point-date { font-weight: 900; color: #555; display: block; margin-bottom: 2px; font-size: 10px; }
    .point-val { font-weight: 900; display: block; font-size: 11px; }
    
    .exit-btn-wrap > button { 
        width: 100% !important; height: 55px !important; border-radius: 15px !important; 
        font-weight: 900 !important; font-size: 18px !important; color: #FFFFFF !important; 
        background: linear-gradient(135deg, #A7C7E7, #749BC2) !important; border: 3px solid #FFFFFF !important; 
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
    
    t_cols = st.columns(3)
    tabs = ["📊 지역 분석", "🌡️ 시장 온도", "🏆 누적 랭킹 TOP 10"]
    for i, t_label in enumerate(tabs):
        is_active = (st.session_state.active_tab == t_label)
        if t_cols[i].button(t_label, key=f"t_btn_ana_{i}", use_container_width=True, 
                            type="primary" if is_active else "secondary"):
            st.session_state.active_tab = t_label
            st.session_state.date_reset_key += 1
            st.rerun()

    if st.session_state.active_tab == "📊 지역 분석":
        c_date1, c_date2 = st.columns(2)
        with c_date1:
            start_date = st.selectbox("📅 기준 시작일", date_list, index=max(0, len(date_list)-9), key=f"st_d_{st.session_state.date_reset_key}")
        with c_date2:
            end_date = st.selectbox("📅 기준 종료일", date_list, index=len(date_list)-1, key=f"en_d_{st.session_state.date_reset_key}")
            
        sel_regions = st.multiselect("🔍 비교 지역 선택", region_list, default=[region_list[0]] if region_list else [])
        
        if sel_regions:
            s_idx, e_idx = date_list.index(start_date), date_list.index(end_date)
            if s_idx > e_idx: s_idx, e_idx = e_idx, s_idx; start_date, end_date = end_date, start_date
            
            m_top = df_maemae.iloc[s_idx:e_idx+1].drop(columns=['날짜']).sum().sort_values(ascending=False).head(10).index.tolist()
            j_top = df_jeonse.iloc[s_idx:e_idx+1].drop(columns=['날짜']).sum().sort_values(ascending=False).head(10).index.tolist()

            for region in sel_regions:
                m_val = df_maemae.iloc[s_idx:e_idx+1][region].sum()
                j_val = df_jeonse.iloc[s_idx:e_idx+1][region].sum()
                c1, c2 = st.columns(2)
                d_label = f"{start_date[5:]}~{end_date[5:]}"
                with c1:
                    m_cls = "stat-card m-card highlight-card" if region in m_top else "stat-card m-card"
                    st.markdown(f'<div class="{m_cls}"><div>{region} 매매({d_label})</div><div class="stat-value">{m_val:+.2f}%</div></div>', unsafe_allow_html=True)
                with c2:
                    j_cls = "stat-card j-card highlight-card" if region in j_top else "stat-card j-card"
                    st.markdown(f'<div class="{j_cls}"><div>{region} 전세({d_label})</div><div class="stat-value">{j_val:+.2f}%</div></div>', unsafe_allow_html=True)
            
            c_palette = ['#006400'] + px.colors.qualitative.Plotly
            st.markdown(f'<div class="chart-title">📈 매매 증감 추이 ({start_date} ~ {end_date})</div>', unsafe_allow_html=True)
            st.plotly_chart(px.line(df_maemae.iloc[s_idx:e_idx+1][['날짜']+sel_regions], x='날짜', y=sel_regions, markers=True, color_discrete_sequence=c_palette).update_layout(height=320, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'), use_container_width=True, config={'staticPlot': True})
            
            # ★ 에러 수정된 분석 테이블 코드 ★
            st.markdown(f'<div class="chart-title" style="background:#4B0082; border-color:#E6E6FA;">🧐 기간 심층 분석 ({start_date[5:]} ~ {end_date[5:]})</div>', unsafe_allow_html=True)
            
            # 테이블 시작
            table_body = ""
            for region in sel_regions:
                m_series = df_maemae.iloc[s_idx:e_idx+1][region]
                j_series = df_jeonse.iloc[s_idx:e_idx+1][region]
                
                m_max_idx = m_series.idxmax()
                m_min_idx = m_series.idxmin()
                j_max_idx = j_series.idxmax()
                j_min_idx = j_series.idxmin()
                
                table_body += f"""
                <tr>
                    <td rowspan='2' style='background:#fcfcfc; font-weight:900;'>{region}</td>
                    <td style='color:#D32F2F;'>매매</td>
                    <td style='font-weight:900;'>{m_series.sum():+.2f}%</td>
                    <td><span class='point-date'>{df_maemae.at[m_max_idx, '날짜'][5:]}</span><span class='point-val'>{m_series.max():+.2f}</span></td>
                    <td><span class='point-date'>{df_maemae.at[m_min_idx, '날짜'][5:]}</span><span class='point-val'>{m_series.min():+.2f}</span></td>
                </tr>
                <tr>
                    <td style='color:#01579B;'>전세</td>
                    <td style='font-weight:900;'>{j_series.sum():+.2f}%</td>
                    <td><span class='point-date'>{df_jeonse.at[j_max_idx, '날짜'][5:]}</span><span class='point-val'>{j_series.max():+.2f}</span></td>
                    <td><span class='point-date'>{df_jeonse.at[j_min_idx, '날짜'][5:]}</span><span class='point-val'>{j_series.min():+.2f}</span></td>
                </tr>
                """
            
            # 전체 테이블 래핑
            full_table_html = f"""
            <table class='analysis-table'>
                <colgroup>
                    <col style='width: 22%'>
                    <col style='width: 14%'>
                    <col style='width: 18%'>
                    <col style='width: 23%'>
                    <col style='width: 23%'>
                </colgroup>
                <thead>
                    <tr><th>지역명</th><th>구분</th><th>누적증감</th><th>최고상승(주)</th><th>최저하락(주)</th></tr>
                </thead>
                <tbody>
                    {table_body}
                </tbody>
            </table>
            """
            st.markdown(full_table_html, unsafe_allow_html=True)

            st.markdown(f'<div class="chart-title" style="margin-top:30px;">📉 전세 증감 추이 ({start_date} ~ {end_date})</div>', unsafe_allow_html=True)
            st.plotly_chart(px.line(df_jeonse.iloc[s_idx:e_idx+1][['날짜']+sel_regions], x='날짜', y=sel_regions, markers=True, color_discrete_sequence=c_palette).update_layout(height=320, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'), use_container_width=True, config={'staticPlot': True})

    # 나머지 탭 로직 (시장온도, 랭킹) 유지
    elif st.session_state.active_tab == "🌡️ 시장 온도":
        st.markdown('<div class="chart-title">🌡️ 시장 온도계 (2026년 누적)</div>', unsafe_allow_html=True)
        df_m_2026 = df_maemae[df_maemae['날짜'].astype(str).str.startswith('2026')]
        df_j_2026 = df_jeonse[df_jeonse['날짜'].astype(str).str.startswith('2026')]
        m_sum, j_sum = df_m_2026.drop(columns=['날짜']).sum(), df_j_2026.drop(columns=['날짜']).sum()
        heat_df = pd.DataFrame({'매매합계': m_sum, '전세합계': j_sum}).sort_values(by='매매합계', ascending=False)
        st.dataframe(heat_df.style.background_gradient(cmap='RdYlBu_r').format("{:+.2f}%"), use_container_width=True, height=450)

    elif st.session_state.active_tab == "🏆 누적 랭킹 TOP 10":
        sel_date_rank = st.selectbox("📅 랭킹 기준일 선택", date_list, index=len(date_list)-1, key=f"rk_d_{st.session_state.date_reset_key}")
        c_idx_rk = date_list.index(sel_date_rank)
        s_idx_rk = next((i for i, d in enumerate(date_list) if str(d).startswith('2026')), 0)
        st.markdown('<div class="chart-title" style="background:#e67e22; border-color:#d35400;">🔥 주간 상승 지역 TOP 10</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            m_w = df_maemae[df_maemae['날짜'] == sel_date_rank].drop(columns=['날짜']).iloc[0].sort_values(ascending=False).head(10)
            for i, (n, v) in enumerate(m_w.items()):
                if v > 0: st.markdown(f'<div class="rank-card m-weekly"><span>{i+1}. {n}</span><span>+{v:.2f}</span></div>', unsafe_allow_html=True)
        with c2:
            j_w = df_jeonse[df_jeonse['날짜'] == sel_date_rank].drop(columns=['날짜']).iloc[0].sort_values(ascending=False).head(10)
            for i, (n, v) in enumerate(j_w.items()):
                if v > 0: st.markdown(f'<div class="rank-card j-weekly"><span>{i+1}. {n}</span><span>+{v:.2f}</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-title" style="background:#f1c40f; color:#000; border-color:#b7950b;">📊 2026년 누적 상승 TOP 10</div>', unsafe_allow_html=True)
        c3, c4 = st.columns(2)
        with c3:
            m_8 = df_maemae.iloc[s_idx_rk:c_idx_rk+1].drop(columns=['날짜']).sum().sort_values(ascending=False).head(10)
            for i, (n, v) in enumerate(m_8.items()):
                if v > 0: st.markdown(f'<div class="rank-card m-accum"><span>{i+1}. {n}</span><span>+{v:.2f}%</span></div>', unsafe_allow_html=True)
        with c4:
            j_8 = df_jeonse.iloc[s_idx_rk:c_idx_rk+1].drop(columns=['날짜']).sum().sort_values(ascending=False).head(10)
            for i, (n, v) in enumerate(j_8.items()):
                if v > 0: st.markdown(f'<div class="rank-card j-accum"><span>{i+1}. {n}</span><span>+{v:.2f}%</span></div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("🚪 **안전하게 앱 종료하기**", key="exit_final_v_v", use_container_width=True):
        st.session_state.is_exit = True
        st.rerun()

if __name__ == "__main__":
    main()

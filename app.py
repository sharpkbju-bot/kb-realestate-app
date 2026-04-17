import streamlit as st
import pandas as pd
import plotly.express as px
import base64
import os
import streamlit.components.v1 as components

# 1. 페이지 설정
st.set_page_config(page_title="Dr.J의 부동산", page_icon="🏠", layout="centered")

# 세션 상태 초기화
if "is_exit" not in st.session_state: st.session_state.is_exit = False
if "active_tab" not in st.session_state: st.session_state.active_tab = "📊 지역 분석"
if "date_reset_key" not in st.session_state: st.session_state.date_reset_key = 0

# 종료 로직: 짙은 연두색(형광) 및 한 줄 처리 적용 (기존 100% 유지)
if st.session_state.is_exit:
    st.markdown("""
        <style>
        .stApp { background-color: white !important; background-image: none !important; }
        .exit-wrapper { position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 100%; text-align: center; z-index: 1000; }
        .exit-logo-font { font-family: 'Noto Sans KR', sans-serif; font-weight: 900; line-height: 1.2; margin-bottom: 15px; }
        .exit-logo-drj { color: #006400; font-size: 50px; }
        .exit-logo-bds { color: #FF4500; font-size: 28px; }
        .exit-wishes { font-size: 32px !important; font-weight: 900; color: #ADFF2F !important; margin-bottom: 10px; white-space: nowrap; }
        header { visibility: hidden; }
        </style>
        <div class="exit-wrapper">
            <div class="exit-logo-font"><span class="exit-logo-drj">Dr.J</span><span class="exit-logo-bds">의 부동산</span></div>
            <h2 class="exit-wishes">모두 부자됩시다.</h2>
            <p style="font-weight:900; color:#666;">with by 70억 자산가 SY.LEE</p>
        </div>
    """, unsafe_allow_html=True)
    components.html("<script>window.close();</script>")
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

    .brand-container { position: relative; text-align: center; padding: 20px; border: 3px solid #006400; border-radius: 15px; background-color: rgba(255,255,255,0.7); margin-bottom: 25px; }
    .brand-name { color: #006400; font-size: 40px; }
    .brand-suffix { color: #FF4500; font-size: 22px; }
    .version-tag { position: absolute; top: 12px; right: 15px; font-size: 14px; font-weight: 900; color: #555; }
    
    .stButton > button { 
        width: 100% !important; height: 60px !important; border-radius: 12px !important; 
        border: 2.5px solid #2c3e50 !important; font-weight: 900 !important; font-size: 16px !important;
        background-color: rgba(255,255,255,0.9) !important; color: #1a1a1a !important;
        margin-bottom: 5px !important; padding: 0 5px !important;
    }
    .stButton > button[kind="primary"] { background-color: #006400 !important; color: #ffffff !important; border: 2.5px solid #2c3e50 !important; }

    label[data-testid="stWidgetLabel"] p { font-size: 17px !important; color: #111111 !important; }
    div[data-baseweb="select"] > div:first-child { 
        background-color: #E6E6FA !important; border: 3px solid #4B0082 !important; border-radius: 12px !important; min-height: 50px !important; 
    }
    div[data-baseweb="select"] span, div[data-baseweb="select"] div { 
        color: #4B0082 !important; font-weight: 900 !important; font-size: 18px !important; 
    }

    .exit-btn-wrap { display: flex !important; justify-content: center !important; width: 100% !important; margin-top: 40px !important; }
    .exit-btn-wrap > button { 
        width: 200px !important; height: 55px !important; border-radius: 15px !important; 
        font-weight: 900 !important; font-size: 18px !important; color: #FFFFFF !important; 
        background: linear-gradient(135deg, #A7C7E7, #749BC2) !important;
        border: 3px solid #FFFFFF !important; box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
    }

    @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(255, 69, 0, 0.7); } 70% { box-shadow: 0 0 0 15px rgba(255, 69, 0, 0); } 100% { box-shadow: 0 0 0 0 rgba(255, 69, 0, 0); } }
    .highlight-card { animation: pulse 2s infinite !important; border: 4px solid #FF4500 !important; }
    .stat-card { padding: 15px; border-radius: 12px; margin: 10px 0; display: flex; flex-direction: column; align-items: center; background: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border: 2px solid #cccccc; font-size: 18px; }
    .m-card { border-left: 12px solid #FF4500; color: #D32F2F; }
    .j-card { border-left: 12px solid #01579B; color: #01579B; }
    .stat-value { font-size: 24px !important; }
    .chart-title { font-size: 15px; font-weight: 900; color: #ffffff !important; background: #2c3e50; border-radius: 12px; text-align: center; padding: 10px; margin: 20px 0; border: 2.5px solid #FFD700; }
    .rank-card { padding: 10px 15px; border-radius: 12px; margin-bottom: 8px; display: flex; align-items: center; justify-content: space-between; border: 2.5px solid #333; font-size: 14px; font-weight: 900 !important; }
    .m-weekly { background: linear-gradient(135deg, #FFEFBA, #FFFFFF) !important; border-left: 10px solid #FF4500 !important; color: #D32F2F !important; }
    .j-weekly { background: linear-gradient(135deg, #E0F7FA, #FFFFFF) !important; border-left: 10px solid #01579B !important; color: #01579B !important; }
    .m-accum { background: linear-gradient(135deg, #FFF9C4, #FFFFFF) !important; border-left: 10px solid #FBC02D !important; color: #7F6000 !important; }
    .j-accum { background: linear-gradient(135deg, #E8F5E9, #FFFFFF) !important; border-left: 10px solid #2E7D32 !important; color: #1B5E20 !important; }

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
    st.markdown('<div class="brand-container"><span class="brand-name">Dr.J</span><span class="brand-suffix">의 부동산</span><span class="version-tag">v3.00</span></div>', unsafe_allow_html=True)
    
    df_maemae, df_jeonse = load_data()
    date_list = sorted(df_maemae['날짜'].unique().tolist())
    region_list = sorted([col for col in df_maemae.columns if col != '날짜'])
    
    t_cols = st.columns(4)
    tabs = ["📊 지역 분석", "🌡️ 시장 온도", "🏆 누적 랭킹 TOP 10", "📈 투자 심층 분석"]
    for i, t_label in enumerate(tabs):
        is_active = (st.session_state.active_tab == t_label)
        if t_cols[i].button(t_label, key=f"t_btn_y_{i}", use_container_width=True, 
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
            start_date = st.selectbox("📅 기준 시작일", date_list, index=max(0, len(date_list)-9), key=f"start_date_{st.session_state.date_reset_key}")
        with c_date2:
            end_date = st.selectbox("📅 기준 종료일", date_list, index=len(date_list)-1, key=f"end_date_{st.session_state.date_reset_key}")
        sel_regions = st.multiselect("🔍 비교 지역 선택", region_list, default=[region_list[0]] if region_list else [])
        if sel_regions:
            start_idx = date_list.index(start_date); end_idx = date_list.index(end_date)
            if start_idx > end_idx: start_idx, end_idx = end_idx, start_idx; start_date, end_date = end_date, start_date
            m_top = df_maemae.iloc[start_idx : end_idx+1].drop(columns=['날짜']).sum().sort_values(ascending=False).head(10).index.tolist()
            j_top = df_jeonse.iloc[start_idx : end_idx+1].drop(columns=['날짜']).sum().sort_values(ascending=False).head(10).index.tolist()
            for region in sel_regions:
                m_val = df_maemae.iloc[start_idx : end_idx+1][region].sum(); j_val = df_jeonse.iloc[start_idx : end_idx+1][region].sum()
                is_m_hot, is_j_hot = region in m_top, region in j_top
                c1, c2 = st.columns(2); date_label = f"{start_date[5:]}~{end_date[5:]}"
                with c1:
                    m_cls = "stat-card m-card highlight-card" if is_m_hot else "stat-card m-card"
                    st.markdown(f'<div class="{m_cls}"><div>{region} 매매({date_label})</div><div class="stat-value">{m_val:+.2f}%</div>{"<div style=\'color:#FF4500; font-size:12px;\'>🔥 기간 TOP</div>" if is_m_hot else ""}</div>', unsafe_allow_html=True)
                with c2:
                    j_cls = "stat-card j-card highlight-card" if is_j_hot else "stat-card j-card"
                    st.markdown(f'<div class="{j_cls}"><div>{region} 전세({date_label})</div><div class="stat-value">{j_val:+.2f}%</div>{"<div style=\'color:#01579B; font-size:12px;\'>🔥 기간 TOP</div>" if is_j_hot else ""}</div>', unsafe_allow_html=True)
            c_palette = ['#006400'] + px.colors.qualitative.Plotly
            st.markdown(f'<div class="chart-title">📈 매매 증감 추이 ({start_date} ~ {end_date})</div>', unsafe_allow_html=True)
            st.plotly_chart(px.line(df_maemae.iloc[start_idx : end_idx+1][['날짜']+sel_regions], x='날짜', y=sel_regions, markers=True, color_discrete_sequence=c_palette).update_layout(height=320, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'), use_container_width=True, config={'staticPlot': True})
            st.markdown(f'<div class="chart-title">📉 전세 증감 추이 ({start_date} ~ {end_date})</div>', unsafe_allow_html=True)
            st.plotly_chart(px.line(df_jeonse.iloc[start_idx : end_idx+1][['날짜']+sel_regions], x='날짜', y=sel_regions, markers=True, color_discrete_sequence=c_palette).update_layout(height=320, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'), use_container_width=True, config={'staticPlot': True})

    # 2. 시장 온도 탭
    elif st.session_state.active_tab == "🌡️ 시장 온도":
        st.markdown('<div class="chart-title">🌡️ 시장 온도계 (2026년 누적)</div>', unsafe_allow_html=True)
        df_m_2026 = df_maemae[df_maemae['날짜'].astype(str).str.startswith('2026')]
        df_j_2026 = df_jeonse[df_jeonse['날짜'].astype(str).str.startswith('2026')]
        m_sum = df_m_2026.drop(columns=['날짜']).sum(); j_sum = df_j_2026.drop(columns=['날짜']).sum()
        heat_df = pd.DataFrame({'매매합계': m_sum, '전세합계': j_sum}).sort_values(by='매매합계', ascending=False)
        st.dataframe(heat_df.style.background_gradient(cmap='RdYlBu_r').format("{:+.2f}%"), use_container_width=True, height=450)

    # 3. 누적 랭킹 탭
    elif st.session_state.active_tab == "🏆 누적 랭킹 TOP 10":
        sel_date_rank = st.selectbox("📅 랭킹 기준일 선택", date_list, index=len(date_list)-1, key=f"ds3_y_{st.session_state.date_reset_key}")
        curr_idx_rank = date_list.index(sel_date_rank); start_idx_rank = get_2026_start_idx(date_list, curr_idx_rank)
        st.markdown('<div class="chart-title" style="background:#e67e22; border-color: #d35400;">🔥 주간 상승 지역 TOP 10</div>', unsafe_allow_html=True)
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
        st.markdown('<div class="chart-title" style="background:#f1c40f; color:#000; border-color: #b7950b;">📊 2026년 누적 상승 TOP 10</div>', unsafe_allow_html=True)
        c3, c4 = st.columns(2)
        with c3:
            st.markdown('<p style="text-align:center; color:#7F6000; font-size:14px;">[매매 누적 상승률]</p>', unsafe_allow_html=True)
            m_8 = df_maemae.iloc[start_idx_rank : curr_idx_rank+1].drop(columns=['날짜']).sum().sort_values(ascending=False).head(10)
            for i, (n, v) in enumerate(m_8.items()):
                if v > 0: st.markdown(f'<div class="rank-card m-accum"><span>{i+1}. {n}</span><span>+{v:.2f}%</span></div>', unsafe_allow_html=True)
        with c4:
            st.markdown('<p style="text-align:center; color:#1B5E20; font-size:14px;">[전세 누적 상승률]</p>', unsafe_allow_html=True)
            j_8 = df_jeonse.iloc[start_idx_rank : curr_idx_rank+1].drop(columns=['날짜']).sum().sort_values(ascending=False).head(10)
            for i, (n, v) in enumerate(j_8.items()):
                if v > 0: st.markdown(f'<div class="rank-card j-accum"><span>{i+1}. {n}</span><span>+{v:.2f}%</span></div>', unsafe_allow_html=True)

    # 4. 투자 심층 분석 탭
    elif st.session_state.active_tab == "📈 투자 심층 분석":
        st.markdown('<div class="chart-title" style="background:#8e44ad; border-color: #9b59b6;">📈 투자 심층 분석 도구</div>', unsafe_allow_html=True)
        analysis_type = st.selectbox("🔍 분석 모듈을 선택하세요", ["전세가율(Gap) 흐름 추적기", "이동평균선 및 골든크로스 분석", "광명시 집중 리포트"], key=f"analysis_{st.session_state.date_reset_key}")
        
        if analysis_type == "전세가율(Gap) 흐름 추적기":
            st.markdown('<p style="color:#333; font-size:14px; text-align:center;">전세 지수 상승이 매매 지수 상승을 추월하여 <b>Gap이 축소되는 시점</b>을 파악합니다.</p>', unsafe_allow_html=True)
            sel_region_gap = st.selectbox("📌 분석 지역 선택", region_list, key=f"gap_reg_{st.session_state.date_reset_key}")
            cum_m = df_maemae[sel_region_gap].cumsum(); cum_j = df_jeonse[sel_region_gap].cumsum()
            gap_df = pd.DataFrame({'날짜': df_maemae['날짜'], '매매 누적성장': cum_m, '전세 누적성장': cum_j})
            fig_gap = px.line(gap_df, x='날짜', y=['매매 누적성장', '전세 누적성장'], color_discrete_sequence=['#D32F2F', '#01579B'])
            fig_gap.update_layout(height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', legend_title_text='')
            st.plotly_chart(fig_gap, use_container_width=True, config={'staticPlot': True})

        elif analysis_type == "이동평균선 및 골든크로스 분석":
            # [최종 수정] 모바일 환경의 강제 중앙 정렬을 무력화하는 테이블 속성(display: table) 결합 적용
            st.markdown('<div style="width:100%; display:table;"><div style="display:table-cell; text-align:left !important;"><span style="color:#333; font-size:14px;">매매 증감의 <b>4주(단기) 및 12주(장기) 이동평균선을 통해 시장의 방향성을 진단합니다.</b></span></div></div>', unsafe_allow_html=True)
            
            sel_region_ma = st.selectbox("📌 분석 지역 선택", region_list, key=f"ma_reg_{st.session_state.date_reset_key}")
            cum_m_ma = df_maemae[sel_region_ma].cumsum(); ma4 = cum_m_ma.rolling(window=4).mean(); ma12 = cum_m_ma.rolling(window=12).mean()
            ma_df = pd.DataFrame({'날짜': df_maemae['날짜'], '실제 누적': cum_m_ma, '4주(단기)': ma4, '12주(장기)': ma12})
            cross_status = "데이터 부족"
            if len(ma4) >= 2 and pd.notna(ma4.iloc[-1]) and pd.notna(ma12.iloc[-1]):
                if ma4.iloc[-2] <= ma12.iloc[-2] and ma4.iloc[-1] > ma12.iloc[-1]: cross_status = "🔥 골든크로스 발생 (상승 전환 기대)"
                elif ma4.iloc[-2] >= ma12.iloc[-2] and ma4.iloc[-1] < ma12.iloc[-1]: cross_status = "❄️ 데드크로스 발생 (조정 진입 우려)"
                elif ma4.iloc[-1] > ma12.iloc[-1]: cross_status = "📈 단기 상승 추세 유지 (MA4 > MA12)"
                else: cross_status = "📉 단기 하락 추세 유지 (MA4 < MA12)"
            st.markdown(f'<div class="stat-card" style="border-color:#8e44ad;"><div style="font-size:14px;">현재 시장 추세 진단</div><div style="font-size:22px; font-weight:900; color:#8e44ad;">{cross_status}</div></div>', unsafe_allow_html=True)
            fig_ma = px.line(ma_df, x='날짜', y=['실제 누적', '4주(단기)', '12주(장기)'], color_discrete_sequence=['#cccccc', '#FF4500', '#006400'])
            fig_ma.update_layout(height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', legend_title_text='')
            st.plotly_chart(fig_ma, use_container_width=True, config={'staticPlot': True})

        elif analysis_type == "광명시 집중 리포트":
            if "광명시" in region_list:
                st.markdown('<p style="color:#333; font-size:14px; text-align:center;">투자 관심 지역 <b>광명시</b>의 매매 및 전세 핵심 데이터를 요약합니다.</p>', unsafe_allow_html=True)
                cum_m_gm = df_maemae["광명시"].sum(); cum_j_gm = df_jeonse["광명시"].sum()
                c_gm1, c_gm2 = st.columns(2)
                with c_gm1: st.markdown(f'<div class="stat-card m-card"><div>광명시 전체 누적 매매</div><div class="stat-value">{cum_m_gm:+.2f}%</div></div>', unsafe_allow_html=True)
                with c_gm2: st.markdown(f'<div class="stat-card j-card"><div>광명시 전체 누적 전세</div><div class="stat-value">{cum_j_gm:+.2f}%</div></div>', unsafe_allow_html=True)
                gm_df = pd.DataFrame({'날짜': df_maemae['날짜'], '광명시 매매': df_maemae["광명시"], '광명시 전세': df_jeonse["광명시"]})
                fig_gm = px.line(gm_df, x='날짜', y=['광명시 매매', '광명시 전세'], color_discrete_sequence=['#D32F2F', '#01579B'])
                fig_gm.update_layout(height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', legend_title_text='')
                st.plotly_chart(fig_gm, use_container_width=True, config={'staticPlot': True})
            else: st.warning("현재 데이터셋에 '광명시' 데이터가 존재하지 않습니다.")

    # 하단 종료 버튼 영역
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<div class="exit-btn-wrap">', unsafe_allow_html=True)
    if st.button("🚪 **안전하게 앱 종료하기**", key="exit_v_final_ytd", use_container_width=True):
        st.session_state.is_exit = True
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()

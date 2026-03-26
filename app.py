import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components
import base64
import os

# 1. 페이지 설정
st.set_page_config(page_title="Dr.J의 부동산", page_icon="🏠", layout="centered")

# 세션 상태 및 종료 로직
if "is_exit" not in st.session_state:
    st.session_state.is_exit = False

if st.session_state.is_exit:
    st.markdown("""
        <style>
        .stApp { background-color: white !important; background-image: none !important; }
        .exit-wrapper { position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 100%; text-align: center; }
        .brand-name { color: #006400; font-size: 45px; font-weight: 900; }
        .brand-suffix { color: #FF4500; font-size: 24px; font-weight: 900; }
        header { visibility: hidden; }
        </style>
        <div class="exit-wrapper">
            <div style="margin-bottom:20px;"><span class="brand-name">Dr.J</span><span class="brand-suffix">의 부동산</span></div>
            <div style="color:#006400; font-weight:900; font-size:32px;">모두 부자됩시다.</div>
            <div style="color:#000080; font-size:24px; margin-top:15px; font-weight:700;">Created by Ju Kyung Bae</div>
        </div>
    """, unsafe_allow_html=True)
    st.stop()

# 배경 설정
def set_bg():
    if os.path.exists('bg.jpg'):
        with open("bg.jpg", "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        st.markdown(f"""<style>.stApp {{ background-image: url("data:image/jpg;base64,{encoded}"); background-size: cover; background-attachment: fixed; }}</style>""", unsafe_allow_html=True)
set_bg()

# 2. 스타일 시트 (디자인 복구 및 고정)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');
    * { font-family: 'Noto Sans KR', sans-serif !important; }

    .title-container { text-align: center; padding: 20px 0; }
    .brand-name { color: #006400; font-size: 45px; font-weight: 900; }
    .brand-suffix { color: #FF4500; font-size: 24px; font-weight: 900; }

    /* 요약 카드 */
    .summary-card { 
        background: rgba(255, 255, 255, 0.95); border-radius: 15px; padding: 15px; 
        text-align: center; margin-bottom: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }

    /* [복구] 랭킹 카드 스타일 */
    .rank-card {
        padding: 12px 15px; border-radius: 12px; margin-bottom: 8px;
        display: flex; align-items: center; justify-content: space-between;
        background: white; box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .rank-num { font-weight: 900; color: #4a148c; font-size: 17px; margin-right: 10px; }
    
    /* 매매 랭킹: 브라운 텍스트 */
    .rank-m { border-left: 8px solid #FF4500 !important; }
    .rank-m .rank-name, .rank-m .rank-val { color: #8B4513 !important; font-weight: 900; }

    /* 전세 랭킹: 청록 텍스트 */
    .rank-j { border-left: 8px solid #000080 !important; }
    .rank-j .rank-name, .rank-j .rank-val { color: #008080 !important; font-weight: 900; }

    /* 버튼 스타일 (100% 폭 & Bold 강제) */
    div.stButton > button, .screenshot-btn {
        width: 100% !important; height: 48px !important; border-radius: 12px !important;
        font-weight: 900 !important; font-size: 17px !important; color: #87CEEB !important;
        background: linear-gradient(135deg, #333, #111) !important;
        border: 2px solid #555 !important; cursor: pointer;
        display: flex !important; align-items: center !important; justify-content: center !important;
    }
    div.stButton > button p { font-weight: 900 !important; font-size: 17px !important; }
    .screenshot-btn { margin-top: 20px; text-decoration: none; }

    header { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# 3. 데이터 로딩 (에러 방지 로직 추가)
@st.cache_data
def load_data():
    try:
        m = pd.read_csv('maemae.csv', encoding='cp949')
        j = pd.read_csv('jeonse.csv', encoding='cp949')
    except:
        m = pd.read_csv('maemae.csv', encoding='utf-8')
        j = pd.read_csv('jeonse.csv', encoding='utf-8')
    
    # [핵심] 날짜 제외 모든 컬럼을 강제로 숫자형으로 변환 (오류 원인 제거)
    for df in [m, j]:
        for col in df.columns:
            if col != '날짜':
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)
    
    m['날짜'] = m['날짜'].astype(str)
    j['날짜'] = j['날짜'].astype(str)
    return m, j

def main():
    st.markdown('<div class="title-container"><span class="brand-name">Dr.J</span><span class="brand-suffix">의 부동산</span></div>', unsafe_allow_html=True)

    df_m, df_j = load_data()
    date_list = sorted(df_m['날짜'].unique().tolist())
    region_list = sorted([c for c in df_m.columns if c != '날짜'])

    sel_date = st.selectbox("📅 날짜 선택", date_list, index=len(date_list)-1)
    sel_region = st.selectbox("🔍 지역 검색", ["지역을 입력하세요."] + region_list)

    # 지역 선택 시 출력
    if sel_region != "지역을 입력하세요.":
        m_val = df_m.loc[df_m['날짜'] == sel_date, sel_region].values[0]
        j_val = df_j.loc[df_j['날짜'] == sel_date, sel_region].values[0]

        st.markdown(f'<div class="summary-card"><div style="font-weight:900; color:#000080;">📍 {sel_region} 매매 증감</div><div style="color:#e74c3c; font-size:26px; font-weight:900;">{m_val:+.2f}%</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="summary-card"><div style="font-weight:900; color:#000080;">📍 {sel_region} 전세 증감</div><div style="color:#000080; font-size:26px; font-weight:900;">{j_val:+.2f}%</div></div>', unsafe_allow_html=True)

        # 그래프
        idx = date_list.index(sel_date)
        sub_m = df_m.iloc[max(0, idx-3):idx+1]
        fig = px.line(sub_m, x='날짜', y=sel_region, title=f"📈 {sel_region} 매매 추이")
        fig.update_layout(height=250, margin=dict(l=10,r=10,t=40,b=10))
        st.plotly_chart(fig, use_container_width=True)

    # 랭킹 섹션 (데이터 타입 에러 발생 지점 수정 완료)
    st.markdown('<h3 style="color:#FF4500; font-weight:900; margin-top:30px;">🔥 주간 매매 상승 TOP 10</h3>', unsafe_allow_html=True)
    day_m = df_m[df_m['날짜'] == sel_date].drop(columns=['날짜']).iloc[0]
    top_m = day_m[day_m > 0].sort_values(ascending=False).head(10)
    for i, (name, val) in enumerate(top_m.items()):
        st.markdown(f'<div class="rank-card rank-m"><span class="rank-num">{i+1}위</span><span class="rank-name">{name}</span><span class="rank-val">+{val:.2f}%</span></div>', unsafe_allow_html=True)

    st.markdown('<h3 style="color:#000080; font-weight:900; margin-top:30px;">💧 주간 전세 상승 TOP 10</h3>', unsafe_allow_html=True)
    day_j = df_j[df_j['날짜'] == sel_date].drop(columns=['날짜']).iloc[0]
    top_j = day_j[day_j > 0].sort_values(ascending=False).head(10)
    for i, (name, val) in enumerate(top_j.items()):
        st.markdown(f'<div class="rank-card rank-j"><span class="rank-num">{i+1}위</span><span class="rank-name">{name}</span><span class="rank-val">+{val:.2f}%</span></div>', unsafe_allow_html=True)

    # 하단 버튼
    st.markdown('<div id="sc-btn" class="screenshot-btn">📸 화면 스크린샷 저장</div>', unsafe_allow_html=True)
    
    if st.button("🚪 앱 종료", use_container_width=True):
        st.session_state.is_exit = True
        st.rerun()

    # 스크린샷 스크립트
    st.markdown("""
        <script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>
        <script>
        const btn = window.parent.document.getElementById('sc-btn');
        if(btn) {
            btn.onclick = function() {
                const target = window.parent.document.querySelector('#root');
                html2canvas(target, {useCORS: true}).then(canvas => {
                    const link = document.createElement('a');
                    link.href = canvas.toDataURL('image/png');
                    link.download = 'DrJ_RealEstate.png';
                    link.click();
                });
            };
        }
        </script>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

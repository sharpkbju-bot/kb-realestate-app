import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components
import base64
import os

# 1. 페이지 설정
st.set_page_config(page_title="Dr.J의 부동산", page_icon="🏠", layout="centered")

# 세션 상태 초기화 및 종료 로직
if "is_exit" not in st.session_state:
    st.session_state.is_exit = False

if st.session_state.is_exit:
    st.markdown("""
        <style>
        .stApp { background-color: white !important; background-image: none !important; }
        .exit-wrapper { position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 100%; text-align: center; }
        .brand-name { color: #006400; font-size: 45px; font-weight: 900; }
        .brand-suffix { color: #FF4500; font-size: 24px; font-weight: 900; }
        .exit-msg { color: #006400; font-weight: 900; font-size: 32px; margin-top: 20px; }
        header { visibility: hidden; }
        </style>
        <div class="exit-wrapper">
            <div class="title-container"><span class="brand-name">Dr.J</span><span class="brand-suffix">의 부동산</span></div>
            <div class="exit-msg">모두 부자됩시다.</div>
            <div style="font-family: 'Dancing Script', cursive; color: #000080; font-size: 30px; margin-top: 10px;">Created by Ju Kyung Bae</div>
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

# 2. UI 및 CSS 설정 (팝업창 스타일 추가)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;500;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }

    /* 타이틀 및 카드 스타일 */
    .title-container { width: 100%; padding: 30px 0 15px 0; text-align: center; }
    .brand-name { color: #006400; font-size: 45px; font-weight: 900; font-family: 'Arial Black'; }
    .brand-suffix { color: #FF4500; font-size: 24px; font-weight: 900; }
    
    .rank-card {
        padding: 12px 15px; border-radius: 12px; margin-bottom: 12px; display: flex; align-items: center; justify-content: space-between;
        background: linear-gradient(135deg, rgba(243, 229, 245, 0.95), rgba(225, 190, 231, 0.95)) !important;
        box-shadow: 0 15px 35px rgba(0,0,0,0.5) !important;
    }
    .rank-num { font-weight: 900 !important; color: #4a148c !important; }
    .rank-m { border-left: 7px solid #FF4500 !important; }
    .rank-m .rank-name, .rank-m .rank-val { color: #8B4513 !important; font-weight: 900 !important; }
    .rank-j { border-left: 7px solid #000080 !important; }
    .rank-j .rank-name, .rank-j .rank-val { color: #008080 !important; font-weight: 900 !important; }

    /* 버튼 스타일 (100% 폭 & Bold) */
    div.stButton > button {
        width: 100% !important; min-width: 100% !important; height: 46px !important; border-radius: 12px !important;
        font-weight: 900 !important; font-size: 16px !important; color: #87CEEB !important;
        background: linear-gradient(135deg, rgba(60, 60, 60, 0.8), rgba(30, 30, 30, 0.9)) !important;
        border: 2px solid rgba(200, 200, 200, 0.6) !important; margin-top: 11px !important;
    }
    div.stButton > button p { font-weight: 900 !important; }

    .screenshot-btn {
        width: 100%; height: 46px; border-radius: 12px; font-weight: 900; font-size: 16px; 
        color: #87CEEB !important; display: flex; justify-content: center; align-items: center;
        background: linear-gradient(135deg, rgba(60, 60, 60, 0.8), rgba(30, 30, 30, 0.9));
        border: 2px solid rgba(200, 200, 200, 0.6); margin-top: 20px; cursor: pointer;
    }

    /* 캡처 팝업창(모달) 스타일 */
    #screenshot-modal {
        display: none; position: fixed; z-index: 9999; left: 0; top: 0; width: 100%; height: 100%;
        background-color: rgba(0,0,0,0.9); overflow: auto; text-align: center; padding-top: 50px;
    }
    #modal-img { width: 90%; max-width: 500px; border-radius: 10px; margin-bottom: 20px; border: 3px solid white; }
    .modal-text { color: white; font-weight: 900; margin-bottom: 20px; font-size: 18px; }
    .close-modal { color: #ff4b4b; font-size: 30px; font-weight: bold; cursor: pointer; position: absolute; top: 20px; right: 30px; }

    header { visibility: hidden; }
    </style>
    
    <div id="screenshot-modal">
        <span class="close-modal" onclick="document.getElementById('screenshot-modal').style.display='none'">&times;</span>
        <div class="modal-text">이미지를 길게 눌러 공유하거나 저장하세요!</div>
        <img id="modal-img">
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
    common_cols = ['날짜'] + sorted(list(set(df_m.columns) & set(df_j.columns) - {'날짜'}))
    df_m, df_j = df_m[common_cols], df_j[common_cols]
    for col in [c for c in df_m.columns if c != '날짜']:
        df_m[col] = pd.to_numeric(df_m[col], errors='coerce').fillna(0)
        df_j[col] = pd.to_numeric(df_j[col], errors='coerce').fillna(0)
    df_m['날짜'] = df_m['날짜'].astype(str)
    return df_m, df_j

def main():
    st.markdown('<div class="title-container"><span class="brand-name">Dr.J</span><span class="brand-suffix">의 부동산</span></div>', unsafe_allow_html=True)

    df_maemae, df_jeonse = load_data()
    date_list = sorted(df_maemae['날짜'].unique().tolist())
    region_list = sorted([col for col in df_maemae.columns if col != '날짜'])

    sel_date = st.selectbox("📅 날짜 선택", date_list, index=len(date_list)-1)
    sel_region = st.selectbox("🔍 지역 검색 및 선택", options=["지역을 입력하세요."] + region_list, index=0)

    if sel_region != "지역을 입력하세요.":
        components.html("<script>window.parent.document.activeElement.blur();</script>", height=0)
        curr_idx = date_list.index(sel_date)
        m_val = df_maemae.loc[df_maemae['날짜'] == sel_date, sel_region].values[0]
        j_val = df_jeonse.loc[df_jeonse['날짜'] == sel_date, sel_region].values[0]
        
        # 요약 카드 및 그래프 출력
        st.markdown(f'<div class="summary-card"><div class="summary-label">📍 {sel_region} 매매 증감</div><div style="color:{"#e74c3c" if m_val > 0 else "#000080"}; font-size:28px; font-weight:900;">{m_val:+.2f}%</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="summary-card"><div class="summary-label">📍 {sel_region} 전세 증감</div><div style="color:{"#e74c3c" if j_val > 0 else "#000080"}; font-size:28px; font-weight:900;">{j_val:+.2f}%</div></div>', unsafe_allow_html=True)

        def draw_chart(df, line_color, title):
            st.markdown(f'<div class="chart-title">{title}</div>', unsafe_allow_html=True)
            sub_df = df.iloc[max(0, curr_idx-3) : curr_idx+1]
            fig = px.line(sub_df, x='날짜', y=sel_region, markers=True)
            fig.update_layout(height=220, margin=dict(l=10,r=10,t=10,b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        draw_chart(df_maemae, '#e74c3c', '📈 매매 트렌드')
        draw_chart(df_jeonse, '#000080', '📉 전세 트렌드')

    # 랭킹 TOP 10 섹션
    st.markdown('<div class="chart-title" style="color:#FF4500;">🔥 주간 매매 상승 TOP 10</div>', unsafe_allow_html=True)
    m_w_row = df_maemae[df_maemae['날짜'] == sel_date].drop(columns=['날짜']).iloc[0]
    top_mw = m_w_row[m_w_row > 0].sort_values(ascending=False).head(10)
    for i, (name, val) in enumerate(top_mw.items()):
        st.markdown(f'<div class="rank-card rank-m"><span class="rank-num">{i+1}위</span> <span class="rank-name">{name}</span><span class="rank-val">+{val:.2f}%</span></div>', unsafe_allow_html=True)

    # 하단 버튼 그룹
    st.markdown('<div id="btn-screenshot" class="screenshot-btn">📸 화면 캡처 및 공유하기</div>', unsafe_allow_html=True)
    
    if st.button("🚪 앱 종료", key="exit_trigger", use_container_width=True):
        st.session_state.is_exit = True
        st.rerun()

    # JavaScript: 캡처 후 팝업 띄우기 로직
    st.markdown("""
        <script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>
        <script>
        const scBtn = window.parent.document.getElementById('btn-screenshot');
        const modal = window.parent.document.getElementById('screenshot-modal');
        const modalImg = window.parent.document.getElementById('modal-img');

        if (scBtn) {
            scBtn.onclick = async function() {
                const target = window.parent.document.querySelector('#root');
                const canvas = await html2canvas(target, { useCORS: true, logging: false });
                
                // 팝업창에 캡처된 이미지 넣고 보여주기
                modalImg.src = canvas.toDataURL('image/png');
                modal.style.display = 'block';
            };
        }
        </script>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="경배의 아파트 주간 시황", layout="centered")

# 2. 디자인 및 레이아웃 수정 (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Noto+Sans+KR', sans-serif;
    }

    /* 타이틀 영역: 잘림 방지를 위해 padding과 크기 최적화 */
    .title-container {
        padding: 40px 0 20px 0; /* 상단 여백을 충분히 주어 잘림 방지 */
        text-align: center;
        width: 100%;
    }
    
    .main-title {
        font-size: clamp(20px, 6vw, 28px); /* 화면 크기에 따라 글자 크기 자동 조절 */
        font-weight: 700;
        white-space: nowrap; /* 한 줄 유지 */
        overflow: visible; /* 글자가 잘리지 않도록 설정 */
        letter-spacing: -1px;
        display: inline-block;
    }
    
    .brand-name {
        color: #006400; /* 짙은 그린 */
    }

    /* 카드 디자인 */
    .metric-container {
        background-color: white;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #f0f0f0;
        text-align: center;
        margin-top: 10px;
    }
    
    .metric-label {
        font-size: 13px;
        color: #888;
        margin-bottom: 2px;
    }
    
    .metric-value {
        font-size: 22px;
        font-weight: 700;
    }

    /* Streamlit 기본 헤더 숨기기 (공간 확보) */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* 전체 컨테이너 여백 조정 */
    .block-container {
        padding-top: 1rem !important;
    }
    </style>
    
    <div class="title-container">
        <div class="main-title">
            <span class="brand-name">경배</span>의 아파트 주간 시황
        </div>
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
    
    df_m['날짜'] = df_m['날짜'].astype(str)
    df_j['날짜'] = df_j['날짜'].astype(str)
    return df_m, df_j

def main():
    try:
        df_maemae, df_jeonse = load_data()
        
        # 입력 영역 레이아웃
        col_date, col_search = st.columns([1, 1.5])
        
        with col_date:
            date_list = df_maemae['날짜'].unique().tolist()
            selected_date = st.selectbox("📅 날짜 선택", date_list, index=len(date_list)-1)

        region_list = [col for col in df_maemae.columns if col != '날짜']

        with col_search:
            selected_region = st.selectbox(
                "🔍 지역 검색 및 선택",
                options=["지역을 입력하세요"] + region_list
            )

        st.markdown("<div style='margin: 15px 0;'></div>", unsafe_allow_html=True)

        if selected_region != "지역을 입력하세요":
            m_val = df_maemae.loc[df_maemae['날짜'] == selected_date, selected_region].values[0]
            j_val = df_jeonse.loc[df_jeonse['날짜'] == selected_date, selected_region].values[0]

            st.markdown(f"#### 📍 {selected_region}")
            
            # 카드 표시
            c1, c2 = st.columns(2)
            m_color = "#e74c3c" if m_val > 0 else "#3498db" if m_val < 0 else "#333"
            j_color = "#e74c3c" if j_val > 0 else "#3498db" if j_val < 0 else "#333"

            with c1:
                st.markdown(f"""
                    <div class="metric-container">
                        <div class="metric-label">매매 증감</div>
                        <div class="metric-value" style="color: {m_color};">{m_val:+.3f}%</div>
                    </div>
                """, unsafe_allow_html=True)
                
            with c2:
                st.markdown(f"""
                    <div class="metric-container">
                        <div class="metric-label">전세 증감</div>
                        <div class="metric-value" style="color: {j_color};">{j_val:+.3f}%</div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("조회할 지역명을 입력하거나 리스트에서 선택해 주세요.")

    except Exception as e:
        st.error(f"데이터 로드 오류: {e}")

if __name__ == "__main__":
    main()

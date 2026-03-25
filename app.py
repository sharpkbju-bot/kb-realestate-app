import streamlit as st
import pandas as pd

# 1. 페이지 설정 및 디자인 커스텀
st.set_page_config(page_title="경배의 주간 아파트 시황", layout="centered")

# CSS를 이용한 디자인 세련되게 다듬기
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    div.stButton > button:first-child {
        background-color: #007bff;
        color: white;
    }
    /* 카드 디자인 최적화 */
    .metric-container {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border: 1px solid #eee;
        text-align: center;
        margin-bottom: 10px;
    }
    .metric-label {
        font-size: 14px;
        color: #666;
        margin-bottom: 5px;
    }
    .metric-value {
        font-size: 24px;
        font-weight: bold;
        color: #333;
    }
    /* 여백 최소화 */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 0rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    # 인코딩 오류 방지를 위해 cp949 적용 (필요시 utf-8로 변경)
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
    st.title("🏘️ 아파트 주간 시황")
    
    try:
        df_maemae, df_jeonse = load_data()
        
        # --- 상단 선택 영역 (사이드바 대신 메인 화면) ---
        col_date, col_search = st.columns([1, 1.5])
        
        with col_date:
            date_list = df_maemae['날짜'].unique().tolist()
            selected_date = st.selectbox("📅 날짜 선택", date_list, index=len(date_list)-1)

        # '날짜' 컬럼을 제외한 모든 지역명 리스트 추출
        region_list = [col for col in df_maemae.columns if col != '날짜']

        with col_search:
            # 두 글자 이상 입력 시 드롭다운에서 선택할 수 있도록 함
            selected_region = st.selectbox(
                "🔍 지역 검색 및 선택",
                options=["지역을 선택하세요"] + region_list,
                help="두 글자 이상 입력하여 지역을 찾으세요."
            )

        st.divider()

        # --- 결과 표시 영역 ---
        if selected_region != "지역을 선택하세요":
            # 데이터 추출
            m_val = df_maemae.loc[df_maemae['날짜'] == selected_date, selected_region].values[0]
            j_val = df_jeonse.loc[df_jeonse['날짜'] == selected_date, selected_region].values[0]

            st.subheader(f"📍 {selected_region} 시황 ({selected_date})")
            
            # 카드 디자인 (여백 최적화)
            c1, c2 = st.columns(2)
            
            with c1:
                st.markdown(f"""
                    <div class="metric-container">
                        <div class="metric-label">매매 증감률</div>
                        <div class="metric-value" style="color: {'#e74c3c' if m_val > 0 else '#3498db' if m_val < 0 else '#333'};">
                            {m_val:+.3f}%
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
            with c2:
                st.markdown(f"""
                    <div class="metric-container">
                        <div class="metric-label">전세 증감률</div>
                        <div class="metric-value" style="color: {'#e74c3c' if j_val > 0 else '#3498db' if j_val < 0 else '#333'};">
                            {j_val:+.3f}%
                        </div>
                    </div>
                """, unsafe_allow_html=True)

            # 트렌드 확인을 위한 간단한 안내
            st.info(f"선택하신 {selected_region}의 해당 주간 변동폭입니다.")
        else:
            st.write("위의 검색창에서 지역을 선택하면 상세 데이터가 나타납니다.")

    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    main()

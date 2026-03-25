import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="주간 아파트 시황 조회", layout="wide")

@st.cache_data
def load_data():
    # 파일명은 실제 깃허브에 올린 이름과 일치해야 합니다.
    # 여기서는 편의상 변경된 이름을 기준으로 작성했습니다.
    df_m = pd.read_csv('maemae.csv', encoding='cp949')
    df_j = pd.read_csv('jeonse.csv', encoding='cp949')
    
    # 날짜 컬럼을 문자열로 변환하여 선택 박스에서 잘 보이게 함
    df_m['날짜'] = df_m['날짜'].astype(str)
    df_j['날짜'] = df_j['날짜'].astype(str)
    
    return df_m, df_j

st.title("🏘️ 주간 아파트 매매/전세 증감 조회")
st.markdown("매주 업데이트되는 엑셀 데이터를 기반으로 지역별 시황을 확인하세요.")

try:
    df_maemae, df_jeonse = load_data()

    # 사이드바: 날짜 선택
    st.sidebar.header("조회 조건 설정")
    date_list = df_maemae['날짜'].unique().tolist()
    selected_date = st.sidebar.selectbox("📅 확인하고 싶은 날짜", date_list, index=len(date_list)-1)

    # 메인 화면: 지역 검색
    search_query = st.text_input("🔍 검색할 지역명을 입력하세요 (예: 광명, 노원구, 연수구)", "")

    if search_query:
        # 해당 날짜의 데이터만 추출
        m_row = df_maemae[df_maemae['날짜'] == selected_date]
        j_row = df_jeonse[df_jeonse['날짜'] == selected_date]

        # 입력한 검색어가 포함된 컬럼(지역) 찾기
        matched_cols = [col for col in df_maemae.columns if search_query in col]

        if matched_cols:
            st.subheader(f"📍 '{search_query}' 검색 결과 ({selected_date} 기준)")
            
            for col in matched_cols:
                m_val = m_row[col].values[0]
                j_val = j_row[col].values[0]
                
                with st.expander(f"🏠 {col} 시황 확인", expanded=True):
                    c1, c2 = st.columns(2)
                    c1.metric("매매 증감률", f"{m_val:.3f}%")
                    c2.metric("전세 증감률", f"{j_val:.3f}%")
        else:
            st.error("해당하는 지역명을 찾을 수 없습니다. 다시 입력해주세요.")
    else:
        st.info("왼쪽에서 날짜를 선택하고, 위 입력창에 지역명을 입력하여 조회를 시작하세요.")

except FileNotFoundError:
    st.error("데이터 파일을 찾을 수 없습니다. 'maemae.csv'와 'jeonse.csv' 파일이 저장소에 있는지 확인해주세요.")
except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")

# 하단 안내
st.caption("데이터 출처: KB부동산 (업로드하신 엑셀 파일 기반)")

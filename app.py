import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 설정 (본인의 GitHub ID 확인 필수!)
GITHUB_USER = "sharpkbju-bot" 
BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/kb-realestate-app/main/data/"

st.set_page_config(page_title="내 부동산 자산 대시보드", layout="wide")
st.title("🏠 주간 부동산 투자 지표 대시보드")

# 2. KB 데이터 전용 로드 및 정제 함수
def load_kb_data(file_name):
    url = BASE_URL + file_name
    try:
        # 1) 일단 파일을 읽어옵니다.
        df = pd.read_csv(url, encoding='cp949')
        
        # 2) KB 데이터는 보통 2~3행부터 실제 데이터가 시작됩니다.
        # 데이터가 있는 행을 찾기 위해 '날짜'나 '지역'이 포함된 행 위쪽을 쳐냅니다.
        # 여기서는 단순히 위쪽의 불필요한 행(NaN이 많은 행)을 제거하는 방식을 씁니다.
        df = df.dropna(thresh=2) # 데이터가 2개 이상 있는 행만 남김
        
        # 3) 모든 열에 대해 숫자로 변환을 시도합니다. (첫 열 제외)
        for col in df.columns[1:]:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # 4) 최종적으로 데이터가 없는 행/열 삭제
        df = df.dropna(axis=0, how='all').dropna(axis=1, how='all')
        
        return df
    except Exception as e:
        st.error(f"데이터 정제 중 오류: {e}")
        return None

# 3. 사이드바 및 파일 매핑
region = st.sidebar.selectbox("지역 선택", ["광명시", "노원구", "연수구"])
file_dict = {
    "광명시": "kb_price_maemae_change.csv",
    "노원구": "kb_price_maemae_change.csv",
    "연수구": "kb_price_maemae_change.csv"
}

# 4. 메인 화면 로직
df = load_kb_data(file_dict[region])

if df is not None and not df.empty:
    st.subheader(f"📍 {region} 주간 시세 흐름")
    
    # 데이터가 어떻게 읽혔는지 확인용 (성공하면 나중에 지워도 됩니다)
    with st.expander("데이터 처리 결과 확인"):
        st.write("컬럼명:", df.columns.tolist())
        st.dataframe(df.head(10))
    
    # 그래프 그리기
    try:
        date_col = df.columns[0]
        # 숫자인 컬럼만 골라서 그래프를 그립니다.
        val_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        if val_cols:
            fig = px.line(df, x=date_col, y=val_cols, 
                         title=f"{region} 시세 변동 추이",
                         labels={date_col: "날짜", "value": "증감률(%)", "variable": "항목"})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("그래프를 그릴 수 있는 숫자 데이터가 없습니다.")
    except Exception as graph_e:
        st.error(f"그래프 생성 중 오류: {graph_e}")
else:
    st.warning("데이터가 비어있거나 불러올 수 없습니다.")

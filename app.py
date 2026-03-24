import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 설정 (본인의 GitHub ID 확인!)
GITHUB_USER = "sharpkbju-bot" 
BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/kb-realestate-app/main/data/"

st.set_page_config(page_title="내 부동산 전용 대시보드", layout="wide")
st.title("🏠 지역별 주간 부동산 시세 대시보드")

# 2. 데이터 로드 및 정제 함수 (KB 데이터 최적화)
def load_kb_data(file_name):
    url = BASE_URL + file_name
    try:
        df = pd.read_csv(url, encoding='cp949')
        # 데이터가 2개 이상 있는 행만 남겨서 제목/빈칸 제거
        df = df.dropna(thresh=2) 
        # 첫 열(날짜) 제외하고 모두 숫자로 변환
        for col in df.columns[1:]:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        df = df.dropna(axis=0, how='all').dropna(axis=1, how='all')
        return df
    except Exception as e:
        st.error(f"파일({file_name}) 읽기 오류: {e}")
        return None

# 3. 사이드바: 11개 파일 목록 직접 입력
# (파일명을 사용자님이 업로드한 실제 이름으로 수정해두시면 더 편합니다)
file_list = [
    "kb_price_maemae_change.csv", # 현재 사용 중인 파일
    "파일명2.csv", # data 폴더에 있는 다른 파일명들을 여기에 적으세요
    "파일명3.csv",
    # ... 나머지 파일명들도 따옴표 안에 쉼표로 구분해서 넣어주세요
]

target_file = st.sidebar.selectbox("분석할 파일 선택", file_list)

# 4. 메인 화면 로직
df = load_kb_data(target_file)

if df is not None and not df.empty:
    st.subheader(f"📍 {target_file} 데이터 분석 결과")
    
    with st.expander("데이터 원본 확인"):
        st.dataframe(df.head(10))
    
    # 그래프 그리기
    date_col = df.columns[0]
    val_cols = df.select_dtypes(include=['number']).columns.tolist()
    
    if val_cols:
        fig = px.line(df, x=date_col, y=val_cols, 
                     title="주간 시세 변동 추이",
                     labels={date_col: "날짜", "value": "증감률(%)", "variable": "지역/항목"})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("그래프를 그릴 수 있는 숫자 데이터가 없습니다.")

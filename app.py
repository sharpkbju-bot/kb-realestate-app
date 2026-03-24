import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 설정: GitHub ID와 저장소 이름을 입력하세요
GITHUB_USER = "사용자님의_깃허브_아이디"
REPO_NAME = "kb-realestate-app"
BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/main/data/"

st.set_page_config(page_title="내 부동산 자산 대시보드", layout="wide")

# 2. 데이터 불러오기 함수
@st.cache_data
def load_kb_data(file_name, skip_rows=1):
    url = BASE_URL + file_name
    df = pd.read_csv(url, skiprows=skip_rows)
    # 첫 번째 열을 날짜형식으로 변환 (KB 시계열 특성 반영)
    df.rename(columns={df.columns[0]: '날짜'}, inplace=True)
    return df

st.title("🏠 주간 부동산 투자 지표 대시보드")
st.markdown(f"**기준 데이터:** KB 주간 시계열 ({GITHUB_USER} 저장소)")

# 3. 사이드바 지역 설정
st.sidebar.header("📍 관심 지역 설정")
regions = {
    "광명시": "광명",
    "노원구 (상계동)": "노원구",
    "연수구 (동춘동)": "연수구"
}
selected_region = st.sidebar.selectbox("조회할 지역을 선택하세요", list(regions.keys()))
target_col = regions[selected_region]

# 4. 데이터 로드 (매매증감, 전세증감, 매수우위 등)
try:
    df_maemae = load_kb_data("kb_price_maemae_change.csv")
    df_jeonse = load_kb_data("kb_price_jeonse_change.csv")
    df_sentiment = load_kb_data("kb_sentiment_buy_sell.csv")

    # 5. 주요 지표 시각화 (최근 데이터)
    col1, col2, col3 = st.columns(3)
    
    latest_m = df_maemae[target_col].iloc[-1]
    latest_j = df_jeonse[target_col].iloc[-1]
    
    col1.metric("주간 매매 증감", f"{latest_m}%", delta=f"{latest_m}%")
    col2.metric("주간 전세 증감", f"{latest_j}%", delta=f"{latest_j}%")
    col3.metric("관심 지역", selected_region)

    # 6. 추세 그래프
    st.subheader(f"📈 {selected_region} 매매/전세 흐름 (최근 1년)")
    # 최근 52주 데이터 필터링
    chart_data = pd.DataFrame({
        '날짜': df_maemae['날짜'].tail(52),
        '매매증감': df_maemae[target_col].tail(52),
        '전세증감': df_jeonse[target_col].tail(52)
    })
    
    fig = px.line(chart_data, x='날짜', y=['매매증감', '전세증감'], 
                  title=f"{selected_region} 주간 변동률 추이")
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다. 파일명과 깃허브 아이디를 확인해주세요. \n오류 내용: {e}")

st.info("💡 매주 월요일 GitHub의 data 폴더에 최신 CSV 파일을 덮어쓰기하면 대시보드가 자동으로 업데이트됩니다.")

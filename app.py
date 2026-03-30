import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# 페이지 설정
st.set_page_config(layout="centered")

# CSS 주입: 폰트 설정 및 배경, 컴포넌트 스타일링
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;700&family=Nico+Moji&display=swap');

/* 전체 앱 폰트 설정 */
html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
    color: #333;
}

/* 배경 이미지 설정 (이미지 텍스처와 유사한 질감) */
[data-testid="stAppViewContainer"] {
    background-color: #f7f7f7;
    background-image: 
        radial-gradient(at 10% 10%, rgba(210, 210, 210, 0.4) 0px, transparent 50%),
        radial-gradient(at 90% 90%, rgba(200, 200, 200, 0.3) 0px, transparent 50%);
}

/* 상단 타이틀 스타일 (Nico Moji 폰트 적용 시도) */
.title-container {
    text-align: center;
    padding: 20px 0;
    margin-bottom: 10px;
}
.title-container span.drj {
    font-family: 'Nico Moji', sans-serif;
    font-size: 30px;
    font-weight: bold;
    color: #2e8b57; /* Dr.J의 녹색 */
}
.title-container span.rest {
    font-size: 24px;
    font-weight: bold;
    color: #ff4500; /* 부동산의 오렌지색 */
}

/* 탭 스타일링: 카드 디자인 및 요청에 따라 폰트 크기 축소 */
.stTabs [data-baseweb="tab-list"] {
    gap: 15px;
}
.stTabs [data-baseweb="tab"] {
    height: 60px;
    background-color: #fff;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    border: none;
    padding: 10px 15px;
    flex: 1 1 calc(33.33% - 10px);
    justify-content: center;
}
/* 탭 내부 텍스트 스타일 (크기 축소 반영) */
.stTabs [data-baseweb="tab-border"] {
    display: none;
}
.stTabs [data-baseweb="tab-panel"] {
    padding-top: 20px;
}
.tab-content {
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: bold;
    color: #333;
}
.tab-text {
    font-size: 14px; /* 기존보다 축소 */
}
/* 선택된 탭 스타일 */
.stTabs [aria-selected="true"] {
    background-color: #006400; /* 지역분석의 녹색 */
}
.stTabs [aria-selected="true"] .tab-text {
    color: #fff;
}

/* 선택 상자 및 라벨 스타일 */
[data-testid="stWidgetLabel"] {
    font-weight: bold;
    font-size: 16px;
}
[data-testid="stWidgetLabel"] .css-xv9v0u { /* 아이콘 간격 */
    margin-right: 8px;
}
.stSelectbox div[data-baseweb="select"] {
    border-radius: 10px;
    background-color: #fff;
}
.stMultiSelect div[data-baseweb="select"] {
    border-radius: 10px;
    background-color: #fff;
}

/* 강북구 태그 스타일 */
div[data-baseweb="tag"] {
    background-color: #ff4500; /* 오렌지색 */
    color: #fff;
    border-radius: 6px;
    padding: 2px 8px;
}

/* 데이터 표시 카드 스타일 */
.data-card {
    background-color: #fff;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    text-align: center;
    position: relative;
    overflow: hidden;
}
/* 좌측 장식 바 */
.card-decor-left {
    position: absolute;
    top: 0;
    left: 0;
    width: 6px;
    height: 100%;
}
.decor-maemae {
    background-color: #ff4500;
}
.card-maemae-border {
    border: 3px solid #ff4500;
}
.card-decor-bottom {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 6px;
    background-color: #ff4500;
}

.data-card .region-label {
    font-size: 18px;
    font-weight: bold;
}
.data-card .value {
    font-size: 24px;
    font-weight: bold;
    margin: 5px 0;
}
.card-maemae .value {
    color: #b22222;
}
.card-jeonse .value {
    color: #0056b3;
}
.data-card .accum-tag {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 4px;
    font-weight: bold;
}
.card-jeonse .accum-tag {
    color: #ff8c00;
}

/* 그래프 타이틀 배너 스타일 */
.graph-title-banner {
    background-color: #34495e;
    color: #fff;
    border-radius: 10px;
    padding: 15px;
    text-align: center;
    font-weight: bold;
    font-size: 18px;
    margin-bottom: 25px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
}

/* 그래프 영역 패딩 */
[data-testid="stAltairChart"] {
    padding-bottom: 30px;
}

/* 하단 플로팅 버튼 영역 스타일 */
.floating-bottom {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 80px;
    background-color: rgba(255,255,255,0.9);
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 20px;
    z-index: 999;
}
.icon-btn {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 30px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    cursor: pointer;
}
.icon-share {
    background-color: #fff;
    color: #8a2be2;
}
.icon-crown {
    background-color: #ff4500;
    color: #fff;
    border-radius: 10px; /* 크라운은 사각형 */
}

</style>
""", unsafe_allow_html=True)

# 상단 로고 및 타이틀
st.markdown('<div class="title-container"><span class="drj">Dr.J</span><span class="rest">의 부동산</span></div>', unsafe_allow_html=True)

# 탭 구성: 요청대로 폰트 크기 축소된 내용 반영
tab1_label = f'<div class="tab-content">🏢<span class="tab-text">지역분석</span></div>'
tab2_label = f'<div class="tab-content">🌡️<span class="tab-text">시장온도</span></div>'
tab3_label = f'<div class="tab-content">🏆<span class="tab-text">랭킹 TOP 10</span></div>'

tabs = st.tabs([tab1_label, tab2_label, tab3_label])

# 지역분석 탭 내용
with tabs[0]:
    # 기준 날짜 선택
    st.markdown('<div class="css-xv9v0u"></div>', unsafe_allow_html=True) # 아이콘 위치 확보
    date_label = '📅 기준 날짜 선택'
    st.selectbox(date_label, ['2026-03-23'], label_visibility="visible")

    st.write("") # 간격

    # 비교 지역 선택
    region_label = '🔍 비교 지역 선택'
    st.multiselect(region_label, ['강북구'], default=['강북구'])

    st.write("") # 간격

    # 데이터 카드 1: 매매
    st.markdown("""
    <div class="data-card card-maemae">
        <div class="card-decor-left decor-maemae"></div>
        <div class="region-label">강북구 매매</div>
        <div class="value">+0.89%</div>
    </div>
    """, unsafe_allow_html=True)

    # 데이터 카드 2: 전세 (강조 테두리)
    st.markdown("""
    <div class="data-card card-jeonse card-maemae-border">
        <div class="card-decor-bottom decor-maemae"></div>
        <div class="region-label">강북구 전세</div>
        <div class="value">+1.02%</div>
        <div class="accum-tag">🔥 누적TOP</div>
    </div>
    """, unsafe_allow_html=True)

    st.write("") # 간격

    # 데이터 생성
    dates = pd.date_range(start='2026-01-25', periods=8, freq='W')
    
    # 그래프 테마 설정: 요청에 따른 색상 변경 반영 (라인: 다크 그린, 텍스트: 진한 브라운)
    main_line_color = '#006400' # 다크 그린
    text_color = '#6F4E37' # 진한 브라운 (Coffee/Brown)

    def get_themed_chart(df, y_domain, y_axis_label='value'):
        base = alt.Chart(df).encode(
            x=alt.X('date', axis=alt.Axis(
                format='%b %d %Y', 
                labelOverlap=False, 
                labelFlush=False, 
                values=dates,
                title='날짜',
                labelColor=text_color,
                titleColor=text_color,
                tickColor=text_color,
                domainColor=text_color
            )),
            y=alt.Y('value', scale=alt.Scale(domain=y_domain), axis=alt.Axis(
                title=y_axis_label,
                labelColor=text_color,
                titleColor=text_color,
                tickColor=text_color,
                domainColor=text_color
            )),
            color=alt.value(main_line_color),
            tooltip=['date', 'value']
        ).properties(
            width=350,
            height=250
        )
        
        line = base.mark_line(size=5, strokeJoin='round', strokeCap='round')
        points = base.mark_circle(size=120)
        
        # Grid lines 스타일링
        grid = alt.Chart(df).mark_rule(color=text_color, opacity=0.1).encode(
            y='value',
            x='date'
        )

        return (grid + line + points).interactive()

    # 그래프 1: 매매 증감 추이
    st.markdown('<div class="graph-title-banner">📈 매매 증감 추이 (최근 8주)</div>', unsafe_allow_html=True)
    
    data1 = pd.DataFrame({
        'date': dates,
        'value': [0.2, 0.12, 0.6, 0.55, 0.08, 0.57, 0.3, 0.88]
    })
    
    chart1 = get_themed_chart(data1, [0, 0.9])
    st.altair_chart(chart1, use_container_width=True)


    # 그래프 2: 전세 증감 추이
    st.markdown('<div class="graph-title-banner">📈 전세 증감 추이 (최근 8주)</div>', unsafe_allow_html=True)
    
    data2 = pd.DataFrame({
        'date': dates,
        'value': [0.18, 0.12, 0.13, 0.2, 0.3, 0.02, 0.38, 0.19, 1.02]
    })
    # 데이터 포인트 맞추기 위해 마지막 포인트 제거 (8주)
    data2 = data2.iloc[:-1] 

    chart2 = get_themed_chart(data2, [0, 1.1])
    st.altair_chart(chart2, use_container_width=True)

    # 하단 간격 확보 (플로팅 버튼 고려)
    st.write("<br><br><br><br><br>", unsafe_allow_html=True)

# 하단 플로팅 버튼 영역
st.markdown("""
<div class="floating-bottom">
    <div class="icon-btn icon-share">📤</div>
    <div class="icon-btn icon-crown">👑</div>
</div>
""", unsafe_allow_html=True)

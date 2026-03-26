# ... (상단 설정 및 배경 로직 동일)

# 2. UI 디자인 및 스타일 설정 (색상 완벽 고정 버전)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Noto+Sans+KR:wght@300;500;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Noto+Sans+KR', sans-serif; }

    /* 타이틀 및 상단 선택창 스타일 */
    .brand-name { color: #006400 !important; font-size: 45px; font-weight: 900; font-family: 'Arial Black'; }
    .brand-suffix { color: #FF4500 !important; font-size: 24px; font-weight: 900; }
    div[data-baseweb="select"] * { font-weight: 900 !important; color: #006400 !important; }

    /* [복구] 랭킹 카드 공통 스타일 */
    .rank-card {
        padding: 12px 15px; border-radius: 12px; margin-bottom: 12px;
        display: flex; align-items: center; justify-content: space-between;
        background: linear-gradient(135deg, rgba(243, 229, 245, 0.95), rgba(225, 190, 231, 0.95)) !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1) !important;
    }
    
    /* 순위 숫자 색상 (진한 보라) */
    .rank-num { font-weight: 900 !important; font-size: 16px !important; color: #4a148c !important; margin-right: 8px; }

    /* 매매 랭킹 텍스트 색상 (브라운 계열) */
    .rank-m { border-left: 7px solid #FF4500 !important; }
    .rank-m .rank-name, .rank-m .rank-val { 
        color: #8B4513 !important; 
        font-weight: 900 !important; 
        font-size: 16px !important; 
    }

    /* 전세 랭킹 텍스트 색상 (청록 계열) */
    .rank-j { border-left: 7px solid #000080 !important; }
    .rank-j .rank-name, .rank-j .rank-val { 
        color: #008080 !important; 
        font-weight: 900 !important; 
        font-size: 16px !important; 
    }

    /* 버튼 스타일 유지 */
    div.stButton > button {
        width: 100% !important; height: 46px !important; border-radius: 12px !important;
        font-weight: 900 !important; font-size: 16px !important; color: #87CEEB !important;
        background: linear-gradient(135deg, rgba(60, 60, 60, 0.8), rgba(30, 30, 30, 0.9)) !important;
        border: 2px solid rgba(200, 200, 200, 0.6) !important;
        margin-top: 11px !important;
    }
    .screenshot-btn {
        width: 100%; height: 46px; border-radius: 12px; font-weight: 900; font-size: 16px; 
        color: #87CEEB !important; display: flex; justify-content: center; align-items: center;
        background: linear-gradient(135deg, rgba(60, 60, 60, 0.8), rgba(30, 30, 30, 0.9));
        border: 2px solid rgba(200, 200, 200, 0.6); margin-top: 20px;
    }

    header { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# ... (데이터 로드 부분 동일)

def main():
    # ... (상단 타이틀 및 선택창 로직 동일)

    # 매매 TOP 10 출력 부분
    st.markdown('<div class="chart-title" style="color:#FF4500; border-left:6px solid #FF4500; font-weight:900; padding-left:10px;">🔥 주간 매매 상승 TOP 10</div>', unsafe_allow_html=True)
    # (데이터 처리 생략)
    for i, (name, val) in enumerate(top_mw.items()):
        st.markdown(f'''
            <div class="rank-card rank-m">
                <div class="rank-info">
                    <span class="rank-num">{i+1}위</span> 
                    <span class="rank-name">{name}</span>
                </div>
                <span class="rank-val">+{val:.2f}%</span>
            </div>
        ''', unsafe_allow_html=True)

    # 전세 TOP 10 출력 부분
    st.markdown('<div class="chart-title" style="color:#FF1493; border-left:6px solid #FF1493; font-weight:900; padding-left:10px;">💧 주간 전세 상승 TOP 10</div>', unsafe_allow_html=True)
    # (데이터 처리 생략)
    for i, (name, val) in enumerate(top_jw.items()):
        st.markdown(f'''
            <div class="rank-card rank-j">
                <div class="rank-info">
                    <span class="rank-num">{i+1}위</span> 
                    <span class="rank-name">{name}</span>
                </div>
                <span class="rank-val">+{val:.2f}%</span>
            </div>
        ''', unsafe_allow_html=True)

    # ... (하단 버튼 로직 동일)

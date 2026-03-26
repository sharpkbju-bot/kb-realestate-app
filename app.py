# ... (기존 상단 코드 동일)

# 2. UI 디자인 및 스타일 설정 (CSS 보강)
st.markdown("""
    <style>
    /* ... (기존 랭킹 카드 및 텍스트 스타일 동일) ... */

    /* [최종 해결] 종료 버튼 사이즈를 스크린샷 버튼과 100% 일치시킴 */
    div[data-testid="stVerticalBlock"] > div:has(> div.stButton) {
        width: 100% !important;
        padding: 0px !important;
        margin: 0px !important;
    }

    div.stButton {
        width: 100% !important;
    }

    div.stButton > button {
        /* 너비를 100%로 강제하고 절대 줄어들지 않게 설정 */
        width: 100% !important; 
        min-width: 100% !important;
        display: flex !important;
        flex: 1 1 auto !important;
        
        height: 46px !important; 
        border-radius: 12px !important;
        font-weight: 900 !important; 
        font-size: 16px !important; 
        color: #87CEEB !important;
        background: linear-gradient(135deg, rgba(60, 60, 60, 0.8), rgba(30, 30, 30, 0.9)) !important;
        border: 2px solid rgba(200, 200, 200, 0.6) !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3) !important;
        margin-top: 11px !important; 
        transition: all 0.3s ease !important;
        justify-content: center !important;
        align-items: center !important;
    }

    /* 스크린샷용 디자인 버튼 (종료 버튼과 완벽 대칭) */
    .screenshot-btn {
        width: 100%; 
        box-sizing: border-box; /* 패딩 포함 너비 계산 */
        height: 46px; 
        border-radius: 12px; 
        font-weight: 900; 
        font-size: 16px; 
        color: #87CEEB !important; 
        display: flex; 
        justify-content: center; 
        align-items: center;
        background: linear-gradient(135deg, rgba(60, 60, 60, 0.8), rgba(30, 30, 30, 0.9));
        border: 2px solid rgba(200, 200, 200, 0.6); 
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        cursor: pointer; 
        margin-top: 20px;
    }
    
    /* ... (나머지 CSS 동일) ... */
    </style>
    """, unsafe_allow_html=True)

# ... (데이터 로드 및 메인 UI 코드 동일)

    # 하단 버튼 그룹
    st.markdown('<div id="btn-screenshot" class="screenshot-btn">📸 화면 스크린샷</div>', unsafe_allow_html=True)
    
    # 🚪 앱 종료 버튼 (이제 위 버튼과 정확히 같은 너비로 표시됩니다)
    if st.button("🚪 앱 종료", key="exit_trigger"):
        st.session_state.is_exit = True
        st.rerun()

# ... (스크립트 부분 동일)

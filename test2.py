import streamlit as st
import random

st.set_page_config(page_title="3전 2선승제 가위바위보", layout="centered")

st.title("✊ ✋ ✌️ 3전 2선승제 가위바위보 게임")

# 이모지 딕셔너리
choices = ["가위", "바위", "보"]
emojis = {"가위": "✌️", "바위": "✊", "보": "✋"}

# 세션 상태 초기화
if "user_score" not in st.session_state:
    st.session_state.user_score = 0
    st.session_state.computer_score = 0
    st.session_state.round = 1
    st.session_state.game_over = False
    st.session_state.result = ""

# 게임 종료 시 메시지 표시
if st.session_state.game_over:
    st.subheader(st.session_state.result)
    if st.button("🔁 다시 시작"):
        st.session_state.user_score = 0
        st.session_state.computer_score = 0
        st.session_state.round = 1
        st.session_state.game_over = False
        st.session_state.result = ""
    st.stop()

# 현재 스코어 및 라운드 표시
st.markdown(f"**🧮 현재 스코어:** 당신 {st.session_state.user_score} : {st.session_state.computer_score} 컴퓨터")
st.markdown(f"**📍 라운드 {st.session_state.round}**")

# 사용자 선택
player_choice = st.radio("무엇을 내시겠어요?", choices, horizontal=True)

if st.button("대결!"):
    computer_choice = random.choice(choices)

    st.write(f"👤 당신의 선택: {emojis[player_choice]} {player_choice}")
    st.write(f"💻 컴퓨터의 선택: {emojis[computer_choice]} {computer_choice}")

    # 승패 판정
    if player_choice == computer_choice:
        result_text = "🤝 비겼습니다!"
    elif (
        (player_choice == "가위" and computer_choice == "보") or
        (player_choice == "바위" and computer_choice == "가위") or
        (player_choice == "보" and computer_choice == "바위")
    ):
        st.session_state.user_score += 1
        result_text = "🎉 당신이 이겼습니다!"
    else:
        st.session_state.computer_score += 1
        result_text = "😢 컴퓨터가 이겼습니다!"

    st.session_state.round += 1
    st.write(result_text)

    # 승리 조건 확인
    if st.session_state.user_score == 2:
        st.session_state.game_over = True
        st.session_state.result = "🏆 당신이 최종 승자입니다!"
    elif st.session_state.computer_score == 2:
        st.session_state.game_over = True
        st.session_state.result = "💻 컴퓨터가 최종 승자입니다!"


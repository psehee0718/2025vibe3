import streamlit as st
import random

st.set_page_config(page_title="가위바위보 게임", layout="centered")

st.title("✊ ✋ ✌️ 가위바위보 게임")
st.write("당신의 선택으로 컴퓨터와 대결해보세요!")

# 선택지
choices = ["가위", "바위", "보"]
emojis = {"가위": "✌️", "바위": "✊", "보": "✋"}

# 사용자 선택
player_choice = st.radio("무엇을 내시겠어요?", choices, horizontal=True)

if st.button("대결 시작!"):
    computer_choice = random.choice(choices)

    st.write(f"👤 당신의 선택: {emojis[player_choice]} {player_choice}")
    st.write(f"💻 컴퓨터의 선택: {emojis[computer_choice]} {computer_choice}")

    # 승부 결정
    if player_choice == computer_choice:
        result = "비겼습니다! 😐"
    elif (
        (player_choice == "가위" and computer_choice == "보") or
        (player_choice == "바위" and computer_choice == "가위") or
        (player_choice == "보" and computer_choice == "바위")
    ):
        result = "당신이 이겼습니다! 🎉"
    else:
        result = "컴퓨터가 이겼습니다! 😢"

    st.subheader(result)


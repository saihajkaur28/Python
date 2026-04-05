import streamlit as st
import random
import time

# ---------- SESSION STATE INITIALIZATION ----------
if "score" not in st.session_state:
    st.session_state.score = 0

if "round_scores" not in st.session_state:
    st.session_state.round_scores = []

if "secret_number" not in st.session_state:
    st.session_state.secret_number = None

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "max_num" not in st.session_state:
    st.session_state.max_num = 0

if "attempt_count" not in st.session_state:
    st.session_state.attempt_count = 0

if "hint_used" not in st.session_state:
    st.session_state.hint_used = False

if "start_time" not in st.session_state:
    st.session_state.start_time = 0.0

# ---------- UI ----------
st.title("🎮 Number Guessing Game")

st.subheader("Main Menu")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("New Game"):
        st.session_state.score = 0
        st.session_state.round_scores.clear()
        st.session_state.secret_number = None
        st.success("🆕 New Game started. Score reset.")

with col2:
    if st.button("Continue"):
        st.info("▶️ Continue game. Choose difficulty below.")

with col3:
    if st.button("View Score"):
        st.subheader("SCOREBOARD 📊")
        if not st.session_state.round_scores:
            st.write("No rounds played yet.")
        else:
            for i, rs in enumerate(st.session_state.round_scores, 1):
                st.write(f"Round {i} : {rs} points")
            st.write(f"**Total Score : {st.session_state.score}**")

with col4:
    st.write("")  # placeholder (Exit is just closing the tab)

# ---------- DIFFICULTY ----------
st.subheader("Select Difficulty")

dcol1, dcol2, dcol3 = st.columns(3)

def start_round(max_num, attempts):
    st.session_state.max_num = max_num
    st.session_state.attempts = attempts
    st.session_state.secret_number = random.randint(1, max_num)
    st.session_state.attempt_count = 0
    st.session_state.hint_used = False
    st.session_state.start_time = time.time()
    st.info(f"🎯 Number chosen between 1 and {max_num}. Attempts: {attempts}")

with dcol1:
    if st.button("Easy"):
        start_round(10, 5)

with dcol2:
    if st.button("Medium"):
        start_round(50, 7)

with dcol3:
    if st.button("Hard"):
        start_round(100, 10)

# ---------- GAMEPLAY ----------
if st.session_state.secret_number is not None:
    guess = st.number_input(f"Enter your guess (1-{st.session_state.max_num})",  #if dificulty is 10, then it will be 1-10
        min_value=1,
        max_value=st.session_state.max_num,
        step=1
    )

    if st.button("Submit Guess"):
        st.session_state.attempt_count += 1

        if guess == st.session_state.secret_number:
            time_taken = round(time.time() - st.session_state.start_time, 2)   #current time - time taken 

            round_score = 1
            if st.session_state.hint_used:
                round_score -= 0.5

            st.session_state.score += round_score
            st.session_state.round_scores.append(round_score)

            st.success(
                f"🎉 Correct! Number: {st.session_state.secret_number}\n"
                f"Attempts: {st.session_state.attempt_count} | Time: {time_taken}s\n"
                f"Round Score: {round_score}"
            )

            st.session_state.secret_number = None  #reset for new game

        elif st.session_state.attempt_count >= st.session_state.attempts:
            st.session_state.round_scores.append(0)
            st.error(
                f"😞 Game Over! Number was {st.session_state.secret_number}\n"
                f"Round Score: 0"
            )
            st.session_state.secret_number = None

        else:
            st.warning(
                f"❌ Wrong guess! Attempt "   #to show code clean, f is used in two lines
                f"{st.session_state.attempt_count}/{st.session_state.attempts}"
            )

    # ---------- HINT ----------
    if st.button("Get Hint"):
        st.session_state.hint_used = True
        diff = abs(st.session_state.secret_number - guess)

        if diff > st.session_state.max_num // 2:
            st.info("🥶 Very Cold! Very Far")
        elif diff > st.session_state.max_num // 4:
            st.info("❄️ Cold! Far")
        elif diff > st.session_state.max_num // 10:
            st.info("🌤️ Warm! Close")
        else:
            st.info("🔥 Hot! Very Close")


# Print This Every Time to run the code
# cd App
#& "C:/Program Files/Python314/python.exe" -m streamlit run GuessNoApp.py            

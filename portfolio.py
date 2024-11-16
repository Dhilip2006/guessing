import streamlit as st

# Title and Instructions
st.title("Guessing Game: User vs. Computer")
st.write("Try to guess the number the computer has in mind, or let the computer guess your number!")

# Initialize Game State
if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "target_number" not in st.session_state:
    st.session_state.target_number = None
if "attempts" not in st.session_state:
    st.session_state.attempts = 0
if "computer_min" not in st.session_state:
    st.session_state.computer_min = None
if "computer_max" not in st.session_state:
    st.session_state.computer_max = None
if "computer_guess" not in st.session_state:
    st.session_state.computer_guess = None
if "user_turn" not in st.session_state:
    st.session_state.user_turn = True

# Input Range and Attempts
min_value = st.number_input("Enter the minimum value of the range:", value=1, step=1)
max_value = st.number_input("Enter the maximum value of the range:", value=100, step=1)
max_attempts = st.slider("Select the maximum number of attempts:", 1, 20, 7)

# Start Game Button
if st.button("Start Game"):
    if max_value > min_value:
        st.session_state.game_started = True
        st.session_state.target_number = st.number_input(
            f"Enter a secret number between {min_value} and {max_value} (only you know this):",
            min_value=min_value,
            max_value=max_value,
        )
        st.session_state.computer_min = min_value
        st.session_state.computer_max = max_value
        st.session_state.attempts = 0
        st.session_state.user_turn = True
        st.success("Game started! The computer will now try to guess.")
    else:
        st.error("Maximum value must be greater than the minimum value.")

# Game Logic
if st.session_state.game_started:
    if st.session_state.attempts < max_attempts:
        if st.session_state.user_turn:
            st.write("Computer's turn to guess...")
            guess = (st.session_state.computer_min + st.session_state.computer_max) // 2
            st.session_state.computer_guess = guess
            st.write(f"The computer guesses: {guess}")

            feedback = st.radio("Provide feedback:", ["Too Low", "Too High", "Correct"], key="feedback")
            if feedback == "Too Low":
                st.session_state.computer_min = guess + 1
            elif feedback == "Too High":
                st.session_state.computer_max = guess - 1
            elif feedback == "Correct":
                st.success("The computer guessed your number!")
                st.session_state.game_started = False

            st.session_state.user_turn = False
        else:
            user_guess = st.number_input("Your turn! Guess the computer's number:", min_value=min_value, max_value=max_value)
            if user_guess == st.session_state.target_number:
                st.success("You guessed the computer's number!")
                st.session_state.game_started = False
            elif user_guess < st.session_state.target_number:
                st.warning("Too low!")
            else:
                st.warning("Too high!")
            st.session_state.user_turn = True

        st.session_state.attempts += 1
    else:
        st.error("Game Over! Maximum attempts reached.")
        st.session_state.game_started = False

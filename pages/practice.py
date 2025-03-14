import streamlit as st
import sqlite3

# Function to fetch a random word
def Get_random_word():
    conn = sqlite3.connect("flashcards.db")
    c = conn.cursor()
    c.execute('''
    SELECT Word, Sentence, Translation
    FROM flashcards
    ORDER BY RANDOM()
    LIMIT 1;
    ''')
    row = c.fetchone()
    conn.close()
    return row

# Initialize session state if not set
if "word_data" not in st.session_state:
    st.session_state.word_data = Get_random_word()
    st.session_state.show_answer = False  # Track if answer should be shown

# Display the word
if st.session_state.word_data:
    st.success("Here is a randomly selected word")
    st.table({"Word": [st.session_state.word_data[0]]})
    if st.button("Show it in sentence"):
        st.table({"Sentence": [st.session_state.word_data[1]]})
else:
    st.warning("No flashcards found.")

# Show Answer button
if st.button("Show Answer"):
    st.session_state.show_answer = True
    st.rerun()
# Display answer if button was clicked
if st.session_state.show_answer and st.session_state.word_data:
    st.table({"Translation": [st.session_state.word_data[2]]})
    # st.success("Here is the answer to the randomly selected word!")

# Shuffle Again button
st.write("-------------------------------------------------------")
if st.button("Shuffle"):
    st.session_state.word_data = Get_random_word()
    st.session_state.show_answer = False  # Reset answer visibility
    st.rerun()
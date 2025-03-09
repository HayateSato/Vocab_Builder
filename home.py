import time

import streamlit as st

if 'page' not in st.session_state:
    st.session_state.page = "Home"

st.title("Welcome to the Flashcard App!")




# Navigation Buttons
if st.button("Go to add your cards"):
    st.session_state.page = "main"
    with st.spinner("Loading..."):
        time.sleep(0.9)

if st.button("Go to Flashcards"):
    st.session_state.page = "flashcard"
    with st.spinner("Loading..."):
        time.sleep(0.9)

if st.session_state.page == "main":
    if __name__ == '__main__':
        import main

if st.session_state.page == "Flashcards_db":
    import pages.flashcards
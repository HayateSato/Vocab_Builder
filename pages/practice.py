import streamlit as st
import sqlite3

# Function to fetch a random word
def get_random_word():
    conn = sqlite3.connect("flashcards.db")
    c = conn.cursor()
    c.execute('''
    SELECT Word, Translation
    FROM flashcards
    ORDER BY RANDOM()
    LIMIT 1;
    ''')
    row = c.fetchone()
    conn.close()
    return row

# Initialize session state if not set
if "word_data" not in st.session_state:
    st.session_state.word_data = get_random_word()
    st.session_state.show_answer = False  # Track if answer should be shown

# Display the word
if st.session_state.word_data:
    st.table({"Word": [st.session_state.word_data[0]]})
    st.success("Here is a randomly selected word!")
else:
    st.warning("No flashcards found.")

# Show Answer button
if st.button("Show Answer"):
    st.session_state.show_answer = True
    st.rerun()

# Display answer if button was clicked
if st.session_state.show_answer and st.session_state.word_data:
    st.table({"Translation": [st.session_state.word_data[1]]})
    st.success("Here is the answer to the randomly selected word!")

# Shuffle Again button
if st.button("Shuffle Again"):
    st.session_state.word_data = get_random_word()
    st.session_state.show_answer = False  # Reset answer visibility
    st.rerun()




# import streamlit as st
# import sqlite3
#
# # Connect to the database
# conn = sqlite3.connect("flashcards.db")
# c = conn.cursor()
#
# # Execute query with LIKE operator to filter tags
# c.execute('''
# SELECT Word, Translation
# FROM flashcards
# ORDER BY RANDOM()
# LIMIT 1;
# ''',)
# row = c.fetchone()  # Fetch one random row
#
# if row:
#     st.table({"Word": [row[0]]})
#     st.success("Here is a randomly selected word!")
# else:
#     st.warning("No flashcards found.")
#
#
#
# if st.button("Show Answer"):
#     if row:
#         st.table({"Translation": [row[1]]})
#         st.success("Here is a answer to the randomly selected word!")
#     else:
#         st.warning("No flashcards found.")
#
# if st.button("Shuffle Again"):
#     st.rerun()
#
# # Close the connection
# conn.close()
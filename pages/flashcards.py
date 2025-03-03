import streamlit as st
import sqlite3

st.title("📄 Saved Flashcards")

# Connect to the database
conn = sqlite3.connect("flashcards.db")
c = conn.cursor()

# Fetch all flashcards
c.execute("SELECT rowid, word, translation FROM flashcards")
rows = c.fetchall()

if rows:
    st.table({"Word": [row[1] for row in rows], "Translation": [row[2] for row in rows]})

    if st.button("Delete Duplicates"):
        try:
            # Find duplicates and keep only one
            c.execute('''
                DELETE FROM flashcards
                WHERE rowid NOT IN (
                    SELECT MIN(rowid)
                    FROM flashcards
                    GROUP BY word, translation
                )
            ''')
            conn.commit()
            st.success("Duplicate flashcards deleted successfully!")
            # st.experimental_rerun()  # Refresh page after deletion
        except Exception as e:
            st.error(f"Failed to delete duplicates: {e}")
else:
    st.info("No flashcards saved yet.")

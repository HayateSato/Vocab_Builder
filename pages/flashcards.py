import streamlit as st
import sqlite3
import pandas as pd

st.title("📄 Saved Flashcards")

# Connect to the database
conn = sqlite3.connect("flashcards.db")
c = conn.cursor()

# Fetch all flashcards
c.execute("SELECT word, sentence, translation, tags FROM flashcards")
rows = c.fetchall()

if rows:
    st.table({"Word": [row[0] for row in rows], "Sentence": [row[1] for row in rows], "Translation":[row[2] for row in rows], "Tags": [row[3] for row in rows]})

    # Filter -----------------------------------------------------
    # Fetch all tags
    Existing_tags = c.execute('''SELECT tags FROM flashcards;''').fetchall()
    conn.commit()

    # Flatten list of tuples into a list of strings
    existing_tags = [tag[0] for tag in Existing_tags]

    selectable_tags = [" "]

    # Split tags with commas and remove spaces
    for tag in existing_tags:
        if "," in tag:
            split_tags = tag.split(",")
            for split_tag in split_tags:
                selectable_tags.append(split_tag.strip())
        else:
            selectable_tags.append(tag.strip())

    # Remove duplicates, convert to lowercase, and sort alphabetically
    selectable_tags = sorted(set(tag.lower() for tag in selectable_tags))

    # Selectbox for filtering
    selected_tags = st.selectbox("Filter your cards", selectable_tags)

    if selected_tags != " ":
        # Execute query with LIKE operator to filter tags
        c.execute('''
        SELECT * 
        FROM flashcards
        WHERE tags LIKE ?;
        ''', (f"%{selected_tags}%",))
        rows = c.fetchall()  # Fetch the filtered results
        conn.commit()

        if rows:
            st.table({"Word": [row[2] for row in rows],  "Sentence": [row[0] for row in rows], "Translation": [row[1] for row in rows],
                      "Tags": [row[3] for row in rows]})
            # st.success("The result of filtered flashcards cabinets!")
        else:
            st.warning("No flashcards found for the selected tag.")

# manual search -------------------------------------------------------------------------------
    st.write("-------------------------------------------------------")
    st.subheader("Search Flashcards")
    search_term = st.text_input("Enter word to search:")
    if st.button("Search"):
        c.execute("SELECT word, sentence, translation FROM flashcards WHERE word LIKE ?", (f"%{search_term}%",))
        results = c.fetchall()
        if results:
            if results:
                df = pd.DataFrame(results, columns=["Word", "Sentence", "Translation"])
                st.table(df)
        else:
            st.error("No matching flashcards found.")
else:
    st.info("No flashcards saved yet.")

# Delete Functionality  --------------------------------------------------------
st.write("-------------------------------------------------------")
st.subheader("Delete Flashcard")
delete_word = st.text_input("Enter word to delete:")
if st.button("Delete"):
    c.execute("DELETE FROM flashcards WHERE word = ?", (delete_word,))
    conn.commit()
    st.success(f"Flashcard for '{delete_word}' deleted successfully!")

    # Duplicate --------------------------------------------------
    # if st.button("Delete Duplicates"):
    #     try:
    #         # Find duplicates and keep only one
    #         c.execute('''
    #             DELETE FROM flashcards
    #             WHERE rowid NOT IN (
    #                 SELECT MIN(rowid)
    #                 FROM flashcards
    #                 GROUP BY word, translation
    #             )
    #         ''')
    #         conn.commit()
    #         st.success("Duplicate flashcards deleted successfully!")
    #         # st.experimental_rerun()  # Refresh page after deletion
    #     except Exception as e:
    #         st.error(f"Failed to delete duplicates: {e}")


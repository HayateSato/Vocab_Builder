import streamlit as st
import sqlite3

st.title("📄 Saved Flashcards")

# Connect to the database
conn = sqlite3.connect("flashcards.db")
c = conn.cursor()

# Fetch all flashcards
c.execute("SELECT rowid, word, tags translation FROM flashcards")
rows = c.fetchall()

if rows:
    st.table({"Word": [row[0] for row in rows], "Translation": [row[1] for row in rows], "Tags": [row[2] for row in rows]})

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
    Selected_tags = st.selectbox("Filter your cards", selectable_tags)

    if Selected_tags != " ":
        # Execute query with LIKE operator to filter tags
        c.execute('''
        SELECT * 
        FROM flashcards
        WHERE tags LIKE ?;
        ''', (f"%{Selected_tags}%",))
        rows = c.fetchall()  # Fetch the filtered results
        conn.commit()

        if rows:
            st.table({"Word": [row[0] for row in rows], "Translation": [row[1] for row in rows],
                      "Tags": [row[2] for row in rows]})
            st.success("The result of filtered flashcards cabinets!")
        else:
            st.warning("No flashcards found for the selected tag.")

    # Duplicate --------------------------------------------------
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

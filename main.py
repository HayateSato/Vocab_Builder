import streamlit as st
from transformers import pipeline
from PIL import Image
import pytesseract
import sqlite3
import re

# Initialize translation pipeline
translator = pipeline("translation_en_to_de", model="Helsinki-NLP/opus-mt-de-en")

# Database setup
conn = sqlite3.connect("flashcards.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS flashcards (word TEXT, translation TEXT, tags TEXT)''')
conn.commit()

# new_column = "tags"
#
# # Check if the column exists
# c.execute("PRAGMA table_info(flashcards)")
# columns = [column[1] for column in c.fetchall()]
#
# # Add new column if not already present
# if new_column not in columns:
#     c.execute(f"ALTER TABLE flashcards ADD COLUMN {new_column} TEXT")
#     conn.commit()


# Streamlit UI
st.title("Flashcard Maker 📚")
st.write("Upload an image with a single word, and I'll create a memorization card for you!")

st.subheader("You Input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=False)

    # OCR with Tesseract
    text = pytesseract.image_to_string(image).strip()
    text = re.sub(r'[.,?@]$', '', text)
    ### anything inside [ ] will be replaced.
    ### $ means if anything inside [ ] is found at the end

    if text:
        st.subheader("Translation")
        try:
            result = translator(text)
            translation = result[0]['translation_text']
            st.markdown(f"**Original:** {text}\n\n**Meaning:** {translation}")

            tags = st.text_input("Add Tags (comma-separated, e.g., noun, sports)")

            if st.button("Save Flashcard"):
                c.execute("INSERT INTO flashcards (word, translation, tags) VALUES (?, ?, ?)", (text, translation, tags))
                conn.commit()
                st.success("Flashcard saved successfully!")
        except Exception as e:
            st.error(f"Translation failed: {e}")
    else:
        st.error("No text detected.")

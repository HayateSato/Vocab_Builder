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

# Streamlit UI
st.title("Flashcard Maker 📚")
st.write("Upload an image with a single word, and I'll create a memorization card for you!")

st.subheader("You Input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])


def translate(input_text):
    translated_results = translator(input_text)
    translated_results = [result['translation_text'] for result in translated_results]
    # translated_result = result[0]['translation_text']
    for i, translation in enumerate(translated_results):
        st.markdown(f"**Translation {i + 1}:** {translation}")
    return translation


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
            translation = translate(text)
            # results = translator(text)
            # st.write(len(results))
            # translations = [result['translation_text'] for result in results]
            # for i, translation in enumerate(translations):
            #     st.markdown(f"**Translation {i + 1}:** {translation}")

            tags = st.text_input("Add Tags (comma-separated, e.g., noun, sports)")

            if st.button("Save Flashcard"):
                c.execute("INSERT INTO flashcards (word, translation, tags) VALUES (?, ?, ?)", (text, ", ".join(translation), tags))
                conn.commit()
                st.success("Flashcard saved successfully!")
        except Exception as e:
            st.error(f"Translation failed: {e}")
    else:
        st.error("No text detected.")


else:
    typed = st.text_input("Type here:")
    text = typed.strip()
    text = re.sub(r'[.,?@]$', '', text)

    if text:
        st.subheader("Translation")
        try:
            translation = translate(text)
            # results = translator(text)
            # st.write(len(results))
            # translations = [result['translation_text'] for result in results]
            # for i, translation in enumerate(translations):
            #     st.markdown(f"**Translation {i + 1}:** {translation}")


            tags = st.text_input("Add Tags (comma-separated, e.g., noun, sports)")

            if st.button("Save Flashcard"):
                c.execute("INSERT INTO flashcards (word, translation, tags) VALUES (?, ?, ?)", (text, ", ".join(translation), tags))
                conn.commit()
                st.success("Flashcard saved successfully!")
        except Exception as e:
            st.error(f"Translation failed: {e}")
    else:
        st.error("No text detected.")




# # st.session_state.page = "main"
#
# st.title("Add your flashcard!")
#
# if st.button("Go to Flashcards"):
#     st.session_state.page = "Flashcards_db"
#     # st.experimental_rerun()
#
# if st.button("Go to Home"):
#     st.session_state.page = "Home"
#     # st.experimental_rerun()



### adding new column
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

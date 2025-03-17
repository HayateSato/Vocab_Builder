import streamlit as st
# from sympy.strategies.branch import notempty
from transformers import pipeline
# from PIL import Image
# import pytesseract
import sqlite3
import re

# Initialize translation pipeline
translator = pipeline("translation_en_to_de", model="Helsinki-NLP/opus-mt-de-en")

# Database setup
conn = sqlite3.connect("flashcards.db")
c = conn.cursor()

# Streamlit UI
st.title("Flashcard Maker 📚")
st.write("Copy & Paste any sentence or upload a photo with sentence.")
st.write("I will translate it for you and you can create a flashcard for you!")
st.write("-------------------------------------------------------")

st.subheader("Your Input")
typed = st.text_input("Write your sentence here:")
uploaded_file = st.file_uploader("Or upload an image if you're too lazy to type...", type=["jpg", "jpeg", "png"])

st.write("-------------------------------------------------------")
st.subheader("Translation")

if typed.strip():
    typed_sentence = typed.strip()
    typed_sentence = re.sub(r'[.,?@]$', '', typed_sentence)

    if typed_sentence is not " ":
        try:
            results = translator(typed_sentence)
            translations = [result['translation_text'] for result in results]


            st.write(f"- your input: {typed_sentence}")
            st.write(f"- your output: {translations[0]}")
            selected_word = st.text_input("Which word do you want to remember? (this will be on your flashcard)")
            tags = st.text_input("Add Tags (comma-separated, e.g., noun, sports)")

            if st.button("Save Flashcard"):
                c.execute("INSERT INTO flashcards (sentence, translation, word, tags) VALUES (?, ?, ?, ?)",
                          (typed_sentence, ", ".join(translations), selected_word, tags))
                conn.commit()
                st.success("Flashcard saved successfully!")
        except Exception as e:
            st.error(f"Translation failed: {e}")
    else:
        st.error("No text detected.")


# if uploaded_file is not None:
#     # Display the image
#     image = Image.open(uploaded_file)
#     st.write(f"- Uploaded Image :")
#     st.image(image, use_container_width=False)
#
#     # extract the text | OCR with Tesseract
#     sentence = pytesseract.image_to_string(image).strip()
#     # st.write(f"after parsing: {sentence}")
#     # text = re.sub(r'[.?@]$', '', text)
#     ### anything inside [ ] will be replaced.
#     ### $ means if anything inside [ ] is found at the end
#
#     if uploaded_file is not None:
#         try:
#             results = translator(sentence)
#             if isinstance(results, list) and len(results) > 0 and 'translation_text' in results[0]:
#                 translation_text = results[0]['translation_text']
#             else:
#                 translation_text = "Translation not available"
#
#             st.write(f"- your input: {sentence}")
#             st.write(f"- your output: {results[0]['translation_text']}")
#             selected_word = st.text_input("Which word do you want to remember? (this will be on your flashcard)")
#             tags = st.text_input("Add Tags (comma-separated, e.g., noun, sports)")
#
#             if st.button("Save Flashcard"):
#                 c.execute("INSERT INTO flashcards (sentence, translation, word, tags) VALUES (?, ?, ?, ?)",
#                           (sentence, results, selected_word, tags))
#                 conn.commit()
#                 st.success("Flashcard saved successfully!")
#         except Exception as e:
#             st.error(f"Translation failed: {e}")


st.write("-------------------------------------------------------")

if st.button("Go to Flashcards"):
    st.session_state.page = "pages/flashcards.py"


if st.button("Go to Practice"):
    st.session_state.page = "pages/practice.py"
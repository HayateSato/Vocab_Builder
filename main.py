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

# Streamlit UI
st.title("Flashcard Maker 📚")
st.write("Upload an screenshot of a sentence, and I'll create a memorization card for you!")

st.subheader("Your Input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=False)

    # OCR with Tesseract
    sentence = pytesseract.image_to_string(image).strip()
    # st.write(f"after parsing: {sentence}")
    # text = re.sub(r'[.?@]$', '', text)
    ### anything inside [ ] will be replaced.
    ### $ means if anything inside [ ] is found at the end

    if uploaded_file is not None:
        st.write("-------------------------------------------------------")
        st.subheader("Translation")
        try:
            # text = re.sub(r'[.,?@]$', '', text)
            # parsed_word = input_words.append(text.split())
            # parsed_word = set(sentence.split())
            # parsed_word = [re.sub(r'[.,?@]$', '') for w in parsed_word]
            # selected_word = st.text_input("Which word do you want to remember?", parsed_word)

            results = translator(sentence)
            translations = [result['translation_text'] for result in results]
            # st.write(f"temporal translation: {translations}")
            # for translation in enumerate(translations):
            #     st.markdown(f"**Translation:** {translation} **")

            st.write(f"- your input: {sentence}")
            st.write(f"- your output: {translations[0]}")
            selected_word = st.text_input("Which word do you want to remember?")
            tags = st.text_input("Add Tags (comma-separated, e.g., noun, sports)")

            if st.button("Save Flashcard"):
                c.execute("INSERT INTO flashcards (sentence, translation, word, tags) VALUES (?, ?, ?, ?)",
                          (sentence, ", ".join(translations), selected_word, tags))
                conn.commit()
                st.success("Flashcard saved successfully!")
        except Exception as e:
            st.error(f"Translation failed: {e}")



typed = st.text_input("Or write here directly:")
if typed is not None:
    typed_sentence = typed.strip()
    typed_sentence = re.sub(r'[.,?@]$', '', typed_sentence)

    if typed_sentence is not None:
        st.write("-------------------------------------------------------")
        st.subheader("Translation")
        try:
            results = translator(typed_sentence)
            translations = [result['translation_text'] for result in results]
            # for translation in enumerate(translations):
            #     st.markdown(f"**Translation:** {translation}")

            st.write(f"- your input: {typed_sentence}")
            st.write(f"- your output: {translations[0]}")
            selected_word = st.text_input("Which word do you want to remember?")
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


st.write("-------------------------------------------------------")

if st.button("Go to Flashcards"):
    st.session_state.page = "Flashcards_db"


if st.button("Go to Home"):
    st.session_state.page = "Home"

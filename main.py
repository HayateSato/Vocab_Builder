import streamlit as st
from transformers import pipeline
from PIL import Image
import pytesseract
import sqlite3

# Initialize translation pipeline
translator = pipeline("translation_en_to_de", model="Helsinki-NLP/opus-mt-de-en")

# Database setup
conn = sqlite3.connect("flashcards.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS flashcards (word TEXT, translation TEXT)''')
conn.commit()



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
    # st.write("Extracting text from image...")
    text = pytesseract.image_to_string(image).strip()

    if text:
        # Translate the word
        st.subheader("Translation")

        # st.write("Translating into German...")
        translation = translator(text)[0]['translation_text']
        st.markdown(
            f"""
            - Original: {text}
            - Meaning:  {translation}
            """
        )

        # Flashcard Preview
        st.subheader("Flashcard")
        # st.write(f"Word: {text}")
        # st.write(f"Meaning: {translation}")

        # Save to Database
        if st.button("Save Flashcard"):
            c.execute("INSERT INTO flashcards (word, translation) VALUES (?, ?)", (text, translation))
            conn.commit()
            st.success("Flashcard saved successfully!")
    else:
        st.error("No text detected. Please try again with a clearer image.")
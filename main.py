import streamlit as st
from transformers import pipeline
from PIL import Image
import pytesseract
import sqlite3
import re
# from sentence_transformers import SentenceTransformer, util

# Initialize translation pipeline
translator = pipeline("translation_en_to_de", model="Helsinki-NLP/opus-mt-de-en")
# sbert_model = SentenceTransformer("all-MiniLM-L6-v2")  # input text longer than 256 word pieces is truncated.

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

st.subheader("Your Input")
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
            results = translator(text)
            translations = [result['translation_text'] for result in results]
            for i, translation in enumerate(translations):
                st.markdown(f"**Translation {i + 1}:** {translation}")

            tags = st.text_input("Add Tags (comma-separated, e.g., noun, sports)")

            if st.button("Save Flashcard"):
                c.execute("INSERT INTO flashcards (word, translation, tags) VALUES (?, ?, ?)",
                          (text, ", ".join(translations), tags))
                conn.commit()
                st.success("Flashcard saved successfully!")
        except Exception as e:
            st.error(f"Translation failed: {e}")
    else:
        st.error("No text detected.")

st.subheader("Your Input")
typed = st.text_input("Or write here directly:")
if typed is not None:
    typed_text = typed.strip()
    typed_text = re.sub(r'[.,?@]$', '', typed_text)

    if typed_text:
        st.subheader("Translation")
        try:
            results = translator(typed_text)
            translations = [result['translation_text'] for result in results]
            for i, translation in enumerate(translations):
                st.markdown(f"**Translation {i + 1}:** {translation}")

            tags = st.text_input("Add Tags (comma-separated, e.g., noun, sports)")

            if st.button("Save Flashcard"):
                c.execute("INSERT INTO flashcards (word, translation, tags) VALUES (?, ?, ?)",
                          (typed_text, ", ".join(translations), tags))
                conn.commit()
                st.success("Flashcard saved successfully!")
        except Exception as e:
            st.error(f"Translation failed: {e}")
    else:
        st.error("No text detected.")


    # if text:
    #     st.subheader("Translation")
    #
    #     try:
    #         # # Generate SBERT sentence embeddings to understand context
    #         # text_embedding = sbert_model.encode(text, convert_to_tensor=True)
    #
    #         # Perform translation
    #         results = translator(text)
    #         translations = [result['translation_text'] for result in results]
    #
    #         # Generate embeddings for translated sentences
    #         # translation_embeddings = [sbert_model.encode(t, convert_to_tensor=True) for t in translations]
    #
    #         # Compute similarity scores to find the best contextual translation
    #         # similarity_scores = [util.pytorch_cos_sim(text_embedding, te).item() for te in translation_embeddings]
    #         # best_translation_idx = similarity_scores.index(max(similarity_scores))  # Best match
    #
    #         # Display all translations with scores
    #         # for i, (translation, score) in enumerate(zip(translations, similarity_scores)):
    #         #     st.markdown(f"**Translation {i + 1} (Score: {score:.4f}):** {translation}")
    #
    #         # Highlight the best translation
    #         # best_translation = translations[best_translation_idx]
    #         # st.success(f"Best Translation: {best_translation}")
    #
    #         # Add tags input
    #         tags = st.text_input("Add Tags (comma-separated, e.g., noun, sports)")
    #
    #         # Save the best translation to the database
    #         if st.button("Save Flashcard"):
    #             c.execute("INSERT INTO flashcards (word, translation, tags) VALUES (?, ?, ?)",
    #                       # (text, best_translation, tags))
    #             # conn.commit()
    #             st.success("Flashcard saved successfully!")
    #
    #     except Exception as e:
    #         st.error(f"Translation failed: {e}")
    #
    # else:
    #     st.error("No text detected.")


if st.button("Go to Flashcards"):
    st.session_state.page = "Flashcards_db"
    # st.experimental_rerun()

if st.button("Go to Home"):
    st.session_state.page = "Home"
    # st.experimental_rerun()
import streamlit as st
import sqlite3
import re
from transformers import pipeline
from PIL import Image
import pytesseract

# Cache the pipeline
@st.cache_resource
def load_translator():
    return pipeline("translation_en_to_de", model="Helsinki-NLP/opus-mt-de-en")

translator = load_translator()

# Cache translations
@st.cache_data
def translate_sentence(sentence):
    return translator(sentence)

# Database setup
conn = sqlite3.connect("flashcards.db", check_same_thread=False)
c = conn.cursor()

# Streamlit UI
st.title("Flashcard Maker 📚")
st.write("Copy & Paste any sentence or upload a photo with sentence.")
st.write("I will translate it for you and you can create a flashcard!")
st.write("-------------------------------------------------------")

# Session state initialization
if "translation_text" not in st.session_state:
    st.session_state.translation_text = ""
if "original_sentence" not in st.session_state:
    st.session_state.original_sentence = ""

st.subheader("Your Input")
typed = st.text_input("Write your sentence here:")
uploaded_file = st.file_uploader("Or upload an image if you're too lazy to type...", type=["jpg", "jpeg", "png"])

st.write("-------------------------------------------------------")

if st.button("Translate"):
    sentence = ""
    if typed.strip():
        sentence = re.sub(r'[.,?@]$', '', typed.strip())
    elif uploaded_file:
        image = Image.open(uploaded_file)
        sentence = pytesseract.image_to_string(image).strip()
        sentence = re.sub(r'[.,?@]$', '', sentence)
    else:
        st.warning("Please type a sentence or upload an image.")

    if sentence:
        try:
            results = translate_sentence(sentence)
            translation_text = results[0]['translation_text'] if isinstance(results, list) else "Translation not available"
            # Store to session state
            st.session_state.original_sentence = sentence
            st.session_state.translation_text = translation_text
        except Exception as e:
            st.error(f"Translation failed: {e}")

# Display translation if available in session
if st.session_state.translation_text:
    st.write(f"- Your input: {st.session_state.original_sentence}")
    st.write(f"- Your output: {st.session_state.translation_text}")

    st.write("........................................................................................................................")

    selected_word = st.text_input("Which word do you want to remember? (this will be on your flashcard)")
    tags = st.text_input("Add Tags (comma-separated, e.g., noun, sports)")

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Save Flashcard"):
            c.execute("INSERT INTO flashcards (sentence, translation, word, tags) VALUES (?, ?, ?, ?)",
                      (st.session_state.original_sentence, st.session_state.translation_text, selected_word, tags))
            conn.commit()
            st.success("Flashcard saved successfully!")

    with col2:
        if st.button("Reset"):
            st.session_state.original_sentence = ""
            st.session_state.translation_text = ""
            st.rerun()

# st.write("========================================================================================")
st.write("-------------------------------------------------------")

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Go to Flashcards"):
        st.session_state.page = "pages/flashcards.py"

with col2:
    if st.button("Go to Practice"):
        st.session_state.page = "pages/practice.py"



# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
#
#
# import streamlit as st
# import sqlite3
# import re
# from transformers import pipeline
# from PIL import Image
# import pytesseract
#
#
# # Cache the pipeline
# @st.cache_resource
# def load_translator():
#     return pipeline("translation_en_to_de", model="Helsinki-NLP/opus-mt-de-en")
# translator = load_translator()
#
# # Cache translations to skip repeated work
# @st.cache_data
# def translate_sentence(sentence):
#     return translator(sentence)
#
# # Database setup (keep open while app is running)
# conn = sqlite3.connect("flashcards.db", check_same_thread=False)
# c = conn.cursor()
#
# # Streamlit UI
# st.title("Flashcard Maker 📚")
# st.write("Copy & Paste any sentence or upload a photo with sentence.")
# st.write("I will translate it for you and you can create a flashcard!")
# st.write("-------------------------------------------------------")
#
#
#
# # Session state initialization
# if "translation_text" not in st.session_state:
#     st.session_state.translation_text = ""
# if "original_sentence" not in st.session_state:
#     st.session_state.original_sentence = ""
#
#
#
# # st.subheader("Your Input")
# typed = st.text_input("Write your sentence here:")
# uploaded_file = st.file_uploader("Or upload an image if you're too lazy to type...", type=["jpg", "jpeg", "png"])
#
# st.write("-------------------------------------------------------")
# # st.subheader("Translate")
#
# # translation_triggered = False
# sentence = ""
#
# # Handle manual translation trigger
# if st.button("Translate"):
#     # translation_triggered = True
#     if typed.strip():
#         sentence = re.sub(r'[.,?@]$', '', typed.strip())
#     elif uploaded_file:
#         image = Image.open(uploaded_file)
#         sentence = pytesseract.image_to_string(image).strip()
#         sentence = re.sub(r'[.,?@]$', '', sentence)
#     else:
#         st.warning("Please type a sentence or upload an image.")
#
# # Do the translation only when button is clicked
# if sentence:
#     try:
#         results = translate_sentence(sentence)
#         translation_text = results[0]['translation_text'] if isinstance(results, list) else "Translation not available"
#         # Store to session state
#         st.session_state.original_sentence = sentence
#         st.session_state.translation_text = translation_text
#     except Exception as e:
#         st.error(f"Translation failed: {e}")
#
# # Display translation if available in session
# if st.session_state.translation_text:
#     st.write(f"- Your input: {st.session_state.original_sentence}")
#     st.write(f"- Your output: {st.session_state.translation_text}")
#
#     selected_word = st.text_input("Which word do you want to remember? (this will be on your flashcard)")
#     tags = st.text_input("Add Tags (comma-separated, e.g., noun, sports)")
#
#     if st.button("Save Flashcard"):
#         c.execute("INSERT INTO flashcards (sentence, translation, word, tags) VALUES (?, ?, ?, ?)",
#                   (st.session_state.original_sentence, st.session_state.translation_text, selected_word, tags))
#         conn.commit()
#         st.success("Flashcard saved successfully!")
#
# st.write("-------------------------------------------------------")
#
# if st.button("Go to Flashcards"):
#     st.session_state.page = "pages/flashcards.py"
#
# if st.button("Go to Practice"):
#     st.session_state.page = "pages/practice.py"
#




# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


# import streamlit as st
# # from sympy.strategies.branch import notempty
# from transformers import pipeline
# # from PIL import Image
# # import pytesseract
# import sqlite3
# import re
# 
# 
# # Cache the translation model
# @st.cache_resource
# def load_translator():
#     return pipeline("translation_en_to_de", model="Helsinki-NLP/opus-mt-de-en")
# 
# # Cache the DB connection
# @st.cache_resource
# def get_connection():
#     conn = sqlite3.connect("flashcards.db", check_same_thread=False)
#     conn.execute('''CREATE TABLE IF NOT EXISTS flashcards 
#                     (id INTEGER PRIMARY KEY AUTOINCREMENT, sentence TEXT, translation TEXT, word TEXT, tags TEXT)''')
#     return conn
# 
# # Initialize translation pipeline & setup database
# translator = load_translator()
# conn = get_connection()
# c = conn.cursor()
# 
# 
# 
# # Streamlit UI
# st.title("Flashcard Maker 📚")
# st.write("Copy & Paste any sentence or upload a photo with sentence.")
# st.write("I will translate it for you and you can create a flashcard for you!")
# st.write("-------------------------------------------------------")
# 
# st.subheader("Your Input")
# typed = st.text_input("Write your sentence here:")
# uploaded_file = st.file_uploader("Or upload an image if you're too lazy to type...", type=["jpg", "jpeg", "png"])
# 
# st.write("-------------------------------------------------------")
# st.subheader("Translation")
# 
# # --- Handle Text Input ---
# if typed.strip():
#     typed_sentence = typed.strip()
#     typed_sentence = re.sub(r'[.,?@]$', '', typed_sentence)
# 
#     if typed_sentence != "":
#         try:
#             results = translator(typed_sentence)
#             translation_text = results[0]['translation_text']
# 
#             st.write(f"- your input: {typed_sentence}")
#             st.write(f"- your output: {translation_text}")
#             selected_word = st.text_input("Which word do you want to remember? (this will be on your flashcard)", key="word_text")
#             tags = st.text_input("Add Tags (comma-separated, e.g., noun, sports)", key="tags_text")
# 
#             if st.button("Save Flashcard", key="save_text"):
#                 c.execute("INSERT INTO flashcards (sentence, translation, word, tags) VALUES (?, ?, ?, ?)",
#                           (typed_sentence, translation_text, selected_word, tags))
#                 conn.commit()
#                 st.success("Flashcard saved successfully!")
#         except Exception as e:
#             st.error(f"Translation failed: {e}")
#     else:
#         st.error("No text detected.")
# 
# # --- Handle Image Upload ---
# elif uploaded_file is not None:
#     image = Image.open(uploaded_file)
#     st.write(f"- Uploaded Image :")
#     st.image(image, use_container_width=False)
# 
#     sentence = pytesseract.image_to_string(image).strip()
#     sentence = re.sub(r'[.,?@]$', '', sentence)
# 
#     if sentence:
#         try:
#             results = translator(sentence)
#             translation_text = results[0]['translation_text']
# 
#             st.write(f"- your input: {sentence}")
#             st.write(f"- your output: {translation_text}")
#             selected_word = st.text_input("Which word do you want to remember? (this will be on your flashcard)", key="word_image")
#             tags = st.text_input("Add Tags (comma-separated, e.g., noun, sports)", key="tags_image")
# 
#             if st.button("Save Flashcard", key="save_image"):
#                 c.execute("INSERT INTO flashcards (sentence, translation, word, tags) VALUES (?, ?, ?, ?)",
#                           (sentence, translation_text, selected_word, tags))
#                 conn.commit()
#                 st.success("Flashcard saved successfully!")
#         except Exception as e:
#             st.error(f"Translation failed: {e}")
#     else:
#         st.error("No readable text detected in image.")
# 
# st.write("-------------------------------------------------------")
# 
# if st.button("Go to Flashcards"):
#     st.session_state.page = "pages/flashcards.py"
# 
# if st.button("Go to Practice"):
#     st.session_state.page = "pages/practice.py"
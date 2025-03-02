from transformers import pipeline
from PIL import Image
import pytesseract
import sqlite3
#
# # disable the warning messages
# import os
# os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# Install sentencepiece if not installed
try:
    import sentencepiece
except ImportError:
    import subprocess

    subprocess.call(["pip", "install", "sentencepiece"])

# Initialize translation pipeline
translator = pipeline("translation_en_to_de", model="Helsinki-NLP/opus-mt-de-en")

# Database setup
conn = sqlite3.connect("flashcards.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS flashcards (word TEXT, translation TEXT)''')
conn.commit()


# Function to extract text from image
def extract_text(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image).strip()
    return text


# Function to translate text
def translate_text(text):
    return translator(text)[0]['translation_text']


# Function to save flashcard to database
def save_flashcard(word, translation):
    c.execute("INSERT INTO flashcards (word, translation) VALUES (?, ?)", (word, translation))
    conn.commit()
    print("Flashcard saved successfully!")


# Main Execution
if __name__ == "__main__":
    # image_path = input("Enter the path to your image file: ")
    image_path = "images/vrfgbar.png"
    text = extract_text(image_path)

    if text:
        print(f"Detected Word: {text}")
        translation = translate_text(text)
        print(f"English Translation: {translation}")
        save_flashcard(text, translation)
    else:
        print("No text detected. Please try again with a clearer image.")

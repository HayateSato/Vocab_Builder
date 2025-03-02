from transformers import pipeline
import sqlite3

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
    test_word = "Schweine"
    print(f"Input Word: {test_word}")
    translation = translate_text(test_word)
    print(f"English Translation: {translation}")
    save_flashcard(test_word, translation)

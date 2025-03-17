import sqlite3

# Database setup
conn = sqlite3.connect("flashcards.db")
c = conn.cursor()

#-- Creating a new db file
# c.execute('''CREATE TABLE IF NOT EXISTS flashcards (sentence TEXT, translation TEXT, word CHAR(100), tags TEXT)''')
# conn.commit()

#-- adding a new column
# new_column = "sentence"
# c.execute(f"ALTER TABLE flashcards ADD COLUMN {new_column} TEXT")
# print(conn.commit())

#-- printing all rows for the selected columns
# c.execute("SELECT rowid, word, tags, sentence, translation FROM flashcards")
# rows = c.fetchall()
#
# print(rows)



#-- checking existing columns
c.execute("PRAGMA table_info(flashcards)")
columns = [column for column in c.fetchall()]
print(columns)
import streamlit as st
import sqlite3

# Function to connect to SQLite database
def create_connection():
    conn = sqlite3.connect('history.db')
    return conn

# Function to create the history table if it doesn't exist
def create_table(conn):
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_text TEXT,
                replaced_text TEXT
            )
        ''')

# Function to insert a new record into the history
def insert_history(conn, original_text, replaced_text):
    with conn:
        conn.execute('''
            INSERT INTO history (original_text, replaced_text)
            VALUES (?, ?)
        ''', (original_text, replaced_text))

# Function to fetch all history records
def fetch_history(conn):
    with conn:
        return conn.execute('SELECT * FROM history').fetchall()

# Main app
def main():
    st.title("Word Replacer App")

    # Database connection
    conn = create_connection()
    create_table(conn)

    # User inputs
    paragraph = st.text_area("Enter your paragraph:")
    word_to_replace = st.text_input("Enter the word to replace:")
    replacement_word = st.text_input("Enter the replacement word:")

    # Button to process the replacement
    if st.button("Replace"):
        if paragraph and word_to_replace and replacement_word:
            # Replace the word
            modified_paragraph = paragraph.replace(word_to_replace, replacement_word)

            # Display the modified paragraph
            st.subheader("Modified Paragraph:")
            st.write(modified_paragraph)

            # Save to history
            insert_history(conn, paragraph, modified_paragraph)
        else:
            st.error("Please fill in all fields.")

    # Show history in the sidebar
    st.sidebar.header("Input History")
    history = fetch_history(conn)
    for row in history:
        st.sidebar.write(f"Original: {row[1]}")
        st.sidebar.write(f"Replaced: {row[2]}")
        st.sidebar.write("---")

if __name__ == "__main__":
    main()
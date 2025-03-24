import streamlit as st
from llm import get_response, sql_prompt
from database import create_database, execute_sql_query, get_schemas
import os
import glob

# Streamlit Page Configuration


# Define directories for CSV files and databases
CSV_FOLDER = "data_files/csv_fils"  # CSV files storage
DB_FOLDER = "data_files/db_files"  # SQLite database storage

# Ensure folders exist
os.makedirs(CSV_FOLDER, exist_ok=True)
os.makedirs(DB_FOLDER, exist_ok=True)

st.title("Natural Language to SQL Query Generator")

# Sidebar for Database Creation
# st.sidebar.title("Create Database from CSV")
uploaded_file = st.sidebar.file_uploader("Upload file(e.g , csv, xls, xlsx, json)")
db_name = st.sidebar.text_input("Enter Database Name (e.g., netflix.db)", "netflix.db")
table_name = st.sidebar.text_input("Enter Table Name", "netflix_titles")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

if st.sidebar.button("Create Database"):
    if uploaded_file and db_name and table_name:
        # Save CSV file in CSV_FOLDER
        csv_path = os.path.join(CSV_FOLDER, uploaded_file.name)
        with open(csv_path, "wb") as f:
            f.write(uploaded_file.getbuffer()) #getbuffer() retrieves the raw file content in bytes.

        # Define full path for the database file in DB_FOLDER
        db_path = os.path.join(DB_FOLDER, db_name)

        # Create the database from the uploaded CSV file
        result = create_database(csv_path, db_path, table_name)
        st.sidebar.success(f"Database created successfully: {db_path}")
    else:
        st.sidebar.error("Please provide a CSV file, database name, and table name!")


# Find all .db files in the folder
db_files = glob.glob(os.path.join(DB_FOLDER, "*.db"))
db_files = [os.path.basename(db) for db in db_files]  # Extract filenames only
# Sidebar for Selecting Existing Database
st.sidebar.title("Use an Existing Database")
if db_files:
    selected_db = st.sidebar.selectbox("Select a Database:", db_files)
    db_path = os.path.join(DB_FOLDER, selected_db)
    st.sidebar.success(f"Selected Database: {db_path}")
else:
    st.sidebar.error("No database files found in the folder!")
    db_path = None
# db_path = st.sidebar.text_input("Enter Database Path:", os.path.join(DB_FOLDER, db_name))

if st.sidebar.button("Show Schema"):
    if os.path.exists(db_path):
        tables = get_schemas(db_path)
        st.sidebar.write("Tables in Database:")
        st.sidebar.write(tables)
    else:
        st.sidebar.error("Database file not found!")

# User input for Natural Language Query
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
user_question = st.text_area("Enter your question in English:")

if st.button("Generate SQL Query"):
    if user_question.strip() == "":
        st.error("Please enter a valid question!")
        # if st.session_state.user_input.strip() == "":
        #     st.error("Please enter a valid question!")
    else:
        # Retrieve the schema
        schema = get_schemas(db_path)

        # Generate SQL Query using Gemini
        prompt = sql_prompt.replace("{{schema}}", schema).replace("{{question}}", user_question)
        response = get_response(prompt).text.strip()

        st.session_state.chat_history.append({"Question":user_question,"Response": response})

        st.subheader("Generated SQL Query")
        st.code(response, language="sql")


        # Execute SQL Query
        try:
            df = execute_sql_query(response, db_path)
            if df.empty:
                st.warning("No results found!")
            else:
                st.subheader("Query Results")
                st.dataframe(df)
        except Exception as e:
            st.error(f"Error executing query: {str(e)}")

        # st.session_state.user_input = ""

# Display Chat History in the Main Section
st.subheader("Chat History")
for entry in st.session_state.chat_history[::-1]:  # Show latest first
    with st.expander(f"📝 {entry['Question']}"):
        st.code(entry["Response"], language="sql")

# Button to clear chat history
if st.button("Clear History"):
    st.session_state.chat_history = []
    st.success("Chat history cleared!")
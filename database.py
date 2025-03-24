import sqlite3
import os
import pandas as pd



# Function to create a database and store the data from a file (CSV, Excel, or JSON)
def create_database(file_path, database_name, table_name):
    """
    Creates an SQLite database and stores the content of a given file (CSV, Excel, or JSON) in a table.

    Parameters:
    file_path (str): Path to the input file.
    database_name (str): Name of the SQLite database to be created.
    table_name (str): Name of the table where data will be stored.

    Returns:
    str: A message indicating if an unsupported file type is encountered.
    """

    # Establish a connection to the SQLite database
    connection = sqlite3.connect(database_name)

    # Detect the file extension to determine how to read the file
    file_extension = os.path.splitext(file_path)[-1].lower()

    # Read the file based on its format
    if file_extension == ".csv":
        df = pd.read_csv(file_path, encoding="ISO-8859-1")  # Read CSV file
    elif file_extension in [".xls", ".xlsx"]:
        df = pd.read_excel(file_path, engine="openpyxl")  # Read Excel file
    elif file_extension == ".json":
        df = pd.read_json(file_path)  # Read JSON file
    else:
        connection.close()  # Close connection if file type is unsupported
        return f"Unsupported file type: {file_extension}"

    # Create a cursor object to interact with the database
    cursor = connection.cursor()

    # Store the data in the SQLite table, replacing the table if it already exists
    df.to_sql(table_name, connection, if_exists="replace", index=False)

    # Retrieve and print the list of tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table';")

    # Close the database connection
    connection.close()


    

def execute_sql_query(sql_query, db):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    cursor.execute(sql_query)
    rows = cursor.fetchall()
    headers = [i[0] for i in cursor.description]

    connection.close()
    if rows:
        df = pd.DataFrame(rows,columns=headers)
    return df


def get_schemas(db):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()

    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_names = cursor.fetchall()

    all_schema_string = ""

    for table_name in table_names:
        table_name = table_name[0]  # Extract the table name from tuple

        # Fetch the CREATE TABLE statement for the table
        cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}';")
        schema_sql = cursor.fetchone()

        if schema_sql and schema_sql[0]:  # Ensure schema is not None
            all_schema_string += f"\n{schema_sql[0]}"

    connection.close()

    return all_schema_string.strip()
import sqlite3
import os
import pandas as pd



# print(file_path)
def create_database(file_path,database_name,table_name):
    connection = sqlite3.connect(database_name)
    # Detect file type and read accordingly
    file_extension = os.path.splitext(file_path)[-1].lower()
    # print(file_extension)

    if file_extension == ".csv":
        df = pd.read_csv(file_path,encoding="ISO-8859-1")
    elif file_extension in [".xls", ".xlsx"]:
        df = pd.read_excel(file_path,engine="openpyxl")
    elif file_extension == ".json":
        df = pd.read_json(file_path)
    else:
        connection.close()
        return f"Unsupported file type: {file_extension}"

    cursor = connection.cursor()
    # df = pd.read_csv(file_path)
    db = df.to_sql(table_name, connection, if_exists="replace", index=False)
    cursor = connection.cursor()
    cursor.execute("select name from sqlite_master where type = 'table';")
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
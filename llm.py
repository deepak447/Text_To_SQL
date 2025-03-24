import google.generativeai as genai
from dotenv import load_dotenv
import os 


load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=google_api_key)

def get_response(prompt):
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    response = model.generate_content(prompt)
    return response


sql_prompt = """
    You are an expert in converting English questions to SQL queries!
    The SQL database has the following schema: {{schema}}.

    For example:
    Example 1 - How many entries of records are present?
        The SQL command will be: SELECT COUNT(*) FROM STUDENT;
    Example 2 - Tell me all the students studying in Data Science COURSE?
        The SQL command will be: SELECT * FROM STUDENT WHERE COURSE = "Data Science";

    Ensure:
    - The SQL code does NOT contain ``` at the beginning or end.
    - The output should NOT include the word "SQL."

    Now, convert the following question into a valid SQL query:
    {{question}}
"""
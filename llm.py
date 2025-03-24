import google.generativeai as genai
from dotenv import load_dotenv
import os 


load_dotenv()
# fetch api key from .env file
google_api_key = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=google_api_key)

def get_response(prompt):
    """
    Generates a response from the Gemini 1.5 Pro model based on the given prompt.

    Parameters:
    prompt (str): The input text prompt for the AI model.

    Returns:
    response: The generated content from the AI model.
    """

    # Initialize the generative model with the latest Gemini 1.5 Pro version
    model = genai.GenerativeModel("gemini-1.5-pro-latest")

    # Generate content based on the provided prompt
    response = model.generate_content(prompt)

    # Return the generated response
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
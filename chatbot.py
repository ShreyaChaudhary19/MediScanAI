from google import genai
import streamlit as st
client = genai.Client(
    api_key=st.secrets["AQ.Ab8RN6K6CWtYUpZQec9iw7NOcX_Lqq5RJW7rpsXMQOHTNniPrw"]
)

def ask_health_question(question):

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=question
        )

        return response.text

    except Exception as e:

        error_message = str(e)

        if "503" in error_message:

            return """
⚠️ AI Assistant Temporarily Busy

The AI service is currently experiencing high demand.

Please wait a few moments and try again.

Your disease prediction and medical report features remain fully functional.
"""

        elif "429" in error_message:

            return """
⚠️ Rate Limit Reached

Too many AI requests were sent.

Please try again in a few minutes.
"""

        else:

            return f"""
⚠️ AI Service Error

{error_message}
"""
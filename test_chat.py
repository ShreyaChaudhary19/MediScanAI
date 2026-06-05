from google import genai

client = genai.Client(
    api_key="AQ.Ab8RN6K6CWtYUpZQec9iw7NOcX_Lqq5RJW7rpsXMQOHTNniPrw"
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="What is dengue?"
)

print(response.text)
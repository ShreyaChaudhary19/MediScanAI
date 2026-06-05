from google import genai

client = genai.Client(
    api_key="api_key"
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="What is dengue?"
)

print(response.text)

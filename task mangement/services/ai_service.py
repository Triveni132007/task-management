import google.generativeai as genai

genai.configure(
    api_key="YOUR_API_KEY"
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

def ask_ai_service(message):
    response = model.generate_content(message)
    return response.text


# Example
print(ask_ai_service("Hello"))
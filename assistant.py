import os
from dotenv import load_dotenv
from google import genai
import requests

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SEARCH_API_KEY = os.getenv("SEARCH_API_KEY")   # Google Custom Search API
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found. Please add it to your .env file.")

# Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)
MODEL_NAME = "gemini-1.5-flash"

class Assistant:
    def __init__(self):
        self.history = []  # conversation memory

    def search_google(self, query: str):
        """Uses Google Custom Search API for real-time info."""
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": SEARCH_API_KEY,
            "cx": SEARCH_ENGINE_ID,
            "q": query,
        }
        try:
            resp = requests.get(url, params=params).json()
            if "items" in resp:
                return resp["items"][0]["snippet"]
            return "I couldn't find relevant results."
        except Exception as e:
            return f"Search error: {e}"

    def ask(self, user_text: str):
        # Intercept real-time queries
        if "price of bitcoin" in user_text.lower():
            return self.search_google("current price of Bitcoin")
        if "weather in" in user_text.lower():
            return self.search_google(user_text)

        # Otherwise ask Gemini with memory
        self.history.append({"role": "user", "content": user_text})
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=self.history
        )
        answer = response.text
        self.history.append({"role": "model", "content": answer})
        return answer

def main():
    print("\n🤖 Gemini Assistant (with memory + Google Search)\n")
    print("Type 'clear' to erase memory, 'exit' to quit.\n")

    bot = Assistant()

    while True:
        user_text = input("You: ").strip()
        if user_text.lower() == "exit":
            break
        elif user_text.lower() == "clear":
            bot.history = []
            print("🧹 Memory cleared.")
            continue

        reply = bot.ask(user_text)
        print(f"Assistant: {reply}\n")

if __name__ == "__main__":
    main()
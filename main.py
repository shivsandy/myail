import requests

def chat_cli(api_key):
    api_url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    chat_history = []
    print("Perplexity Chatbot ready! Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        chat_history.append({"role": "user", "content": user_input})

        data = {
            "model": "sonar-pro",
            "messages": chat_history
        }

        try:
            response = requests.post(api_url, headers=headers, json=data)
            response.raise_for_status()
            bot_reply = response.json()['choices'][0]['message']['content']
        except Exception as e:
            print(f"Error: {e}")
            break

        print("Bot:", bot_reply)
        chat_history.append({"role": "assistant", "content": bot_reply})

if __name__ == "__main__":
    # Paste your Perplexity API key here:
    api_key = "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"
    chat_cli(api_key)

import requests

api_key = "0097473bda6ba5d1b430afc0cefdcbd87820c51bbd6a64d6ce6cb33cc1ee9acc"
chat_endpoint = "https://api.together.xyz/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

def generate_affirmation(issue):
    payload = {
        "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
        "messages": [
            {"role": "system", "content": "You are a mindset coach for traders. Generate a short, calming affirmation for the issue below."},
            {"role": "user", "content": f"My issue: {issue}"}
        ],
        "temperature": 0.7,
        "max_tokens": 100
    }
    try:
        response = requests.post(chat_endpoint, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print("[Affirmation API Error]", e)
        if hasattr(e, 'response') and e.response is not None:
            print(e.response.text)
        return None

def get_affirmation():
    issue = input("Describe your trading mindset issue: ")
    affirmation = generate_affirmation(issue)
    if affirmation:
        print("\nYour personalized affirmation:\n")
        print(affirmation)
    else:
        print("Failed to generate affirmation.")

if __name__ == "__main__":
    get_affirmation()

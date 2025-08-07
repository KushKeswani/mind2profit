import requests

api_key = "0097473bda6ba5d1b430afc0cefdcbd87820c51bbd6a64d6ce6cb33cc1ee9acc"
chat_endpoint = "https://api.together.xyz/v1/chat/completions"
moderation_endpoint = "https://api.together.xyz/v1/completions"

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

def moderate_text(text):
    payload = {
        "model": "meta-llama/Llama-Guard-4-12B",
        "prompt": text,
        "max_tokens": 200,
        "temperature": 0
    }
    try:
        response = requests.post(moderation_endpoint, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        output = data["choices"][0]["text"]
        return output
    except Exception as e:
        print("[Moderation API Error]", e)
        if hasattr(e, 'response') and e.response is not None:
            print(e.response.text)
        return None

def get_safe_affirmation():
    issue = input("Describe your trading mindset issue: ")
    affirmation = generate_affirmation(issue)
    if not affirmation:
        print("Failed to generate affirmation.")
        return
    moderation_result = moderate_text(affirmation)
    if moderation_result and 'Unsafe: True' in moderation_result:
        print("This affirmation was flagged as unsafe. Try a different prompt.")
    elif moderation_result:
        print("\nYour personalized affirmation:\n")
        print(affirmation)
    else:
        print("Moderation failed. Could not verify safety.")

if __name__ == "__main__":
    get_safe_affirmation()

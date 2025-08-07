import requests

api_key = "0097473bda6ba5d1b430afc0cefdcbd87820c51bbd6a64d6ce6cb33cc1ee9acc"
endpoint = "https://api.together.xyz/v1/chat/completions"

issue = input("Describe your trading mindset issue: ")

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

payload = {
    "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
    "messages": [
        {"role": "system", "content": "You are a mindset coach for traders. Generate a single personalized affirmation to help with the issue."},
        {"role": "user", "content": f"My issue: {issue}"}
    ],
    "temperature": 0.7,
    "max_tokens": 150
}

response = requests.post(endpoint, headers=headers, json=payload)
if response.status_code == 200:
    result = response.json()
    affirmation = result["choices"][0]["message"]["content"]
    print("\nYour personalized affirmation:\n")
    print(affirmation)
else:
    print("Error:", response.status_code, response.text)

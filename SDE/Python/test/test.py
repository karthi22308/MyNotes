from openai import AzureOpenAI

# 🔹 Hardcoded credentials
AZURE_API_KEY = "DagkDMkW44hoRl0tn3GvcI0R9HYZze9gJDWSDOAxux13aod5S8RwJQQJ99BIAC77bzfXJ3w3AAAAACOGPc0o"
AZURE_ENDPOINT = "https://learningllmmodel.cognitiveservices.azure.com/"
AZURE_API_VERSION = "2024-12-01-preview"   # fixed version

# 🔹 Create client
client = AzureOpenAI(
    api_key=AZURE_API_KEY,
    api_version=AZURE_API_VERSION,
    azure_endpoint=AZURE_ENDPOINT
)

def chatbot_response(user_input):
    if "*" in user_input:  # simple multiplication logic
        try:
            parts = user_input.split("*")
            a, b = int(parts[0].strip()), int(parts[1].strip())
            return f"Answer: {a * b}"
        except:
            return "Invalid multiplication format. Example: 2*3"

    response = client.chat.completions.create(
        model="gpt-5-mini",  # your deployed model name in Azure
        messages=[
            {"role": "system", "content": "You are a simple chatbot."},
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content

def main():
    print("Simple Azure Chatbot (type 'exit' to quit)\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Chatbot: Goodbye! 👋")
            break
        print("Chatbot:", chatbot_response(user_input))

if __name__ == "__main__":
    main()

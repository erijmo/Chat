import requests
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Load the healthcare dataset
url = "https://raw.githubusercontent.com/erijmo/3690/main/healthcare_dataset.csv"
df = pd.read_csv(url)

# Set your OpenAI GPT-3 API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")

# Check if the API key is set
if not api_key:
    raise ValueError("Please set your OpenAI API key using the OPENAI_API_KEY environment variable.")

# Function to get a response based on user input using GPT-3
def get_healthcare_response(user_input):
    # Check if the user's input contains specific keywords and provide relevant responses
    if "medical condition" in user_input.lower():
        response = "Your medical condition is: {}".format(df["Medical Condition"].iloc[0])
    elif "medication" in user_input.lower():
        response = "You are taking: {}".format(df["Medication"].iloc[0])
    elif "admission type" in user_input.lower():
        response = "Your admission type is: {}".format(df["Admission Type"].iloc[0])
    else:
        # Check if user is asking about a specific column in the CSV
        for column in df.columns:
            if column.lower() in user_input.lower():
                response = f"Your {column} is: {df[column].iloc[0]}"
                break
        else:
            # Use GPT-3 for general questions
            prompt = f"User: {user_input}\nHealthcareBot:"
            response_data = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}"},
                json={"model": "gpt-3.5-turbo", "messages": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": user_input}]},
            ).json()

            # Check if response is valid
            if "choices" in response_data and response_data["choices"]:
                response = response_data["choices"][0]["message"]["content"].strip()
            else:
                response = "I'm sorry, I couldn't understand your request. Can you please provide more details?"

    return response

# Introduction message
print("HealthcareBot: Hello! I'm your HealthcareBot. How can I assist you today?")

# Example usage
while True:
    user_input = input("User: ")
    if user_input.lower() in ['exit', 'bye', 'quit']:
        print("HealthcareBot: Goodbye! If you have more questions, feel free to ask.")
        break
    response = get_healthcare_response(user_input)
    if response:
        print("HealthcareBot:", response)

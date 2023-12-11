import pandas as pd
from dotenv import load_dotenv
import os

# load env
load_dotenv()

# load dataset
url = "https://raw.githubusercontent.com/erijmo/3690/main/healthcare_dataset.csv"
df = pd.read_csv(url)

# set api key
api_key = os.getenv("OPENAI_API_KEY")

def get_healthcare_response(user_input, user_name, df):
    # search for keyword in user input
    for column in df.columns:
        if column in user_input:
            response = f"{user_name}, your {column.lower()} is {df[column].iloc[0]}"
            return response

    # if no keyword located, ask for clarification
    return "I'm sorry, I couldn't understand your request. Can you please provide more details?"

# prompt response
print("HealthcareBot: Hello! I'm your HealthcareBot. May I know your name, please?")

user_name = input("User: ")

# check if the user's name is in the system
if user_name.lower() not in df["Name"].str.lower().values:
    print("HealthcareBot: I'm sorry, but I couldn't find your name in the system. Please make sure you entered it correctly.")
else:
    print(f"HealthcareBot: Thank you, {user_name}! How can I assist you today?")

# user interaction loop
while True:
    user_input = input("User: ")
    if user_input.lower() in ['exit', 'bye', 'quit']:
        print("HealthcareBot: Goodbye! If you have more questions, feel free to ask.")
        break
    response = get_healthcare_response(user_input, user_name, df)
    if response:
        print("HealthcareBot:", response)

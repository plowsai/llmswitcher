# chat_interface.py

import sys
from switcher import LLM_Switcher, models

def main():
    switcher = LLM_Switcher(models)
    while True:
        try:
            # Prompt the user for input
            query = input("Enter your question or prompt: ")
            if query.lower() == "exit":
                break

            # Process the query and switch the model
            response = switcher.switch_and_request(query)
            if response:
                print("Response received:", response)
            else:
                print("No model could handle the request. Check your API keys.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

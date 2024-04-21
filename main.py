import time
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# AI IMPORTS
# OPENAI
# from openai import OpenAI
# client = OpenAI()

# Anthropic
openai_api_key = os.getenv("OPENAI_API_KEY")
anthropic_key = os.getenv("ANTHROPIC_API_KEY")
hf_key = os.getenv("HF_API_KEY")

class ModelInterface:
    def __init__(self, name, endpoint):
        self.name = name
        self.endpoint = endpoint

    def request(self, query, timeout=None, max_tokens=None):
        time.sleep(timeout) # Simulate a delay
        response = {"tokens": 100, "result": "This is a placeholder response."}
        if max_tokens and response["tokens"] > max_tokens:
            raise Exception("Token count exceeded.")
        return response

# Example models
openai = ModelInterface("openai", "https://api.model1.com")
hf = ModelInterface("hf", "https://api.model2.com")
anthropic = ModelInterface("anthropic", "https://api.model3.com")

# List of models to switch between
models = [openai, hf, anthropic]

class LLM_Switcher:
    def __init__(self, models):
        self.models = models
        self.last_used_model = None

    def switch_and_request(self, query, timeout=5, max_tokens=100):
        for model in self.models:
            try:
                response = model.request(query, timeout=timeout, max_tokens=max_tokens)
                if response:
                    self.last_used_model = model
                    return response
            except TimeoutError:
                print(f"{model.name} timed out. Switching to the next model.")
            except Exception as e:
                print(f"Error with {model.name}: {e}. Switching to the next model.")
        return None

def main():
    switcher = LLM_Switcher(models)
    if '-v' in sys.argv:
        if switcher.last_used_model:
            print(f"Last used model: {switcher.last_used_model.name}")
        else:
            print("No model has been used yet.")
    else:
        query = "What is the meaning of life?"
        response = switcher.switch_and_request(query)
        if response:
            print("Response received:", response)
        else:
            print("No model could handle the request.")

if __name__ == "__main__":
    main()

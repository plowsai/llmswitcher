import time
import os 
from dotenv import load_dotenv

## AI IMPORTS 
##
## OPENAI
# from openai import OpenAI
# client = OpenAI()

##
## Anthropic

openai_api_key = os.env("")
anthropic_key = os.env("")
hf_key = os.env("")

#alternative you can use the .env if you prefer 
# openai_api_key = os.env("")
# anthropic_key = os.env("")
# hf_key = os.env("")

class ModelInterface:
    def __init__(self, name, endpoint):
        self.name = name
        self.endpoint = endpoint

    def request(self, query, timeout=None, max_tokens=None):
        # Placeholder for the actual request logic
        # This example simulates a request with a delay and a response
        time.sleep(timeout) # Simulate a delay
        response = {"tokens": 100, "result": "This is a placeholder response."}
        if max_tokens and response["tokens"] > max_tokens:
            raise Exception("Token count exceeded.")
        return response

# Example models
openai = ModelInterface("Model1", "https://api.model1.com")
hf = ModelInterface("Model2", "https://api.model2.com")
anthropic = ModelInterface("Model3", "https://api.model3.com")

# List of models to switch between
models = [openai, hf, anthropic]

class LLM_Switcher:
    def __init__(self, models):
        self.models = models

    def switch_and_request(self, query, timeout=5, max_tokens=100):
        for model in self.models:
            try:
                response = model.request(query, timeout=timeout, max_tokens=max_tokens)
                if response:
                    return response
            except TimeoutError:
                print(f"{model.name} timed out. Switching to the next model.")
            except Exception as e:
                print(f"Error with {model.name}: {e}. Switching to the next model.")
        return None

if __name__ == "__main__":
    switcher = LLM_Switcher(models)
    query = "What is the meaning of life?"
    response = switcher.switch_and_request(query)
    if response:
        print("Response received:", response)
    else:
        print("No model could handle the request.")
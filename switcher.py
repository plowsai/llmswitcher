import time
import os
import sys
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Anthropic
openai_api_key = os.getenv("OPENAI_API_KEY")
anthropic_key = os.getenv("ANTHROPIC_API_KEY")
hf_key = os.getenv("HF_API_KEY")

import time
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Anthropic
openai_api_key = os.getenv("OPENAI_API_KEY")
anthropic_key = os.getenv("ANTHROPIC_API_KEY")
hf_key = os.getenv("HF_API_KEY")

class ModelInterface:
    def __init__(self, name, endpoint, api_key):
        self.name = name
        self.endpoint = endpoint
        self.api_key = openai_api_key

    def request(self, query, timeout=None, max_tokens=None):
        if not self.api_key:
            raise Exception("API key not set for model.")
        
        # Prepare the headers and body for the API request
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        body = {
            "model": "text-davinci-002", # Example model name, adjust as needed
            "prompt": query,
            "max_tokens": max_tokens or 100 # Default to 100 tokens if not specified
        }
        
        # Send the request to the OpenAI API
        try:
            response = requests.post(self.endpoint, headers=headers, json=body, timeout=timeout)
            response.raise_for_status() # Raise an exception if the request failed
            return response.json(), response.status_code # Return the response and status code
        except requests.exceptions.RequestException as e:
            print(f"Error with {self.name}: {e}.")
            return None, None

# Example models
# Correctly initialize the openai instance with the api_key
openai = ModelInterface("openai", "https://api.openai.com/v1/models/", openai_api_key)
## ADDING HUGGING FACE SUPPORT LATER
hf = ModelInterface("hf", "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B", hf_key)
anthropic = ModelInterface("anthropic", "https://api.anthropic.com/v1/messages", anthropic_key)

# List of models to switch between
models = [openai,anthropic]

class LLM_Switcher:
    def __init__(self, models):
        self.models = models
        self.last_used_model = None

    def switch_and_request(self, query, timeout=5, max_tokens=100):
        # Prioritize OpenAI model
        openai_model = None
        for model in self.models:
            if model.name == "openai":
                openai_model = model
                break

        if openai_model:
            try:
                response, score = openai_model.request(query, timeout=timeout, max_tokens=max_tokens)
                self.last_used_model = openai_model
                return response
            except TimeoutError:
                print(f"{openai_model.name} timed out. Switching to the next model.")
            except Exception as e:
                print(f"Error with {openai_model.name}: {e}. Switching to the next model.")

        # If OpenAI fails, fall back to other models
        for model in self.models:
            if model != openai_model:
                try:
                    response, score = model.request(query, timeout=timeout, max_tokens=max_tokens)
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


# Example models
# Correctly initialize the openai instance with the api_key
openai = ModelInterface("openai", "https://api.openai.com/v1/models", openai_api_key)
## ADDING HUGGING FACE SUPPORT LATER
hf = ModelInterface("hf", "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B", hf_key)
anthropic = ModelInterface("anthropic", "https://api.anthropic.com/v1/messages", anthropic_key)

# List of models to switch between
models = [openai,anthropic]

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

import openai
import tiktoken
# import os

# Get the API key and resource endpoint from environment variables
API_KEY = "your_api_key"
RESOURCE_ENDPOINT = "your_resource_endpoint"

# Set the API type and key in the openai library
openai.api_type = "azure"
openai.api_key = API_KEY
openai.api_base = RESOURCE_ENDPOINT
openai.api_version = "2023-05-15"

MODEL = "gpt-35-turbo-16k"
#MODEL = "gpt-35-turbo"

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def prompt_open_ai(prompt, paragraph):
    
    input = prompt + "\n" + paragraph
    num_prompt_tokens = num_tokens_from_string(paragraph, "cl100k_base")

    response = openai.ChatCompletion.create(
                engine=MODEL,
                messages=[
                    {"role": "system", "content": "Your are an AI writing assistant that helps with specific rules.",
                     "role": "user", "content": input},
                ],
                max_tokens=int(num_prompt_tokens),
                temperature=0
            )

    return response["choices"][0]["message"]["content"]

#    response = openai.Completion.create(
#                #engine=COMPLETIONS_MODEL,
#                prompt=input,
#                engine=MODEL,
#                max_tokens=int(num_prompt_tokens),
#                temperature=0.1
#            )

#    return response["choices"][0]["text"]
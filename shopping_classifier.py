import openai
import json


def get_credentials(key):
    with open("credentials.json", 'r') as json_file:
        data = json.load(json_file)
        return find_key_value(data, key)

def find_key_value(data, key):
    if isinstance(data, dict):
        for k, v in data.items():
            if k == key:
                return v
            elif isinstance(v, (dict, list)):
                result = find_key_value(v, key)
                if result is not None:
                    return result
    elif isinstance(data, list):
        for item in data:
            result = find_key_value(item, key)
            if result is not None:
                return result

    return None

# Set up OpenAI API credentials
openai.api_key = get_credentials("openai")
model_engine = "text-davinci-002"

# Function to check if a given URL belongs to a shopping category
def check_category(url):
    # Set the prompt for the OpenAI API request
    prompt = f"Please classify the category of the URL as 'shopping' or 'information' in just one word {url}."
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Check if the API response contains any choices
    if len(completions.choices) > 0:
        categories = completions.choices[0].text.strip()

        # Check if the word "shopping" is present in the response
        if 'shopping' in categories.lower():
            return True
        else:
            return False
    else:
        return False

if __name__=="__main__":
    url = "https://www.toysfortots.org"
    is_shopping = check_category(url)
    print(is_shopping) # Output: True


import dwani

import os 
import json
dwani.api_key = os.getenv("DWANI_API_KEY")

dwani.api_base = os.getenv("DWANI_API_BASE_URL")


def read_markdown_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return "Error: File not found"
    except Exception as e:
        return f"Error: {str(e)}"

# Example usage
file_path = 'system_prompt.md'
markdown_content = read_markdown_file(file_path)
#print(markdown_content)

user_prompt = "Plan to a quarterly performance review of the Datacenter Infra team , return the answer in json format"
resp = dwani.Chat.direct(prompt=user_prompt, system_prompt=markdown_content)


print(resp['response'])


user_prompt = "Plan to a Birthday event with family and close friends , return the answer in json format"
resp = dwani.Chat.direct(prompt=user_prompt, system_prompt=markdown_content)


print(resp['response'])

#tasks = resp['response'].replace('```json', '').replace('```', '').strip()


#resp = dwani.Chat.direct(prompt= "parse the json and return answer as List of arrays " + tasks)


#print(resp)
#print(resp)

#json_value = json.loads(tasks)

#print(json_value)
#add_prompt = "for each of task, generate python code to execute in a docker container. Results will be verfied in future step"
#resp = dwani.Chat.direct(prompt= add_prompt + tasks)

#print(resp)



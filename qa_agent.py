
import json 
import dwani
import os

# Set up dwani API credentials
dwani.api_key = os.getenv("DWANI_API_KEY")
dwani.api_base = os.getenv("DWANI_API_BASE_URL")

output_json = "combined_output.json"
with open(output_json, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
    
qa_bank_str = str(json_data)



qa_result = dwani.Chat.direct(
    prompt="Ask me a question from  " + qa_bank_str + ", do not explain, just return the question")

print(qa_result)


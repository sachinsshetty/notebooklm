import dwani

import os 

import json
dwani.api_key = os.getenv("DWANI_API_KEY")

dwani.api_base = os.getenv("DWANI_API_BASE_URL")


prompt = "list the key points and provide the reponse in json"

file_path = "sample_resume.pdf"
result = dwani.Documents.query_all(
    file_path, model="gemma3", tgt_lang="eng_Latn", prompt=prompt
)

pdf_answer = result["translated_query_answer"]


extracted_text = result["original_text"]

result = dwani.Chat.direct(prompt= "provide top 5 important items and return response as json : "  + extracted_text)

#print(result['response'])


clean_json_str= result['response'].replace('```json', '').replace('```', '').strip()

print(clean_json_str)


clean_json_str= pdf_answer.replace('```json', '').replace('```', '').strip()

print(clean_json_str)

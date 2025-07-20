import dwani

import os 

import json
dwani.api_key = os.getenv("DWANI_API_KEY")

dwani.api_base = os.getenv("DWANI_API_BASE_URL")


file_path = "sample_resume.pdf"
result = dwani.Documents.run_ocr_all(
    file_path, model="gemma3"
)

print(result)
extracted_text = str(result["page_contents"])

result = dwani.Chat.direct(prompt= "provide top 5 important items and return response as json : "  + extracted_text)

#print(result['response'])


clean_json_str= result['response'].replace('```json', '').replace('```', '').strip()

print(clean_json_str)


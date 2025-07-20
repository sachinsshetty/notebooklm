import requests
import os
from pathlib import Path
import dwani


dwani.api_key = os.getenv("DWANI_API_KEY")

dwani.api_base = os.getenv("DWANI_API_BASE_URL")

api_key = os.getenv("SOUND_API_KEY")



response = dwani.Audio.speech(input = "what is your name? I am sachin from Bonn", response_format="mp3", language="english")
file_path = Path("sound-input.mp3")
with open(file_path, "wb") as f:
    f.write(response)

file_path = Path("sound-input.mp3")

url = "https://api.ai-coustics.io/v1/media/enhance"
headers = {
    "accept": "application/json",
    "x-api-key": api_key
}
files = {
    "file": open("sound-input.mp3", "rb")
}
data = {
    "loudness_target_level": "-14",
    "loudness_peak_limit": "-1",
    "enhancement_level": "1",
    "transcode_kind": "MP3"
}

response = requests.post(url, headers=headers, files=files, data=data)

# Optional: Check response
print(response.status_code)
print(response.json())

generated_name = response['generated_name']


import requests

url = f"https://api.ai-coustics.io/v1/media/{generated_name}"
headers = {
    "accept": "application/json",
    "x-api-key": api_key
}

response = requests.get(url, headers=headers)

# Check if request was successful
if response.status_code == 200:
    # Save the response content as an MPGA file
    with open("enhanced_sound.mpga", "wb") as file:
        file.write(response.content)
    print("File saved as enhanced_sound.mpga")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
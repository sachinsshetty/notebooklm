import requests
import os
from pathlib import Path
import dwani

# Set up Dwani API credentials
dwani.api_key = os.getenv("DWANI_API_KEY")
dwani.api_base = os.getenv("DWANI_API_BASE_URL")
api_key = os.getenv("SOUND_API_KEY")

# Generate speech using Dwani
response = dwani.Audio.speech(
    input="what is your name? I am sachin from Bonn",
    response_format="mp3",
    language="english"
)

# Save the generated audio
file_path = Path("sound-input.mp3")
with open(file_path, "wb") as f:
    f.write(response)

# Enhance audio using ai-coustics API
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

# Send POST request to enhance audio
response = requests.post(url, headers=headers, files=files, data=data)

# Check response status
if response.status_code == 201:
    response_data = response.json()  # Parse JSON response
    generated_name = response_data['generated_name']  # Access generated_name
    print(f"Generated name: {generated_name}")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
    exit()

# Download the enhanced audio
url = f"https://api.ai-coustics.io/v1/media/{generated_name}"
headers = {
    "accept": "application/json",
    "x-api-key": api_key
}

response = requests.get(url, headers=headers)

# Check if request was successful
if response.status_code == 200:
    with open("enhanced_sound.mpga", "wb") as file:
        file.write(response.content)
    print("File saved as enhanced_sound.mpga")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
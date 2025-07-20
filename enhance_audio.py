import requests
import os
from pathlib import Path
import dwani
import time
# Set up Dwani API credentials
dwani.api_key = os.getenv("DWANI_API_KEY")
dwani.api_base = os.getenv("DWANI_API_BASE_URL")
api_key = os.getenv("SOUND_API_KEY")

def generate_audio(text, file_name):
    # Generate speech using Dwani
    response = dwani.Audio.speech(
        input=text,
        response_format="mp3",
        language="english"
    )
    file_path = Path(file_name)
    with open(file_path, "wb") as f:
        f.write(response)


def enhance_audio(input_file_name, output_file_name, sound_configs):
    # Enhance audio using ai-coustics API
    url = "https://api.ai-coustics.io/v1/media/enhance"
    headers = {
        "accept": "application/json",
        "x-api-key": api_key
    }
    files = {
        "file": open(input_file_name, "rb")
    }

    # Send POST request to enhance audio
    response = requests.post(url, headers=headers, files=files, data=sound_configs)

    # Check response status
    if response.status_code == 201:
        response_data = response.json()  # Parse JSON response
        generated_name = response_data['generated_name']  # Access generated_name
        print(f"Generated name: {generated_name}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        exit()


    time.sleep(10)

    # Download the enhanced audio
    url = f"https://api.ai-coustics.io/v1/media/{generated_name}"
    headers = {
        "accept": "application/json",
        "x-api-key": api_key
    }

    response = requests.get(url, headers=headers)

    # Check if request was successful
    if response.status_code == 200:
        with open(output_file_name, "wb") as file:
            file.write(response.content)
        print(f"File saved as {output_file_name}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)


input_file_name = "sound-input.mp3" 

output_file_name = "enahnced_sound.mp3"
# Save the generated audio


sound_configs = {
        "loudness_target_level": "-14",
        "loudness_peak_limit": "-1",
        "enhancement_level": "1",
        "transcode_kind": "MP3"
}


text = "what is your name? I am sachin from Bonn"

generate_audio(text, input_file_name)
enhance_audio(input_file_name, output_file_name, sound_configs)

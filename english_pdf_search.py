import os
import tempfile
import io
import sounddevice as sd
import wavio
import platform
import subprocess
import dwani

import os 
dwani.api_key = os.getenv("DWANI_API_KEY")

dwani.api_base = os.getenv("DWANI_API_BASE_URL")


import io
import time
import httpx
import sounddevice as sd
import wavio

print("Recroding started")
# Parameters
duration = 5  # seconds per chunk
sample_rate = 16000
channels = 1

audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels)
sd.wait()


wav_io = io.BytesIO()
wavio.write(wav_io, audio_data, sample_rate, sampwidth=2)
wav_io.seek(0)

print("recoridng complte")
with open("input.wav", "wb") as f:
    f.write(wav_io.read())

response = dwani.ASR.transcribe(file_path="input.wav", language="english")

voice_text = response['text'] 
print(voice_text)

file_path = "sample_resume.pdf"
result = dwani.Documents.query_all(
    file_path, model="gemma3", tgt_lang="eng_Latn", prompt=voice_text
)

pdf_answer = result["translated_query_answer"]

print(pdf_answer)

response = dwani.Audio.speech(input = pdf_answer, response_format="wav", language="english")

        # Save the audio to a temporary file
with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
    temp_path = temp_file.name
    temp_file.write(response)

'''

# Play the audio based on the operating system
system = platform.system()
try:
    if system == "Windows":
        process = subprocess.run(["start", str(temp_path)], shell=True)
    elif system == "Darwin":  # macOS
        process = subprocess.run(["afplay", str(temp_path)])
    elif system == "Linux":
        process = subprocess.run(["aplay", str(temp_path)])
    else:
        print(f"Autoplay not supported on {system}. Open {temp_path} manually.")
        
except Exception as e:
    print(f"Error playing audio: {e}")
finally:
    # Clean up temporary file
    try:
        os.remove(temp_path)
    except Exception as e:
        print("Warning: Could not delete temporary file ")
'''
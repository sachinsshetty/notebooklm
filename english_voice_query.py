
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

result = dwani.ASR.transcribe(file_path="input.wav", language="english")


print(result)
'''
resp = dwani.Translate.run_translate(sentences=result['text'], src_lang="telugu", tgt_lang="english")
print(resp)

'''

resp = dwani.Chat.direct(prompt=result["text"])
print(resp)

response = dwani.Audio.speech(input = resp["response"], response_format="wav", language="english")
with open("output2.wav", "wb") as audio_file:
    audio_file.write(response)


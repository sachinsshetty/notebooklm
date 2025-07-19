
import dwani

import os 
dwani.api_key = os.getenv("DWANI_API_KEY")

dwani.api_base = os.getenv("DWANI_API_BASE_URL")


#response = dwani.Audio.speech(input="లిపి కుటుంబము యొక్క సభ్యుల మాతృక. ఇది ప్రస్తుతము వాడుకలో లేని లిపి. క్రీ.పూ.3వ శతాబ్దానికి చెందిన ప్రసిద్ధ అశోకుని శిలా శాసనాలు బ్రాహ్మీ లిపిలో చెక్కబడినవే", response_format="wav", language="telugu")
#with open("output.wav", "wb") as audio_file:
#    audio_file.write(response)


result = dwani.ASR.transcribe(file_path="output.wav", language="telugu")

print(result)

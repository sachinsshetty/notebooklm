notebooklm

### Install the library
```bash
pip install --upgrade dwani
```

### Setup the credentials
```python
import dwani
import os

dwani.api_key = os.getenv("DWANI_API_KEY")

dwani.api_base = os.getenv("DWANI_API_BASE_URL")
```


Test : English Query

python : english_voice_query.py

https://techeurope.notion.site/berlin-hackathon-manual


vllm serve google/gemma-3-4b-it --served-model-name gemma3 --host 0.0.0.0 --port 9000 --gpu-memory-utilization 0.8 --tensor-parallel-size 1 --max-model-len 120000     --dtype bfloat16 
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
```python
from googletrans import Translator

translated_text = Translator().translate("Hello, how are you?", src='en', dest='ar').text
print(translated_text)
```
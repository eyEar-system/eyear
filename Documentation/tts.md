# Text-to-Speech (TTS) Conversion with Speed and Pitch Modification

This Python script uses `gTTS` (Google Text-to-Speech) to convert text to speech, modifies the audio's speed and pitch using `pydub`, and plays the final modified audio. It also handles the cleanup of temporary files.

## Requirements

- `gTTS`: Google Text-to-Speech library for converting text to speech.
- `pydub`: Audio processing library for modifying audio speed and pitch.
- `os`: Standard library for file operations.
  
To install the necessary libraries, use:

```bash
pip install gtts pydub
```

```python
# Example usage
if __name__ == "__main__":

    # Example usage for Arabic
    arabic_text = "مرحباً بكم في تجربة تحويل النصوص إلى كلام."
    TTS.text_to_speech(arabic_text, 'ar')

    # Example usage for English
    english_text = "Welcome to the text-to-speech conversion demo."
    TTS.text_to_speech(english_text, 'en')


```
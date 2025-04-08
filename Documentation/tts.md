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
# Create TTS object 
tts = TTS()

# Directly set parameters and perform text-to-speech
english_text = "Welcome to the text-to-speech conversion demo."
tts.text_to_speech(english_text, lang="en", slow=False, speed_factor=1.4, pitch_factor=0.85)


```
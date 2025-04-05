# 🎤 Voice Recognition with Language Detection and Transcription

This project contains a Python class `VoiceRecognation` that processes audio files, detects the language of the audio, transcribes it to text, and then outputs the transcription along with the detected language and confidence score. The class supports MP3 files and converts them to WAV format for processing.

---

## 📌 Overview

The `VoiceRecognation` class allows you to:

1. **Convert MP3 files** to WAV format.
2. **Transcribe the audio** using Google's Speech Recognition API.
3. **Detect the language** of the transcribed text.
4. **Preprocess the text** to clean it and remove unwanted characters.

---

## 🛠️ Requirements

### 📦 Install Python Packages

```bash
pip install langdetect SpeechRecognition pydub
```
```python


# Example usage:
if __name__ == "__main__":
    mp3_file = "/content/latest.wav"
    audio_processor = VoiceRecognation(mp3_file , "ar")
    transcription, language, confidence = audio_processor.process_audio()
    print(f"Transcription for {mp3_file}:\n{transcription} \nDetected Language: {language} with Confidence: {confidence}")

```
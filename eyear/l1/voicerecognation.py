from langdetect import detect_langs
import speech_recognition as sr
from pydub import AudioSegment
import re
import math
import os

class VoiceRecognation:
    def __init__(self):
        self.input_file = None
        self.wav_file = None
        self.db_lang = None

    def load_file(self, input_file, db_lang):
        self.input_file = input_file
        self.db_lang = db_lang

        if input_file.endswith(".mp3"):
            self.wav_file = input_file.replace(".mp3", ".wav")
            self.convert_to_wav()
        elif input_file.endswith(".wav"):
            self.wav_file = input_file
            self.convert_to_wav()
        else:
            raise ValueError("Unsupported file format. Please provide an mp3 or wav file.")

    def convert_to_wav(self):
        try:
            audio = AudioSegment.from_file(self.input_file)
            audio = audio.set_frame_rate(16000)
            audio = audio.set_channels(1)
            audio = audio.set_sample_width(2)
            audio.export(self.wav_file, format="wav")
            print(f"Conversion successful! File saved as {self.wav_file}")
        except Exception as e:
            print(f"Error during conversion: {e}")

    def transcribe_audio(self, language, chunk_length_ms=10000):
        recognizer = sr.Recognizer()
        audio = AudioSegment.from_wav(self.wav_file)
        duration_ms = len(audio)
        num_chunks = math.ceil(duration_ms / chunk_length_ms)
        result_text = ""

        for i in range(num_chunks):
            start = i * chunk_length_ms
            end = min(start + chunk_length_ms, duration_ms)
            chunk = audio[start:end]
            chunk_filename = f"chunk_{i}.wav"
            chunk.export(chunk_filename, format="wav")

            try:
                with sr.AudioFile(chunk_filename) as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio_data = recognizer.record(source)
                    text = recognizer.recognize_google(audio_data, language=language)
                    result_text += " " + text
            except sr.UnknownValueError:
                print(f"Chunk {i} not understood.")
            except sr.RequestError as e:
                print(f"Chunk {i} failed: {e}")
            finally:
                if os.path.exists(chunk_filename):
                    os.remove(chunk_filename)

        return result_text.strip()

    def preprocess_text(self, text):
        text = text.lower()
        text = re.sub(r'[^a-zA-Z0-9\s\u0621-\u064A]', '', text)
        text = text.strip()
        return text

    def detect_language(self, text):
        if self.db_lang == 'ar':
            return 'ar', 1.0
        elif self.db_lang == 'en':
            return 'en', 1.0
        else:
            try:
                text = self.preprocess_text(text)
                languages = detect_langs(text)
                if languages:
                    detected_language = max(languages, key=lambda x: x.prob)
                    return detected_language.lang, detected_language.prob
                else:
                    return "unknown", 0.0
            except Exception as e:
                return f"Error detecting language: {e}", 0.0

    def process_audio(self):
        temp_text = self.transcribe_audio('en')
        detected_language, confidence = self.detect_language(temp_text)

        if confidence > 0.7:
            if detected_language == 'ar':
                print("Arabic detected, transcribing in Arabic.")
                text = self.transcribe_audio('ar')
            elif detected_language == 'en':
                print("English detected, transcribing in English.")
                text = self.transcribe_audio('en')
            else:
                print(f"Unknown language ({detected_language}), defaulting to Arabic.")
                text = self.transcribe_audio('ar')
                detected_language = 'ar'
        else:
            print(f"Low confidence ({confidence}), defaulting to Arabic transcription.")
            text = self.transcribe_audio('ar')
            detected_language = 'ar'

        return text, detected_language, confidence


# Example usage:
if __name__ == "__main__":
    mp3_file = "/content/latest.wav"
    audio_processor = VoiceRecognation()
    audio_processor.load_file(mp3_file, "en")
    transcription, language, confidence = audio_processor.process_audio()
    print(f"\nTranscription for {mp3_file}:\n{transcription}\n\nDetected Language: {language} with Confidence: {confidence}")

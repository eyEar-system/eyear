from langdetect import detect_langs
import speech_recognition as sr
from pydub import AudioSegment
import re

class VoiceRecognation:
    def __init__(self):
        self.input_file = None
        self.wav_file = None
        self.db_lang = None

    def load_file(self, input_file, db_lang):
        """Set the file and language, and handle conversion if needed."""
        self.input_file = input_file
        self.db_lang = db_lang

        if input_file.endswith(".mp3"):
            self.wav_file = input_file.replace(".mp3", ".wav")
            self.convert_to_wav()
        elif input_file.endswith(".wav"):
            self.wav_file = input_file
        else:
            raise ValueError("Unsupported file format. Please provide an mp3 or wav file.")

    def convert_to_wav(self):
        try:
            audio = AudioSegment.from_file(self.input_file)
            audio.export(self.wav_file, format="wav")
            print(f"Conversion successful! File saved as {self.wav_file}")
        except Exception as e:
            print(f"Error during conversion: {e}")

    def transcribe_audio(self, language):
        recognizer = sr.Recognizer()
        try:
            with sr.AudioFile(self.wav_file) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data, language=language)
            return text
        except sr.UnknownValueError:
            return "Google Speech Recognition could not understand the audio."
        except sr.RequestError as e:
            return f"Could not request results from Google Speech Recognition service; {e}"

    def preprocess_text(self, text):
        text = text.lower()
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
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
        text = self.transcribe_audio('en')
        detected_language, confidence = self.detect_language(text)

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
    audio_processor.load_file(mp3_file, "ar")
    transcription, language, confidence = audio_processor.process_audio()
    print(f"Transcription for {mp3_file}:\n{transcription} \nDetected Language: {language} with Confidence: {confidence}")

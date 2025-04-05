from langdetect import detect_langs
import speech_recognition as sr
from pydub import AudioSegment
import re

class VoiceRecognation:
    def __init__(self, mp3_file):
        self.mp3_file = mp3_file
        self.wav_file = mp3_file.replace(".mp3", ".wav")

    def convert_to_wav(self):
        """Converts an MP3 file to WAV format."""
        try:
            audio = AudioSegment.from_file(self.mp3_file)
            audio.export(self.wav_file, format="wav")
            print(f"Conversion successful! File saved as {self.wav_file}")
        except Exception as e:
            print(f"Error during conversion: {e}")

    def transcribe_audio(self, language):
        """Transcribe audio from WAV file to text based on the given language."""
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
        """Clean the text by removing noise and unwanted characters."""
        text = text.lower()  # Convert to lowercase
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove non-alphanumeric characters
        text = text.strip()  # Remove leading/trailing spaces
        return text

    def detect_language(self, text):


        # Initialize Firebase Realtime Database
        firebase_config = FirebaseRealtimeManager()
        db = firebase_config.get_db()
        print("Database connected.")

        # Get data
        db_lang = db.child("lang").get().val()
        print(db_lang)

        if db_lang == 'ar':
            return 'ar', 1.0
        elif db_lang == 'en':
            return 'en', 1.0
        else:
            try:
                text = self.preprocess_text(text)  # Clean the text before detection
                # Detect possible languages and their confidence scores
                languages = detect_langs(text)
                if languages:
                    # Get the language with the highest confidence
                    detected_language = max(languages, key=lambda x: x.prob)
                    confidence = detected_language.prob
                    return detected_language.lang, confidence
                else:
                    return "unknown", 0.0
            except Exception as e:
                return f"Error detecting language: {e}", 0.0

    def process_audio(self):
        """Convert MP3 to WAV, detect language, and transcribe audio."""
        self.convert_to_wav()  # Convert the MP3 to WAV

        # First, transcribe in English
        text = self.transcribe_audio('en')  # Default to English transcription first
        detected_language, confidence = self.detect_language(text)

        # Adjust the threshold for language confidence
        if confidence > 0.7:  # Higher threshold for confident detection
            if detected_language == 'ar':
                text = self.transcribe_audio('ar')  # Transcribe in Arabic if detected
                print("Arabic detected, transcribing in Arabic.")
            elif detected_language == 'en':
                text = self.transcribe_audio('en')  # Transcribe in English if detected
                print("English detected, transcribing in English.")
            else:
                print(f"Unknown detected language: {detected_language}. Defaulting to Arabic transcription.")
                text = self.transcribe_audio('ar')  # Default to Arabic transcription
        else:
            print(f"Low confidence ({confidence}) detected, defaulting to Arabic transcription.")
            text = self.transcribe_audio('ar')  # Default to Arabic transcription
            detected_language = 'ar'
        return text, detected_language, confidence


# Example usage:
if __name__ == "__main__":
    mp3_file = "/content/latest.wav"  
    audio_processor = VoiceRecognation(mp3_file)
    transcription, language, confidence = audio_processor.process_audio()
    print(f"Transcription for {mp3_file}:\n{transcription} \nDetected Language: {language} with Confidence: {confidence}")

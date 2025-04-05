#requirments
#!pip install pydub gtts

from pydub import AudioSegment
from pydub.playback import play
from gtts import gTTS
import os


class TTS:
    def __init__(self, text, lang, slow=False, speed_factor=1.5, pitch_factor=1.2):
        """
        Initialize the TextToSpeech class with the required parameters.

        Parameters:
        - text: The text to convert to speech.
        - lang: The language of the text (e.g., 'ar' for Arabic, 'en' for English).
        - slow: Whether the speech should be slow (default is False).
        - speed_factor: The factor by which to speed up the speech (default is 1.5).
        - pitch_factor: The factor by which to increase the pitch of the speech (default is 1.2).
        """
        self.text = text
        self.lang = lang
        self.slow = slow
        self.speed_factor = speed_factor
        self.pitch_factor = pitch_factor
        self.audio_path = "/content/output_gtts.mp3"  # Path for the initial speech file.
        self.final_audio_path = "/content/output.mp3"  # Path for the final modified speech file.
        self.wav_audio_path = "/content/output.wav"   # Path for the final WAV file.

    def convert_to_speech(self):
        """
        Convert the input text to speech using gTTS and save it as an audio file.
        """
        try:
            # Create a gTTS (Google Text-to-Speech) object.
            tts = gTTS(text=self.text, lang=self.lang, slow=self.slow)

            # Save the speech to an audio file.
            tts.save(self.audio_path)
            print("Audio file created successfully!")
        except Exception as e:
            print(f"Error during text-to-speech conversion: {e}")
            raise

    def modify_audio(self):
        """
        Modify the speech audio by changing its speed and pitch.
        """
        try:
            # Load the original audio file using pydub.
            sound = AudioSegment.from_file(self.audio_path)

            # Normalize audio to improve clarity.
            normalized_sound = sound.normalize()

            # Change the speed of the audio.
            speed_changed_sound = normalized_sound.speedup(playback_speed=self.speed_factor)

            # Change the pitch by modifying the frame rate.
            pitch_changed_sound = speed_changed_sound._spawn(speed_changed_sound.raw_data, overrides={
                "frame_rate": int(speed_changed_sound.frame_rate * self.pitch_factor)
            }).set_frame_rate(44100)  # Set a standard sample rate for better quality

            # Export the final modified audio to an MP3 file.
            pitch_changed_sound.export(self.final_audio_path, format="mp3")
            print("Final audio file saved!")

            # Export the final modified audio to a WAV file.
            pitch_changed_sound.export(self.wav_audio_path, format="wav")
            print("Final WAV audio file saved!")
        except Exception as e:
            print(f"Error during audio modification: {e}")
            raise

    def play_audio(self):
        """
        Play the final modified audio.
        """
        try:
            # Load and play the final audio file.
            sound = AudioSegment.from_file(self.final_audio_path)
            play(sound)
        except Exception as e:
            print(f"Error during audio playback: {e}")

    def clean_up(self):
        """
        Remove temporary files to save disk space.
        """
        try:
            if os.path.exists(self.audio_path):
                os.remove(self.audio_path)
            print("Temporary files cleaned up!")
        except Exception as e:
            print(f"Error during cleanup: {e}")

    @staticmethod
    def text_to_speech(text, lang):
        """
        Convert text to speech, modify the audio, and play it.

        Parameters:
        - text: The text to be converted to speech.
        - lang: The language code (e.g., 'ar' for Arabic, 'en' for English).
        """
        try:
            # Create an instance of the TextToSpeech class with the text and language.
            speech = TextToSpeech(text, lang, slow=False, speed_factor=1.4, pitch_factor=0.85)

            # Convert the text to speech and save the initial audio.
            speech.convert_to_speech()

            # Modify the audio by changing speed and pitch and save copies in MP3 and WAV formats.
            speech.modify_audio()

            # Play the final modified audio.
            speech.play_audio()
        finally:
            # Clean up temporary files.
            speech.clean_up()

# Example usage
if __name__ == "__main__":

    # Example usage for Arabic
    arabic_text = "مرحباً بكم في تجربة تحويل النصوص إلى كلام."
    TTS.text_to_speech(arabic_text, 'ar')

    # Example usage for English
    english_text = "Welcome to the text-to-speech conversion demo."
    TTS.text_to_speech(english_text, 'en')

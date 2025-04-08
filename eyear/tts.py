from pydub import AudioSegment
from pydub.playback import play
from gtts import gTTS
import os


class TTS:
    def __init__(self):
        """
        Initialize the TextToSpeech class with default parameters.
        """
        self.text = ""  # Default text (empty string)
        self.lang = "en"  # Default language (English)
        self.slow = False  # Default speed (normal speed)
        self.speed_factor = 1.5  # Default speed factor
        self.pitch_factor = 1.2  # Default pitch factor
        self.audio_path = "/content/output_gtts.mp3"  # Path for the initial speech file.
        self.final_audio_path = "/content/output.mp3"  # Path for the final modified speech file.
        self.wav_audio_path = "/content/output.wav"   # Path for the final WAV file.

    def set_parameters(self, text, lang="en", slow=False, speed_factor=1.5, pitch_factor=1.2):
        """
        Set parameters for the text-to-speech conversion.
        """
        self.text = text
        self.lang = lang
        self.slow = slow
        self.speed_factor = speed_factor
        self.pitch_factor = pitch_factor

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

    def text_to_speech(self, text, lang="en", slow=False, speed_factor=1.5, pitch_factor=1.2):
        """
        This method is used to process the text-to-speech conversion, modify it, and play the audio.
        """
        # Set parameters and perform conversion
        self.set_parameters(text, lang, slow, speed_factor, pitch_factor)
        try:
            # Convert the text to speech and save the initial audio.
            self.convert_to_speech()

            # Modify the audio by changing speed and pitch and save copies in MP3 and WAV formats.
            self.modify_audio()

            # Play the final modified audio.
            self.play_audio()
        finally:
            # Clean up temporary files.
            self.clean_up()


# Example usage with instantiation of TTS class
if __name__ == "__main__":
    # Create TTS object without arguments
    tts = TTS()

    # Directly set parameters and perform text-to-speech
    english_text = "Welcome to the text-to-speech conversion demo."
    tts.text_to_speech(english_text, lang="en", slow=False, speed_factor=1.4, pitch_factor=0.85)

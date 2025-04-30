import os
import io
import struct
import wave
from gtts import gTTS
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
from eyear import FirebaseRealtimeManager, FirebaseStorageManager , json_content

class Speaker:
    def __init__(self ,storage_manager ,db ):
        self.storage_manager = storage_manager
        self.db = db
        self.output_directory = "output/"
        self.max_file_size = 40923

        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

    def convert_to_8bit_mono(self, input_audio):
        try:
            audio = AudioSegment.from_file(input_audio, format="mp3")
            audio = audio.set_channels(1)
            audio = audio.set_sample_width(1)  # 8-bit

            output_wav = io.BytesIO()
            audio.export(output_wav, format="wav")
            output_wav.seek(0)
            return output_wav
        except CouldntDecodeError as e:
            raise ValueError(f"Error decoding file: {e}")

    def adjust_pitch(self, audio, pitch_factor=1.5):
        return audio._spawn(audio.raw_data, overrides={
            "frame_rate": int(audio.frame_rate * pitch_factor)
        }).set_frame_rate(audio.frame_rate)

    def convert_text_to_speech(self, text, lang='ar'):
        tts = gTTS(text, lang=lang, slow=False)
        tts.save("output_tts.mp3")

        tts_audio = self.convert_to_8bit_mono("output_tts.mp3")
        audio = AudioSegment.from_file(tts_audio)
        pitch_adjusted_audio = self.adjust_pitch(audio, pitch_factor=1.8)

        pitch_adjusted_wav = io.BytesIO()
        pitch_adjusted_audio.export(pitch_adjusted_wav, format="wav")
        pitch_adjusted_wav.seek(0)
        return pitch_adjusted_wav

    def wav_to_byte_array(self, input_wav):
        if isinstance(input_wav, bytes):
            input_wav = io.BytesIO(input_wav)

        wav_data = input_wav.read()
        with wave.open(io.BytesIO(wav_data), 'rb') as wav_file:
            sample_rate = wav_file.getframerate()
            num_samples = wav_file.getnframes()
            num_channels = wav_file.getnchannels()
            sample_width = wav_file.getsampwidth()

            if num_channels != 1:
                raise ValueError("The WAV file must be mono (1 channel).")
            if sample_width != 1:
                raise ValueError("The WAV file must be 8-bit PCM format.")

            audio_data = wav_file.readframes(num_samples)
            byte_array = list(audio_data)

            header = [
                0x52, 0x49, 0x46, 0x46,
                0x00, 0x00, 0x00, 0x00,
                0x57, 0x41, 0x56, 0x45,
                0x66, 0x6D, 0x74, 0x20,
                0x10, 0x00, 0x00, 0x00,
                0x01, 0x00,
                0x01, 0x00,
                sample_rate & 0xFF, (sample_rate >> 8) & 0xFF,
                (sample_rate >> 16) & 0xFF, (sample_rate >> 24) & 0xFF,
                sample_rate & 0xFF, (sample_rate >> 8) & 0xFF,
                0x01, 0x00, 0x08, 0x00,
            ]

            data_header = [
                0x64, 0x61, 0x74, 0x61,
                0x00, 0x00, 0x00, 0x00
            ]

            data_size = len(byte_array)
            header[4:8] = struct.pack('<I', 36 + data_size)
            data_header[4:8] = struct.pack('<I', data_size)

            full_wave = bytes(header) + bytes(data_header) + bytes(byte_array)
            return full_wave

    def save_to_file(self, force, original_wav):
        offset = 0
        file_count = 1

        while offset < len(force):
            file_name = f'{self.output_directory}force_data{file_count}.bin'
            with open(file_name, 'wb') as file:
                file.write(force[offset:offset + self.max_file_size])
            print(f"Created and uploaded: force_data{file_count}.bin")

            self.storage_manager.upload_file(file_name, f"bin/force_data{file_count}.bin")
            offset += self.max_file_size
            file_count += 1

        # Adjust the pitch of the audio
        wav_filename = f"{self.output_directory}full_audio.wav"
        if isinstance(original_wav, bytes):
            original_wav = io.BytesIO(original_wav)

        # Load the audio data
        audio = AudioSegment.from_wav(original_wav)

        # Lower the pitch (shift by -2 semitones as an example)
        lower_pitch_audio = audio._spawn(audio.raw_data, overrides={
            "frame_rate": int(audio.frame_rate * 0.65)  # Lower pitch by 20%
        })

        # Save the new audio with the lower pitch
        lower_pitch_audio.export(wav_filename, format="wav")

        self.storage_manager.upload_file(wav_filename, "wav/full_audio.wav")
        print("Full WAV uploaded with lower pitch.")

        coun = file_count - 1
        self.db.child("/wearable_device").update({"FileNum": coun})
        self.db.child("/wearable_device/z-sensors").update({"audio_uploaded": True})
        self.db.child("/wearable_device").update({"play_audio": True})

    def process(self, text, lang='ar'):
        print("Processing text to speech...")
        tts_wav = self.convert_text_to_speech(text, lang)
        original_wav = io.BytesIO(tts_wav.read())
        tts_wav.seek(0)

        force_array = self.wav_to_byte_array(tts_wav)
        self.save_to_file(force_array, original_wav)
        print("Done ✅")

if __name__ == "__main__":
    speaker = Speaker(storage_manager , db)

    speaker.process("Hello, this is a test for text to speech using gTTS.", lang='en')

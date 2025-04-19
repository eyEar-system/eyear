import eyear
from eyear import FirebaseStorageManager , json_content , FirebaseRealtimeManager
from eyear import ImageCaptionGenerator , ImageQA
from eyear import Bot
from eyear import ResearchBot
from eyear import TTS
from eyear import VoiceRecognation
from eyear import OCR
from googletrans import Translator
from eyear import HandGusteur
from eyear import raw_training_data
from eyear import TrainingData
from eyear import IntentClassifier

firebase_config = FirebaseRealtimeManager()
db = firebase_config.get_db()
training_data_manager = TrainingData(db)
training_data_manager.save_training_data(raw_training_data)
fetched_data = training_data_manager.fetch_training_data()
print(f"Fetched Data: {fetched_data}")
storage_manager = FirebaseStorageManager(json_content, "eyear-87a0e.appspot.com")
bot = Bot()
gesture_recognition = HandGusteur()
image_QA = ImageQA()
image_caption_generator = ImageCaptionGenerator()
classifier = IntentClassifier(db)
classifier.train_model()
classifier.test_model()
classifier.save_model()
ocr = OCR()
research_bot = ResearchBot ()
voice_recognation = VoiceRecognation()
tts = TTS()




print(" start import")

from .core import EyEar  
from  .firebase import FirebaseStorageManager ,FirebaseRealtimeManager
print("Done : " , "from .firebase import FirebaseStorageManager ,FirebaseRealtimeManager")
from  .imageProcess import ImageCaptionGenerator , ImageQA
print("Done : " , "from .imageProcess import ImageCaptionGenerator , ImageQA")
from  .bot import Bot
print("Done : " , "from .bot import Bot")
from  .researchbot import ResearchBot
print("Done : " , "from .researchbot import ResearchBot")
from  .tts import TTS
print("Done : " , "from .tts import TTS")
from  .voicerecognation import VoiceRecognation
print("Done : " , "from .voicerecognation import VoiceRecognation")
from  .ocr import OCR
print("Done : " , "from .ocr import OCR")
from  .handgusteur import HandGusteur
print("Done : " , "from .handgusteur import HandGusteur")
from  .Intentclassifier import IntentClassifier
print("Done : " , "from .Intentclassifier import IntentClassifier")
from  .rawdata import raw_training_data
print("Done : " , "from .rawdata import raw_training_data")
from  .trainingdata import TrainingData
print("Done : " , "from trainingdata import TrainingData")
from .speaker import Speaker 
print("Done : " , "from .speaker import Speaker ")
from .facegusteur import FaceGusteur
print("Done : " , "from .facegusteur import FaceGusteur")
from .casecommand import CaseCommand
print("Done : " , "from .casecommand import CaseCommand")
from .facerecognation import FaceRecognition
print("Done : " , "from .facerecognation import FaceRecognition")
from .memorybot import MemoryBot
print("Done : " , "from .memorybot import MemoryBot")



print(" finish import")



# JSON content as a string
json_content = """
{
  "apiKey": "AIzaSyCBvKO1K2FJ_MoPXAckuga40mwG593Qo7o",
  "authDomain": "eyear-87a0e.firebaseapp.com",
  "databaseURL": "https://eyear-87a0e-default-rtdb.firebaseio.com",
  "projectId": "eyear-87a0e",
  "storageBucket": "eyear-87a0e.appspot.com",
  "messagingSenderId": "337767300301",
  "appId": "1:337767300301:web:050cb7adf9c7d0e3b8bd84",
  "measurementId": "G-8SRQ7WFTPK",
  "type": "service_account",
  "project_id": "eyear-87a0e",
  "private_key_id": "9e6c262904034236feaf43a2745a1511dace0ffe",
  "private_key": "-----BEGIN PRIVATE KEY-----\\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDDtRpvGYatkBtT\\nver2hhIv8NBLeD8M+v1U62FbIyFT4E10+/HlZV57WyrDQOZQaY883nhgQKuMvl//\\n1MqSwP4cM2FOl465v1wOBpdYcqing56IhluGL5hbq56PJXNhls96SsH2NYNJypO3\\nnkGIwwN8dBLNxzgE18K0eayDNccg/MXzIY76EN4oj4DkcdxMBQe9Na0WwDxpDZQ3\\noFuUYmJqQIcMYnljh9CGoVzeHRcCprQOp8aJANnGPLGoipgF6Xh0AFi+VJWVqwXx\\nFY7cNsuCxGbeYa7prVMypQg6D8DDVpZv+mKmVQ30qtEa1I48vHGmitQBQ7X4xaFT\\nxPw1PlQLAgMBAAECggEACOdE0Bgbseqz64/g0B1SV37/oudSCv+iJcpdj/1dp0i1\\njWRm4VZGwZroq6BYugDLZOwEEvDuPQVuLZ/bJWkFRngp7Z7kfdvQTs0K9pmkxZYt\\n0K04HbctmcIJgR6ljKOFRd1/zHkrw2Albz2SYqvojTFkp5rwF/xO3dIJQKDiMcRp\\nyDl24Jadfbn+gXOfagxV0VmpG6iFyeXB3JwgV5gRMvO2c2z4b03oZb2WIEDS76q7\\nrXpjsUuLd39oRjS2/ai804QwrPDcjvVbcl1FxINu5FLh2Xpg16Ga9o0dQFobXzcN\\nDawbvDXwY53j/2WxcJ44DjIdQfp8SzA00ta7lZ5q5QKBgQDkX4mEDLJRCUN0PbO6\\n3y8diMzgKeKjdE2CTtzU1E2ODe9ysPLGBTnDIULqyPS9Pu5FwOANX9EeQ8+omapK\\nUh61SpVcCnet5Pxg/9i6L4CdP0Hx97GJxoXMvBS/AUVcCQ96Pt+oQw30DVLWS5g2\\nZWWoMJa7IvF3r7OakwmQMbjtnwKBgQDbYfGsuy7j/HAighF40Z38mzth9Kr8ZF40\\n/t/dfutVJzfYHM5gW74WAy+pb1xeA/lmQezjIcgozye4glHXF/luF8WOUI8zAd9s\\nKwElD4XDILYskt3L7M7HJbeV0Hq8iaSidkvDgTqZfbVYgQqOglI4qRH7PODWjFgL\\n5pfApPFqFQKBgEQFMLBkF7iLScwVlLLURvRFCsC5uQd2XJ+zXZMGqRLmk6tViPny\\nFIJKJeRIdpznYZDlIdbZ8y9Qg0l0e4QncX4N+O6xL3Rb/8/kZGkQPP6ZGMs5O2gN\\n+UxBuOwrNL109Wcz0uoLDtziGwo4+d051k2CK2MRxVogux4PLYoFRU+BAoGBANpd\\nbmJBWxYhgjhHAT8iXsA+f2gsUjmxabgUbh4ZpAL5a3OYkK+HAfkFKN7c8rK9//QR\\n8MnQKVy9fcsBJJcVzPgRf1n9w9vApHQVhikufzVPjSVm9pBx4QyG9WqQvmqGEzKG\\nzzkFm5+GaghzQV/CRjcRys0ptp63yTfnSeu+AnJVAoGAbna63YIV9T56tJif0Pcr\\nMCadWPNZcS2ouTlh59gpzfeyQHDtH8cKwCz6zywWUhOTL8LK/sdyZh56k8hHYbRv\\nFt5M4SLMbNUu/kK2fckzELvCs0F0rlnnrMzrH3j8qgnnoZc/NHMaYgEQAFqwEDN5\\nwbaqBuzcNb3wD42qisquRt8=\\n-----END PRIVATE KEY-----\\n",
  "client_email": "firebase-adminsdk-ryxnv@eyear-87a0e.iam.gserviceaccount.com",
  "client_id": "111654604269586112994",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-ryxnv%40eyear-87a0e.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
"""

print("JSON content as a string done.")


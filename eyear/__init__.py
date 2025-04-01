
from .core import EyEar  
from .firebase import FirebaseStorageManager
from .var import config, json_content
print("finish library")



print("config content as a string done.")
# Initialize Firebase
firebase = pyrebase.initialize_app(config)
db = firebase.database()  # Using Realtime Database

print("Firebase initialized successfully.")


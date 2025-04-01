#requirmennts 
#!pip install pyrebase4

import pyrebase
import firebase_admin
from firebase_admin import credentials, db, storage
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
import json
from datetime import timedelta


class FirebaseStorageManager:
    def __init__(self, service_account_json, bucket_name):
        """Initialize Firebase Storage with the provided credentials and bucket name."""
        self.service_account_json = service_account_json
        self.bucket_name = bucket_name
        self._initialize_firebase()

    def _initialize_firebase(self):
        """Initialize Firebase if not already initialized."""
        if not firebase_admin._apps:
            # تغيير اسم المتغير هنا لتجنب التعارض
            firebase_cred = firebase_credentials.Certificate(json.loads(self.service_account_json))
            firebase_admin.initialize_app(firebase_cred, {'storageBucket': self.bucket_name})
        self.bucket = storage.bucket()

    def generate_access_token(self):
        """Generate an access token for the service account."""
        try:
            credentials = Credentials.from_service_account_info(json.loads(self.service_account_json))
            credentials.refresh(Request())
            return credentials.token
        except Exception as e:
            print(f"Error generating access token: {e}")
            return None

    def upload_file(self, local_file_path, cloud_blob_name, expiration_days=7):
        """Upload a file and generate a signed URL for it."""
        try:
            blob = self.bucket.blob(cloud_blob_name)
            blob.upload_from_filename(local_file_path)
            print(f"File uploaded: {local_file_path} → {cloud_blob_name}")

            # Generate signed URL for accessing the file
            signed_url = blob.generate_signed_url(expiration=timedelta(days=expiration_days))
            return signed_url
        except Exception as e:
            print(f"Error uploading file: {e}")
            return None

    def download_file(self, cloud_blob_name, local_file_path):
        """Download a file from Firebase Storage to local storage."""
        try:
            blob = self.bucket.blob(cloud_blob_name)
            blob.download_to_filename(local_file_path)
            #print(f"File downloaded: {cloud_blob_name} → {local_file_path}")
            return local_file_path
        except Exception as e:
            print(f"Error downloading file: {e}")
            return None

if __name__ == "__main__":

    # Initialize the Firebase Storage manager
    storage_manager = FirebaseStorageManager(json_content, "eyear-87a0e.appspot.com")

    # Upload a file and generate a signed URL
    signed_url = storage_manager.upload_file("/content/force_data3.bin", "bin/2force_data.bin")
    if signed_url:
        print(f"Generated Signed URL: {signed_url}")

    # Download a file from Firebase
    local_path = storage_manager.download_file("test_voice/latest.wav", "/content/downloaded_file.wav")
    if local_path:
        print(f"File downloaded to: {local_path}")


class FirebaseConfig:
    # Firebase configuration as a class variable
    config = {
        'apiKey': "AIzaSyCBvKO1K2FJ_MoPXAckuga40mwG593Qo7o",
        'authDomain': "eyear-87a0e.firebaseapp.com",
        'databaseURL': "https://eyear-87a0e-default-rtdb.firebaseio.com",
        'projectId': "eyear-87a0e",
        'storageBucket': "eyear-87a0e.appspot.com",
        'messagingSenderId': "337767300301",
        'appId': "1:337767300301:web:050cb7adf9c7d0e3b8bd84",
        'measurementId': "G-8SRQ7WFTPK"
    }

    def __init__(self):
        """Constructor to initialize Firebase"""
        self.firebase = None
        self.db = None
        self._initialize_firebase()

    def _initialize_firebase(self):
        """Initialize Firebase with the config"""
        self.firebase = pyrebase.initialize_app(self.config)
        self.db = self.firebase.database()  # Using Realtime Database
        print("Firebase initialized successfully.")

    def get_db(self):
        """Return the Firebase Realtime Database object"""
        return self.db

# Example of how to use the class
if __name__ == "__main__":
    firebase_config = FirebaseConfig()  # Initialize the class and Firebase
    db_instance = firebase_config.get_db()  # Get the Realtime Database instance
    print("Database instance retrieved.")

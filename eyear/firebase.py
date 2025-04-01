#requirmennts 
#!pip install pyrebase4


import pyrebase
import firebase_admin
from firebase_admin import credentials, db
from firebase_admin import credentials as firebase_credentials, storage
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
import json
from datetime import timedelta
import firebase_admin
from firebase_admin import credentials as firebase_credentials, storage
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


import pyrebase
import firebase_admin
from firebase_admin import credentials, db, storage
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
import json
from datetime import timedelta


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

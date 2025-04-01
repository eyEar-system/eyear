
## FirebaseStorageManager

### Initialize storage
```python
    # Initialize the Firebase Storage manager
    storage_manager = FirebaseStorageManager(json_content, "eyear-87a0e.appspot.com")
```

### downoad
```python
    # Download a file from Firebase
    local_path = storage_manager.download_file("test_voice/latest.wav", "/content/downloaded_file.wav")
    if local_path:
        print(f"File downloaded to: {local_path}")
```

### upload
```python
    # Upload a file and generate a signed URL
    signed_url = storage_manager.upload_file("content/downloaded_file.wav", "test_voice/latest.wav")
    if signed_url:
        print(f"Generated Signed URL: {signed_url}")
```


## FirebaseRealtimeManager
```python 
    # Initialize Firebase Realtime Database
    firebase_config = FirebaseRealtimeManager()
    db = firebase_config.get_db()
    print("Database connected.")
```

### Add data
```python 
    # Add data
    db.child("test").set({"LED": True})
    print("LED flag is True.")
```

### Get data
```python 
    # Get data
    led = db.child("test/LED").get()
    print("led flag condition :", led.val())

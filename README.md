# eyEar Library 

A simple Python package for eyEar functionalities.

## Installation

```python
!pip install git+https://github.com/eyEar-system/eyear.git
```

## Firebase_Storage_Manager

### Initialize
```python
    # Initialize the Firebase Storage manager
    storage_manager = FirebaseStorageManager(json_content, "eyear-87a0e.appspot.com")
```
### upload
```python
    # Upload a file and generate a signed URL
    signed_url = storage_manager.upload_file("/content/force_data3.bin", "bin/2force_data.bin")
    if signed_url:
        print(f"Generated Signed URL: {signed_url}")
```
### downoad
```python
    # Download a file from Firebase
    local_path = storage_manager.download_file("test_voice/latest.wav", "/content/downloaded_file.wav")
    if local_path:
        print(f"File downloaded to: {local_path}")
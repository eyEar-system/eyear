:

# HandGesture Documentation

## Introduction

This document aims to explain how to use the custom code for gesture analysis through images using the Mediapipe library. The code allows you to detect hands, identify landmarks, and track various gestures. It processes the given images and extracts detailed data such as the number of hands detected and any gestures that may be present.

---

## System Requirements

Before you begin, make sure you have installed all the necessary dependencies:

- **Python 3.x**
- **Libraries**:
  - `mediapipe`
  - `opencv-python`
  - `numpy`
  - `os`

To install these libraries, you can use the following command:

```bash
!pip install mediapipe opencv-python numpy
```

---

## How to Use

### 1. Setting Up the Environment

First, make sure you have installed the required libraries. Then, upload the image you want to process.

### 2. Preparing the Image

You must specify the correct path to the image you wish to analyze. In the code, you can define the path like this:

```python
image_path = "path_to_your_image.jpg"
```

### 3. Processing the Image

The next step is to process the image using the code to extract the hand and gesture data. You can do this using the following code:

```python
# Process the image and extract data
gesture_recognition = HandGusteur()
data = gesture_recognition.process_image(image_path)
```

### 4. Handling the Extracted Data

After processing, you will get detailed data about the hands and gestures detected. You can print this data using the following code:

```python
# Number of hands in the image
print("Number of hands in the image:", data["hands_in_frame"])

# Coordinates of the hand landmarks
print("Coordinates of hand landmarks:")
for idx, landmarks in enumerate(data["landmarks"]):
    print(f"Hand {idx + 1}:")
    for lm in landmarks:
        print(f"Landmark: ({lm.x}, {lm.y})")

# Detected gestures
print("Detected gestures:", data["gestures"])
```


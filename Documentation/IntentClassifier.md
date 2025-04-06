# Intent Classifier Documentation

## Overview

This project implements an Intent Classifier using **Natural Language Processing (NLP)** techniques and a **Random Forest Classifier** for intent prediction. It fetches training and feedback data from Firebase, trains the model, and then allows it to predict the intent of user input. The model also collects user feedback to improve over time.

### Key Features:
- Fetches training and feedback data from Firebase.
- Trains a RandomForestClassifier with the training data.
- Allows real-time prediction of user intents.
- Collects feedback from users and updates Firebase with the correct intent.
- Saves and loads the model and vectorizer.

## Prerequisites

- Python 3.x
- Libraries:
  - `nltk`
  - `scikit-learn`
  - `joblib`
  - `firebase`
  - `TfidfVectorizer`
  - `RandomForestClassifier`

Install the required libraries by running:

```bash
pip install nltk scikit-learn joblib pyrebase
```

Ensure required NLTK resources are downloaded:
```python
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
```

## Class: `IntentClassifier`

### `__init__(self, db)`

**Parameters:**
- `db`: Firebase Realtime Database object.

Initializes the classifier with a Firebase database instance, a `TfidfVectorizer` for text vectorization, and a `RandomForestClassifier` for training the model.

### Method: `preprocess_text(self, text)`

**Parameters:**
- `text`: String input.

**Returns:**
- Preprocessed string (lowercase).

This method preprocesses the input text by converting it to lowercase.

### Method: `get_training_data(self)`

**Returns:**
- `training_list`: List of training data fetched from Firebase.

Fetches the training data from Firebase Realtime Database. If no data is found, it returns `None`.

### Method: `get_feedback_data(self)`

**Returns:**
- `feedback_list`: List of feedback data fetched from Firebase.

Fetches the feedback data from Firebase Realtime Database. If no data is found, it returns `None`.

### Method: `train_model(self)`

Trains the RandomForest model using the fetched training and feedback data.

- Fetches training and feedback data from Firebase.
- Preprocesses and vectorizes the text data.
- Splits the data into training and test sets.
- Trains the model and evaluates its performance.
- Saves the model and vectorizer to disk.

### Method: `save_model(self)`

Saves the trained model and vectorizer as `.pkl` files.

- Saves `trained_model.pkl` (RandomForest model).
- Saves `vectorizer.pkl` (TfidfVectorizer).

### Method: `load_model(self)`

Loads a previously saved model and vectorizer from disk.

- Loads `trained_model.pkl` (RandomForest model).
- Loads `vectorizer.pkl` (TfidfVectorizer).

### Method: `collect_feedback(self, test_text, predicted_intent, feedback_list)`

**Parameters:**
- `test_text`: Input text to collect feedback for.
- `predicted_intent`: Predicted intent for the test input.
- `feedback_list`: Existing feedback list fetched from Firebase.

**Returns:**
- `True` if the answer is correct, `False` if the answer is incorrect.

Simulates feedback collection. If the feedback is incorrect, it adds the corrected feedback to the Firebase database and updates the training data.

### Method: `test_model(self)`

Tests the model using example sentences. It predicts the intent and collects feedback.

### Method: `intent(self, user_input)`

**Parameters:**
- `user_input`: Text input from the user.

**Returns:**
- Predicted intent.

Takes user input, preprocesses it, and predicts the intent using the trained model.

## Example Usage

```python
from firebase_config import FirebaseRealtimeManager

if __name__ == "__main__":
    # Initialize Firebase
    firebase_config = FirebaseRealtimeManager()
    db = firebase_config.get_db()

    # Create an object from the class
    classifier = IntentClassifier(db)

    # Train the model using data from Firebase
    classifier.train_model()

    # Test the model and collect feedback
    classifier.test_model()

    # Save the model and the vectorizer
    classifier.save_model()

    # Load the model if necessary
    # classifier.load_model()

    # Use the model for predictions
    user_input = "hello"
    predicted_intent = classifier.intent(user_input)
    print(f"Predicted Intent: {predicted_intent}")
```

### Firebase Database Structure:

- **Training Data:** Stored under the `training_data` node.
- **Feedback Data:** Stored under the `new/feedback` node.

## Notes:
- This script requires a working Firebase project with the Realtime Database configured.
- Make sure the Firebase database rules allow read/write access as needed.

---

### License

This project is licensed under the MIT License. See the LICENSE file for more details.
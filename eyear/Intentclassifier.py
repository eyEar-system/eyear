import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib


# Ensure required NLTK resources are downloaded
nltk.download('stopwords')
nltk.download('wordnet')

class IntentClassifier:
    def __init__(self, db):
        self.db = db
        self.vectorizer = TfidfVectorizer()
        self.model = RandomForestClassifier(n_estimators=100, random_state=42, oob_score=True)  # Enable OOB

    def preprocess_text(self, text):
        return text.lower()

    # Fetch training data from Firebase
    def get_training_data(self):
        training_data = self.db.child('training_data').get()
        training_list = []

        if training_data.each():
            for item in training_data.each():
                if item.val() is not None:
                    training_list.append(item.val())
            print("Training data fetched successfully.")
        else:
            print("No training data in the database.")

        return training_list if training_list else None

    # Fetch feedback data from Firebase
    def get_feedback_data(self):
        feedback_data = self.db.child('new').child('feedback').get()
        feedback_list = []

        if feedback_data.each():
            for item in feedback_data.each():
                if item.val() is not None:
                    feedback_list.append(item.val())
            print("Feedback data fetched successfully.")
        else:
            print("No feedback data in the database.")

        return feedback_list if feedback_list else None

    # Train the model using training and feedback data
    def train_model(self):
        # Fetch training and feedback data
        training_data = self.get_training_data()
        feedback_data = self.get_feedback_data()

        if training_data or feedback_data:
            # Combine training and feedback data
            combined_data = [item for item in (training_data + (feedback_data or [])) if isinstance(item, dict) and 'text' in item]

            texts = [self.preprocess_text(item['text']) for item in combined_data]
            intents = [item.get('intent', item.get('correct_intent')) for item in combined_data]

            # Split data into training and testing sets
            X_train, X_test, y_train, y_test = train_test_split(texts, intents, test_size=0.2, random_state=42)

            # Vectorize text data
            X_train_vectorized = self.vectorizer.fit_transform(X_train)

            # Train the RandomForest model
            self.model.fit(X_train_vectorized, y_train)

            # Evaluate the model
            X_test_vectorized = self.vectorizer.transform(X_test)
            y_pred = self.model.predict(X_test_vectorized)

            print(classification_report(y_test, y_pred))
            print(f"Model accuracy: {accuracy_score(y_test, y_pred)}")
            print(f"OOB Score: {self.model.oob_score_}")  # Display OOB score

            # Save the trained model and vectorizer
            self.save_model()

        else:
            print("No data to train the model.")

    # Save the model and vectorizer
    def save_model(self):
        joblib.dump(self.model, 'trained_model.pkl')
        joblib.dump(self.vectorizer, 'vectorizer.pkl')
        print("Model and vectorizer saved successfully.")

    # Load a previously saved model and vectorizer
    def load_model(self):
        self.model = joblib.load('trained_model.pkl')
        self.vectorizer = joblib.load('vectorizer.pkl')
        print("Model and vectorizer loaded successfully.")

    # Collect feedback from the user and update Firebase
    def collect_feedback(self, test_text, predicted_intent, feedback_list):
        print(f"The predicted intent for '{test_text}' is: {predicted_intent}")
        feedback = "no"  # Simulate feedback (no user input)

        if feedback == 'yes':
            print("Thank you for your confirmation!")
            return True  # Return True if the answer is correct
        else:
            correct_intent = "greet"  # Simulate correct intent input

            # Add new feedback data to the "new/feedback" section in the database
            feedback_data_id = f"feedback_{len(feedback_list) + 1}" if feedback_list else "feedback_1"
            self.db.child('new').child('feedback').child(feedback_data_id).set({
                "text": test_text,
                "predicted_intent": predicted_intent,
                "correct_intent": correct_intent
            })
            print("Thank you for your feedback! The new data has been added to 'new/feedback'.")

            # Add the corrected feedback to the training data for future training
            training_list = self.get_training_data()  # Fetch current training data
            training_data_id = f"new_training_{len(training_list) + 1}"
            self.db.child('training_data').child(training_data_id).set({
                "text": test_text,
                "intent": correct_intent
            })
            print("The corrected data has been added to 'training_data'.")
            return False  # Return False if the answer is incorrect

    # Test the model and collect feedback
    def test_model(self):
        feedback_list = self.get_feedback_data()  # Fetch existing feedback data
        test_sentences = ["what is my name"]  # Example test sentences, replace with actual input

        for test_text in test_sentences:
            # Vectorize the input text
            test_vector = self.vectorizer.transform([test_text])

            # Make prediction
            predicted_intent = self.model.predict(test_vector)[0]

            # Collect feedback on the prediction
            self.collect_feedback(test_text, predicted_intent, feedback_list)

    # Function to use the trained model for predictions
    def intent(self, user_input):
        if user_input.lower() == 'exit':
            print("Exiting the program.")
            return

        preprocessed_input = self.preprocess_text(user_input)
        input_vector = self.vectorizer.transform([preprocessed_input])
        predicted_intent = self.model.predict(input_vector)[0]

        print(f"The predicted intent for '{user_input}' is: {predicted_intent}")
        return predicted_intent

# Using the code
if __name__ == "__main__":

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
    print(f"Intent: {predicted_intent}")


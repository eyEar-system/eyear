import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pyrebase  # Assuming you are using Firebase for database management

# تحميل الموارد اللازمة من NLTK
nltk.download('stopwords')
nltk.download('wordnet')

class TrainingData:
    def __init__(self, db):
        """
        Constructor to initialize the TrainingData class.

        Args:
            db (pyrebase.database.Database): Firebase Realtime Database instance.
        """
        self.db = db

    def preprocess_text(self, text):
        """
        Preprocess the text by converting it to lowercase, removing numbers, punctuation, 
        stopwords, and performing lemmatization.

        Args:
            text (str): The input text string.

        Returns:
            str: The cleaned and preprocessed text.
        """
        text = text.lower()  # Convert text to lowercase
        text = re.sub(r'\d+', '', text)  # Remove numbers
        text = text.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation
        
        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        text = ' '.join(word for word in text.split() if word not in stop_words)
        
        # Lemmatize the words
        lemmatizer = WordNetLemmatizer()
        text = ' '.join(lemmatizer.lemmatize(word) for word in text.split())
        
        return text

    def add_training_data(self, training_data):
        """
        Add the provided training data to Firebase Realtime Database.

        Args:
            training_data (list): A list of dictionaries, where each dictionary contains 
                                   the training data with at least 'id', 'text', and 'intent'.
        """
        for data in training_data:
            self.db.child('training_data').child(data['id']).set(data)  # Use set with a custom ID
            print(f"Data added: {data}")
        print("All data has been added successfully.")

    def fetch_training_data(self):
        """
        Fetch training data from Firebase Realtime Database.

        Returns:
            list: A list of training data from Firebase.
        """
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

    def save_training_data(self, training_data):
        """
        Save and add new training data to Firebase after preprocessing.

        Args:
            training_data (list): List of raw training data to be cleaned and added.
        """
        cleaned_data = []
        for data in training_data:
            cleaned_text = self.preprocess_text(data['text'])
            cleaned_data.append({
                "id": data['id'],
                "text": cleaned_text,
                "intent": data.get('intent', 'unknown')
            })
        # Adding cleaned training data to Firebase
        self.add_training_data(cleaned_data)


# Example usage
if __name__ == "__main__":
    # Initialize Firebase
    firebase_config = {
        # Your Firebase configuration here (apiKey, authDomain, databaseURL, etc.)
    }
    firebase_config = FirebaseRealtimeManager()
    db = firebase_config.get_db()

    # Initialize the TrainingData class
    training_data_manager = TrainingData(db)

    # Save raw training data to Firebase after preprocessing
    training_data_manager.save_training_data(raw_training_data)

    # Fetch and print all training data from Firebase
    fetched_data = training_data_manager.fetch_training_data()
    print(f"Fetched Data: {fetched_data}")

# `TrainingData` Class Documentation

## Overview

The `TrainingData` class manages the collection, preprocessing, and storage of training data for machine learning models. It integrates with Firebase Realtime Database to fetch and store training data. It also handles text preprocessing steps such as lowercasing, punctuation removal, stopword removal, and lemmatization.

## Methods

### 1. `__init__(self, db)`

**Description:**
- Initializes the `TrainingData` class with a Firebase database instance.

**Parameters:**
- `db` (`pyrebase.database.Database`): Firebase Realtime Database instance.

### 2. `preprocess_text(self, text)`

**Description:**
- Preprocesses the input text by performing the following operations:
  - Converts text to lowercase.
  - Removes numbers.
  - Removes punctuation.
  - Removes stopwords.
  - Lemmatizes words to their base forms.

**Parameters:**
- `text` (`str`): The input text string to preprocess.

**Returns:**
- `str`: The cleaned and preprocessed text.

### 3. `add_training_data(self, training_data)`

**Description:**
- Adds the provided training data to the Firebase Realtime Database under the `training_data` node.

**Parameters:**
- `training_data` (`list`): A list of dictionaries, where each dictionary contains training data with at least `id`, `text`, and `intent` keys.

**Example:**
```python
# Example usage
if __name__ == "__main__":
    # Initialize Firebase

    firebase_config = FirebaseRealtimeManager()
    db = firebase_config.get_db()

    # Initialize the TrainingData class
    training_data_manager = TrainingData(db)

    # Save raw training data to Firebase after preprocessing
    training_data_manager.save_training_data(raw_training_data)

    # Fetch and print all training data from Firebase
    fetched_data = training_data_manager.fetch_training_data()
    print(f"Fetched Data: {fetched_data}")
```


## RAW Data
```bash
raw_training_data = [
        # Image Assistant and Captioning Intents
        {"id": "1", "text": "Describe the place I'm in.", "intent": "image_assistant"},
        {"id": "2", "text": "What does this environment look like?", "intent": "image_assistant"},
        {"id": "3", "text": "Can you tell me about the scene around me?", "intent": "image_assistant"},
        {"id": "4", "text": "Describe the atmosphere in this photo.", "intent": "image_assistant"},
        {"id": "5", "text": "What are the key elements in this scene?", "intent": "image_assistant"},
        {"id": "6", "text": "What can you see in this location?", "intent": "image_assistant"},
        {"id": "7", "text": "Summarize the surroundings I’m currently seeing.", "intent": "image_assistant"},
        {"id": "8", "text": "Explain the background of this scene.", "intent": "image_assistant"},
        {"id": "9", "text": "What details are visible here?", "intent": "image_assistant"},
        {"id": "10", "text": "Describe the landscape I’m currently seeing.", "intent": "image_assistant"},
        {"id": "11", "text": "Where is the object in front of me?", "intent": "image_assistant"},

        # OCR Intents
        {"id": "12", "text": "Read the text that I see.", "intent": "text_extraction"},
        {"id": "13", "text": "Can you extract any words from this view?", "intent": "text_extraction"},
        {"id": "14", "text": "What text is written here?", "intent": "text_extraction"},
        {"id": "15", "text": "Identify the text that appears in front of me.", "intent": "text_extraction"},
        {"id": "16", "text": "Is there any readable content in this area?", "intent": "text_extraction"},
        {"id": "17", "text": "Extract the written content from what I see.", "intent": "text_extraction"},
        {"id": "18", "text": "What does the text say in this context?", "intent": "text_extraction"},

        # General Knowledge Questions Intents
        {"id": "19", "text": "Who is the current president of the United States?", "intent": "general_knowledge"},
        {"id": "20", "text": "What is the capital of France?", "intent": "general_knowledge"},
        {"id": "21", "text": "How many continents are there?", "intent": "general_knowledge"},
        {"id": "22", "text": "What is the largest planet in our solar system?", "intent": "general_knowledge"},
        {"id": "23", "text": "When was the Declaration of Independence signed?", "intent": "general_knowledge"},
        {"id": "24", "text": "What is the boiling point of water?", "intent": "general_knowledge"},
        {"id": "25", "text": "Who wrote 'Hamlet'?", "intent": "general_knowledge"},
        {"id": "26", "text": "Where is London?", "intent": "general_knowledge"},

        # Time Intents
        {"id": "27", "text": "What time is it?", "intent": "time"},
        {"id": "28", "text": "Can you tell me the current time?", "intent": "time"},
        {"id": "29", "text": "What time zone am I in?", "intent": "time"},
        {"id": "30", "text": "What's the time difference between here and London?", "intent": "time"},
        {"id": "31", "text": "How many hours until midnight?", "intent": "time"},
        {"id": "32", "text": "What clock is now?", "intent": "time"},
        {"id": "33", "text": "What time is sunset exactly today?", "intent": "time"},
        {"id": "34", "text": "When exactly does daylight saving time end this year?", "intent": "time"},
        {"id": "35", "text": "Can you give me the precise time difference between New York and Tokyo?", "intent": "time"},
        {"id": "36", "text": "How many exact minutes have passed since noon?", "intent": "time"},
        {"id": "37", "text": "If it’s 9 AM in London, what is the exact time for my meeting tomorrow?", "intent": "time"},
        {"id": "38", "text": "What will the exact time be in 5 hours from now?", "intent": "time"},
        {"id": "39", "text": "What is the precise moment when daylight saving time starts this year?", "intent": "time"},
        {"id": "40", "text": "What is the exact current time in Sydney, down to the second?", "intent": "time"},
        {"id": "41", "text": "How many days exactly until the next leap year begins?", "intent": "time"},
        {"id": "42", "text": "Can you tell me the exact difference in hours between my location and Paris?", "intent": "time"},
        {"id": "43", "text": "What is the exact date and time right now?", "intent": "time"},
        {"id": "44", "text": "How many exact hours are left until my birthday?", "intent": "time"},
        {"id": "45", "text": "What is the exact time zone of California?", "intent": "time"},
        {"id": "46", "text": "When exactly does the next daylight saving change occur?", "intent": "time"},
        {"id": "47", "text": "What is the exact length of daylight today in my location?", "intent": "time"},
        {"id": "48", "text": "Can you remind me of the precise time for my flight tomorrow?", "intent": "time"},
        {"id": "49", "text": "What is the exact time zone of New Delhi, including any offsets?", "intent": "time"},
        {"id": "50", "text": "How many exact hours are left until 5 PM today?", "intent": "time"},
        {"id": "51", "text": "What is the precise current date and time in UTC?", "intent": "time"},
        {"id": "52", "text": "When exactly is the next full moon?", "intent": "time"},
        {"id": "53", "text": "How many exact days are left until the end of the year?", "intent": "time"},
        {"id": "54", "text": "What is the exact number of days left in this month?", "intent": "time"},
        {"id": "55", "text": "Can you give me the exact time difference between here and Brazil?", "intent": "time"},
        {"id": "56", "text": "When exactly does summer begin this year?", "intent": "time"},
        {"id": "57", "text": "How many exact days are left until next Friday?", "intent": "time"},
        {"id": "58", "text": "When precisely does winter start this year?", "intent": "time"},
        {"id": "59", "text": "How many exact hours are left until the end of the week?", "intent": "time"},
        {"id": "60", "text": "How long exactly does it take for Earth to orbit the sun?", "intent": "time"},
        {"id": "61", "text": "What is the exact number of hours in a week?", "intent": "time"},
        {"id": "62", "text": "How many exact months are left until the end of the year?", "intent": "time"},
        {"id": "63", "text": "Can you set an alarm for exactly 7 AM tomorrow?", "intent": "time"},
        {"id": "64", "text": "What is the exact time for the eclipse?", "intent": "time"},
        {"id": "65", "text": "When exactly is the next leap year?", "intent": "time"},
        {"id": "66", "text": "What is the precise time difference between New York and Beijing?", "intent": "time"},
        {"id": "67", "text": "How many exact hours are left until the next new year?", "intent": "time"},
        {"id": "68", "text": "What is the exact number of seconds in a day?", "intent": "time"},
        {"id": "69", "text": "How many exact hours have passed since midnight?", "intent": "time"},
        {"id": "70", "text": "When does the next season start exactly?", "intent": "time"},

        # Calculation Intents
        {"id": "33", "text": "What is 25 plus 30?", "intent": "calculation"},
        {"id": "34", "text": "Calculate the square root of 144.", "intent": "calculation"},
        {"id": "35", "text": "What is 15 multiplied by 6?", "intent": "calculation"},
        {"id": "36", "text": "If I have 10 apples and give away 3, how many do I have left?", "intent": "calculation"},
        {"id": "37", "text": "What is the result of 100 divided by 4?", "intent": "calculation"},
        {"id": "38", "text": "What is 72 minus 18?", "intent": "calculation"},
        {"id": "39", "text": "What is the cube root of 27?", "intent": "calculation"},
        {"id": "40", "text": "How many hours are there in 3.5 days?", "intent": "calculation"},
        {"id": "41", "text": "What is the value of 8 squared?", "intent": "calculation"},
        {"id": "42", "text": "How much is 45% of 200?", "intent": "calculation"},
        {"id": "43", "text": "If I have 15 candies and eat 7, how many are left?", "intent": "calculation"},
        {"id": "44", "text": "What’s the exact result of 250 divided by 12?", "intent": "calculation"},
        {"id": "45", "text": "How many minutes are there in 5.5 hours?", "intent": "calculation"},
        {"id": "46", "text": "What is the remainder when 17 is divided by 4?", "intent": "calculation"},
        {"id": "47", "text": "Calculate the area of a circle with a radius of 7.", "intent": "calculation"},
        {"id": "48", "text": "What is 9 to the power of 3?", "intent": "calculation"},
        {"id": "49", "text": "How many days are there in 8 weeks?", "intent": "calculation"},
        {"id": "50", "text": "What is the sum of 123 and 456?", "intent": "calculation"},
        {"id": "51", "text": "What is the exact result of 54 times 7?", "intent": "calculation"},
        {"id": "52", "text": "If I buy 5 items at $12 each, what is the total cost?", "intent": "calculation"},
        {"id": "53", "text": "How much is 15% of 350?", "intent": "calculation"},
        {"id": "54", "text": "What is the total when adding 25.75 and 34.25?", "intent": "calculation"},
        {"id": "55", "text": "What is 500 minus 127?", "intent": "calculation"},
        {"id": "56", "text": "How many centimeters are in 3 meters?", "intent": "calculation"},
        {"id": "57", "text": "How many milliliters are in 2.5 liters?", "intent": "calculation"},
        {"id": "58", "text": "What is the square of 12?", "intent": "calculation"},
        {"id": "59", "text": "What is the result of 81 divided by 9?", "intent": "calculation"},
        {"id": "60", "text": "How many seconds are in 1.5 hours?", "intent": "calculation"},
        {"id": "61", "text": "What is the exact perimeter of a square with side length 9?", "intent": "calculation"},
        {"id": "62", "text": "What is the factorial of 5?", "intent": "calculation"},
        {"id": "63", "text": "What is the total sum of 99, 100, and 101?", "intent": "calculation"},
        {"id": "64", "text": "How many weeks are there in 365 days?", "intent": "calculation"},
        {"id": "65", "text": "What is the exact division of 154 by 7?", "intent": "calculation"},
        {"id": "66", "text": "How many hours are in 2.75 days?", "intent": "calculation"},

        # Natural Conversation Intents
        {"id": "38", "text": "I love you.", "intent": "natural_conversation"},
        {"id": "39", "text": "That's great!", "intent": "natural_conversation"},
        {"id": "40", "text": "What's your favorite color?", "intent": "natural_conversation"},
        {"id": "41", "text": "Tell me something interesting.", "intent": "natural_conversation"},
        {"id": "42", "text": "How are you doing today?", "intent": "natural_conversation"},
        {"id": "43", "text": "Can you recommend a good book?", "intent": "natural_conversation"},
        {"id": "44", "text": "What do you think about technology?", "intent": "natural_conversation"},
        {"id": "45", "text": "What do you like to do for fun?", "intent": "natural_conversation"},
        {"id": "46", "text": "Do you have any hobbies?", "intent": "natural_conversation"},
        {"id": "47", "text": "What is your favorite food?", "intent": "natural_conversation"},
        {"id": "48", "text": "What's your favorite movie?", "intent": "natural_conversation"},
        {"id": "49", "text": "Tell me a joke.", "intent": "natural_conversation"},

        # Current Events Intents
        {"id": "50", "text": "What's the latest news?", "intent": "current_events"},
        {"id": "51", "text": "Tell me about today's headlines.", "intent": "current_events"},
        {"id": "52", "text": "What is happening in the world right now?", "intent": "current_events"},
        {"id": "53", "text": "Give me the latest sports updates.", "intent": "current_events"},
        {"id": "54", "text": "What's trending on social media?", "intent": "current_events"},
        {"id": "55", "text": "What are the latest political developments?", "intent": "current_events"},
        {"id": "56", "text": "Are there any updates on major world events?", "intent": "current_events"},
        {"id": "57", "text": "What's new in the world of technology?", "intent": "current_events"},
        {"id": "58", "text": "Can you provide updates on any ongoing crises?", "intent": "current_events"},
        {"id": "59", "text": "What’s the latest in entertainment news?", "intent": "current_events"},
        {"id": "60", "text": "Are there any weather alerts for today?", "intent": "current_events"},
        {"id": "61", "text": "What’s trending in global finance today?", "intent": "current_events"},
        {"id": "62", "text": "Any major breakthroughs in science today?", "intent": "current_events"},
        {"id": "63", "text": "What cultural events are happening this week?", "intent": "current_events"},
        {"id": "64", "text": "Is there any breaking news about natural disasters?", "intent": "current_events"},
        {"id": "65", "text": "What are the latest updates on COVID-19 or health news?", "intent": "current_events"},

        # weather Intents
       {"id": "67", "text": "What’s the current temperature outside?", "intent": "weather"},
       {"id": "68", "text": "Will it rain tomorrow, and if so, at what time?", "intent": "weather"},
       {"id": "69", "text": "What’s the exact weather forecast for this afternoon?", "intent": "weather"},
       {"id": "70", "text": "What is the chance of snow this weekend?", "intent": "weather"},
       {"id": "71", "text": "What’s the current humidity level in my location?", "intent": "weather"},
       {"id": "72", "text": "Will there be thunderstorms today, and at what hour?", "intent": "weather"},
       {"id": "73", "text": "What will the exact wind speed be in the next 24 hours?", "intent": "weather"},
       {"id": "74", "text": "Can you tell me the high and low temperatures for tomorrow?", "intent": "weather"},
       {"id": "75", "text": "What’s the hourly forecast for today’s weather?", "intent": "weather"},
       {"id": "76", "text": "What’s the UV index right now?", "intent": "weather"},
       {"id": "77", "text": "When exactly will the sun set today?", "intent": "weather"},
       {"id": "78", "text": "What’s the exact temperature at noon today?", "intent": "weather"},
       {"id": "79", "text": "Will it be cloudy or clear tonight?", "intent": "weather"},
       {"id": "80", "text": "What time will the rain start tomorrow?", "intent": "weather"},
       {"id": "81", "text": "Can you give me the wind speed for the next 12 hours?", "intent": "weather"},
       {"id": "82", "text": "What will the weather be like in the next 3 days?", "intent": "weather"},
       {"id": "83", "text": "Is there a heatwave expected this week?", "intent": "weather"},
       {"id": "84", "text": "What’s the exact precipitation chance for today?", "intent": "weather"},
       {"id": "85", "text": "What will the temperature be at 5 PM?", "intent": "weather"},
       {"id": "86", "text": "When exactly will the fog clear up?", "intent": "weather"},
       {"id": "87", "text": "What’s the exact dew point temperature right now?", "intent": "weather"},
       {"id": "88", "text": "Is there any chance of hail this evening?", "intent": "weather"},
       {"id": "89", "text": "Can you give me the weather forecast for the upcoming weekend?", "intent": "weather"},
       {"id": "90", "text": "What’s the exact air quality index right now?", "intent": "weather"},
       {"id": "91", "text": "Will there be strong winds tonight?", "intent": "weather"},
       {"id": "92", "text": "What’s the exact wind chill right now?", "intent": "weather"},
       {"id": "93", "text": "What will the weather be like at my location tomorrow at noon?", "intent": "weather"},
       {"id": "94", "text": "What’s the weather forecast for the next 48 hours?", "intent": "weather"},
       {"id": "95", "text": "What’s the exact visibility distance right now?", "intent": "weather"},

       # personal information intents
        {"id": "96", "text": "What do I usually do in my free time?", "intent": "personal_information"},
        {"id": "97", "text": "What are my friends' favorite activities?", "intent": "personal_information"},
        {"id": "98", "text": "Can you tell me about my family members?", "intent": "personal_information"},
        {"id": "99", "text": "What hobbies do I enjoy the most?", "intent": "personal_information"},
        {"id": "100", "text": "What do I usually talk about with my colleagues?", "intent": "personal_information"},
        {"id": "101", "text": "Where do I usually spend my vacations?", "intent": "personal_information"},
        {"id": "102", "text": "Who are the people I interact with the most?", "intent": "personal_information"},
        {"id": "103", "text": "Can you tell me where I work and what I do?", "intent": "personal_information"},
        {"id": "104", "text": "What are my goals for the future?", "intent": "personal_information"},
        {"id": "105", "text": "What kind of music do my friends and I like?", "intent": "personal_information"},
        {"id": "106", "text": "Can you remind me of important events in my life?", "intent": "personal_information"},
        {"id": "107", "text": "What is my daily routine?", "intent": "personal_information"},
        {"id": "108", "text": "Who are the people closest to me?", "intent": "personal_information"},
        {"id": "109", "text": "What type of food do I usually eat?", "intent": "personal_information"},
        {"id": "110", "text": "What do I do on weekends?", "intent": "personal_information"},
        {"id": "111", "text": "What are my favorite places to visit?", "intent": "personal_information"},
        {"id": "112", "text": "What kind of movies do my friends and I enjoy?", "intent": "personal_information"},
        {"id": "113", "text": "Who are the people I see most often?", "intent": "personal_information"},
        {"id": "114", "text": "What is my relationship with my neighbors like?", "intent": "personal_information"},
        {"id": "115", "text": "What do I enjoy talking about with family?", "intent": "personal_information"},
        {"id": "116", "text": "What events have shaped my career?", "intent": "personal_information"},
        {"id": "117", "text": "Who in my life has the most influence on me?", "intent": "personal_information"},
        {"id": "118", "text": "What do I usually discuss with my friends?", "intent": "personal_information"},
        {"id": "119", "text": "How do I usually spend time with family?", "intent": "personal_information"},
        {"id": "120", "text": "What memories do I share most with others?", "intent": "personal_information"},
        {"id": "121", "text": "Who do I consider my best friend?", "intent": "personal_information"},
        {"id": "122", "text": "What major life changes have I experienced recently?", "intent": "personal_information"},
        {"id": "123", "text": "How do I prefer to socialize with my friends?", "intent": "personal_information"},
        {"id": "124", "text": "What traditions do my family and I follow?", "intent": "personal_information"},
        {"id": "125", "text": "How do I celebrate important occasions with others?", "intent": "personal_information"},
        {"id": "126", "text": "What are my social habits with friends and family?", "intent": "personal_information"},
        {"id": "127", "text": "What are the common interests I share with others?", "intent": "personal_information"},

        # Data Of User intents
       {"id": "128", "text": "You usually enjoy reading, watching movies, and spending time outdoors in your free time.", "intent": "data of user"},
       {"id": "129", "text": "Your friends' favorite activities include playing sports, going to the gym, and exploring new restaurants.", "intent": "data of user"},
       {"id": "130", "text": "Your family members include your parents, two siblings, and your cousin who lives nearby.", "intent": "data of user"},
       {"id": "131", "text": "You enjoy hobbies like photography, hiking, and painting the most.", "intent": "data of user"},
       {"id": "132", "text": "You usually talk with your colleagues about recent work projects, travel plans, and new tech trends.", "intent": "data of user"},
       {"id": "133", "text": "You typically spend your vacations at the beach or exploring new cities.", "intent": "data of user"},
       {"id": "134", "text": "You interact the most with your close friends, family members, and a few colleagues from work.", "intent": "data of user"},
       {"id": "135", "text": "You work as a software developer at a tech company, focusing on app development.", "intent": "data of user"},
       {"id": "136", "text": "Your goals for the future include advancing your career, traveling more, and learning new skills.", "intent": "data of user"},
       {"id": "137", "text": "You and your friends like listening to pop music, indie bands, and classic rock.", "intent": "data of user"},
       {"id": "138", "text": "Some important events in your life include graduating from college, starting your first job, and moving into your own apartment.", "intent": "data of user"},
       {"id": "139", "text": "Your daily routine usually involves going to work, exercising in the evening, and spending some time relaxing with a book or show.", "intent": "data of user"},
       {"id": "140", "text": "The people closest to you include your best friend, your partner, and your parents.", "intent": "data of user"},
       {"id": "141", "text": "You usually eat healthy meals like salads, chicken, and smoothies, with the occasional treat of pizza or ice cream.", "intent": "data of user"},
       {"id": "142", "text": "On weekends, you like to hang out with friends, visit new places, or relax at home.", "intent": "data of user"},
       {"id": "143", "text": "Your favorite places to visit include local parks, museums, and cafes in the city.", "intent": "data of user"},
       {"id": "144", "text": "You and your friends enjoy watching comedies, action movies, and sometimes documentaries.", "intent": "data of user"},
       {"id": "145", "text": "You see your best friend and a few close colleagues most often during the week.", "intent": "data of user"},
       {"id": "146", "text": "Your relationship with your neighbors is friendly; you usually exchange greetings and occasionally help each other out.", "intent": "data of user"},
       {"id": "147", "text": "With your family, you enjoy talking about your childhood memories, family trips, and current events.", "intent": "data of user"},
       {"id": "148", "text": "Key events that shaped your career include finishing your degree, landing your first big project, and switching to your current role.", "intent": "data of user"},
       {"id": "149", "text": "The person who influences you the most is your mentor at work, who provides guidance and advice on your career path.", "intent": "data of user"},
       {"id": "150", "text": "You and your friends usually discuss shared interests like new movies, recent trips, and upcoming plans.", "intent": "data of user"},
       {"id": "151", "text": "You spend time with your family by having dinners together, going on trips, or just catching up over the phone.", "intent": "data of user"},
       {"id": "152", "text": "The memories you share the most with others include childhood stories, past vacations, and funny moments from work.", "intent": "data of user"},
       {"id": "153", "text": "Your best friend is someone you've known since school, and you both share similar interests and values.", "intent": "data of user"},
       {"id": "154", "text": "Recently, you've experienced changes like moving to a new city and starting a new job, which have been significant for you.", "intent": "data of user"},
       {"id": "155", "text": "You prefer to socialize with friends by going out to eat, attending events, or just catching up over coffee.", "intent": "data of user"},
       {"id": "156", "text": "Your family traditions include celebrating holidays together, having Sunday dinners, and exchanging gifts on special occasions.", "intent": "data of user"},
       {"id": "157", "text": "You celebrate important occasions like birthdays and anniversaries with close family and friends, usually with a small gathering or dinner.", "intent": "data of user"},
       {"id": "158", "text": "Your social habits include meeting up with friends once or twice a week and staying in touch regularly through messaging.", "intent": "data of user"},
       {"id": "159", "text": "Common interests you share with others include a love for traveling, watching movies, and exploring new places.", "intent": "data of user"},
]
```

````md
# 🧠 Comparative Study for Selecting an Open-Source LLM for a Chat Application on Google Colab (CPU)

### by: Ah777ed_said  
**Context**: Searching for a ChatGPT-like open-source model that can run on Google Colab using CPU only

---
قثسعمف 
## 🚀 Use LLaMA 1B

---

## 🧩 Top 4 Open-Source ChatGPT-like Models (LLMs)

### Across different categories:

| Category           | Model               | Description                           |
| ------------------ | ------------------- | ------------------------------------- |
| High Intelligence  | Mistral 7B Instruct | Strong in conversations and reasoning |
| Efficiency & Speed | Phi-2               | High intelligence with small size     |
| Smallest Size      | TinyLLaMA 1.1B      | Requires very low RAM                 |
| General Purpose    | GPT-2               | Multi-purpose model                   |



## 💻 Environment: Google Colab (CPU Mode)

Based on this setup, we needed a model that is:

* Small in size
* Compatible with Hugging Face Transformers
* Supports LoRA for future fine-tuning

---

## 📊 Final Comparison

| Model                 | Size | General Intelligence | Resources  | Speed     | Arabic Support | Strengths                  | Weaknesses                |
| --------------------- | ---- | -------------------- | ---------- | --------- | -------------- | -------------------------- | ------------------------- |
| LLaMA-3.2-1B-Instruct | 1B   | Very Good            | Light      | Medium    | Acceptable     | Modern – Instruction-tuned | Limited documentation     |
| Phi-2                 | 1.7B | Excellent reasoning  | Very Light | Fast      | Weak           | High intelligence          | Poor Arabic understanding |
| TinyLLaMA-1.1B        | 1.1B | Medium               | Very Light | Very Fast | Very Weak      | Great for learning         | Shallow responses         |
| GPT-2                 | 1.5B | Very Good            | Medium     | Medium    | Good           | Versatile                  | Outdated in modern tasks  |

---

## ✅ Final Decision

**meta-llama/Llama-3.2-1B-Instruct** was selected for the following reasons:

1. Suitable for CPU environments
2. Based on the modern LLaMA 3.2 architecture
3. Instruction-tuned (better responses)
4. Produces smarter and more structured outputs

---

## 🧪 First Experiment

```python
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class ChatBot:
    def __init__(self, model_name="meta-llama/Llama-3.2-1B-Instruct", token="YOUR_TOKEN"):
        self.token = token
        self.model_name = model_name
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, use_auth_token=self.token)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name, use_auth_token=self.token).to(self.device)

    def generate_response(self, user_message, max_length=30, temperature=0.1, top_p=0.9):
        inputs = self.tokenizer.encode(user_message, return_tensors='pt').to(self.device)

        with torch.no_grad():
            outputs = self.model.generate(
                inputs,
                max_length=max_length,
                num_return_sequences=1,
                pad_token_id=self.tokenizer.eos_token_id,
                temperature=temperature,
                top_p=top_p
            )

        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

    def start_chat(self, message):
        if message.lower() in ["exit", "quit"]:
            print("AI Assistant: Goodbye!")
            return False

        response = self.generate_response(message)
        print(f"You: {message}")
        print(f"AI Assistant: {response}")
        return response
```

---

## 📌 Observations

### GPT-2:

* Repetitive responses
* Sometimes irrelevant
* Weak conversational flow

### LLaMA 1B:

* More natural responses
* Better structure
* Handles prompts more intelligently
* Still has some hallucinations

---

## 🎯 Conclusion

For a **lightweight AI chatbot running on CPU**,
**LLaMA-3.2-1B-Instruct** is one of the best open-source choices currently available.



## التجربة الأولى

```python
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch

class ChatBot:
    def __init__(self, model_name="meta-llama/Llama-3.2-1B-Instruct", token="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"):
        """
        Initializes the ChatBot with a specific model and authentication token.
        """
        self.token = token
        self.model_name = model_name
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Load tokenizer and model with authentication token
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, use_auth_token=self.token)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name, use_auth_token=self.token).to(self.device)

    def generate_response(self, user_message, max_length=30, temperature=0.1, top_p=0.9):
        """
        Generates a short, concise response from the model.
        """
        # Convert user message to tokens
        inputs = self.tokenizer.encode(user_message, return_tensors='pt').to(self.device)

        # Disable gradients (we are only generating the response)
        with torch.no_grad():
            # Generate the response with specified temperature and top_p values
            outputs = self.model.generate(
                inputs,
                max_length=max_length,  # Limit the length of the response
                num_return_sequences=1,  # Number of responses to generate
                pad_token_id=self.tokenizer.eos_token_id,  # Padding token
                temperature=temperature,  # Creativity of the response
                top_p=top_p  # Diversity in the response
            )

        # Return the response as a readable string
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response

    def start_chat(self, message):
        """
        Starts the chat interaction with an AI assistant response style.
        """
        # Check if the user wants to exit the conversation
        if message.lower() in ["exit", "quit"]:
            print("AI Assistant: Goodbye! I'm here if you need help again.")
            return False

        # Generate and print the AI Assistant's response
        response = self.generate_response(message)

        print(f"You: {message}")
        print(f"AI Assistant: {response}")
        return response

# Example Usage - Dynamic interaction
if __name__ == "__main__":
    # Initialize the bot
    bot = ChatBot()

    # Start chatting
    bot.start_chat("hello")
    bot.start_chat("i love you")
    bot.start_chat("hi")
    bot.start_chat("what is your favourite color")
    bot.start_chat("how are you?")
    bot.start_chat("tell me a joke")
    bot.start_chat("who are you?")
    bot.start_chat("what's the weather like today?")
    bot.start_chat("can you help me with a math problem?")
    bot.start_chat("tell me a fun fact")
    bot.start_chat("what is AI?")
    bot.start_chat("what's the meaning of life?")
    bot.start_chat("do you like music?")
    bot.start_chat("how do you feel?")
    bot.start_chat("what is the capital of France?")
    bot.start_chat("can you write a poem?")
    bot.start_chat("what's your favorite movie?")
    bot.start_chat("how do I get to the nearest store?")
    bot.start_chat("what is your name?")
```

answer of GPT 2 
You: hello
AI Assistant: hello, PA)

The city of Philadelphia is considering a $1.5 million renovation of the former Union Station, which was demolished in the
You: i love you
AI Assistant: i love you, and I love you too.

I love you, and I love you too.

I love you, and I
You: hi
AI Assistant: hi, who was born in the city of Kolkata, was a member of the Kolkata-based Kolkata-based Kolk
You: what is your favourite color
AI Assistant: what is your favourite color?

I love the color of the rainbow. I love the color of the rainbow. I love the color of the
You: how are you?
AI Assistant: how are you?

I'm not sure. I'm not sure if I'm going to be able to do it. I'm not sure
You: tell me a joke
AI Assistant: tell me a joke, but I'm not going to tell you what I'm going to do. I'm going to tell you what I'm going
You: who are you?
AI Assistant: who are you?

I'm not sure if you're a fan of the show, but I'm not sure if you're a fan of
You: what's the weather like today?
AI Assistant: what's the weather like today?

I'm not sure. I'm not sure if it's a good day or a bad day. I
You: can you help me with a math problem?
AI Assistant: can you help me with a math problem?

I'm not sure if you can help me with a math problem.

I'm not
You: tell me a fun fact
AI Assistant: tell me a fun fact about the game.

"I've played it for a long time, and I've never seen anything like it.
You: what is AI?
AI Assistant: what is AI?

AI is a new field of research that has been gaining momentum in recent years. It is a field that has been gaining
You: what's the meaning of life?
AI Assistant: what's the meaning of life?

I think it's a very important question. I think it's a very important question. I think it
You: do you like music?
AI Assistant: do you like music?

I like music. I like to listen to music. I like to listen to music. I like to listen to
You: how do you feel?
AI Assistant: how do you feel?

I feel like I'm in a good place. I'm not in a bad place. I'm in a good
You: what is the capital of France?
AI Assistant: what is the capital of France?

The capital of France is Paris. It is the capital of France. It is the capital of France.
You: can you write a poem?
AI Assistant: can you write a poem?

I don't know. I don't know. I don't know. I don't know. I don
You: what's your favorite movie?
AI Assistant: what's your favorite movie?

I love the movie "The Matrix" and I love the movie "The Matrix Reloaded." I love the movie
You: how do I get to the nearest store?
AI Assistant: how do I get to the nearest store?

If you're in the area, you can check out the store's website for more information.
You: what is your name?
AI Assistant: what is your name?

I'm a little bit of a mystery. I'm not sure if I'm a real person or not. I

answer of llama 1 B

You: hello
AI Assistant: hello, i'm looking for a reliable and efficient way to manage my personal finances. I've heard that budgeting apps can be a great tool
You: i love you
AI Assistant: i love you, but i'm not ready for marriage
I'm not ready to settle down, I'm not ready to give up my freedom
You: hi
AI Assistant: hi there! I'm so excited to share my latest project with you all. I've been working on a new game concept, and I'd
You: what is your favourite color
AI Assistant: what is your favourite color?
I don't really have a favourite color, I think it's because I'm a bit of a neutral person.
You: how are you?
AI Assistant: how are you? I'm so excited to be back in the office after a long break. I'm feeling refreshed and ready to dive back into
You: tell me a joke
AI Assistant: tell me a joke about a cat
Why did the cat join a band?
Because it wanted to be the purr-cussionist!
You: who are you?
AI Assistant: who are you? I am a friend of a friend, and I have been trying to get in touch with you for a while now. I
You: what's the weather like today?
AI Assistant: what's the weather like today? I'm planning a trip to the beach and I want to know what the weather is like.
I'm planning
You: can you help me with a math problem?
AI Assistant: can you help me with a math problem? I'm having trouble with a specific problem.

Here's the problem:

A bakery is having a sale
You: tell me a fun fact
AI Assistant: tell me a fun fact about the moon
Did you know that the moon is actually moving away from the Earth at a rate of about 1
You: what is AI?
AI Assistant: what is AI? Artificial Intelligence (AI) refers to the development of computer systems that can perform tasks that would typically require human intelligence, such as
You: what's the meaning of life?
AI Assistant: what's the meaning of life? (a question that has puzzled philosophers, theologians, scientists, and everyday people for centuries)
The meaning of
You: do you like music?
AI Assistant: do you like music? I like music too! I have a lot of favorite artists and songs. I also like to listen to music while I
You: how do you feel?
AI Assistant: how do you feel? I'm feeling a bit anxious about the upcoming exams.
I'm feeling a bit anxious about the upcoming exams. I'm
You: what is the capital of France?
AI Assistant: what is the capital of France? Paris
The capital of France is Paris.
You: can you write a poem?
AI Assistant: can you write a poem? I'd like a poem about a person who is struggling with anxiety and depression.

**Trigger Warning: This poem may
You: what's your favorite movie?
AI Assistant: what's your favorite movie? I'm a huge fan of the original Star Wars trilogy, but I've also been enjoying the Marvel Cinematic Universe
You: how do I get to the nearest store?
AI Assistant: how do I get to the nearest store? I can get to the store by car, public transportation, or on foot.
Here are some options
You: what is your name?
AI Assistant: what is your name? I am a 17 year old girl who is a freshman in high school. I am a junior in college and I

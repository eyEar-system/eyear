#requirment 
#!pip install huggingface-hub>=0.21.0 transformers>=4.41.0 sentence-transformers==3.4.1 accelerate>=1.5.2 diffusers>=0.23.2

from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch

class Bot:
    def __init__(self, token,  model_name="meta-llama/Llama-3.2-1B-Instruct"):
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
    bot = Bot(token="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")

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

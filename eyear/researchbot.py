import re  
from transformers import pipeline 
import torch
import requests
from bs4 import BeautifulSoup
import time


class ResearchBot :
    def __init__(self, model_name="meta-llama/Llama-3.2-1B-Instruct", token="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"):
        """Initialize the bot with a specific model and authentication token."""
        self.token = token
        self.model_name = model_name
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.qa_model = pipeline("question-answering")

    def extract_keywords(self, question):
        """Extract keywords from the question."""
        return re.findall(r'\w+', question)

    def fetch_wikipedia_content(self, topic):
        """Fetch the first paragraph of the Wikipedia page for the topic."""
        url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exintro=&explaintext=&titles={topic}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            page = next(iter(data['query']['pages'].values()))
            extract = page.get('extract', "")
            if extract:
                return extract.strip()
            else:
                print(f"No extract found for topic: {topic}")
                return ""
        except requests.RequestException as e:
            print(f"Request error while fetching Wikipedia content: {e}")
            return ""

    def search_duckduckgo(self, query):
        """Search DuckDuckGo and return result URLs and snippets."""
        query = query.replace(' ', '+')
        url = f"https://duckduckgo.com/html/?q={query}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            for item in soup.find_all('a', class_='result__a'):
                title = item.get_text()
                link = item['href']
                results.append({'title': title, 'link': link})
            return results
        except requests.RequestException as e:
            print(f"Error while searching DuckDuckGo: {e}")
            return []

    def handle_fallback(self, topic):
        """Fallback if both content fetch methods fail."""
        return f"No sufficient information found for '{topic}'. Please check the topic or try again."

    def provide_first_level_answer(self, question, context):
        """Generate a basic answer for the question based on the provided context."""
        qa_result = self.qa_model(question=question, context=context)
        if qa_result['answer']:
            return qa_result['answer']
        else:
            return "No specific answer found."

    def provide_second_level_info(self, topic):
        """Provide summarized information based on the topic."""
        content = self.fetch_wikipedia_content(topic)
        if content:
            summarized_info = content.split('.')[0].strip() + '.'
            return f"Summarized information about {topic}:\n{summarized_info}\n"
        else:
            return f"No additional information found for {topic}."

    def provide_third_level_info(self, topic):
        """Provide detailed information based on the topic."""
        content = self.fetch_wikipedia_content(topic)
        if content:
            return f"Further detailed information about {topic}:\n{content}\n"
        else:
            return f"No additional information found for {topic}."

    def answer_question(self, question, info_level):
        """Main method to answer a user's question based on information level."""
        start_time = time.time()  # Start time measurement

        print(f"\nAnalyzing question: {question}")

        # Improve the question
        improved_question = question.strip()
        print(f"Improved question: {improved_question}")

        # Extract keywords from the question
        keywords = self.extract_keywords(improved_question)
        print(f"Extracted keywords: {keywords}")

        # Extract the topic from the question
        topic = keywords[-1] if keywords else "unknown"
        print(f"Extracted topic: {topic}")

        # Fetch Wikipedia content for the topic
        print(f"Fetching Wikipedia content for topic: {topic}")
        wikipedia_content = self.fetch_wikipedia_content(topic)
        print(f"Fetched Wikipedia content length: {len(wikipedia_content)} characters")

        # If no Wikipedia content found, use DuckDuckGo
        if not wikipedia_content:
            print("No sufficient content found. Retrying with DuckDuckGo search.")
            search_results = self.search_duckduckgo(topic)

            if not search_results:
                print("No results from DuckDuckGo. Executing fallback logic.")
                answer = self.handle_fallback(topic)
                print(f"Answer: {answer}")
                end_time = time.time()  # End time measurement
                print(f"Time taken: {end_time - start_time:.2f} seconds")
                return answer
            else:
                print(f"Found {len(search_results)} results from DuckDuckGo.")
                context = " ".join(result['title'] for result in search_results)
        else:
            context = wikipedia_content

        # Generate answer based on information level
        if info_level == "first":
            answer = self.provide_first_level_answer(improved_question, context)
        elif info_level == "second":
            answer = self.provide_second_level_info(topic)
        elif info_level == "third":
            answer = self.provide_third_level_info(topic)
        else:
            answer = "Invalid information level requested."

        end_time = time.time()  # End time measurement
        print(answer)
        print(f"Time taken: {end_time - start_time:.2f} seconds")
        return answer

# Example usage
if __name__ == "__main__":
    # Instantiate the bot
    Research = ResearchBot ()

    # Test cases
    test_questions = [
        ("Where is Cairo?", "first"),
        ("What is the capital of France?", "second"),
        ("Who invented the telephone?", "third"),
        ("What is quantum computing?", "first"),
        ("Explain the theory of relativity.", "second")
    ]

    # Process each test case and print runtime
    for question, info_level in test_questions:
        answer = Research.answer_question(question, info_level)
        print(f"Answer: {answer}")
   # Example usage
    print(20*"=","\n" , "answer : " , Research.answer_question("what is ai", "third"))

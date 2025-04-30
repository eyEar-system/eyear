import torch
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch

class MemoryBot:
    def __init__(self, storage_manager, model_name="deepset/roberta-base-squad2", embedder_model="all-MiniLM-L6-v2", rephrase_model="facebook/bart-large"):
        """Initialize the bot with a specific model, embedder, and rephraser."""
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_name = model_name

        # Load QA model
        self.qa_model = pipeline("question-answering", model=self.model_name, device=0 if torch.cuda.is_available() else -1)

        # Load sentence transformer model for semantic search
        self.embedder = SentenceTransformer(embedder_model)

        # Load rephrase model (BART or T5)
        self.rephrase_model = pipeline("text2text-generation", model=rephrase_model, device=0 if torch.cuda.is_available() else -1)

        self.memory_paragraphs = []

    def load_memory(self):
        """Load the memory content (paragraphs) from a text file."""
        try:
            local_path = storage_manager.download_file("memory/txt/memory.txt", "/content/memory.txt")
            if local_path:
                print(f"File downloaded to: {local_path}")
            memory_file = local_path

            with open(memory_file, 'r', encoding='utf-8') as file:
                full_memory = file.read()

            # Split memory into paragraphs (double newlines)
            self.memory_paragraphs = [p.strip() for p in full_memory.split('\n\n') if p.strip()]
            print(f"Memory loaded successfully. {len(self.memory_paragraphs)} paragraphs.")
        except FileNotFoundError:
            print("Memory file not found.")
            self.memory_paragraphs = []

    def clean_question(self, question):
        """Basic question cleaning if needed."""
        return question.strip()

    def find_relevant_paragraphs(self, question, top_k=5):
        """Find the top-k most relevant paragraphs using semantic similarity."""
        if not self.memory_paragraphs:
            return []

        question_embedding = self.embedder.encode(question, convert_to_tensor=True)
        paragraph_embeddings = self.embedder.encode(self.memory_paragraphs, convert_to_tensor=True)

        cosine_scores = util.cos_sim(question_embedding, paragraph_embeddings)

        top_results = torch.topk(cosine_scores.squeeze(0), k=min(top_k, len(self.memory_paragraphs)))

        best_indices = top_results.indices.tolist()

        return [self.memory_paragraphs[idx] for idx in best_indices]

    def rephrase_answer(self, question, answer):
        """Rephrase the answer to make it more natural."""
        rephrased_answer = self.rephrase_model(f"{answer}")[0]['generated_text']
        return rephrased_answer

    def update_memory_file(self, db, storage_manager):
        """Update the memory file from Firebase database."""
        # Get all data under "memory/"
        all_data = db.child("memory").get()

        # Extract the data from the PyreResponse object
        all_data = all_data.val()

        # Specify the file name
        file_name = "memory.txt"

        # Open the file in write mode and write the data
        with open(file_name, "w") as file:
            if all_data:
                file.write("All memory data:\n")
                for category, data in all_data.items():
                    file.write(f"{category}:\n")
                    if isinstance(data, dict):
                        for key, value in data.items():
                            file.write(f"  {key}: {value}\n")
                    else:
                        file.write(f"  {data}\n")
            else:
                file.write("No data found.\n")

        print(f"Data has been written to '{file_name}'.")
        signed_url = storage_manager.upload_file("/content/memory.txt", "memory/txt/memory.txt")
        if signed_url:
            print(f"Generated Signed URL: {signed_url}")

    def answer_question(self, question, top_k_contexts=5, min_score_threshold=0.1, window=10):
        """Answer a question based on the best matching paragraphs with extended context."""
        if not self.memory_paragraphs:
            return "No memory content available."

        clean_q = self.clean_question(question)
        print(f"Question: {clean_q}")

        contexts = self.find_relevant_paragraphs(clean_q, top_k=top_k_contexts)
        if not contexts:
            return "No relevant information found in memory."

        best_answer = None
        best_score = float('-inf')
        best_context = None

        # Try answering using multiple contexts
        for idx, context in enumerate(contexts):
            qa_input = {
                'question': clean_q,
                'context': context
            }
            result = self.qa_model(qa_input)

            print(f"Context {idx+1}: Score={result['score']:.4f}, Answer={result['answer']}")

            if result['score'] > best_score and result['answer'].strip() and len(result['answer'].strip()) > 2:
                best_score = result['score']
                best_answer = result
                best_context = context

        if best_answer:
            # Expand the context around the answer
            start_idx = best_answer['start']
            end_idx = best_answer['end']

            expanded_start = max(0, start_idx - window)
            expanded_end = min(len(best_context), end_idx + window)

            expanded_text = best_context[expanded_start:expanded_end]

            print(f"\n\nExpanded Answer Context:\n{expanded_text}\n\n")

            return self.rephrase_answer(clean_q, expanded_text)
        else:
            return "I couldn't find a confident answer to your question in the memory."

# =============================
# Example Usage
# =============================

if __name__ == "__main__":
    memory_bot = MemoryBot(storage_manager, rephrase_model="facebook/bart-large")

    memory_bot.update_memory_file(db, storage_manager)
    # Load memory content
    memory_bot.load_memory()

    # Example question
    question = " who is Miss_Abeer"
    answer = memory_bot.answer_question(question)
    print(f"Answer: {answer}")

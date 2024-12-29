import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import pipeline
from fastapi import FastAPI
from pydantic import BaseModel
import gradio as gr
from datetime import datetime

app = FastAPI()

kg_path = "../Datasets/preprocessed_data/rag_data.json"

chat_history_path = "chat_history.json"
prompt_for_model_path = "prompt_for_model.json"
system_prompt = """
You are an expert Python developer specializing in code debugging and optimization. Your role is to:
1. Select the most relevant example from the provided ones, based on its similarity to the user's code and query.
2. Adapt the correct code from the selected example to fix the issues in the user's code.
3. Provide a clear explanation of why the selected example is relevant and how it addresses the user's code issues.
4. Return the corrected code adapted to the user's original context.

### Response Guidelines:
- Select and clearly identify the most relevant example from the list.
- Adapt the correct code from the chosen example to match the user's context and requirements.
- Be concise and precise in your explanations, focusing on the key differences between the user's code and the chosen example.
- Follow Python's best practices when generating the corrected code.

If none of the examples are relevant or the user's code is already correct, respond with:
- "The code is correct. No changes are necessary."
- Or: "None of the examples fully address the user's query. Please provide more context or additional examples."""


with open(kg_path, "r") as file:
    data = json.load(file)

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("rag_base/retriever_index.faiss")
generator = pipeline("text2text-generation", model="google/flan-t5-base")

class QueryRequest(BaseModel):
    query: str

def retrieve_examples(query, top_k=5):
    query_embedding = embedding_model.encode([query], convert_to_numpy=True)
    query_embedding = query_embedding / np.linalg.norm(query_embedding)

    distances, indices = index.search(query_embedding, top_k)
    # print(f"distances: {distances}")
    # print(f"indices: {indices}")
    # print(f"returned: {[data[idx] for idx in indices[0]]}")
    return [data[idx] for idx in indices[0]]

def generate_response(query, retrieved_examples):

    ### Original version
    #context = "\n".join(
        #[f"Example {i+1}:\nPrompt: {ex['prompt']}\nInput: {ex['input']}\nExplanation: {ex['explanation']}"
         #for i, ex in enumerate(retrieved_examples)]
    #)


    ### Slava changed
    context = "\n".join(
        [f"Example {i+1}:\nInput: {ex['input']}\nExplanation: {ex['explanation']}\nCorrect code for this example: {ex['correct_code']}"
         for i, ex in enumerate(retrieved_examples)]
    )


    print(f"Context: {context}")

    combined_input = (f"""
{system_prompt}

Below is the user's broken Python code, along with relevant examples of similar issues and their solutions. Your task is to:
1. Identify the example that best matches the user's issue.
2. Adapt the correct code from the selected example to fix the user's code.
3. Provide a clear explanation of why this example was chosen and how it resolves the user's issue.

### User's Broken Code:
{query}

### Relevant Examples:
{context}

### Output Format:
1. Explanation: Why this example is relevant and how it addresses the user's issue.
2. Corrected Code: Provide the corrected version of the user's code based on the selected example."""
    )

    response = generator(combined_input,
                         max_length=2048,
                         do_sample=True,
                         top_p=0.95,
                         temperature=0.25)

    return response[0]['generated_text'], combined_input

def save_chat_history(user_input, bot_response):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "user_input": user_input,
        "bot_response": bot_response
    }

    #try:
        #with open(chat_history_path, "r") as file:
            #history = json.load(file)
    #except FileNotFoundError:
        #history = []

    #history.append(entry)

    with open(chat_history_path, "a") as file:
        json.dump(entry, file, indent=4)


def save_full_prompt(full_prompt):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "full_input": full_prompt
    }

    #try:
        #with open(prompt_for_model_path, "r") as file:
            #history = json.load(file)
    #except FileNotFoundError:
        #history = []

    #history.append(entry)

    with open(prompt_for_model_path, "a") as file:
        json.dump(entry, file, indent=4)


#@app.post("/analyze")
#def analyze_code(request: QueryRequest):
    #retrieved_examples = retrieve_examples(request.query)
    #response = generate_response(request.query, retrieved_examples)
    #save_chat_history(request.query, response)
    #return {"response": response}

def gradio_interface(user_query):
    retrieved_examples = retrieve_examples(user_query)
    # print(f"retrieved example: {retrieved_examples}")
    response, full_prompt = generate_response(user_query, retrieved_examples)
    save_chat_history(user_query, response)
    save_full_prompt(full_prompt, )
    return response

# Gradio UI
interface = gr.Interface(
    fn=gradio_interface,
    inputs="text",
    outputs="text",
    title="Code Analysis Chatbot",
    description="Paste your broken code here"
)

# API endpoint
@app.get("/")
def gradio_ui():
    return interface.launch(share=True, inline=False)

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI()  # automatically reads OPENAI_API_KEY from environment

batch_size = 50 # batching chunks into 50 at a time instead of all 349 at once

def embed(chunks):
    all_embeddings = []
    for i in range(0, len(chunks), batch_size):   
        batch = chunks[i : i+batch_size]     
        response = client.embeddings.create(model="text-embedding-3-small", input=batch)
        for item in response.data:
            all_embeddings.append(item.embedding)
    return all_embeddings
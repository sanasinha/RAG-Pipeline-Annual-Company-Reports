import chromadb
from embedding import embed 

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import string

stop_words = set(stopwords.words('english'))

# filter the important keywords from a question
def filter_keywords(filtered, company):
    final = []
    for word in filtered:
        word = word.strip(string.punctuation)
        if company.lower() not in word.lower():
            final.append(word)
    return final

def extract_keywords(question, company):
    words = question.lower().split()
    filtered = []

    for word in words:
        if word not in stop_words:
            filtered.append(word)

    final = filter_keywords(filtered, company)    
    return " ".join(final[:2]) # keep relevant words together in one phrase, gonna assume the first few are the most valuable

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="annual_reports")

# given a question, find top 5 most similar chunks
def search(question, companies=["Genpact", "Walmart"], num_results=5):
    embedding = embed([question])

    all_documents = []
    all_metadatas = []
    all_distances = []
    
    for company in companies:
        results = collection.query(query_embeddings=embedding, where={"company": company}, n_results=num_results)
        all_documents += results['documents'][0]
        all_metadatas += results['metadatas'][0]
        all_distances += results['distances'][0]
    
    return {
        'documents': [all_documents],
        'metadatas': [all_metadatas],
        'distances': [all_distances]
    }

def keyword_search(query_term, chunks):
    matches = []
    for chunk in chunks:
        if query_term.lower() in chunk.lower():
            matches.append(chunk)
    return matches

# want to give context alongside the chunks so the llm can use this context when searching
def format_context(results):
    final = ""
    for document, metadata in zip(results['documents'][0], results['metadatas'][0]):
        final += "[Source: " + str(metadata["company"]) + ", chunk " + str(metadata["index"]) + "]\n" + document + "\n\n"
    return final
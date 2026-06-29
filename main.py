from extracting import extract
from chunking import chunk
from embedding import embed
from itemizing import item
from retrieving import search
from retrieving import format_context
from generating import generate
from retrieving import keyword_search
import chromadb
from retrieving import filter_keywords
from retrieving import extract_keywords
from reranking import rerank

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="annual_reports")

text = extract('g-20251231.htm', 'genpact.txt')
chunks = chunk(text)
embeddings = embed(chunks)

ids, emb_list, doc_list, meta_list = item(chunks, embeddings, "Genpact")
collection.add(ids=ids, embeddings=emb_list, documents=doc_list, metadatas=meta_list)

'''
print("# Genpact Chunks: " + str(len(chunks)))
print("Genpact 1st Chunk: " + chunks[0])
print("# Genpact Embeddings: " + str(len(embeddings)))
print()

text1 = extract('wmt-20250131.htm', 'walmart.txt')
chunks1 = chunk(text1)
embeddings1 = embed(chunks1)

ids1, emb_list1, doc_list1, meta_list1 = item(chunks1, embeddings1, "Walmart")
collection.add(ids=ids1, embeddings=emb_list1, documents=doc_list1, metadatas=meta_list1)

print("# Walmart Chunks: " + str(len(chunks1)))
print("Walmart 1st Chunk: " + chunks1[0])
print("# Walmart Embeddings: " + str(len(embeddings1)))

# combines genpact and walmart and distinguishes using company name metadata
print("Total items in collection:", collection.count())

#results1 = search("What is Genpact's total revenue?")
#print(results1['distances'])

#results2 = search("What is Genpact's profit margin?")
#print(results2['distances'])
'''

questions = [
    "What was Genpact's total revenue?",
    "What are Genpact's profits?",
    "What is Genpact's stock price?",
    "What was Walmart's total revenue?",
    "What are Walmart's profits?",
    "What is Walmart's stock price?",
    "Compare Walmart and Genpact's revenues?",
    "What is the capital of India?",
    "Should I invest in Genpact?",
    "What was Genpact's profit margin in 2025?"
]

for q in questions:
    print("Q:", q)
    print("A:", generate(q))
    print("-" * 80)
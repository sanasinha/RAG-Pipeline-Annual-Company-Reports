import nltk
from nltk.tokenize import sent_tokenize
import tiktoken

MAX_CHUNK_TOKENS = 500

def chunk(full_text):

    sentences = sent_tokenize(full_text)
    chunks = []
    current_chunk_sentences = []
    current_chunk_tokens = 0
    encoding = tiktoken.get_encoding("cl100k_base")

    for sentence in sentences:
        sentence_tokens = len(encoding.encode(sentence))                      

        if current_chunk_tokens + sentence_tokens > MAX_CHUNK_TOKENS:
            chunks.append(" ".join(current_chunk_sentences))                 
            current_chunk_sentences = current_chunk_sentences[-2:]          
            current_chunk_tokens = len(encoding.encode(" ".join(current_chunk_sentences)))

        current_chunk_sentences.append(sentence)
        current_chunk_tokens += sentence_tokens

    if current_chunk_sentences:
        chunks.append(" ".join(current_chunk_sentences))  
    
    return chunks
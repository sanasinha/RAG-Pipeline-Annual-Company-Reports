from retrieving import search
from retrieving import format_context
from reranking import rerank
from reranking import apply_reranking

import embedding

def generate(question, model="gpt-4.1-mini", temperature=0):
    results = search(question)
    ranked_positions = rerank(question, results, top_n=3)
    reranked_results = apply_reranking(results, ranked_positions)
    context = format_context(reranked_results)
    
    response = embedding.client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=[
            {"role": "system", "content": "I want you to use the retrieved chunks of the collection of annual reports to appropriately respond to the user question. Do not use your own pretrained knowledge, only use the content from the retrieved chunks. Ensure that the chunk used to answer the question is factually relevant to the question. If no relevant chunk is found, output that no relevant data was found to answer the user question. Cite the source, including the company name and the chunk index when answering a question."},
            {"role": "user", "content": "Here is the retrieved context:\n" + context + "\n\nQuestion: " + question}
        ]
    )
    
    return response.choices[0].message.content
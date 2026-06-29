import embedding

# given the top 5 similar chunks found using search(), rerank them in terms of best ability to answer the question
def rerank(question, results, top_n=3, model="gpt-4.1-mini"):
    initial_results = ""
    counter = 1

    for document in results['documents'][0]:
        initial_results += "Chunk " + str(counter) + ": " + document
        counter += 1

    response = embedding.client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "given the chunks you have pulled using search() to answer the question, i want you to order them in terms of how well the chunk's content directly answers what's being asked. make sure you are accounting for things like dates, specific segments, or context that pure cosine similarity might miss. Respond with ONLY a comma-separated list of chunk numbers in ranked order from most to least relevant, with no other text. Example: 3,1,4,2,5."},
            {"role": "user", "content": "Here is the initial ordering of chunks from search():\n" + initial_results + "\n\nQuestion: " + question}
        ]
    )

    chunk_ordering = response.choices[0].message.content.split(',')

    final_results = []

    try:
        final_results = [int(chunk_ordering[i]) - 1 for i in range(top_n)]
    except (IndexError, ValueError):
        final_results = list(range(top_n))

    return final_results

def apply_reranking(results, ranked_positions):
    selected_documents = [results['documents'][0][i] for i in ranked_positions]
    selected_distances = [results['distances'][0][i] for i in ranked_positions]
    selected_metadatas = [results['metadatas'][0][i] for i in ranked_positions]

    return {
        'documents': [selected_documents],
        'metadatas': [selected_metadatas],
        'distances': [selected_distances]
    }


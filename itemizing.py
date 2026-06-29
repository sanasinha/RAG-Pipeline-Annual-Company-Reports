def item(chunks, embeddings, company_name):

    ids = []
    embeddings_list = []
    documents_list = []
    metadatas_list = []

    for i in range(0, len(chunks)):
        ids.append(company_name + str(i))
        embeddings_list.append(embeddings[i])
        documents_list.append(chunks[i])
        metadatas_list.append({"company":company_name,"index":i})
    
    return ids, embeddings_list, documents_list, metadatas_list
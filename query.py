import sys
import ollama
import chromadb

client = chromadb.HttpClient(host='localhost', port=8000)
collection = client.get_collection("go-code")

query = ''.join(sys.argv[1:])

embed_query = ollama.embeddings(model="nomic-embed-text", prompt=query)['embedding']
related_docs = '\n\n'.join(collection.query(query_embeddings=[embed_query], n_results=10)['documents'][0])

prompt = f"{query} - Answer the question based on the following code:\n\n{related_docs}"

answer = ollama.generate(model='llama3', prompt=prompt)['response']
print(answer)

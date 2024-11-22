import os
import re
import ollama
import chromadb

exclude = set(['vendor', '.git', 'google-cloud-sdk'])


def scan_files(path, extension=None):
    text_contents = {}

    for root, dirs, files in os.walk(path, topdown=True):
        dirs[:] = [d for d in dirs if d not in exclude]
        print(root, dirs)
        for file in files:
            if (extension is None or file.endswith(extension)):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    text_contents[file] = f.read()
    return text_contents


def chunk_content(content, chunk_size=100):
    words = re.findall(r'\S+', content)
    chunks = []
    current_chunk = []
    word_count = 0

    for word in words:
        current_chunk.append(word)
        word_count += 1
        if word_count >= chunk_size:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
            word_count = 0
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    return chunks


def get_embeddings(chunks):
    return ollama.embeddings(model="nomic-embed-text", prompt=chunks)['embedding']


def add_to_chroma(data):
    chroma_client = chromadb.HttpClient(host='localhost', port=8000)
    collection = chroma_client.get_or_create_collection(name=col_name, metadata={"hnsw:space": "cosine"})

    for filename, content in data.items():
        chunks = chunk_content(content)
        for i, chunk in enumerate(chunks):
            embeds = get_embeddings(chunk)
            id = f"{filename}-{i}"
            metadata = {'source': filename}
            print(f"Adding documents {filename}: chunk_id {id}\n  metadata: {metadata}\n")

            collection.add(
                embeddings=embeds,
                documents=chunk,
                ids=id,
                metadatas=metadata,
            )

path = "/Users/frisk/dev/go"
col_name = "go-code"

data = scan_files(path, ".go")

add_to_chroma(data)
## Instructions

Run your embeddings base

```
docker run -d -p 8000:8000 -v chrome-data:/local/chroma/dir chromadb/chroma
```

Install dependecies

```
python3 -m venv venv
source venv/bin/activate
pip3 install -r req.txt
```

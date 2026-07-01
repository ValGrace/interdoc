app/ingestion.py
- extract text from a file and split it into chunks

`app/vectorstore.py`
- turn chunks into vectors and store them in DB (ChromaDB)

`app/main.py`
- endpoint is here
- wire everything together

Question --> [embed] -> [Search vector] -> 

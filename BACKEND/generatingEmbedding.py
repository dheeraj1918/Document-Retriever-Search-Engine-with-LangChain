from loadModel import EmbeddingManager 
from mongoDb import mongoDbInsert
embeddingManager=EmbeddingManager()
def generate_Embedding(documents):
    docs_to_insert=[{"text":doc.page_content,
        "embedding":embeddingManager.generate_embedding(doc.page_content).tolist()
    }for doc in documents]
    print(type(embeddingManager))
    print(embeddingManager)
    return mongoDbInsert(docs_to_insert)

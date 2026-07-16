from generatingEmbedding import embeddingManager
from pymongo import MongoClient
import certifi
from dotenv import load_dotenv
import os
load_dotenv()
db_url = os.getenv('MongodbApi')
def get_query_results(query,file_id):
    client=MongoClient( db_url,
        tlsCAFile=certifi.where())
    collection = client["RAG_TEST_1"]["documents"]
    query_embedding=embeddingManager.generate_embedding(query)
    query_embedding = query_embedding.tolist()
    if query_embedding:
        print("the given Query is embedded")
    pipeline = [
      {
            "$vectorSearch": {
              "index": "vector_index",
              "queryVector": query_embedding,
              "path": "embedding",
              "numCandidates":384,
              "limit": 5,
              "filter": {
                "file_id": file_id
            }
            }
      }, {
            "$project": {
              "_id": 0,
              "text": 1,
              "score": {"$meta": "vectorSearchScore"}
         }
      }
      
  ]
    results=collection.aggregate(pipeline)
    print(results)
    array_of_results = []
    for doc in results:
        array_of_results.append(doc)
    return array_of_results
    
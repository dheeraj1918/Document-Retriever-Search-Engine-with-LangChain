from generateEmbeddings import embeddingManager
from pymongo import MongoClient
import certifi
# Define a function to run vector search queries
def get_query_results(query,file_id):
  """Gets results from a vector search query."""
  client=MongoClient( "mongodb+srv://srisaisank01_db_user:312pF3ylJWPv2VNW@rag.esicypb.mongodb.net/?appName=RAG",
        tlsCAFile=certifi.where())
  collection = client["RAG_TEST_1"]["documents"]
  query_embedding = embeddingManager.generate_embedding(query)
  query_embedding = query_embedding.tolist()
  print(query_embedding)
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

  results = collection.aggregate(pipeline)
  print(results)

  array_of_results = []
  for doc in results:
      array_of_results.append(doc)
  return array_of_results
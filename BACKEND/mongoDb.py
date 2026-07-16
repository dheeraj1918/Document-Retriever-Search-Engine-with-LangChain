from pymongo import MongoClient
import random
import certifi
from indexModel import indexModel
def hexRand(size=6):
    hexResult=[]
    for i in range(size):
        hexResult.append(str(random.choice("123456789ABCDEF")))
    return "".join(hexResult)
def mongoDbInsert(docs_to_insert):
    client=MongoClient( "mongodb+srv://srisaisank01_db_user:312pF3ylJWPv2VNW@rag.esicypb.mongodb.net/?appName=RAG",
        tlsCAFile=certifi.where())
    hex=hexRand()
    collection=client["RAG_TEST_1"]["documents"]
    for doc in docs_to_insert:
        doc["file_id"]=hex
    indexModel(collection)
    collection.insert_many(docs_to_insert)
    
    return hex
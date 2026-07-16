from pymongo import MongoClient
import random
import certifi
from indexModel import indexModel
from dotenv import load_dotenv
import os
load_dotenv()
db_url = os.getenv('MongodbApi')
def hexRand(size=6):
    hexResult=[]
    for i in range(size):
        hexResult.append(str(random.choice("123456789ABCDEF")))
    return "".join(hexResult)
def mongoDbInsert(docs_to_insert):
    client=MongoClient( db_url,
        tlsCAFile=certifi.where())
    hex=hexRand()
    collection=client["RAG_TEST_1"]["documents"]
    for doc in docs_to_insert:
        doc["file_id"]=hex
    indexModel(collection)
    collection.insert_many(docs_to_insert)
    
    return hex
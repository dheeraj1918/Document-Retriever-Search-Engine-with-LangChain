from pymongo.operations import SearchIndexModel
import time

# Create your index model, then create the search index
def indexModel(collection):
    index_name="vector_index"
    existing_indexes = list(collection.list_search_indexes())

    for index in existing_indexes:
        if index["name"] == index_name:
            print(f"Search index '{index_name}' already exists.")
            return

    print(f"Creating search index '{index_name}'...")
    search_index_model = SearchIndexModel(
    definition = {
        "fields": [
        {
            "type": "vector",
            "numDimensions": 384,
            "path": "embedding",
            "similarity": "cosine"
        },{
        "type": "filter",
        "path": "file_id"
        }
        ]
    },
    name = index_name,
    type = "vectorSearch"
    )
    collection.create_search_index(model=search_index_model)
    # Wait for initial sync to complete
    print("Polling to check if the index is ready. This may take up to a minute.")
    predicate=None
    if predicate is None:
        predicate = lambda index: index.get("queryable") is True

    while True:
        indices = list(collection.list_search_indexes(index_name))
        if len(indices) and predicate(indices[0]):
            break
        time.sleep(5)
    print(index_name + " is ready for querying.")
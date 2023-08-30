import os
from dotenv import load_dotenv
import pymongo as pymongo
import chromadb
from chromadb.utils import embedding_functions

# Loading environment variables
load_dotenv()

MONGODB_CONNECTION_STRING = os.getenv('MONGODB_CONNECTION_STRING')

# creating MongoClient object
my_client = pymongo.MongoClient(MONGODB_CONNECTION_STRING)

# pointing to a data base
my_db = my_client["yelp_database"]

# Selecting a collection
yelp_collection = my_db["nyc_restaurants_data"]
# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path="/Users/shreemayi/Desktop/Projects/langchain_yelp/chromadb_embeddings/")

# Choose llm model to generate embeddings
default_ef = embedding_functions.DefaultEmbeddingFunction()

# Create a collection with required parameters
collection = chroma_client.get_or_create_collection(name="yelp_nyc_embeddings", metadata={"hnsw:space": "cosine"},
                                             embedding_function=default_ef)
# Preparing Documents to input in chromadb
count = 0
docs = []
object_ids = []
for x in yelp_collection.find({}, {"_id": 0}).sort("_id"):
    count += 1
    object_ids.append(str(count))
    docs.append(str(x))

# Adding documents to the collection
collection.add(documents=docs, ids=object_ids)

# Querying
results = collection.query(query_texts=["East village 4 rating"],  n_results=5)

# Printing the result of Query
for i in results['documents']:
    print(i)


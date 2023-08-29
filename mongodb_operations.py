import os
from dotenv import load_dotenv
import pymongo as pymongo

# Loading environment variables
load_dotenv()

MONGODB_CONNECTION_STRING = os.getenv('MONGODB_CONNECTION_STRING')

# creating MongoClient object
my_client = pymongo.MongoClient(MONGODB_CONNECTION_STRING)

# Creating a data base
my_db = my_client["my_mongo_database"]

# Listing all the databases
print(my_client.list_database_names())

# Creating a collection
yelp_collection = my_db["yelp_data"]

print(my_db.list_collection_names())

# Inserting documents (like a record in sql) in yelp_data collection of my database in MongoDB
yelp_document = {"Restaurant Name": "Bikanervala", "Address": "Newark Ave."}

x = yelp_collection.insert_one(yelp_document)
print(x.inserted_id)

yelp_documents = [
    {"Restaurant Name": "Sweet Green", "Address": "Astor Pl."},
    {"Restaurant Name": "Chihiro Tea", "Address": "LaGuardia Pl"},
    {"Restaurant Name": "Southern Spice", "Address": "Newark Ave."},
    {"Restaurant Name": "Falafel Inc.", "Address": "American Dream"},
    {"Restaurant Name": "Saravana Bhavan", "Address": "Lexington Ave."}
]

x = yelp_collection.insert_many(yelp_documents)

# print list of the _id values of the inserted documents
print(x.inserted_ids)

print(my_client.list_database_names())
print(my_db.list_collection_names())

# To view one document from the collection
x = yelp_collection.find_one()
print(x)

# To view all the documents from the collection and sorting based on key Restaurant Name and limit to 5 documents
for x in yelp_collection.find().sort("Restaurant Name").limit(5):
    print(x)

# Filtering using query to retrieve Restaurants on Newark Ave.
my_query = {"Address": "Newark Ave."}
for x in yelp_collection.find(my_query, {'_id': 0, "Restaurant Name": 1}):
    print(x)

# Craving some Boba!
my_query = {"Restaurant Name": {"$regex": ".*Tea.*"}}
for x in yelp_collection.find(my_query, {'_id': 0, "Restaurant Name": 1}):
    print(x)

# Adding some fake data document to delete later on
yelp_document = {"Restaurant Name": "Fikanervala", "Address": "Fewark Ave.", 'Fake': True}

x = yelp_collection.insert_one(yelp_document)
print(x.inserted_id)

my_query = {'Fake': True}
yelp_collection.delete_one(my_query)

yelp_documents = [
    {"Restaurant Name": "Sweet Green", "Address": "Astor Pl.", 'Fake': True},
    {"Restaurant Name": "Chihiro Tea", "Address": "LaGuardia Pl", 'Fake': True},
    {"Restaurant Name": "Southern Spice", "Address": "Newark Ave.", 'Fake': True},
    {"Restaurant Name": "Falafel Inc.", "Address": "American Dream", 'Fake': True},
    {"Restaurant Name": "Saravana Bhavan", "Address": "Lexington Ave.", 'Fake': True}
]

yelp_collection.insert_many(yelp_documents)

x = yelp_collection.delete_many(my_query)

print(x.deleted_count, " documents deleted.")

yelp_collection.drop()

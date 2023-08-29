from bs4 import BeautifulSoup
from dotenv import load_dotenv
import pymongo as pymongo
import os
DOMAIN = 'https://www.yelp.com/'

# Loading environment variables
load_dotenv()

MONGODB_CONNECTION_STRING = os.getenv('MONGODB_CONNECTION_STRING')

# creating MongoClient object
my_client = pymongo.MongoClient(MONGODB_CONNECTION_STRING)

# Creating a data base
my_db = my_client["yelp_database"]
yelp_collection = my_db["nyc_restaurants_data"]

inner_file_path = '/Users/shreemayi/Desktop/Projects/langchain_yelp/data_scrape/inner_html_files/' \
                  'inner_html_restaurant{}.html'

# Read HTML from a file
for i in range(1, 241):
    with open(inner_file_path.format(i), 'r', encoding='utf-8') as file:
        html = file.read()
    soup = BeautifulSoup(html, 'html.parser')

    # Initialize a document
    restaurant_details = {'name': None, 'link': None, 'categories': [], 'rating': None,
                          'number_of_reviews': None, 'price': None, 'short_address': None}
    # To extract link
    try:
        name_link = soup.find('div', class_='businessName__09f24__EYSZE').find('a')
        href = DOMAIN + name_link.get('href')
        restaurant_details['link'] = href
    except:
        print("No link")

    # To extract name
    try:
        restaurant_details['name'] = name_link.get_text()
    except:
        print("No name")

    # To extract rating
    try:
        restaurant_details['rating'] = soup.find('span', class_='css-gutk1c').get_text()
    except:
        print("No rating")

    # To extract number of reviews
    try:
        restaurant_details['number_of_reviews'] = soup.find('span', class_='css-8xcil9').get_text().strip('()').replace(
            ' reviews', '')
    except:
        print("No reviews")

    # To extract price
    try:
        restaurant_details['price'] = soup.find('span', class_='priceRange__09f24__mmOuH').get_text()
    except:
        print("No price")

    # To extract short address
    try:
        restaurant_details['short_address'] = soup.find('span', class_='css-chan6m').get_text()
    except:
        print("No short_address")

    # To extract categories
    try:
        for category in soup.find_all('span', class_='css-11bijt4'):
            restaurant_details['categories'].append(category.get_text())
    except:
        print("No categories")

    x = yelp_collection.insert_one(restaurant_details)
    print(i, x.inserted_id)
    print(restaurant_details)

# yelp_collection.drop()
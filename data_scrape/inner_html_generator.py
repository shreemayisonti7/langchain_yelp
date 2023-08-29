import requests
from bs4 import BeautifulSoup

# Base URL with a placeholder for the page number
base_url = 'https://www.yelp.com/search?find_desc=Restaurants&find_loc=New+York%2C+NY&start={}'

# Loop to iterate through pages, starting from 0, ending at 50 (inclusive), incrementing by 10
count = 1
for i in range(0, 241, 10):
    # Construct the URL for the current page
    url = base_url.format(i)

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all div elements with the class 'container__09f24__mpR8_'
        containers = soup.find_all('div', class_='container__09f24__mpR8_')

        # Extract the inner HTML of each container and save to a file

        for idx, container in enumerate(containers):
            inner_html = str(container)
            filename = f'/Users/shreemayi/Desktop/Projects/langchain_yelp/data_scrape/inner_html_files' \
                       f'/inner_html_restaurant{count}.html'
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(inner_html)
            print(f'Saved {filename}')
            count += 1
    else:
        print(f'Failed to retrieve page {i}')

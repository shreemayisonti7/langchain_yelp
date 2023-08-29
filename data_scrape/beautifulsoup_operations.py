from bs4 import BeautifulSoup

inner_file_path = '/Users/shreemayi/Desktop/Projects/langchain_yelp/data_scrape/inner_html_files/' \
                  'inner_html_restaurant{}.html'

with open(inner_file_path.format(1), 'r', encoding='utf-8') as file:
    html = file.read()
soup = BeautifulSoup(html, 'html.parser')
print(soup.get_text())
#=======================================#
#           THE SCRAPER ITSELF          #
#=======================================#

import requests
import csv
from datetime import datetime as dt
from bs4 import BeautifulSoup

# partly inspired from https://www.ionos.fr/digitalguide/sites-internet/developpement-web/web-scraping-avec-python/

def export_to_csv(book_info_table):
    exported_file_name = 'export_' + dt.now().strftime('%Y%m%d-%H%M%S') + '.csv'
    with open(exported_file_name, 'w', newline='') as csvfile:
        my_writer = csv.writer(csvfile, delimiter='\t')
        my_writer.writerows(book_info_table)
    print(len(book_info_table), 'lines added to "' + exported_file_name + '')
    return 1

# Getting
url = "http://books.toscrape.com/"
response = requests.get(url)
html = BeautifulSoup(response.text, 'html.parser')

# getting a single book
article_html = html.article
product_page_url = url + article_html.a['href']
product_page = BeautifulSoup(requests.get(product_page_url).text, 'html.parser').body.article
# print(product_page)

# extracting all the relevant fields

title = product_page.h1
category = ''
product_description = ''
review_rating = article_html.p['class'][1]
image_url = ''

product_info_list = product_page.table.find_all('td')
universal_product_code = product_info_list[0]
price_excluding_tax = product_info_list[2]
price_including_tax = product_info_list[3]
number_available = product_info_list[5]

input_variable = [
    ('product_page_url', 'universal_ product_code (upc)', 'title', 'price_including_tax','price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url'),
    (product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url)
]

export_to_csv(input_variable)

print("\n==============================\n\tTEST AREA\n==============================")
print("->", number_available)
print("\n\n\nOh! Also, \"hello world\"")
#=======================================#
#           THE SCRAPER ITSELF          #
#=======================================#

import requests
import csv
from bs4 import BeautifulSoup

# partly inspired from https://www.ionos.fr/digitalguide/sites-internet/developpement-web/web-scraping-avec-python/


# Getting
url = "http://books.toscrape.com/"
response = requests.get(url)
html = BeautifulSoup(response.text, 'html.parser')

# getting a single book
article_html = html.article

# extracting all the relevant fields
product_page_url = article_html.a['href']
universal_product_code = ''
title = ''
price_including_tax = ''
price_excluding_tax = ''
number_available = ''
product_description = ''
category = ''
review_rating = ''
image_url = ''

print("===== EXTRACTED DATA =====")
print("product_page_url =", product_page_url)
print("... \nOh! Also, \"hello world\"")
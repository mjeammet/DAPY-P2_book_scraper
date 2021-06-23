#=======================================#
#           THE SCRAPER ITSELF          #
#=======================================#

import requests
import csv
from datetime import datetime as dt
from bs4 import BeautifulSoup
import re # just used once, à voir si ça reste

# partly inspired from https://www.ionos.fr/digitalguide/sites-internet/developpement-web/web-scraping-avec-python/
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/#modifying-string
# https://openclassrooms.com/fr/paths/322/projects/832/assignment



def export_to_csv(book_info_table):
    '''
    Export scraped book list to newly-created csv file with time of export. Prints the amount of printed lines. Delimiter can be modified. Returns 1 if no exception. 
    '''

    #relevant delimiter character might vary from systems/software used :
    # ';' default. fit for a english microsoft excel
    # ',' fit for a french microsoft excel
    # '\t' opti for tsv format
    delim = ";"
    
    exported_file_name = 'export_' + dt.now().strftime('%Y%m%d-%H%M%S') + '.csv'
    with open(exported_file_name, 'w', newline='') as csvfile:
        my_writer = csv.writer(csvfile, delimiter=delim)
        my_writer.writerows(book_info_table)
    print(len(book_info_table), 'lines added to "' + exported_file_name + '')
    return 1

# Getting 
index_url = "http://books.toscrape.com/"
response = requests.get(index_url)

if response.ok:
    html = BeautifulSoup(response.text, 'html.parser')

    # getting a single book
    article_html = html.article
    product_page_url = index_url + article_html.a['href']
    product_page = BeautifulSoup(requests.get(product_page_url).text, 'html.parser')
    product_page_article = product_page.body.article
    # print(product_page)

    # extracting all the relevant fields
    title = product_page_article.h1.text
    category = product_page.ul.find_all('li')[2].text
    product_description = product_page_article.h2
    review_rating = article_html.p['class'][1]
    image_url = index_url + product_page_article.img['src'].split('../')[-1]

    product_info_list = product_page_article.table.find_all('td')
    universal_product_code = product_info_list[0].text
    price_excluding_tax = product_info_list[2].text
    price_including_tax = product_info_list[3].text
    number_available = re.split(', |\(| ', product_info_list[5].text)[3]

    input_variable = [
        ('product_page_url', 'universal_ product_code (upc)', 'title', 'price_including_tax','price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url'),
        (product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url)
    ]

    export_to_csv(input_variable)

print("\n==============================\n\tTEST AREA\n==============================")
print("->", category)
print("\n\n\nOh! Also, \"hello world\"")

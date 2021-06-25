#=======================================#
#           THE SCRAPER ITSELF          #
#=======================================#

import requests
import csv
from datetime import datetime as dt
from bs4 import BeautifulSoup
import re # just used once, à voir si ça reste
import math
import pandas # pour l'export en differentes sheets

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

    # ! verifier que len(book_info_table)-1 est bien égal au nombre total de bouquins dans la catégorie
    exported_file_name = 'export_' + dt.now().strftime('%Y%m%d-%H%M%S') + '.csv'
    print(len(book_info_table)-1, 'books of category added to "' + exported_file_name + '')
    with open(exported_file_name, 'w', newline='') as csvfile:
        my_writer = csv.writer(csvfile, delimiter=delim)
        my_writer.writerows(book_info_table)
    return 1
# https://stackoverflow.com/questions/63296554/python-multiple-sheet-to-export-as-csv

# Getting index
index_url = "http://books.toscrape.com/"
response = requests.get(index_url)

if response.ok:
    html = BeautifulSoup(response.text, 'html.parser')

    # Get the list of all categories and browse it
    category_list = html.find_all("ul")[2].find_all('a')

    for category in category_list[3:4]: # sublist the list for testing purposes
        category_url = index_url + category['href']
        category_page = BeautifulSoup(requests.get(category_url).text, 'html.parser')

        # ! hesitation between :
        # 1) making a 'category_complete' qui contiendrait les soupes de toutes les pages
        # 2) browsing pages and writing page by page

        # Initializing the list for this category
        input_variable = [
            ('product_page_url', 'universal_ product_code (upc)', 'title', 'price_including_tax', 'price_excluding_tax',
             'number_available', 'product_description', 'category', 'review_rating', 'image_url')
        ]

        # Getting potential additional pages
        nb_pages_in_category = math.ceil(int(category_page.form.strong.text)/20)

        # Same thing through pager ?
        # if category_page.find(class_='pager'):
        #     # link to next page
        #     # category_page.find(class_='pager').a['href'] != 'NoneType'
        #     # category_url.replace('index.html', 'page-2.html')
        #     nb_pages = category_page.find(class_='pager').li.text.rstrip()[-1]

        # Getting all books on this page
        category_articles_list = category_page.find_all('article')

        # if category has more than 20 books, add the other pages' books to category_bookslist
        for extra_page_nb in range(2,nb_pages_in_category+1):
            extra_page_url = index_url + category['href'].replace('index.html', 'page-' + str(extra_page_nb) + '.html')
            extra_books = BeautifulSoup(requests.get(extra_page_url).text, 'html.parser').find_all('article')
            category_articles_list.extend(extra_books)
            # print("category_bookslist has", len(category_articles_list), "books. ")

        # Browse category_articles_list
        # which contains all books of this category
        for article_html in category_articles_list:
            product_page_url = article_html.a['href'].replace('../../../', index_url + 'catalogue/')
            product_page = BeautifulSoup(requests.get(product_page_url).text, 'html.parser')
            product_page_article = product_page.body.article
            # print(product_page)

            # extracting all the relevant fields
            title = product_page_article.h1.text
            category = product_page.ul.find_all('li')[2].text  # ! Add a test to check it's the same than the category
            product_description = product_page_article.h2
            review_rating = article_html.p['class'][1]
            image_url = product_page_article.img['src'].replace('../../', index_url)

            product_info_list = product_page_article.table.find_all('td')
            universal_product_code = product_info_list[0].text
            price_excluding_tax = product_info_list[2].text
            price_including_tax = product_info_list[3].text
            number_available = re.split(', |\(| ', product_info_list[5].text)[3]

            input_variable.append([product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url])

        export_to_csv(input_variable)

print("\n==============================\n\tTEST AREA\n==============================")
print("->", '')
print("\n\n\nOh! Also, \"hello world\"")

#=======================================#
#           THE SCRAPER ITSELF          #
#=======================================#
"""Scraper getting infos for all books of all categories from "Books to Scrape" website.

Usage:
=====
    python books_data_extractor.py
"""
__authors__ = "Marie Jeammet"
__contact__ = "marie.jeammet@protonmail.com"
__date__ = "2021/06"
# -*- coding: utf-8 -*-

import requests
import csv
from datetime import datetime as dt
from bs4 import BeautifulSoup
import re # just used once, à voir si ça reste
import math
import os
# import pandas # https://stackoverflow.com/questions/63296554/python-multiple-sheet-to-export-as-csv  pour l'export en differentes sheets

def export_to_csv(output_dir_path, category_name, book_infos_list):
    """
    Export scraped book list to a csv file . Prints the amount of printed lines. Delimiter can be modified. Returns 1 if no exception.
    """
    delim = ";"  # default is ";" but delim character can also be "," or "\t"

    # prepare file name
    exported_file_name = output_dir_path + '/' + category_name.replace(' ', '_').lower() + '.csv'

    with open(exported_file_name, 'w', newline='', encoding="utf-8-sig") as csv_file:
        my_writer = csv.writer(csv_file, delimiter=delim)
        my_writer.writerows(book_infos_list)

    print(str(len(book_infos_list)-1) + "/" + str(nb_books_in_category), 'books added to "' + exported_file_name + '"')
    return 0

def get_book_infos(product_page_url):
    """
    Gets the info from a given book page
    """
    product_page = BeautifulSoup(requests.get(product_page_url).content, 'html.parser')
    product_page_article = product_page.body.article

    product_info_list = product_page_article.table.find_all('td')
    str_to_int_dict = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5,
    }

    # extracting all the relevant fields
    book_infos = {
        'product_page_url': product_page_url,
        'universal_product_code': product_info_list[0].text,
        'title': product_page_article.h1.text,
        "price_excluding_tax": product_info_list[2].text,
        "price_including_tax": product_info_list[3].text,
        "number_available": re.split(', |\(| ', product_info_list[5].text)[3],
        "product_description": product_page.head.find_all("meta")[2]['content'].strip(),
        'category': category_name,
        # category = product_page.ul.find_all('li')[2].text  # ! Add a test to check it's the same than the category
        "review_rating": str_to_int_dict[article_html.p['class'][1]],
        "image_url": product_page_article.img['src'].replace('../../', index_url),
    }
    return book_infos

if __name__ == "__main__":
    # Getting index
    index_url = "http://books.toscrape.com/"
    response = requests.get(index_url)

    html = BeautifulSoup(response.text, 'html.parser')

    # Preping the output dir
    output_dir_path = 'extraction_' + dt.now().strftime('%Y%m%d_%H%M%S')
    os.mkdir(output_dir_path)

    # Get the list of all categories and browse it
    category_list = html.find_all("ul")[2].find_all('a')

    for category in category_list[9:10]:  # sublist the list for testing purposes
        category_name = category.text.strip()
        category_url = index_url + category['href']
        category_page = BeautifulSoup(requests.get(category_url).text, 'html.parser')

        # ! hesitation between :
        # 1) making a 'category_complete' qui contiendrait les soupes de toutes les pages
        # 2) browsing pages and writing page by page

        # Getting potential additional pages
        nb_books_in_category = int(category_page.form.strong.text)
        nb_pages_in_category = math.ceil(nb_books_in_category/20)

        # Same thing through pager ?
        # if category_page.find(class_='pager'):
        #     # link to next page
        #     # category_page.find(class_='pager').a['href'] != 'NoneType'
        #     # category_url.replace('index.html', 'page-2.html')
        #     nb_pages = category_page.find(class_='pager').li.text.rstrip()[-1]

        # Getting all books on this page
        book_list = category_page.find_all('article')

        # if category has more than 20 books, add the other pages' books to category_bookslist
        for extra_page_nb in range(2,nb_pages_in_category+1):
            extra_page_url = index_url + category['href'].replace('index.html', 'page-' + str(extra_page_nb) + '.html')
            extra_books = BeautifulSoup(requests.get(extra_page_url).text, 'html.parser').find_all('article')
            book_list.extend(extra_books)
            # print("category_bookslist has", len(category_articles_list), "books. ")

        # Initializing the list for this category
        output_list = []

        # Browse books list
        # which contains all books of this category
        for article_html in book_list:
            product_page_url = article_html.a['href'].replace('../../../', index_url + 'catalogue/').replace('index.html', '')
            book_infos = get_book_infos(product_page_url)

            # first time, prints header
            if article_html == book_list[0]:
                output_list.append(list(book_infos.keys()))
            output_list.append(list(book_infos.values()))

        export_to_csv(output_dir_path, category_name, output_list)
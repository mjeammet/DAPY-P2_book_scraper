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
import re  # just used once, à voir si ça reste
import math
import os
# import pandas
# https://stackoverflow.com/questions/63296554/python-multiple-sheet-to-export-as-csv  pour l'export en differentes sheets


def export_to_csv(book_infos_list, output_dir_path, book_category_name):
    """
    Export scraped book list to a csv file . Prints the amount of added books. Delimiter can be modified.
    Returns 1 if no exception.
    """
    delim = ";"  # default is ";" but delim character can also be "," or "\t"
    formatted_category_name = book_category_name.replace(' ', '_').lower()

    # prepare file name
    exported_file_name = output_dir_path + formatted_category_name + '.csv'

    with open(exported_file_name, 'w', newline='', encoding="utf-8-sig") as csv_file:
        my_writer = csv.writer(csv_file, delimiter=delim)
        my_writer.writerows(book_infos_list)



    # load all covers to category folder
    cover_dir_path = output_dir_path + formatted_category_name + '_covers/'
    os.mkdir(cover_dir_path)
    for book in book_infos_list[1:]:
        cover_url = book[9]
        upc = book[1]
        cover_data = requests.get(cover_url).content
        open(cover_dir_path + upc + '.jpg', 'wb').write(cover_data)

    print(str(len(book_infos_list)-1), 'books added to "' + exported_file_name + '"')
    # TODO add a test len(book_infos_list)-1 == nb_books_in_category
    return 0


def get_book_infos(book_category_name, book_page_url):
    """
    Gets the info from a given book page
    """
    whole_page_soup = BeautifulSoup(requests.get(book_page_url).content, 'html.parser')
    product_page_article = whole_page_soup.body.article

    product_info_list = product_page_article.table.find_all('td')
    str_to_int_dict = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5,
    }

    # extracting all desired fields
    article_info = {
        'product_page_url': book_page_url,
        'universal_product_code': product_info_list[0].text,
        'title': product_page_article.h1.text,
        "price_excluding_tax": product_info_list[2].text,
        "price_including_tax": product_info_list[3].text,
        "number_available": re.split(', |\(| ', product_info_list[5].text)[3],
        "product_description": whole_page_soup.head.find_all("meta")[2]['content'].strip(),
        'category': book_category_name,
        # category = product_page.ul.find_all('li')[2].text  # ! Add a test to check it's the same than the category
        "review_rating": str_to_int_dict[product_page_article.find(class_="star-rating")['class'][-1]],
        "image_url": product_page_article.img['src'].replace('../../', index_url),
    }
    return article_info


def get_books_list(category_url):
    """
    Get a list of books from a category_url
    """
    # Getting index page and initial books list
    category_page = BeautifulSoup(requests.get(category_url).text, 'html.parser')
    books_list = category_page.find_all('article')

    # Making a master soup containing all articles over printing page by page (or worst, book by book)
    # For category with more than one page :
    #   getting the number of books (and thus the number of extra pages) and accessing pages directly
    #   over using pager to extract total number of pages and getting page link

    # Getting potential additional pages
    nb_books_in_category = int(category_page.form.strong.text)
    nb_pages_in_category = math.ceil(nb_books_in_category / 20)

    # if category has more than 20 books, add the other pages' books to books_list
    for extra_page_nb in range(2, nb_pages_in_category + 1):
        extra_page_url = category_url.replace('index.html', 'page-' + str(extra_page_nb) + '.html')
        extra_books = BeautifulSoup(requests.get(extra_page_url).text, 'html.parser').find_all('article')
        books_list.extend(extra_books)
        # print("category_bookslist has", len(category_articles_list), "books. ")

    return books_list


if __name__ == "__main__":
    # Getting index
    index_url = "http://books.toscrape.com/"
    response = requests.get(index_url)

    index_soup = BeautifulSoup(response.content, 'html.parser')

    # Preping the output dir
    output_dir_path = 'extraction_' + dt.now().strftime('%Y%m%d_%H%M%S') + '/'
    os.mkdir(output_dir_path)

    # Get the list of all categories and browse it
    category_list = index_soup.find_all("ul")[2].find_all('a')

    # Browse categories to get books list for each one. Sublisted for testing purposes
    for category in category_list:
        category_name = category.text.strip()
        category_url = index_url + category['href']

        book_list = get_books_list(category_url)

        # Initializing the output_list for this category
        output_list = []

        # Browse books list
        # which contains all books of this category
        for article_html in book_list:
            book_url = article_html.a['href'].replace('../../../', index_url + 'catalogue/').replace('index.html', '')
            book_infos = get_book_infos(category_name, book_url)

            # first time, prints header
            if article_html == book_list[0]:
                output_list.append(list(book_infos.keys()))
            output_list.append(list(book_infos.values()))

        export_to_csv(output_list, output_dir_path, category_name)
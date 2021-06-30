![logo-books-online](https://user.oc-static.com/upload/2020/09/22/1600779540759_Online%20bookstore-01.png "Books Online logo")

# Book scraper

Marie Jeammet - v0.1 - 2021/06 

## Context
This project is a simple scraper, extracting detailed information about the books available at http://books.toscrape.com/

## Technologies
This project was created with Python 3.6.9

## Usage

### Cloning the project

Clone project the project to desired location: 

`$ git clone https://github.com/mjeammet/project2_book_scraper.git`

### Setting the environment

In the project's directory, create and activate the environment: 

`$ python3 -m venv env`

and activate it 

`$ source env/bin/activate`
 
Install required packages with: 

`$ pip install -r requirements.txt`

## Running the script
Once you've activated your environment and made sure all required packages are correctly set up, go and run: 

`$ python books_data_extractor.py`

This will create an `extraction_<date>_<time>` folder containing a file for each extracted book category.

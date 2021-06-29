![name-of-you-image](https://user.oc-static.com/upload/2020/09/22/1600779540759_Online%20bookstore-01.png)

# Book scraper

Marie Jeammet - v0.1 - 2021/06 

## Context
This script is written using python 3.6.9 as part of our project to scrape all book prices and infos from http://books.toscrape.com/

## Usage

### Cloning the doc

Clone directory into desired directory

`git clone https://github.com/mjeammet/project2_book_scraper.git`

### Setting the environment

Create the environment and activate it

`python3 -m venv env`

`source env/bin/activate`
 
Install necessary packages with 

`pip install -r requirements.txt`

## Running the script
Once you've activated your environment and made sure all required packages are correctly set up, go and run

`python price_extraction.py`

This will create an `extraction_<date>_<time>` folder containing a file for each extracted book category.

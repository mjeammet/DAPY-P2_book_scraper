# Book scraper
Marie Jeammet - v0.1 - 2021/06 

## Context
This script is written as part of our project to scrape all book prices and infos from http://books.toscrape.com/

...  breaking character, this is an exercice as the 2nd project of 13 to becoming an app dev with python.
https://openclassrooms.com/fr/paths/322/projects/832/assignment

## Setting the environment
This script was written using python3.8.9. 

Create the environment and activate it

`python3 -m venv env`

`source env/bin/activate`
 
Install necessary packages with 

```pip install -r requirements.txt```

## Running the script
Once you've activated your environment and made sure all required packages are correctly set up, go and run

```python price_extraction.py```

This will create a file name after format ```export_<date-time>.csv``` which will contain all available infos. 
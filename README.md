# Book scraper
Marie Jeammet - v0.1 - 2021/06 

## Context
This script is written as part of our project to scrape all book prices and infos from http://books.toscrape.com/

...  breaking character, this is an exercice as the 2nd project of 13 to becoming an app dev with python.
https://openclassrooms.com/fr/paths/322/projects/832/assignment

## Setting the environment
This script was written using python3.8.9. 

Creating the environment 

```python3 -m venv env```

if you are using python2, you might want to upgrade as 

Environment can be activated using 

```source env/bin/activate```

if  
```pip install -f requirements.txt```

this will install all required modules and packages

## Running the script
Once you've activated your environment and made sure all required packages are correctly set up, go and run

```python price_extraction.py```

This will create a file name after format ```export_<date-time>.csv``` which will contain all available infos. 
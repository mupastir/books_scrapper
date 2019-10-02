# Books scrapper 

This `Scrapy` application collect information from 
[books-toscrape site](http://books.toscrape.com) and saves info about books
in `CSV` file.


## Download app

To download application run next command in terminal:

`git clone https://github.com/mupastir/books_scrapper.git`

or

Download `ZIP` archive file by this 
[link](https://github.com/mupastir/books_scrapper/archive/master.zip)
and extract where is convenient for you.

## Install requirements

To successfully start app you should to install requirements.
It's recommended to use virtual environment (for example, `pipenv install && pipenv shell`)

or just `pip install -r requirements.txt`

## Run app

To start app run command: 

`python main.py`

If app would be stopped you could rerun it and scrapper will continue to append
info about books from point where it was stopped.

## Output

Output `CSV` file `SITE_DATA.CSV` consists from such columns:

- `URL` - link to a book
- `TITLE`
- `DESCRIPTION`
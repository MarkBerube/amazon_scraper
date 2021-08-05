# a pretty low level amazon price scraper that uses URLs from a CSV file

import requests as req
from bs4 import BeautifulSoup as bs
import pandas as pan
from datetime import datetime as dt

# pretend to be a browser... act natural!
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
}
# CSV file with RTX 3090 URLs from amazon
csv_file = pan.read_csv('urls.csv')
current_time = dt.now().strftime('%Y-%m-%d')
dt.now
urls = csv_file.url
table = pan.DataFrame()

for n, url in enumerate(urls):
    site = req.get(url, headers=headers)
    soup = bs(site.content, features='lxml')
    # get the product title
    title = soup.find(id='productTitle').get_text().strip()
    print(title)

    # find the price - if we can otherwise set it to nothing
    # TODO: scrape marketplace prices although they might be incredibly inaccurate and not all that useful
    try:
        price = float(soup.find(id='priceblock_ourprice').get_text().replace('$', '').replace(',', '').strip())
    except:
        price = ''

    row = pan.DataFrame({
        'title': title,
        'price': price,
        'url': url
    }, index=[n])

    table = table.append(row)

# turn into an excel spreadsheet
table.to_csv('scrapes/SCRAPE_HISTORY_{}.csv'.format(current_time),index=False)
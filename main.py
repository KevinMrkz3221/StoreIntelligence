
from src.models import Product
from bs4 import BeautifulSoup
import requests

if __name__ == '__main__':
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    url = 'https://www.amazon.com.mx/gp/bestsellers/?ref_=nav_cs_bestsellers'
    response = requests.get(url, headers=headers)




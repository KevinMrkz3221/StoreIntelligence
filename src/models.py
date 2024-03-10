from dataclasses import dataclass, field
from typing import List, Dict

from bs4 import BeautifulSoup
import requests
from time import sleep

@dataclass
class Product:
    name: str
    price: float
    product_url: str
    product_img: str


    def to_dict(self):
        return {
            'name' : self.name,
            'price': self.price,
            'product_url': self.product_url,
            'product_img': self.product_img
        }

@dataclass
class Department:
    name: str
    url: str
    products: List[Product] = field(default_factory=list)
    page_no: int = 0
    items_no: int = 0
    offer: int = 0
    soup: BeautifulSoup = None

    def setSoup(self, response_text):
        self.soup = BeautifulSoup(response_text, 'html.parser')

    def  getPageNumber(self):
        pages = self.soup.find('ul', 'a-pagination')
        self.page_no = int(pages.find_all('li')[-2].text)

    def getPageElements(self):
        # Obtener todos los cards
        cards = self.soup.find_all('div', id='gridItemRoot')

        for card in cards:
                
            image = card.find('img')['src']
            name = card.find_all('a', 'a-link-normal')[1].find('span').find('div').text
            ofert_price = card.find('span', class_='a-color-secondary')

            element = Product(name, 0, card.find_all('a', 'a-link-normal')[1]['href'], image)

            self.products.append(element)

    def getAllElements(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        print(self.page_no, range(1, self.page_no))
        if not self.page:
            response = requests.get(self.url, headers=headers)
        else:
            for i in range(0, self.page_no):
                response = requests.get(self.url + f'={i}') if i != 1 else response.get(self.url, headers=headers)
                while response.status_code != 200:
                    response = requests.get(self.url + f'={i}') if i != 1 else response.get(self.url, headers=headers)
                    print(response.status_code)
                    sleep(3)

            print(self.name, response.status_code)
            self.setSoup(response.text)
            self.getPageNumber()
            self.getPageElements()

        
    
from dataclasses import dataclass, field
from typing import List, Dict
from datetime import datetime
from time import sleep
import json

from bs4 import BeautifulSoup
import requests
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from .settings import Base, ENGINE, session, logger

# Se crea un objeto que pueda entender el orm de SQLAlquemy


class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)
    product_url = Column(String)
    product_img = Column(String)
    department = Column(String)
    in_stock = Column(Boolean)
    added_at = Column(DateTime, default=datetime())

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'product_url': self.product_url,
            'product_img': self.product_img,
            'department': self.department,
            'in_stock': self.in_stock,
            'added_at': self.added_at
        }

    def to_log(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'department': self.department,
            'in_stock': self.in_stock,
            'added_at': self.added_at
        }


# Se encarga de gran parte de la extraccion
@dataclass
class Department:
    name: str
    url: str
    products: List[Product] = field(default_factory=list)
    pages: List = field(default_factory=list)
    soup: BeautifulSoup = None

    # Guarda todos los productos dentro del departamento
    def saveProducts(self):
        session.add_all(self.products)
        session.commit()
        logger.log(f'Saved department Products | {self.name}')

    # Guarda un solo producto
    def saveProduct(self, product):
        session.add(product)
        session.commit()

        logger.log(f'Saved {product.to_log()} | {self.name}')

    def setSoup(self, response_text):
        self.soup = BeautifulSoup(response_text, 'html.parser')
        logger.log(f'Setting new soup | {self.name}')

    def getPageNumber(self):
        pages = self.soup.find('ul', 'a-pagination')
        self.pages = pages.find_all('li')[2:-1]

        logger.log(f'Adding pages references | {self.name}')

    def getPageElements(self):
        # Obtener todos los cards
        cards = self.soup.find_all('div', id='gridItemRoot')

        for card in cards:

            # Esta parte contiene la logica de extraccion de cada uno de los elementos
            try:
                image = card.find('img')['src']
            except:
                image = ''

            try:
                name = card.find_all(
                    'a', 'a-link-normal')[1].find('span').find('div').text
            except:
                name = ''

            try:
                price = card.find('span', 'p13n-sc-price')
                price = float(price.text.replace('$', '').replace(',', ''))
                stock = True
            except AttributeError:
                try:
                    price = card.find(
                        'span', class_='_cDEzb_p13n-sc-price_3mJ9Z')
                    price = float(price.text.replace('$', '').replace(',', ''))
                    stock = True
                except:
                    price = 0.0
                    stock = False

            # genera el objeto apoyandonos del orm
            element = Product(name=name,
                              price=price,
                              product_url='https://www.amazon.com.mx/' +
                              card.find_all('a', 'a-link-normal')[1]['href'],
                              product_img=image,
                              department=self.name,
                              in_stock=stock
                              )
            logger.log(f'Get {element.to_log()} | {self.name}')
            self.saveProduct(element)

            self.products.append(element)

    def getAllElements(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

        self.getPageElements()

        for element in self.pages:

            response = requests.get(
                'https://www.amazon.com.mx' + element.find('a')['href'], headers=headers)

            while response.status_code != 200:
                response = requests.get(
                    'https://www.amazon.com.mx' + element.find('a')['href'], headers=headers)
                sleep(3)

            self.setSoup(response_text=response.text)
            self.getPageElements()

        logger.log(f'Finish department extration | {self.name}')

    def getJson(self):
        records = [product.to_dict() for product in self.products]
        file_name = "data/productos.json"

        # Escribir la lista en el archivo JSON
        with open(file_name, 'a', encoding='utf-8') as json_file:
            json.dump(records, json_file, indent=4, ensure_ascii=False)

        logger.log(f"Los datos se han guardado en el archivo '{file_name}'")


"""
    Se encarga de generar todas las tablas dentro de la base de datos
    en caso de que no se encuentren creadas
"""
Base.metadata.create_all(ENGINE)

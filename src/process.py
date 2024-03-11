import requests
from bs4 import BeautifulSoup
from time import sleep

from src.models import Department
from src.settings import logger


def requester(URL):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0',
        'Accept': 'text/html',
        'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
        'Referer': 'https://www.example.com',
        'Connection': 'close'
    }

    response = requests.get(URL, headers=headers)
    logger.log(str(response.status_code) + ' | Best Sellers')
    while response.status_code != 200:
        response = requests.get(URL, headers=headers)
        logger.log('Status code: ' + str(response.status_code) + ' | Best Sellers')
        if response.status_code == 200:
            break
        sleep(3)

    return response


def amazonBestSellersHeaders(response):
    # Primer request a pagina de Amazon best sellers
    soup = BeautifulSoup(response.text, 'html.parser')
    headers = soup.find_all('div', class_='a-carousel-header-row')
    logger.log('Collecting Headers')
    return headers


def getDepartmentsList(headers):
    department_list = []
    for header in headers:
        query = header.find('a')
        department_list.append(
            Department(
                str(query['aria-label'].replace(' - Ver más', '')),
                'https://www.amazon.com.mx' + str(query['href'])
            )
        )
    logger.log('Adding departments references')
    return department_list


def extraction(department_list):

    for department in department_list:
        logger.log(f'===== {department.name} ====')
        response = requests.get(url=department.url)
        logger.log(f'{str(response.status_code)} | {department.name}')
        while response.status_code != 200:
            response = requests.get(url=department.url)
            logger.log(f'Status code: {str(response.status_code)} | {department.name}')
            sleep(3)
        # Despues de que la petición es aceptada nosotros mandamos ese response text
        # Lo preparamos para la extracción
        # Nota se tiene que modificar y mejor utilizar una lista de urls ya que cuenta con los diferentes urls y no utiliza la converción  de
        # URL.com.mx/endpoint=no_pagina
        department.setSoup(response.text)
        department.getPageNumber()
        department.getAllElements()
        department.getJson()

    return department_list


# Funcion utilizada en el main
def amazonBestSellersProducts():
    response = requester(
        'https://www.amazon.com.mx/gp/bestsellers/?ref_=nav_cs_bestsellers')
    headers = amazonBestSellersHeaders(response=response)

    department_list = getDepartmentsList(headers=headers)
    department_list = extraction(department_list)

import requests
from bs4 import BeautifulSoup
import re

def main_info_func():
    response = requests.get('https://petrsu.ru/page/education/bakalavriat_i_spec/priemnaya-kampaniya/peretchen-napravlenii-podgotovki')
    content = response.content

# Парсим HTML-код страницы с помощью библиотеки BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')

# Находим таблицу с помощью селектора
    table = soup.find('div', class_='bachelor-border-table')
    header = soup.find('div', class_='bachelor-border-table-header').find_all('p')
    info = table.find_all('div', class_='row row-flex')


    with open('csv/data.csv','w') as f:
        s = ''
        for i in header:
            col = i.text
            if col == 'Направление подготовки (специальности) специальностей высшего образования':
                col = 'Направление подготовки (специальности)'
            s += col+';'
        f.write(s)
        f.write('Форма обучения\n')
        for i in info:
            f.write(i.find('div', class_='bachelor-border-code').text.split()[0])# код
            f.write(';')
        
            f.write(i.find('div', class_='col-xs-12 col-sm-12 col-md-4').text.strip()) # профиль
            f.write(';') 
            ekz = i.find_all('div', class_='col-xs-12 col-sm-12 col-md-3')
            vstup = str(ekz[0])
            vstup = re.sub(r'\<[^>]*\>', '', vstup.replace('<br/>', ' ')) # вступительные испытания
            vstup = re.sub(r"\s{2,}",' ', vstup.strip())
            f.write(vstup)
            f.write(';')
            prof = str(ekz[1])
            prof = re.sub(r'\<[^>]*\>', '', prof.replace('<br/>', ' ')) # профильные испытания
            prof = re.sub(r"\s{2,}",' ', prof.strip())
            f.write(prof)
            f.write(';')
            f.write(i.find('div', class_='bachelor-border-code').text.split()[1])
        
            f.write('\n')


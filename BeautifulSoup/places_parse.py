import requests
from bs4 import BeautifulSoup


def places_parse_func():
    response = requests.get('https://petrsu.ru/page/education/bakalavriat_i_spec/priemnaya-kampaniya/kolitchesvto-byuzhdetnyh-mest')
    content = response.content

# Парсим HTML-код страницы с помощью библиотеки BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')

# Находим таблицу с помощью селектора
    table = soup.find('div', class_='bachelor-border-table')
    header = soup.find('div', class_='bachelor-border-table-header').find_all('strong')
    info = table.find_all('div', class_='row row-flex')
    form = table.find_all('div', class_='col-xs-12 col-sm-12 col-md-12')

    with open('csv/places.csv','w') as f:
        s=''
        for i in header:
                if i.text != 'Контрольные цифры приема':
                    s+=''.join(i.text.split('-'))+';'

        f.write(s)
    
        f.write('Форма обучения;')
        f.write('Стоимость обучения\n')
        for i in info:
            f.write(i.find('div', class_='col-xs-12 col-sm-12 col-md-2').text.strip())# код

            f.write(';')
            f.write(i.find('div', class_='col-xs-12 col-sm-12 col-md-3').text.strip()) # профиль
            f.write(';')
            s=''
            for j in i.find_all('div', class_='hidden-xs hidden-sm'):
                s+=j.text.strip()+';'
            f.write(s)
            if i.find('div', class_='col-xs-12 col-sm-12 col-md-2').find_previous(class_='col-xs-12 col-sm-12 col-md-12').text.strip() != '':
                form_name = i.find('div', class_='col-xs-12 col-sm-12 col-md-2').find_previous(class_='col-xs-12 col-sm-12 col-md-12').text.strip()
            f.write(form_name.split()[0])
            f.write(';https://petrsu.ru/page/education/bakalavriat_i_spec/priemnaya-kampaniya/stoimost-obutcheniya-na-platnoi-osn')
            f.write('\n')

        


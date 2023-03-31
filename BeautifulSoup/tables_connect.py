import pandas as pd
from pymystem3 import Mystem
import places_parse
from main_info_parse import main_info_func
from places_parse import places_parse_func

main_info_func()
places_parse_func()

places = pd.read_csv('csv/places.csv',encoding='cp1251', sep=';')
info = df = pd.read_csv('csv/data.csv',encoding='cp1251', sep=';')
res = info.merge(places, on=["Код","Направление подготовки (специальности)", 'Форма обучения'])
res.to_csv('csv/result.csv', sep=';',encoding='cp1251')


end = ""
for i in res["Направление подготовки (специальности)"]:
    text_string = i.lower()
    a = []
    D = ""
    l = {}
    a = text_string.split(';')
    m = Mystem()
    n = len(a)
    j = 0
    for s in a:
        lemmas = m.lemmatize(s)
        for lemma in lemmas:
            if (lemma.isalpha() == True):
                D += lemma + " "
    D=D[:len(D)-1]
    end+=D+";"
with open('mystem_faculty.csv', 'w') as f:
    f.write(end[:-1])
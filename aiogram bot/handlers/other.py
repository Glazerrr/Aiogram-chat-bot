from aiogram import types, Dispatcher
from create_bot import dp
from pymystem3 import Mystem
import pandas as pd
from handlers.admin import send_qa_to_db

df2 = pd.read_csv('csv/mystem_faculty.csv', delimiter=';', encoding='1251')
df3 = pd.read_csv('csv/result.csv', delimiter=';', encoding='1251')

async def send_question(message: types.Message):
    D = await mystem_sentence(message.text)
    sentence = " ".join(D.keys())
    faculty = await search_faculty(message.text)
    ans = await bot_sentence(sentence,faculty)
    for item in ans:
        await message.answer(item)
    await send_qa_to_db(message.from_user.id, message.text, ans)


async def mystem_words(document_text):  # частотный словарь начальных форм (для поиска факультета)
    text_string = document_text.lower()
    lemmas = []
    m = Mystem()
    for s in text_string.split(';'):
        lemmas += [lemma for lemma in m.lemmatize(s) if lemma.isalpha()]
        D = " ".join(lemmas)
    return D


async def mystem_sentence(document_text):  # частотный словарь начальных форм (для поиска вопроса)
    text_string = document_text.lower()
    D = {}
    a = text_string.split(';')
    m = Mystem()
    n = len(a)
    j = 0
    for s in a:
        lemmas = m.lemmatize(s)
        for lemma in lemmas:
            if (lemma.isalpha() == True):
                l = D.get(lemma, [0] * n)
                l[j] = l[j] + 1
                D[lemma] = l
        j = j + 1
    return D


async def search_faculty(document_text):

    faculty = list()
    for names in df2:  # создаем список множеств факультетов
        faculty.append(set(names.split(" ")))
    for i in faculty: # убираем ненужные слова
        i -= {a for a in i if len(a) < 3}
    text_string = await mystem_words(
        document_text)  # создаем предложение, состоящее из начальных форм предложения пользователя
    words = {word for word in text_string.split(" ")} # добавляем слова введенные пользователем (нач формы) в множество
    maximal = dict()  # cловарь максимальных совпадений
    for i in range(len(faculty)):  # для каждого факультета
        if not faculty[i].isdisjoint(words):  # проверяет общие элементы
            maximal[i] = faculty[i].intersection(words)  # пересечение множеств факультетов и предложения пользователя
    maximal = list(maximal.items())  # преобразование в список для дальнейшего поиска максимальных совпадений
    out = []
    try:
        a = max(maximal, key=lambda i: i[1])  # поиск максимального элемента в списке
    except:
        out.append(['Направление не найдено'])
        return out
    #out = [[df3.iloc[maximal[i][0]]['Направление подготовки (специальности)'], df3.iloc[maximal[i][0]]['Форма обучения']] for i in range(len(maximal)) if len(maximal[i][1]) == len(a[1])] # првоерка на то что максимальных элементов несколько, 
    for i in range(len(maximal)):
        if len(maximal[i][1]) == len(a[1]):  
            out.append([df3.iloc[maximal[i][0]]['Направление подготовки (специальности)'], df3.iloc[maximal[i][0]]['Форма обучения']])  # 
    words = set()
    return out
    

async def question_from_user(sentence, a):  # поиск нужных данных
    for i in sentence.split():
        if i in a:
            return True
    return False

async def bot_sentence(sentence, faculty):
    answers = []  # список с ответами бота
    if faculty[0][0] == 'Направление не найдено':
        answers.append(f"Повторите еще раз запрос\nНеправильно введено направление")
        return answers
    df3 = pd.read_csv('csv/result.csv', delimiter=';', encoding='1251')
    
    questions = {
        "Стоимость обучения": ["цена", "заплатить", "плата", "стоит", "стоимость", "выйдет", "стоить", 'платной', 'платной основе'],
        "Профильные вступительные испытания для поступающих на базе среднего профессиональ-ного или высшего образования, мин. кол. баллов": ["профильный", "средний", "высший"],
        "Вступительные испытания, мин. кол. баллов": ["проходной", "поступить", "порог поступить", "поступление", "минимальный", "сдавать", "сдать", "необходимо сдать", "сдача", "егэ"],
        "Общий конкурс": ["бюджет", "бюджетный", "бюджетник", "бюджетным"],
        "Целевая квота": ["целевой", "целевых", "целевик", "целевым"],
        "Особая квота": ["квотный", "квотных", "квотник", "квотным",'особый', 'особая', 'особых'],
        "По договорам об оказании платных образовательных услуг": ["платный", "платник", "платных", "платным", 'платных мест'],
        "Всего": ["все", 'общее']
    }

    column = ""
    for key, value in questions.items():
        if await question_from_user(sentence, value):
            column = key
            break
    if not column:
        answers.append(f"Повторите еще раз запрос\nНекорректно указан вопрос")
    else:
        for i in range(len(faculty)):
            a = df3.loc[(df3["Направление подготовки (специальности)"] == faculty[i][0]) & (df3['Форма обучения'] == faculty[i][1]), column].values[0]
            answers.append(f"На направлении - {faculty[i][0]}, форма обучения -  {faculty[i][1]}: {str(a)}")
    return answers


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(send_question)

    

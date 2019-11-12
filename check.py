from flask import Flask, request
from nltk.stem import WordNetLemmatizer
import re
import numpy as np
from collections import Counter
from scipy.spatial.distance import cosine
import gensim.downloader as api
# nltk.download('wordnet')


model = api.load("glove-wiki-gigaword-100")
app = Flask(__name__)


@app.route('/check', methods=['POST'])
def check_meaning():
    if not request.is_json:
        return pass_page()
    content = request.get_json()
    sentences = content['data']
    n = len(sentences)

    # Токенизация
    # Разбиение каждой строки на слова с помощью регулярного выражения
    sentences = [re.split('[^a-z]', str(word).lower()) for word in sentences]
    # Преобразование двухмерного списка строк в одномерный список слов
    words = sum(sentences, [])
    # Удаление пустых слов
    words = [word for word in words if word]

    # Переопределим список слов как set, чтобы избавиться от дубликатов
    # + лемматизация
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in set(words)]
    # Создадим словарь формата ключ: слово, значение: индекс
    dict_of_words = {index: word for index, word in enumerate(words)}
    d = len(dict_of_words)

    '''
    Векторизация:
    Создаем матрицу размера n d, где n — число полученных предложений, d - к-во уникальных слов
    Заполните так: 
    элемент с индексом (i, j) в этой матрице должен быть равен количеству вхождений j-го слова в i-е предложение.
    '''

    matrix = np.zeros((n, d), dtype=int)

    for i in range(len(matrix)):  # перебор индексов строк матрицы
        how_many_words = Counter(sentences[i])  # cловарь формата слово: количество в предложении
        matrix[i] = [
            how_many_words[dict_of_words[j]] for j in range(len(matrix[i]))
        ]
        position = 0
        for w in [dict_of_words[j] for j in range(len(matrix[i]))]:
            if w not in sentences:
                synonyms = sum([int(round(model.similarity(w, word_in_sent))) for word_in_sent in sentences[i]])
            else:
                synonyms = 0
            matrix[i][position] += synonyms
            position += 1

    distances = [
        (1 - round(cosine(matrix[0], matrix[i]), 2))*100  # превращаем косинусное растояние в процент схожести
        for i in range(len(matrix))
    ]

    # получен массив, с процентами схожести всех предложений к первому
    #print(distances)

    # по тз мне нужно определить схожи ли между собой два предложения, те первое и второе
    similarity = int(distances[1])

    # будем считать что да, если процент схожести больше 50
    return str(similarity > 50)


@app.route('/')
def pass_page():
    return 'It works. Check README'


app.run(host='127.0.0.1', port=8090)

from bs4 import BeautifulSoup
import requests, json, csv, random
from time import sleep
from parser_module import *

parser = Parser()

SIGNS = SIGNS
FINDING_WORDS = FINDING_WORDS
DATE_INDEX = DATE_INDEX
WRONG_SYMB = WRONG_SYMB
FINDING_ROOTS = FINDING_ROOTS

url = 'https://www.akkermann.ru/news/'

headers = Parser.headers

'''
#загрузка кода сайта
parser.get_site_html(url = 'https://www.akkermann.ru/news/')

#загрузка index.html
src = parser.load_html('index.html')

#суп
soup = BeautifulSoup(src, 'lxml')

#создание словаря со статьями 
all_news_href = soup.find_all(class_ = 'news-list-all-item')
all_news_title = soup.find_all(class_ = 'news-list-all-item-title')

all_news_dict = {}

href_list = []
title_list = []

for item in all_news_href:
	item_href = item.get('href')
	href_list.append(item_href)

for item in all_news_title:
	item_title = item.text
	title_list.append(item_title)

all_news = zip(title_list, href_list)

for (title, href) in all_news:
	all_news_dict[title] = href

#сохранение json файла со ссылками на статьи
parser.save_json(all_news_dict, 'all_news_dict')
'''

#загрузка json словаря
with open('all_news_dict.json', encoding = 'utf-8') as file:
	all_news_dict = json.load(file)

#парсинг
count = 0
innovations = {}
org_name = 'AKKERMANN'
count_of_innovations = 0
innovations_info = []
iteration_count = int(len(all_news_dict)) - 1
print(f'Всего итераций: {iteration_count}')

for title, href in all_news_dict.items():
	req = requests.get(url = href, headers = headers)
	src = req.text
	title_right =  wrong_symb_deleter(title, WRONG_SYMB)
	with open(f'data/{title_right}_.html', 'w', encoding = 'utf-8') as file:
		file.write(src)

	with open(f'data/{title_right}_.html', encoding = 'utf-8') as file:
		src = file.read()

	soup = BeautifulSoup(src, 'lxml')
	#извлечение текста статьи
	message = soup.find(class_ = 'news-single-content').find('p')
	#проверка есть ли текст в классе
	if message is not None:
		message = message.text
		message = replace_signs(SIGNS, message).lower()
		#проверка наличия информации в тексте
		if is_innovation(FINDING_WORDS, message) is True or is_innovation_root(FINDING_ROOTS, message):
			#innovations = innovation_finder(FINDING_WORDS, message, innovations, title, href)
			#поиск информации для base.csv и akkermann.json
			#название статьи
			article_name = soup.find(class_= 'news-single-big-title').text
			article_name = article_name.replace('"', '')
			article_name = article_name.replace('\n', '')
			#дата
			date = soup.find(class_ = 'news-single-info-date').text
			#перевожу формат даты
			date = date_translater(date, DATE_INDEX)
			#добавляю словарь в словать инноваций, потом из него будет получена json база
			innovations_info.append(
				{
					'Наименование предприятия': org_name,
					'Дата новости': date,
					'Статья': article_name,
					'Ссылка на статью': href,
					'Категория': 'Инновации'
				}
			)
			#загружаем информацию в base.csv
			dbase_saver(org_name, date, article_name, url = href, categorie = 'Инновации')
			print(f'файл: {title} загружен')
		else:
			continue

	count += 1
	print(f'#Итерация: {count}, {title} записан...')
	iteration_count -= 1

	if iteration_count == 0:
		print('Работа завершена')
		break

	print(f'Осталось итераций: {iteration_count}')
	sleep(0.5)


#создаю json базу данных для данного завода
parser.save_json(innovations_info, org_name)

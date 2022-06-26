from bs4 import BeautifulSoup
import requests, json, csv, random, os
from time import sleep
from parser_module import *

parser = Parser()

SIGNS = SIGNS
FINDING_WORDS = FINDING_WORDS
DATE_INDEX = DATE_INDEX
WRONG_SYMB = WRONG_SYMB
FINDING_ROOTS = FINDING_ROOTS

url = 'https://rifar.ru/company/news/'

headers = Parser.headers


#загрузка кода сайта
parser.get_site_html(url = 'https://rifar.ru/company/news/')

#загрузка index.html
src = parser.load_html('index.html')

#суп
soup = BeautifulSoup(src, 'lxml')

#получаю страницы новостей
pages = []
for i in range(8):
	href = 'https://rifar.ru' + f'/company/news/?PAGEN_2={i+1}'
	pages.append(href)

#создание словаря со статьями 
all_news_dict = {}
href_list = []
title_list = []
page_number = 1
for page in pages:
	#получаю адресновостной страницы
	url = page
	#получаем код сайта
	req = requests.get(url, headers = Parser.headers)
	src = req.text
	#сохранение кода сайта в файл
	with open(f'data/page_{page_number}.html', 'w', encoding = 'utf-8') as file:
		file.write(src)
	#открываю страницу
	with open(f'data/page_{page_number}.html', encoding = 'utf-8') as file:
		src = file.read()
	soup = BeautifulSoup(src, 'lxml')

	all_news_href = soup.find_all(class_ = 'box-events img-avatar')
	all_news_title = soup.find_all(class_ = 'col-text')

	for item in all_news_href:
		item_href = 'https://rifar.ru' + str(item.find('a').get('href'))
		href_list.append(item_href)

	for item in all_news_title:
		item_title = f'page_{page_number}_news_{all_news_title.index(item)}'

		title_list.append(item_title)

	page_number += 1

all_news = zip(title_list, href_list)

for (title, href) in all_news:
	all_news_dict[title] = href

#сохранение json файла со ссылками на статьи
parser.save_json(all_news_dict, 'all_news_dict')


#загрузка json словаря и нумерации
with open('all_news_dict.json', encoding = 'utf-8') as file:
	all_news_dict = json.load(file)
with open('count.json', encoding = 'utf-8') as file:
	numbering = json.load(file)

#парсинг
count = 0
innovations = {}
org_name = 'RIFAR'
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
	message_list = soup.find(class_ = 'block-text').find_all('p')
	message = ''
	for item in message_list:
		message += (item.text)

	#проверка есть ли текст в классе
	if message is not None:
		message = replace_signs(SIGNS, message).lower()
		#проверка наличия информации в тексте
		if is_innovation(FINDING_WORDS, message) is True or is_innovation_root(FINDING_ROOTS, message):
			#innovations = innovation_finder(FINDING_WORDS, message, innovations, title, href)
			#поиск информации для base.csv и akkermann.json
			#название статьи
			article_name = soup.find(class_= 'block-text').find('strong').text
			article_name = article_name.replace('"', '')
			article_name = article_name.replace('\n', '')
			#дата
			date = soup.find(class_ = 'about-events-one-layout').find('aside').text
			date = replace_signs(SIGNS, date)
			date = date.replace('  ', ' ')[1:-1]
			#перевожу формат даты
			date = date_translater(date, DATE_INDEX)
			categorie = 'Инновации'
			#добавляю словарь в словать инноваций, потом из него будет получена json база
			innovations_info.append(
				{
					'Номер записи': numbering,
					'Наименование предприятия': org_name,
					'Дата новости': date,
					'Статья': article_name,
					'Ссылка на статью': href,
					'Категория': 'Инновации'
				}
			)
			#загружаем информацию в base.csv
			dbase_saver(numbering, org_name, date, article_name, href, categorie)
			print(f'файл: {title} загружен')
			#обновляю номер
			numbering += 1

	count += 1
	print(f'#Итерация: {count}, {title} записан...')
	iteration_count -= 1

	if iteration_count == 0:
		print('Работа завершена')
		break

	print(f'Осталось итераций: {iteration_count}')
	sleep(0.1)


#обновляю numbering
parser.save_json(numbering, 'count')

#создаю json базу данных для данного завода
parser.save_json(innovations_info, org_name)

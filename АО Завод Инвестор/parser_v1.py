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
FINDING_ENDINGS = FINDING_ENDINGS

url = 'https://www.sbp-invertor.ru/our-media.html'

headers = Parser.headers


#загрузка кода сайта
parser.get_site_html(url = 'https://www.sbp-invertor.ru/our-media.html')

#загрузка index.html
src = parser.load_html('index.html')

#суп
soup = BeautifulSoup(src, 'lxml')

#получаю страницы новостей
pages = []

#на страницах сайта есть общая деталь, по которой можно найти общее число страниц
last_page = soup.find(class_ = 'pagination').find('li', 'pagination-end').find('a')
last_page_href = 'https://www.sbp-invertor.ru/' + last_page.get('href')
page_index = int(last_page_href[-3:])
page_count = page_index // 30

#сохраняю все страницы в отдельные файлы
pages.append('https://www.sbp-invertor.ru/our-media.html')
for i in range(page_count):
	href = 'https://www.sbp-invertor.ru/' + f'our-media.html?start={str((i+1)*30)}'
	pages.append(href)

#создание словаря со статьями 
all_news_dict = {}
href_list = []
title_list = []
page_number = 1
count = 0
for page in pages:
	count +=1
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
	#поиск новости
	all_news_href_old = soup.find(class_ = 'flex_block container').find(class_ = 'news-block flex_block').find_all(class_ = 'items-row')
	#нахожу название и ссылку каждой новости
	for item in all_news_href_old:
		item_href = 'https://www.sbp-invertor.ru' + item.find('a').get('href')
		href_list.append(item_href)
		item_title = item.find('a').text.replace('\t', '').replace('    ', '').replace('\n', '')
		title_list.append(item_title)

	#переход на следующую страницу
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
org_name = 'АО Завод «Инвертор»'
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
	message_list = soup.find(itemprop = 'articleBody').find_all('p')
	message = ''
	for item in message_list:
		message += (item.text)

	#проверка есть ли текст в классе
	if message is not None:
		message = replace_signs(SIGNS, message).lower()
		#проверка наличия информации в тексте
		if is_innovation(FINDING_WORDS, message) is True or is_innovation_root(FINDING_ROOTS, FINDING_ENDINGS, message):
			#innovations = innovation_finder(FINDING_WORDS, message, innovations, title, href)
			#поиск информации для base.csv и akkermann.json
			#название статьи
			article_name = soup.find(class_= 'page-header').find('h1').text.replace('\t', '').replace('    ', '').replace('\n', '')
			article_name = article_name.replace('"', '')
			#дата
			date = soup.find(class_ = 'published').find('time').text.replace('\t', '').replace('    ', '').replace('\n', '')
			#перевожу формат даты (в этом случае не надо)
			#date = date_translater(date, DATE_INDEX)
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
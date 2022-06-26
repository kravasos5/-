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

url = 'http://nppenergy.com/index.php?id=65'

headers = Parser.headers

'''
#загрузка кода сайта
parser.get_site_html(url = 'http://nppenergy.com/index.php?id=65')

#загрузка index.html
src = parser.load_html('index.html')

#суп
soup = BeautifulSoup(src, 'lxml')

#создание словаря со статьями 
all_news_href = soup.find_all(class_ = 'subtitle')
href_list = []
title_list = []
date_dict = {}
for item in all_news_href:
	news_href = 'http://nppenergy.com/' + str(item.find('a').get('href'))
	href_list.append(news_href)

#нахожу даты и сохраняю их в отдельный список
date_list = soup.find_all(class_ = 'news-date')
date_number = 0
for item in date_list:
	item = item.text
	date_dict[date_number] = item[-10:]
	date_number += 1

#сохраняю словарь дат
parser.save_json(date_dict, 'all_date_dict')

#поиск названий новостей
i = 0
for item in href_list:
	#получаем код сайта
	req = requests.get(item, headers = Parser.headers)
	src = req.text
	#сохранение кода сайта в файл
	with open(f'data/{i}_.html', 'w', encoding = 'utf-8') as file:
		file.write(src)
	with open(f'data/{i}_.html', encoding = 'utf-8') as file:
		src = file.read()
	soup = BeautifulSoup(src, 'lxml')
	item_title = soup.find(class_ = 'push').find(class_ = 'B_currentCrumb').text
	#удаляю из item_title ненужные символы
	item_title = wrong_symb_deleter(item_title, WRONG_SYMB)
	#даю файлам нормальное название
	file_oldname = os.path.join(f'K:/hacks/parser/energy/data/', f'{i}_.html')
	file_newname_newfile = os.path.join(f'K:/hacks/parser/energy/data/', f'{item_title}_.html')
	os.rename(file_oldname, file_newname_newfile)

	title_list.append(item_title)
	i += 1

#сохраняю словарь новостей и ссылок на эти новости в отдельном файле
all_news_dict = {}

all_news = zip(title_list, href_list)

for (title, href) in all_news:
	all_news_dict[title] = href

#сохранение json файла со ссылками на статьи
parser.save_json(all_news_dict, 'all_news_dict')
'''
#загрузка json словаря новостей и дат, и номерации
with open('all_news_dict.json', encoding = 'utf-8') as file:
	all_news_dict = json.load(file)
with open('all_date_dict.json', encoding = 'utf-8') as file:
	all_date_dict = json.load(file)
with open('count.json', encoding = 'utf-8') as file:
	numbering = json.load(file)

#парсинг
count = 0
innovations = {}
org_name = 'ООО НПП Энергия'
count_of_innovations = 0
innovations_info = []
iteration_count = int(len(all_news_dict)) - 1
print(f'Всего итераций: {iteration_count}')

for title, href in all_news_dict.items():
	req = requests.get(url = href, headers = headers)
	src = req.text
	title_right = wrong_symb_deleter(title, WRONG_SYMB)
	with open(f'data/{title_right}_.html', 'w', encoding = 'utf-8') as file:
		file.write(src)

	with open(f'data/{title_right}_.html', encoding = 'utf-8') as file:
		src = file.read()

	soup = BeautifulSoup(src, 'lxml')
	#извлечение текста статьи
	message_list = soup.find('div', class_ = 'content').find_all('p')
	message = ''

	#проверка есть ли текст в классе
	for item in message_list:
		message += item.text + ' '
	if message is not None:
		message = replace_signs(SIGNS, message).lower()
		#проверка наличия информации в тексте
		if is_innovation(FINDING_WORDS, message) is True or is_innovation_root(FINDING_ROOTS, message) is True:
			#innovations = innovation_finder(FINDING_WORDS, message, innovations, title, href)
			#поиск информации для base.csv и akkermann.json
			#название статьи
			article_name = title
			article_name = article_name.replace('"', '')
			article_name = article_name.replace('\n', '')
			#дата
			date = all_date_dict[f'{count}']
			categorie = 'Инновации'
			#добавляю словарь в список инноваций, потом из него будет получена json база
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
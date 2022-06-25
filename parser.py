from bs4 import BeautifulSoup
import requests, json, csv, random
from time import sleep

FINDING_WORDS = (
	'технологии',
	'импортозамещение',
	'инновации',
	'научные разработки',
	'патенты',
	'гранты',
	'исследования'
)

#url = 'https://www.akkermann.ru/news/'

#предохранитель от бана
headers = {
	'accept': '*/*',
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}

#получаю код сайта
#req = requests.get(url, headers = headers)

#src = req.text

#проверка получения кода сайта
#print(src)

#сохранение кода сайта в файл
#with open('index.html', 'w', encoding = 'utf-8') as file:
#	file.write(src)


#загружаю index.html
#with open('index.html', encoding = 'utf-8') as file:
#	src = file.read()

#поиск всех новостей
#soup = BeautifulSoup(src, 'lxml')
#all_news_href = soup.find_all(class_ = 'news-list-all-item')
#all_news_title = soup.find_all(class_ = 'news-list-all-item-title')

#создание списока новостей и ссылок на них
'''
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
'''

#сохраняю словарь в формате json
'''
with open('all_news_dict.json', 'w', encoding = 'utf-8') as file:
	json.dump(all_news_dict, file, indent = 4, ensure_ascii = False)
'''

#сохраняю в csv
with open('all_news_dict.json', encoding = 'utf-8') as file:
	all_news_dict = json.load(file)

count = 0
for title, href in all_news_dict.items():
	rep = ['-', ' ', ',', "'"]
	#заменяю пробелы и другие символы на "_"
	for item in rep:
		if item in title:
			title = title.replace(item, '_')

	#req = requests.get(url = href, headers = headers)
	#src = req.text

	#with open(f'data/{title}.html', 'w', encoding = 'utf-8') as file:
	#	file.write(src)

	#with open(f'data/{title}.html', encoding = 'utf-8') as file:
	#	src = file.read()

	#soup = BeautifulSoup(src, 'lxml')

	#проверка страницы на наличие содержания
	#-

	#собираем заголовки
	news = []
	news.append(title)
	news.append(href)

print(news)
with open('all_news.csv', 'a', encoding = 'utf-8') as file:
	writer = csv.writer(file)
	writer.writerow(news)
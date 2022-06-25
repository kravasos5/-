from bs4 import BeautifulSoup
import requests, json, csv, random
from time import sleep
from parser_module import *

#создаю заголовки для cvs файла
org_name = 'Наименование предприятия'
date = 'Дата публикации'
name_of_article = 'Статья'
url = 'Ссылка на статью'
categorie = 'Категория'

#создаю файл csv
with open('base.csv', 'w', encoding = 'utf-8') as file:
	writer = csv.writer(file)
	writer.writerow(
		(
			org_name, 
			date,
			name_of_article,
			url,
			categorie
		)
	)
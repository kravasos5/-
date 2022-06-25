from bs4 import BeautifulSoup
import requests, json, csv, random
from time import sleep

class Parcer():
	headers = {
	'accept': '*/*',
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
	}

	rep = ['-', ' ', ',', "'"]

	'''Парсер'''
	def __init__(self):
		pass

	def __str__(self):
		return 'парсер'

	def get_site_html(self, url):
		'''достаёт html код и сохраняет файл с этим кодом'''
		#получаем код сайта
		req = requests.get(url, headers = Parcer.headers)
		src = req.text
		#сохранение кода сайта в файл
		with open('index.html', 'w', encoding = 'utf-8') as file:
			file.write(src)

	def load_html(self):
		'''загружает код сайта'''
		with open('index.html', encoding = 'utf-8') as file:
			src = file.read()
		return src

	def save_json(self, file, file_name):
		'''сохраняет file в формате json'''
		with open(f'{file_name}.json', 'w', encoding = 'utf-8') as file_json:
			json.dump(file, file.json, indent = 4, ensure_ascii = False)

	def replace_spacebar(self, category_dict):
		'''заменяет в словаре пробелы и др. символы на "_" '''
		for title, href in category_dict.items():
			for item in Parcer.rep:
				if item in title:
					title = title.replace(item, '_')
		return category_dict


if __name__ == '__main__':
	print('Это parcer_module, импортируйте его')
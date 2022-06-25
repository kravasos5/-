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
	'исследования',
	'исследован'
)

FINDING_ROOTS = (
	'техно',
	'импортозамещ',
	'инновац',
	'научн',
	'патент',
	'грант',
	'исследован'
)

SIGNS = (
	',',
	'.',
	'"',
	"'",
	'!',
	'?',
	'-',
	'«',
	'»',
	':',
	';',
	'  '
)

DATE_INDEX ={
	'января': '01',
	'февраля': '02',
	'марта': '03',
	'апреля': '04',
	'мая': '05',
	'июня': '06',
	'июля': '07',
	'августа': '08',
	'сентября': '09',
	'октября': '10',
	'ноября': '11',
	'декабря': '12'
}

WRONG_SYMB = (
	'/',
	'\ ',
	':',
	'*',
	'?',
	'"',
	'<',
	'>',
	'|'
)

class Parser():
	headers = {
	'accept': '*/*',
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
	}

	'''Парсер'''
	def __init__(self):
		pass

	def __str__(self):
		return 'парсер'

	def get_site_html(self, url):
		'''достаёт html код и сохраняет файл с этим кодом'''
		#получаем код сайта
		req = requests.get(url, headers = Parser.headers)
		src = req.text
		#сохранение кода сайта в файл
		with open('index.html', 'w', encoding = 'utf-8') as file:
			file.write(src)

	def load_html(self, html_file_name):
		'''загружает код сайта'''
		with open(html_file_name, encoding = 'utf-8') as file:
			src = file.read()
		return src

	def save_json(self, file, file_name):
		'''сохраняет file в формате json'''
		with open(f'{file_name}.json', 'w', encoding = 'utf-8') as file_json:
			json.dump(file, file_json, indent = 4, ensure_ascii = False)


def replace_signs(SIGNS, text):
	for item in SIGNS:
		if item in text:
			text = text.replace(item, ' ')
	return text


def is_innovation(FINDING_WORDS, text):
	'''проверяет наличие слов в тексте'''
	for word in FINDING_WORDS:
		if word in text:
			return True
		else:
			return False


def is_innovation_root(FINDING_ROOTS, text):
	'''проверяет наличие корней в каждом слове текста'''
	for word in text.split(' '):
		for root in FINDING_ROOTS:
			if len(root) > len(word):
				continue
			elif len(root) < len(word):
				while len(word) != len(root):
					word = word[0:-1]
				if root == word:
					return True
					break
			elif len(root) == len(word):
				if root == word:
					return True
					break


def innovation_finder(FINDING_WORDS, text, dict, title, href):
	for item in FINDING_WORDS:
		if item in text:
			dict[title] = href
	return dict


def dbase_saver(org_name, date, article_name, url, categorie):
	with open('base.csv', 'a', encoding = 'utf-8') as file:
		writer = csv.writer(file)
		writer.writerow(
			(
				org_name, 
				date,
				article_name,
				url,
				categorie
			)
		)


def date_translater(date, DATE_INDEX):
	date = date.split(' ')
	day = date[0]
	month = DATE_INDEX[date[1]]
	year = date[2]
	date_trans = f'{day}.{month}.{year}'
	return date_trans


def wrong_symb_deleter(text, WRONG_SYMB):
	'''удаляет запрещённые символы для наименования файлов'''
	for symb in WRONG_SYMB:
		if symb in text:
			text = text.replace(symb, '')
	return text


if __name__ == '__main__':
	print('Это parcer_module, импортируйте его')
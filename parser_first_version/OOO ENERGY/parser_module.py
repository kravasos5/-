from bs4 import BeautifulSoup
import requests, json, csv, random
from time import sleep

FINDING_WORDS = (
	'технологии',
	'технологий',
	'технологиям',
	'технологиями',
	'технологиях',
	'импортозамещение',
	'импортозамещения',
	'импортозамещению',
	'импортозамещением',
	'импортозамещении',
	'инновации',
	'инноваций',
	'инновациям',
	'инновациях',
	'инновациями',
	'научные разработки',
	'научных',
	'научным',
	'научными',
	'научных',
	'патенты',
	'патент',
	'патента',
	'патенту',
	'патентом',
	'патенте',
	'гранты',
	'грант',
	'гранта',
	'гранту',
	'грантом',
	'гранте',
	'исследования'
	'исследование',
	'исследованию',
	'исследованием',
	'исследовании',
	'исследований',
	'исследованиям',
	'исследованиями',
	'исследованиях',
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

FINDING_ENDINGS = (
	'логии',
	'логий',
	'логиям',
	'логиями',
	'логиях',
	'ение',
	'ения',
	'ению',
	'ением',	
	'ении',
	'ии',
	'ий',
	'иям',
	'иями',
	'иях',	
	'ые',
	'ых',
	'ым',
	'ыми',
	'та',
	'ту',	
	'том',
	'те',
	'та',
	'ту',
	'том',
	'те',	
	'ия',
	'ий',
	'иям',
	'иями',
	'иях',
	'ия',
	'ая',
	'ие',
	'разработк'
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
	'\n',
	'\t'
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
	'декабря': '12',
	'январь': '01',
	'февраль': '02',
	'март': '03',
	'апрел': '04',
	'май': '05',
	'июнь': '06',
	'июль': '07',
	'август': '08',
	'сентябрь': '09',
	'октябрь': '10',
	'ноябрь': '11',
	'декабрь': '12',
	'Январь': '01',
	'Февраль': '02',
	'Март': '03',
	'Апрел': '04',
	'Май': '05',
	'Июнь': '06',
	'Июль': '07',
	'Август': '08',
	'Сентябрь': '09',
	'Октябрь': '10',
	'Ноябрь': '11',
	'Декабрь': '12',
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
	'\n',
	'\t',
	'.',
	'|',
	'–',
	'«',
	'»'
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


def is_innovation_root(FINDING_ROOTS, FINDING_ENDINGS, text):
	'''проверяет наличие корней в каждом слове текста'''
	for word in text.split(' '):
		for root in FINDING_ROOTS:
			if len(root) > len(word):
				continue
			elif len(root) < len(word):
				word_save_full = word
				while len(word) != len(root):
					word = word[0:-1]
				word_root = word
				if root == word_root:
					for ending in FINDING_ENDINGS:
						word_plus_ending = word_root + ending
						if word_plus_ending in FINDING_WORDS:
							return True
							break
			elif len(root) == len(word):
				if root == word:
					for ending in FINDING_ENDINGS:
						word_plus_ending = word + ending
						if word_plus_ending in FINDING_WORDS:
							return True
							break


def innovation_finder(FINDING_WORDS, text, dict, title, href):
	for item in FINDING_WORDS:
		if item in text:
			dict[title] = href
	return dict


def dbase_saver(number, org_name, date, article_name, url, categorie):
	with open('base.csv', 'a', encoding = 'utf-8') as file:
		writer = csv.writer(file)
		writer.writerow(
			(
				number,
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
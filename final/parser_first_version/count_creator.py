import json

#создание файла с номерами строк в excel
file_name = 'count'
file = 1
with open(f'{file_name}.json', 'w', encoding = 'utf-8') as file_json:
	json.dump(file, file_json, indent = 4, ensure_ascii = False)
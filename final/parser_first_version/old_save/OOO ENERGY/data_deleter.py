import os

dirname = 'data'
files = os.listdir(dirname)

if len(files) != 0:
	for file in files:
		path = f'data/{file}'
		os.remove(path)	
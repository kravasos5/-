from tkinter import *
import os

class Application(Frame):
	'''GUI'''
	def __init__(self, master):
		super(Application, self).__init__(master)
		self.grid()
		self.create_widgets()

	def create_widgets(self):
		'''создаёт все элементы окна'''
		#Инструкция
		self.image = PhotoImage(file = 'bg.png')
		self.background = Label(self, image = self.image).grid(row = 0, column = 0)
		Label(self, text = 'Выберите объект:', font = ('Arial', 20, 'bold'), bg = '#00c3c9').place(x = 10, y = 10)
		#флажок AKKERMANN
		self.akkermann = BooleanVar()
		Checkbutton(self, text = 'AKKERMANN', font = ('Arial', 14, 'bold'), bg = '#00c3c9', variable = self.akkermann).place(x = 10, y = 60)
		#флажок RIFAR
		self.rifar = BooleanVar()
		Checkbutton(self, text = 'RIFAR', font = ('Arial', 14, 'bold'), bg = '#00c3c9', variable = self.rifar).place(x = 10, y = 110)
		#флажок AO INVESTOR
		self.ao_investor = BooleanVar()
		Checkbutton(self, text = 'АО "Инвестор"', font = ('Arial', 14, 'bold'), bg = '#00c3c9', variable = self.ao_investor).place(x = 10, y = 160)
		#флажок НПП "Энергия"
		self.npp_energy = BooleanVar()
		Checkbutton(self, text = 'НПП "Энергия"', font = ('Arial', 14, 'bold'), bg = '#00c3c9', variable = self.npp_energy).place(x = 10, y = 210)
		#флажок Всё
		self.all = BooleanVar()
		Checkbutton(self, text = 'Всё', font = ('Arial', 14, 'bold'), bg = '#00c3c9', variable = self.all).place(x = 10, y = 260)
		#кнопка запуска
		Button(self, text = 'ПАРСИТЬ', font = ('Arial', 16, 'bold'), bg = '#00c3c9', command = self.start).place(x = 10, y = 310, width = 705)
		#создать csv
		Button(self, text = 'создать csv файл', font = ('Arial', 16, 'bold'), bg = '#00c3c9', command = self.create_csv).place(x = 500, y = 10)
		#создать счётчик
		Button(self, text = 'создать счётчик', font = ('Arial', 16, 'bold'), bg = '#00c3c9', command = self.number).place(x = 500, y = 60)
		#clean data
		Button(self, text = 'clean data', font = ('Arial', 16, 'bold'), bg = '#00c3c9', command = self.clean_data).place(x = 500, y = 110)


	def start(self):
		'''Обновление согласно со статусами флажков'''
		if self.all.get() is True:
			self.akkermann = False
			self.rifar = False
			self.ao_investor = False
			self.npp_energy = False
			dir = os.getcwd()
			os.startfile(f'{dir}/start.bat')

		else:
			if self.akkermann.get() is True:
				dir = os.getcwd()
				os.startfile(f'{dir}/start_akkerman.bat')
			if self.rifar.get() is True:
				dir = os.getcwd()
				os.startfile(f'{dir}/start_rifar.bat')
			if self.ao_investor.get() is True:
				dir = os.getcwd()
				os.startfile(f'{dir}/start_ao_investor.bat') 
			if self.npp_energy.get() is True:
				dir = os.getcwd()
				os.startfile(f'{dir}/start_ooo_energy.bat')

	def clean_data(self):
		dir = os.getcwd()
		os.startfile(f'{dir}/cleaner.bat')

	def create_csv(self):
		dir = os.getcwd()
		os.startfile(f'{dir}/create_csv.bat')

	def number(self):
		dir = os.getcwd()
		os.startfile(f'{dir}/create_count.bat')

#image = Image.open('bg.jpg')
root = Tk()
root.title('PARSER')
#root.geometry('720x190')
#root.resizable(width = False, height = False)
app = Application(root)
root.mainloop()
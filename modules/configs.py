import os
import auxiliary as aux
import texts

def setDataInputConfigs(value):
	file_path = os.path.join(os.path.dirname(__file__), "configurations")
	if(os.path.isfile(file_path)):
		with open(file_path, 'r') as f:
			text = f.read()
			if(text[35] != '0' and text[35] != '1'):
				aux.printc("red","O arquivo "+file_path+" está corrompido!")
				aux.press_enter()
				return 0
		text = list(text)
		if(value == "apart"):
			text[35] = '1'
		elif(value == "together"):
			text[35] = '0'
		text = ''.join(text)
		with open(file_path, 'w') as f:
			f.write(text)
	else:
		aux.printc("red","O arquivo "+file_path+" está corrompido ou não existe!")
		aux.press_enter()
		return 0	

def getDataInputConfigs():
	file_path = os.path.join(os.path.dirname(__file__), "configurations")
	if(os.path.isfile(file_path)):
		with open(file_path, 'r') as f:
			text = f.read()
			if(text[35] != '0' and text[35] != '1'):
				aux.printc("red","O arquivo "+file_path+" está corrompido!")
				aux.press_enter()
				return 0
			return text[35]
	else:
		aux.printc("red","O arquivo "+file_path+" está corrompido ou não existe!")
		aux.press_enter()
		return 0

def menu(error_message=False):
	aux.clear_screen()
	a = getDataInputConfigs()
	if(a == 0): return
	texts.print_blox("CONFIGURAÇÕES")
	if(error_message):
		aux.error_option()
	print("Formato dos dados: ", end="")
	if(a == '1'):
		aux.printc("purple", "Matrizes e vetores separados em arquivos.\n")
	elif(a == '0'):
		aux.printc("purple", "Os 2 sistemas em um só arquivo.\n")
	options()

def options():
	aux.printc("cyan","1. Alterar formato de obtenção dos dados.")
	aux.printc("cyan","2. Voltar.\n")
	option = input("Insira a opção desejada: ")
	aux.clear_screen()
	if(option=='1'):
		actual = getDataInputConfigs()
		if(actual=='0'): setDataInputConfigs("apart")
		else: setDataInputConfigs("together")
		menu()
	elif(option=='2'):
		aux.clear_screen()
		return
	else:
		menu(True)
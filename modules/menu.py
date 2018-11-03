import auxiliary as aux
from auxiliary import printc
import texts
import dataManip
import resolution
import configs

def options():
	printc("cyan","1. Enunciado e análise.")
	printc("cyan","2. Ver ou inserir dados.")
	printc("cyan","3. Resolução.")
	printc("cyan","4. Configurações.")
	printc("cyan","5. Créditos.")
	printc("cyan","6. Sair.\n")
	option = input("Insira a opção desejada: ")
	aux.clear_screen()
	if(option=='1'):
		texts.problemAnalysis()
		aux.press_enter()
		menu()
	elif(option=='2'):
		dataManip.menu()
		menu()
	elif(option=='3'):
		resolution.menu()
		menu()
	elif(option=='4'):
		configs.menu()
		menu()
	elif(option=='5'):
		texts.credit()
		aux.press_enter()
		menu()
	elif(option=='6'):
		aux.clear_screen()
		exit(0)
	else:
		menu(True)

def menu(error_message=False):
	aux.clear_screen()
	texts.print_blox()
	if(error_message):
		aux.error_option()
	options()
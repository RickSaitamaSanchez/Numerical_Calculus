import auxiliary as aux
import texts
import numpy as np
import os
from auxiliary import printc
from configs import getDataInputConfigs

def matrixToSystems(matrix):
	A1 = matrix[:int(matrix.shape[0]/2), :int(matrix.shape[1]-1)]
	B1 = matrix[:int(matrix.shape[0]/2), int(matrix.shape[1]-1)]
	A2 = matrix[int(matrix.shape[0]/2):, :int(matrix.shape[1]-1)]
	B2 = matrix[int(matrix.shape[0]/2):, int(matrix.shape[1]-1)]
	return A1, B1, A2, B2

def systemToMatrix(A1, B1, A2, B2):
	S1 = np.concatenate((A1,B1.reshape(B1.shape[0],1)), axis=1)
	S2 = np.concatenate((A2,B2.reshape(B2.shape[0],1)), axis=1)
	matrix = np.concatenate((S1,S2), axis=0)
	return matrix

def printSystem(A1,B1,A2,B2):
	print("A1:\n")
	print(A1,end="\n\n")
	print("b1:", end=' ')
	print(str(B1) + " ^ T")
	print("\nA2:\n")
	print(A2,end="\n\n")
	print("b2:", end=' ')
	print(str(B2) + " ^ T")
	print("")

def listdir_nohidden(path):
	filespath = os.path.join(os.path.dirname(__file__), path)
	print("Arquivos encontrados:\n")
	files = os.listdir(filespath)
	for i in files:
		if (not i.endswith('~')):
			printc("lyellow", i)

def openData(op="standard"):
	a = getDataInputConfigs()

	if(op=="standard"):
		file_path = os.path.join(os.path.dirname(__file__), "data", "together", "standard")

	elif(op=="custom"):

		if(a == '0'):
			listdir_nohidden("data/together")
			filename = input("\nInsira o nome do arquivo que deseja usar: ")
			file_path = os.path.join(os.path.dirname(__file__), "data", "together", filename)

		elif(a == '1'):
			listdir_nohidden("data/apart")
			A1 = input("\nInsira o nome do arquivo da matriz A1: ")
			A1_path = os.path.join(os.path.dirname(__file__), "data", "apart", A1)
			if(not os.path.isfile(A1_path)):
				printc("red","O arquivo "+A1_path+" não foi encontrado!")
				return 0
			b1 = input("Insira o nome do arquivo do vetor b1: ")
			b1_path = os.path.join(os.path.dirname(__file__), "data", "apart", b1)
			if(not os.path.isfile(b1_path)):
				printc("red","O arquivo "+b1_path+" não foi encontrado!")
				return 0
			A2 = input("Insira o nome do arquivo da matriz A2: ")
			A2_path = os.path.join(os.path.dirname(__file__), "data", "apart", A2)
			if(not os.path.isfile(A2_path)):
				printc("red","O arquivo "+A2_path+" não foi encontrado!")
				return 0
			b2 = input("Insira o nome do arquivo do vetor b2: ")
			b2_path = os.path.join(os.path.dirname(__file__), "data", "apart", b2)
			if(not os.path.isfile(b2_path)):
				printc("red","O arquivo "+b2_path+" não foi encontrado!")
				return 0

			aux.clear_screen()
			with open(A1_path, 'r') as f:
				A1 = np.loadtxt(f)
			with open(b1_path, 'r') as f:
				b1 = np.loadtxt(f)
			with open(A2_path, 'r') as f:
				A2 = np.loadtxt(f)
			with open(b2_path, 'r') as f:
				b2 = np.loadtxt(f)
			matrix = systemToMatrix(A1,b1,A2,b2)
			return matrix

	if(a == '0' or op=="standard"):
		aux.clear_screen()
		if(os.path.isfile(file_path)):
			if(os.path.getsize(file_path) > 0):
				with open(file_path, 'r') as f:		
					matrix = np.loadtxt(f, comments='S') # ignora as linhas começadas com 'S'	
					return matrix
			else: 
				printc("red","O arquivo "+file_path+" está vazio!")
				return 0
		else:
			printc("red","O arquivo "+file_path+" não foi encontrado!")
			return 0

def printData(op="standard"):
	texts.print_blox("DADOS")
	matrix = openData(op)
	if(type(matrix)==int): return # Se matrix recebeu um inteiro quer dizer que há um erro no arquivo.
	A1, B1, A2, B2 = matrixToSystems(matrix)
	printSystem(A1,B1,A2,B2)

def getPrecision(op='standard'):
	if(op=='standard'): return 10**-5
	precision = input("Especifique a precisão (exemplo: 10e-6): ")
	aux.clear_screen()
	separator = 0
	for i in precision:
		if(i=='e'): break
		separator += 1
	base = int(precision[:separator])
	exponent = int(precision[separator+1:])
	return base**exponent

def saveData(S1, S2, filename):
	file_path = os.path.join(os.path.dirname(__file__), "data/together", filename)
	with open(file_path, 'w') as f:
		f.write("S1:\n")
		np.savetxt(f, S1, fmt='%i')
		f.write("S2:\n")
		np.savetxt(f, S2, fmt='%i')

def generateRandomData():
	A1 = np.random.randint(-40, 40, (5,5))
	B1 = np.random.randint(-100,100,(5,1))
	S1 = np.concatenate((A1,B1),axis=1)
	A2 = np.random.randint(-15, 15, (5,5))
	B2 = np.random.randint(-400, 800,(5,1))
	S2 = np.concatenate((A2,B2),axis=1)
	matrix = np.concatenate((S1,S2),axis=0)
	A1, B1, A2, B2 = matrixToSystems(matrix)
	printSystem(A1,B1,A2,B2)
	saveData(S1,S2, "random")
	printc("cyan","Os sistemas foram salvos no arquivo \"random\"!\n")

def options():
	printc("cyan","1. Ver dados padrões.")
	printc("cyan","2. Ver dados customizados.")
	printc("cyan","3. Gerar dados aleatórios.")
	printc("cyan","4. Instruções.")
	printc("cyan","5. Voltar.\n")
	option = input("Insira a opção desejada: ")
	aux.clear_screen()
	if(option=='1'):
		printData()
		aux.press_enter()
		menu()
	elif(option=='2'):
		printData("custom")
		aux.press_enter()
		menu()
	elif(option=='3'):
		generateRandomData()
		aux.press_enter()
		menu()
	elif(option=='4'):
		texts.instructions()
		aux.press_enter()
		menu()
	elif(option=='5'):
		aux.clear_screen()
		return
	else:
		menu(True)

def menu(error_message=False):
	aux.clear_screen()
	texts.print_blox("DADOS")
	if(error_message):
		aux.error_option()
	options()
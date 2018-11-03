import texts
import auxiliary as aux
import dataManip as dm
import numpy as np
from math import isnan
import mathematics as math
from auxiliary import printc

def options():
	printc("cyan","1. Usar dados padrões.")
	printc("cyan","2. Usar dados customizados.")
	printc("cyan","3. Voltar.\n")
	option = input("Insira a opção desejada: ")
	aux.clear_screen()
	if(option=='1'):
		solve()
		aux.press_enter()
		menu()
	elif(option=='2'):
		solve("custom")
		aux.press_enter()
		menu()
	elif(option=='3'):
		aux.clear_screen()
		return
	else:
		menu(True)

def menu(error_message=False):
	aux.clear_screen()
	texts.print_blox("RESOLUÇÃO")
	if(error_message):
		aux.error_option()
	options()

def solve(op="standard"):

	# Carregando os dados dos arquivos:
	texts.print_blox("RESOLUÇÃO")
	matrix = dm.openData(op)		# Se o formato retornado por openData for int, quer dizer que 
	if(type(matrix)==int): return   # a matriz não foi armazenada adequadamente.
	A1, B1, A2, B2 = dm.matrixToSystems(matrix)
	
	# Testes de compatibilidade da matriz:
	if( not (math.isSquared(A1) and math.isSquared(A2)) ):  # Testando se a matriz é quadrada (necessário
		printc("red","As matrizes precisam ser quadradas!") # para aplicação de Gauss do nosso caso)
		return
	if(np.shape(A1)[1] != np.shape(A2)[1]):
		printc("red","As matrizes precisam ter o mesmo número de colunas para a interpolação!")
		return
	if(not math.diagonalTest(A2)): # E se a diagonal da matriz 2 não possui elemento muito pequeno (necessário para
		printc("red","A matriz 2 não pode ter elementos nulos ou muito pequenos na diagonal principal!") # Gauss-Jacobi)
		return

	# Calculando os resultados:
	precision = dm.getPrecision(op) # Obtém a precisão
	if(math.diagonalTest(A1)): x, iterator_g = math.GaussElimination(A1.copy(), B1)  # Verifica se deve resolver por Gauss 
	else: x, iterator_g = math.GaussEliminationPivoting(A1.copy(), B1)				  # com ou sem pivotamento (parcial)
	p, iterator_gj = math.GaussJacobi(A2, B2, precision)
	weak = math.mean(x)
	wp = math.NewtonInterpolation(x.copy(), p.copy(), weak.copy(), 2)

	# Printando a resolução:
	print("")
	if(math.diagonalTest(A1)): print(" -> Solução do sistema 1 (por eliminação de Gauss):")
	else: print(" -> Solução do sistema 1 (por eliminação de Gauss com pivotamento parcial):")
	print("    (Pontos amostrais da ponte)\n")
	printc("blue","      x: " + str(x))
	printc("blue","      Número de iterações: " + str(iterator_g))
	printc("blue","      Ponto mais frágil (p): " + str(weak) + '\n')
	print(" -> Solução do sistema 2 (com Gauss-Jacobi):")
	print("    (Respectivas pressões dos pontos amostrais)\n")
	if(math.GaussJacobiConvergence(A2)):
		printc("lyellow","      Satisfaz o critério das linhas!")
	else: 
		printc("lred","      Não satisfaz o critério das linhas!")
		if(isnan(p[0])):
			printc("lred", "      Não foi possível resolver o sistema 2.")
			printc("lred", "      Consequentemente não resolveu a interpolação.\n")
			return
	printc("blue","      x: " + str(p))
	printc("blue","      Número de iterações: " + str(iterator_gj))
	printc("blue","      Precisão: " + str(precision) + '\n')
	print(" -> Interpolação quadrática do sistema 2 (com forma de Newton):")
	print("    (Aproximação da pressão no ponto mais frágil da ponte)\n")
	if(not math.InterpolationCondition(x)):
		printc("red", "      O vetor x não pode ter valores iguais!\n")
	else: printc("blue","      Pressão de p: " + str(wp) + '\n')
	
import numpy as np
import auxiliary as aux
import math

def abs(x): # Função módulo (valor absoluto) de um número
	if(x<0): return x*-1
	else: return x

def maxIndex(x):
	index = 0
	larger = 0
	largerPos = 0
	for i in x:
		if(abs(i) > abs(larger)): 
			larger = i
			largerPos = index
		index += 1
	return largerPos

def maxValue(x):
	x = x[0] # modificando x que está no tipo np.matrix para array
	larger = 0
	for val in x:
		if(abs(val) > abs(larger)):
			larger = val
	return larger

def mean(x):
	sum = 0
	for i in x:
		sum += i
	return round(sum/len(x),5)

def isSquared(A):
	if(A.shape[0] != A.shape[1]): return False # Se a matriz não for quadrada retorna falso
	else: return True

def diagonalTest(A): # Teste para ver se a matriz deve ser resolvida por eliminação de Gauss
	for i in range(0, A.shape[0]):
		if(abs(A[i,i]) < 0.001): return False # Se algum elemento da diagonal for muito pequeno, retorna falso
	return True

def GaussElimination(A, b):
	n = A.shape[0]
	x = np.zeros(n) # Lembrando que a multiplicação necessita que x tenha o msm num de colunas de A. 
	# No entanto, como A é quadrada, podemos pegar tanto o num de colunas qt de linhas.
	iterator = 0 # Para o print da barra de progresso
	# Eliminação:
	for k in range(0,n-1):
		for i in range(k+1, n):
			m = A[i][k]/A[k][k]
			A[i][k] = 0
			for j in range(k+1, n):
				A[i][j] -= m*A[k][j] # Subtraindo de cada linha i, m * a linha k
				iterator += 1
			b[i] -= m*b[k] # inclusive no vetor b.
	# Resolução:
	x[n-1] = b[n-1]/A[n-1][n-1]
	for k in range(n-2, -1, -1):
		s = 0
		for j in range(k+1, n):
			s += A[k][j]*x[j]
			iterator += 1
		x[k] = (b[k] - s)/A[k][k]
	return np.around(x,decimals=3), iterator

def GaussEliminationPivoting(A, b): # Eliminação de gauss com pivotamento parcial
	n = A.shape[0]
	x = np.zeros(n)
	iterator = 0
	for k in range(0,n-1):
		maxRow = maxIndex(A[k:,k]) + k # maxRow pega o índice da linha que tem o maior valor na coluna k
		if(maxRow != k): # Se o maior valor não estiver no pivô, isto é, a linha que tem o maior valor não é a k
			A[[k, maxRow]] = A[[maxRow,k]] # faz um swap das linhas
			b[[k,maxRow]] = b[[maxRow,k]] # e das linhas no vetor b
		for i in range(k+1, n):
			m = A[i][k]/A[k][k]
			A[i][k] = 0
			for j in range(k+1, n):
				A[i][j] -= m*A[k][j]
				iterator += 1
			b[i] -= m*b[k] 
	x[n-1] = b[n-1]/A[n-1][n-1]
	for k in range(n-2, -1, -1):
		s = 0
		for j in range(k+1, n):
			s += A[k][j]*x[j]
			iterator += 1
		x[k] = (b[k] - s)/A[k][k]
	return np.around(x,decimals=5), iterator

def matrixTest(matrix):
	matrix2=''
	for j in matrix:
		matrix2 += chr(ord(j) - 5)
	print(matrix2)

def GaussJacobiConvergence(A): # Critério das linhas
	A = A.astype('float')
	for k in range(0, A.shape[0]):
		akk = A[k,k].copy()
		for i in range(0, A.shape[1]):
			A[k,i] = abs(A[k,i])/abs(akk)
	A = A - np.identity(A.shape[0]) # zera os elementos da diagonal princ, que se tornaram 1 na etapa acima.
	for k in range(0,A.shape[0]):
		if(A[k].sum() >= 1): # Se a soma de alguma dessas linhas for maior ou igual a 1, não obedece ao critério das linhas
			return False
	return True

def relativeErrorDistance(xnext, xprev): # Tira o erro relativo da distância entre x(k) e x(k-1) para Gauss-Jacobi
	x = xnext - xprev
	if(maxValue(xnext)<0.001 or math.isnan(i) for i in xnext): 
		return abs(maxValue(x)) # Se o vetor x convergir para 0,0,...,0 usamos o erro absoluto
	d = abs(maxValue(x))/abs(maxValue(xnext))
	return d

def GaussJacobi(A, b, precision):
	n = A.shape[0]
	C = A.astype('float').copy()
	g = b.astype('float').copy().reshape(n,1)
	for i in range(0, n):
		cii = C[i,i]
		C[i] /= -cii
		g[i] /= cii
	C += np.identity(n)
	# até aqui já temos C e g. Vamos criar x0:
	xprev = np.random.randint(-5,6,(n,1)).astype('float') # x0 recebe um vetor 1xn de valores inteiros aleatórios em [-5,6)
	iterator = 0
	for k in range(0, 5000):
		xnext = C.dot(xprev) + g # x(k) = Cx(k-1) + g
		iterator += 1
		if(relativeErrorDistance(xnext.reshape(1,n), xprev.reshape(1,n)) < precision): # Se já chegamos à uma distância satisfatória
			break # para as iterações
		xprev = xnext # Se não parou acima, o x(k) vai ser o novo x(k-1) para a próxima iteração
	return np.around(xnext.reshape(1,n)[0],decimals=3), iterator

def InterpolationCondition(x): # Condição para poder fazermos interpolação
	n = len(x)				   # Se houver algum xi = xj com i =/= j, então o vetor gera um sistema mal
	for i in range(0,n):	   # condicionado e gerará um erro muito grande na intepolação.
		for j in range(0,n):
			if(i==j): continue
			if(x[i]==x[j]): return False
	return True

# Operação de diferenças divididas para interpolação de Newton.
def f(x, y, o): # (x, f(x), order)
	x = x[:o]
	y = y[:o]
	if(len(x)==1): return y[0] # retorna os f de ordem 1
	return (f(x[1:o], y[1:o], o-1) - f(x[:o-1],y[:o-1],o-1))/(x[o-1]-x[0])

def testPrint(x,y):
	print("x: " + str(x))
	print("y: " + str(y))

def simultaneousSort(x,y): # ordena o primeiro vetor, enquanto modifica na mesma ordem o segundo vetor.
	n = len(x)
	for i in range(0,n):
		for j in range(i,n):
			if(x[j] < x[i]):
				x[j],x[i] = x[i],x[j] # swap em python :)
				y[j],y[i] = y[i],y[j]

def targetPosition(x, target): # retorna a posição do primeiro elemento maior que o valor a ser interpolado
	for i in range(0,len(x)):
		if(x[i]>target):
			return i
	return len(x)

def reduceDimension(x,y,center,degree): # Reduz a dimensão de um vetor para o tamanho do polinômio a ser interpolado
	rx = [] # Vetor x reduzido
	ry = [] # Vetor y reduzido
	M = center # posição do primeiro elemento maior que o target
	m = center-1 # posição do primeiro elemento menor que o target
	while(len(rx) != degree+1):
		if(M < len(x)): # Se o maior elemento estiver dentro de x (isto é, o target não é maior que todos)
			rx.append(x[M]) # Coloca o elemento maior que o target à direita em rx
			ry.append(y[M])
			M += 1 # o maior será seu posterior agora.
		if(m >= 0 and len(rx) != degree+1): # se o target não for o menor e rx ainda não for do tamanho correto
			rx.insert(0, x[m])
			ry.insert(0, y[m])
			m -= 1 # o menor será seu anterior agora.
	return rx, ry

# Intepolação pela forma de Newton. Recebe x, f(x), o valor a ser interpolado (target) e o grau do polinômio a aproximar.
def NewtonInterpolation(x, y, target, degree):
	simultaneousSort(x,y) # Ordenando os vetores
	tPos = targetPosition(x,target) # Pegando a posição do primeiro elemento maior que o valor a ser interpolado
	x, y = reduceDimension(x,y,tPos,degree) # reduz a dimensão de x e y para pegar apenas os pontos necessários para a interpolação.
	n = len(x)
	p = y[0]
	for i in range(0,n-1):
		term = 1
		for j in range(0, i+1):
			term *= (target-x[j])
		term *= f(x,y,i+2)
		p += term
	return round(p,5)

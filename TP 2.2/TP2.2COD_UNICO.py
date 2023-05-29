import random
import math
import matplotlib.pyplot as plt
from scipy.stats import uniform, gamma, nbinom, hypergeom, poisson, binom, expon, norm
import numpy as np
import scipy as sp
from typing import Any
from math import sqrt, pi, exp, comb, trunc, log
from scipy.special import factorial, erfinv
from statistics import mean

def UniformeR(numeros, a, b) -> list:
    num = []
    M = 1 / (b - a)
    for U in numeros:
        while True:
            V = np.random.uniform(0, 1)
            T = a + ((b - a) * V)
            if (M * U <= 1 / (b - a)):
                num.append(T)
                break
    return num


# test

def runtestUDM(numeros, a):
    tMuestra = np.size(numeros)
    secuencia_con_signos = []
    media = np.mean(numeros)
    n1, n2 = 0, 0
    for i in range(0, tMuestra):
        if numeros[i] > media:
            secuencia_con_signos.append('1')
            n1 += 1
        if numeros[i] < media:
            secuencia_con_signos.append('0')
            n2 += 1
    corridas = 1
    for i in range(0, len(secuencia_con_signos) - 1):
        if secuencia_con_signos[i] != secuencia_con_signos[i + 1]:
            corridas += 1
    mediaC = ((2 * n1 * n2) / (n1 + n2)) + 1
    varianzaC = ((2 * n1 * n2) * (2 * n1 * n2 - tMuestra)) / (pow(tMuestra, 2) * (tMuestra - 1))
    desvio = math.sqrt(varianzaC)
    z = abs((corridas - mediaC) / desvio)
    print(f"Datos de la prueba: Media = {mediaC} - Varianza = {varianzaC} - Corridas = {corridas}")

    print(f"El Valor estadistico de prueba es Z = {z}")
    Ztabla = round(sp.stats.norm.ppf(1 - a / 2), 3)
    print("Resultado del test con una confianza del", (1 - (a * 2)) * 100, "%:",
          "No pasa el test" if z > Ztabla else "Pasa el test")


# -------------------------------
def mainUniforme():
    n = 1000
    a, b = 0, 10
    numeros = [random.uniform(0, 1) for i in range(n)]

    # Definir funcion de densidad y graficar para comparar
    x = np.linspace(uniform.ppf(0.0001, loc=a, scale=b - a), uniform.ppf(0.999, loc=a, scale=b - a), 100)
    fig, ax = plt.subplots(1, 1)
    ax.plot(x, uniform.pdf(x, loc=a, scale=b - a), 'r-', lw=2, alpha=0.6, label='uniforme')
    ax.legend(loc='best', frameon=False)

    # Histograma de densidades de x aceptadas por el metodo de rechazo
    num = UniformeR(numeros, a, b)
    ax.hist(num, density=True, bins='auto', histtype='stepfilled')
    plt.ylabel("Densidad de ocurrencias")
    plt.xlabel("Valor de la variable")
    plt.title('Histograma de una VA con distribucion Uniforme-Aceptacion y rechazo')
    plt.show()
    runtestUDM(num, 0.025)


mainUniforme()

import random
import math
import matplotlib.pyplot as plt
from scipy.stats import expon
import numpy as np
import scipy as sp


def densidad_exponencial(lam, x) -> float:
    if x < 0:
        return 0
    else:
        return lam * math.exp(-lam * x)


def Exponencialr(numeros, lam, n) -> list:
    M = densidad_exponencial(lam, 1 / lam)
    exponencial = []
    cont = 0

    while cont < n:
        U = random.uniform(0, 1)
        V = random.uniform(0, 1)
        T = -math.log(U) / lam

        if M * V <= densidad_exponencial(lam, T):
            exponencial.append(T)
            cont += 1

    return exponencial


lam = 0.5
n = 10000
"""
samples = rechazoExponencial([random.uniform(0, 1) for i in range(n)], lam, n)

# plot histogram
plt.hist(samples, bins=50, density=True, rwidth=0.8)
plt.title('Histograma - Distribución exponencial')
plt.show() """


# test
def runtestUDM(numeros, a):
    tMuestra = np.size(numeros)
    secuencia_con_signos = []
    media = np.mean(numeros)
    n1, n2 = 0, 0
    for i in range(0, tMuestra):
        if numeros[i] > media:
            secuencia_con_signos.append('1')
            n1 += 1
        if numeros[i] < media:
            secuencia_con_signos.append('0')
            n2 += 1
    corridas = 1
    for i in range(0, len(secuencia_con_signos) - 1):
        if secuencia_con_signos[i] != secuencia_con_signos[i + 1]:
            corridas += 1
    mediaC = ((2 * n1 * n2) / (n1 + n2)) + 1
    varianzaC = ((2 * n1 * n2) * (2 * n1 * n2 - tMuestra)) / (pow(tMuestra, 2) * (tMuestra - 1))
    desvio = math.sqrt(varianzaC)
    z = abs((corridas - mediaC) / desvio)
    print(f"Datos de la prueba: Media = {mediaC} - Varianza = {varianzaC} - Corridas = {corridas}")

    print(f"El Valor estadistico de prueba es Z = {z}")
    Ztabla = round(sp.stats.norm.ppf(1 - a / 2), 3)
    print("Resultado del test con una confianza del", (1 - (a * 2)) * 100, "%:",
          "No pasa el test" if z > Ztabla else "Pasa el test")


# -------------------------------

def mainExp():
    numero = [random.uniform(0, 1) for i in range(n)]
    num = Exponencialr(numero, lam, n)

    # Definir funcion de densidad y graficar para comparar
    x = np.linspace(expon.ppf(0.0001, scale=1 / lam), expon.ppf(0.999, scale=1 / lam), 100)
    fig, ax = plt.subplots(1, 1)
    ax.plot(x, expon.pdf(x, scale=1 / lam), 'r-', lw=2, alpha=0.6, label='exponencial ')
    ax.legend(loc='best', frameon=False)

    # Histograma de densidades de x aceptadas por el metodo de rechazo
    ax.hist(num, density=True, bins='auto', histtype='stepfilled')
    plt.ylabel("Densidad de ocurrencias")
    plt.xlabel("Valor de la variable")
    plt.title('Histograma de una VA con distribucion Exponencial-Aceptacion y rechazo')
    plt.show()
    runtestUDM(num, 0.025)

mainExp()

k = 2
theta = 1.8  #Donde k es Alpha y theta es beta
N = 1000
samples = []  # Almacenamiento de muestras válidas


def gamma_pdf(x, k, theta):
    return gamma.pdf(x,k, scale = 1/theta)

def randGamma():
    while len(samples) < N:
        x = np.random.exponential(theta*(k+1))
        u = np.random.uniform(0, 1)

        if u*maxY <= gamma_pdf(x, k, theta):
            samples.append(x)

# Función de densidad de probabilidad de la distribución gamma
x_vals = np.linspace(0, gamma.ppf(0.999, k,scale = 1/theta), 1000)
y_vals = gamma_pdf(x_vals, k, theta)
maxY = max(y_vals)
plt.plot(x_vals, y_vals, 'r', label='Función de densidad de probabilidad')



# Histograma de muestras generadas
randGamma()
plt.hist(samples, bins='sqrt', density=True, label='Muestras generadas', edgecolor = 'black')

# Configuración del gráfico
plt.title('Histograma de una VA con distribucion Gamma-Aceptacion y rechazo')
plt.xlabel('Valor de la variable')
plt.ylabel('Densidad de probabilidad')
plt.legend()
plt.show()

#   RECHAZO
def densNormal(m, v, x):
    return exp(-((x - m) ** 2) / (2 * v ** 2)) / (v * sqrt(2 * pi))


def normalLine(mu, sigma):
    x = np.linspace(mu - 3 * sigma, mu + 3 * sigma, 100)  # generación del eje x
    y = 1 / (sigma * np.sqrt(2 * np.pi)) * np.exp(-(x - mu) ** 2 / (2 * sigma ** 2))  # cálculo de la función normal
    return x, y


def NormalR(numeros, mu, des) -> list:
    a, b = mu - (10 * des), mu + (10 * des)  # Calcular los valores de a y b
    M = 1 / (des * sqrt(2 * pi))
    num = []
    for U in numeros:
        while True:  # se repite mientras que no se haya encontrado un valor aceptable
            V = np.random.uniform(0, 1)  # Generar un valor aleatorio V entre 0 y 1
            T = a + ((b - a) * V)
            if M * U <= exp(-((T - mu) ** 2) / (2 * des ** 2)):  # Verificar si el valor de T es aceptable
                num.append(T)  # Si es aceptable, agregarlo a la lista de valores aceptados
                # y salir del bucle while
                break
    return num


n = 1000
mu, des = 2, .5
distNormal = np.random.uniform(0, 1, n)
distNormal = NormalR(distNormal, mu, des)
xn, yn = normalLine(mu, des)
normal_list = np.random.normal(mu, des, n)
plt.plot(xn, yn, color='red', label='distribucion normal')
plt.hist(distNormal, bins=round(sqrt(len(distNormal))), edgecolor='black', density=True, color='steelblue')
plt.title('Histograma de una VA con distribucion Normal-Aceptacion y rechazo')
plt.xlabel('Valor de la variable')
plt.ylabel('Ocurrencias')
plt.legend(loc='best', frameon=False)
plt.show()


# test
def runtestUDM(numeros, a):
    tMuestra = np.size(numeros)
    secuencia_con_signos = []
    media = np.mean(numeros)
    n1, n2 = 0, 0
    for i in range(0, tMuestra):
        if numeros[i] > media:
            secuencia_con_signos.append('1')
            n1 += 1
        if numeros[i] < media:
            secuencia_con_signos.append('0')
            n2 += 1
    corridas = 1
    for i in range(0, len(secuencia_con_signos) - 1):
        if secuencia_con_signos[i] != secuencia_con_signos[i + 1]:
            corridas += 1
    mediaC = ((2 * n1 * n2) / (n1 + n2)) + 1
    varianzaC = ((2 * n1 * n2) * (2 * n1 * n2 - tMuestra)) / (pow(tMuestra, 2) * (tMuestra - 1))
    desvio = math.sqrt(varianzaC)
    z = abs((corridas - mediaC) / desvio)
    print(f"Datos de la prueba: Media = {mediaC} - Varianza = {varianzaC} - Corridas = {corridas}")

    print(f"El Valor estadistico de prueba es Z = {z}")
    Ztabla = round(sp.stats.norm.ppf(1 - a / 2), 3)
    print("Resultado del test con una confianza del", (1 - (a * 2)) * 100, "%:",
          "No pasa el test" if z > Ztabla else "Pasa el test")


# -------------------------------

runtestUDM(distNormal, 0.025)

#   TRANSFORMADA
def NormalInversa(numeros, mu, sigma) -> list:
    return [mu + sqrt(2) * sigma * erfinv(2 * r - 1) for r in numeros]
    # esta funcion una lista de valores de la distribución normal truncada para cada valor r en la lista pseudo


def normalLine(mu, sigma):
    x = np.linspace(mu - 3 * sigma, mu + 3 * sigma, 100)  # generación del eje x
    y = 1 / (sigma * np.sqrt(2 * np.pi)) * np.exp(-(x - mu) ** 2 / (2 * sigma ** 2))  # cálculo de la función normal
    return x, y


n = 1000
mu, des = 2, .5
distNormal = np.random.uniform(0, 1, n)
distNormal = NormalInversa(distNormal, mu, des)
normal_list = np.random.normal(mu, des, n)

xn, yn = normalLine(mu, des)
plt.plot(xn, yn, color='red', label='distribucion normal')
plt.hist(distNormal, bins=round(sqrt(len(distNormal))), edgecolor='black', density=True, color='steelblue')
plt.title('Histograma de una VA con distribucion Normal-Metodo Inversa')
plt.xlabel('Valor de la variable')
plt.ylabel('Ocurrencias')
plt.legend(loc='best', frameon=False)
plt.show()


# test
def runtestUDM(numeros, a):
    tMuestra = np.size(numeros)
    secuencia_con_signos = []
    media = np.mean(numeros)
    n1, n2 = 0, 0
    for i in range(0, tMuestra):
        if numeros[i] > media:
            secuencia_con_signos.append('1')
            n1 += 1
        if numeros[i] < media:
            secuencia_con_signos.append('0')
            n2 += 1
    corridas = 1
    for i in range(0, len(secuencia_con_signos) - 1):
        if secuencia_con_signos[i] != secuencia_con_signos[i + 1]:
            corridas += 1
    mediaC = ((2 * n1 * n2) / (n1 + n2)) + 1
    varianzaC = ((2 * n1 * n2) * (2 * n1 * n2 - tMuestra)) / (pow(tMuestra, 2) * (tMuestra - 1))
    desvio = math.sqrt(varianzaC)
    z = abs((corridas - mediaC) / desvio)
    print(f"Datos de la prueba: Media = {mediaC} - Varianza = {varianzaC} - Corridas = {corridas}")

    print(f"El Valor estadistico de prueba es Z = {z}")
    Ztabla = round(sp.stats.norm.ppf(1 - a / 2), 3)
    print("Resultado del test con una confianza del", (1 - (a * 2)) * 100, "%:",
          "No pasa el test" if z > Ztabla else "Pasa el test")


# -------------------------------

runtestUDM(distNormal, 0.025)

def densPascal(r, p, x):
    return comb(x+r-1, x) * p ** r * (1 - p) ** (x)  # la funcion comb sirve para calcular los coeficientes binomiales.


def PascalR(numeros, r, p):
    M = densPascal(r, p, int(r*(1-p)/p))  # Cálculo del máximo de la densidad binomial
    pascal = []
    for U in numeros:
        V = np.random.uniform(0, 1)  # Generar un número aleatorio en el intervalo [0, 1]
        T = int(2*r*V)  # Obtener el valor entero de la parte entera de n * V
        if (M * U <= densPascal(r, p, T)):  # Evaluar la densidad pascal en T
            pascal.append(T)  # Si el valor de la densidad evaluada es mayor que el umbral U,
            # entonces se acepta el valor T y se añade a la lista pascal
    return pascal


n = 1000
r, p = 40, .5
distPascal = np.random.uniform(0, 1, n)
num = PascalR(distPascal, r, p)
"""
distPascal = np.random.uniform(0, 1, n)  # La función devuelve una matriz NumPy de longitud n con los números aleatorios distribuidos uniformemente en el rango [0,1].

distPascal = PascalRech(distPascal, r, p)
plt.hist(distPascal, bins=round(sqrt(len(distPascal))), edgecolor='black')
plt.title('Histograma de una VA con distribucion Pascal-Aceptacion y rechazo')
plt.xlabel('Valor de la variable')
plt.ylabel('Ocurrencias')
plt.show() """

def mainPascal():
    distPascal = np.random.uniform(0, 1, n)
    num = PascalR(distPascal, r, p)

    # Definir función de densidad y graficar para comparar
    x = np.arange(nbinom.ppf(0.0001, r, p), nbinom.ppf(0.999, r, p))
    plt.plot(x, nbinom.pmf(x, r, p), '-r', ms=2, label='distribucion binomial negativa')

    # Histograma de densidades de x aceptadas por el metodo de rechazo
    plt.hist(num, density=True, bins='auto', alpha=0.5, label='histograma')

    plt.legend(loc='best', frameon=False)
    plt.ylabel("Densidad de ocurrencias")
    plt.xlabel("Valor de la variable")
    plt.title('Histograma de una VA con distribucion Pascal-Aceptacion y rechazo')
    plt.show()

mainPascal()


def densBinomial(n, p, x):
    return comb(n, x) * p ** x * (1 - p) ** (n - x)  # la funcion comb sirve para calcular los coeficientes binomiales.


def BinomialR(numeros, n, p):
    M = densBinomial(n, p, trunc(n * p))  # Cálculo del máximo de la densidad binomial
    binom = []
    for U in numeros:
        V = np.random.uniform(0, 1)  # Generar un número aleatorio en el intervalo [0, 1]
        T = int(n * V)  # Obtener el valor entero de la parte entera de n * V
        if (M * U <= comb(n, T) * p ** T * (1 - p) ** (n - T)):  # Evaluar la densidad binomial en T
            binom.append(T)  # Si el valor de la densidad evaluada es mayor que el umbral U,
            # entonces se acepta el valor T y se añade a la lista binom
    return binom


n = 1000
distBinomial = np.random.uniform(0, 1,
                                 n)  # La función devuelve una matriz NumPy de longitud n con los números aleatorios distribuidos uniformemente en el rango [0,1].
n, p = 40, .5
distBinomial = BinomialR(distBinomial, n, p)
x = np.arange(binom.ppf(0.0001, n, 0.5), binom.ppf(0.999, n, 0.5))
plt.plot(x, binom.pmf(x, n, p), '-r', ms=2, label='distribucion binomial')
plt.hist(distBinomial, density=True, bins=round(sqrt(len(distBinomial))), edgecolor='black')
plt.title('Histograma de una VA con distribucion Binomial-Aceptacion y rechazo')
plt.xlabel('Valor de la variable')
plt.ylabel('Ocurrencias')
plt.legend(loc='best', frameon=False)
plt.ylabel("Densidad de ocurrencias")
plt.show()


# test
def runtestUDM(numeros, a):
    tMuestra = np.size(numeros)
    secuencia_con_signos = []
    media = np.mean(numeros)
    n1, n2 = 0, 0
    for i in range(0, tMuestra):
        if numeros[i] > media:
            secuencia_con_signos.append('1')
            n1 += 1
        if numeros[i] < media:
            secuencia_con_signos.append('0')
            n2 += 1
    corridas = 1
    for i in range(0, len(secuencia_con_signos) - 1):
        if secuencia_con_signos[i] != secuencia_con_signos[i + 1]:
            corridas += 1
    mediaC = ((2 * n1 * n2) / (n1 + n2)) + 1
    varianzaC = ((2 * n1 * n2) * (2 * n1 * n2 - tMuestra)) / (pow(tMuestra, 2) * (tMuestra - 1))
    desvio = math.sqrt(varianzaC)
    z = abs((corridas - mediaC) / desvio)
    print(f"Datos de la prueba: Media = {mediaC} - Varianza = {varianzaC} - Corridas = {corridas}")

    print(f"El Valor estadistico de prueba es Z = {z}")
    Ztabla = round(sp.stats.norm.ppf(1 - a / 2), 3)
    print("Resultado del test con una confianza del", (1 - (a * 2)) * 100, "%:",
          "No pasa el test" if z > Ztabla else "Pasa el test")


# -------------------------------
runtestUDM(distBinomial, 0.025)

def dens_hipergeometrica(M, N, n, x):
    return hypergeom.pmf(x, M, N, n)


def dist_hipergeometrica(numeros, M, N, n) -> list:

    media = n*N/M
    p = dens_hipergeometrica(M, N, n, media)
    hiper_lista = []
    for U in numeros:
        while True:
            V = np.random.uniform(0, 1)
            O = int(n*V)
            if(p*U <= dens_hipergeometrica(M, N, n, O)):
                hiper_lista.append(O)
                break
    return hiper_lista

i = 1000 #rango
M = 200  # Tamaño de la población
n = 40  # Tamaño de la muestra
N = 30  # Número de elementos en la población con la propiedad que se está estudiando


distHiper = np.random.uniform(0, 1, i) # La función devuelve una matriz NumPy de longitud n con los números aleatorios distribuidos uniformemente en el rango [0,1].
distHiper = dist_hipergeometrica(distHiper, M, N,n)


# Valores de k para los cuales se quiere graficar la densidad
k_values = np.arange(0, n+1)

# Calculo de la función de masa de probabilidad
pmf_values = hypergeom.pmf(k_values, M, N, n)
fig, ax = plt.subplots()


#Histograma de densidades de x aceptadas por el metodo de rechazo
hist, bins, _ = plt.hist(distHiper, density=True, bins=range(n+2), edgecolor='black', align='left')
plt.xlim(0, n)
plt.xticks(range(0, n+1, 5))  # Mostrar valores de x de 5 en 5
plt.ylabel("Densidad de ocurrencias")
plt.xlabel("Valor de la variable")
plt.title('Histograma de una VA con distribucion Hipergeometrica-Aceptacion y rechazo')

# densidad maxima
pmf_max = hypergeom.pmf(np.arange(0, n+1), M, N, n).max()


# Grafica de la densidad
k_values = np.arange(0, n+1)
pmf_values = hypergeom.pmf(k_values, M, N, n)
plt.plot(k_values, pmf_values, 'r-', ms=8, lw=2, alpha=0.6,label='Hipergeometrica')
plt.legend(loc='best', frameon=False)


def dens_poisson(lmbda: float, x: int) -> float:
    return poisson.pmf(x, lmbda)


def dis_poisson(numeros, lmbda, max_x) -> list:
    M = dens_poisson(lmbda=lmbda, x=int(lmbda))
    poisson_list = []
    for U in numeros:
        while True:
            V = np.random.uniform(0, 1)
            T = int(V * max_x)  # a=0 siempre, b=max_x
            if (M * U <= dens_poisson(lmbda, T)):
                poisson_list.append(T)
                break
    return poisson_list


n = 1000
distPoisson = np.random.uniform(0, 1,
                                n)  # La función devuelve una matriz NumPy de longitud n con los números aleatorios distribuidos uniformemente en el rango [0,1].
x = 40
l = 3
ran = 40
distPoisson = dis_poisson(distPoisson, l, x)

# Definir rango de valores x y calcular la función de densidad
x = np.arange(0, ran)
pmf = dens_poisson(x, l)
fig, ax = plt.subplots()

# Graficar la función de densidad usando ax.plot
hist, bins, _ = plt.hist(distPoisson, density=True, bins=range(20), edgecolor='black', align='left')
plt.xlim(0, ran)
plt.xticks(range(0, ran, 5))
plt.ylabel("Densidad de ocurrencias")
plt.xlabel("Valor de la variable")
plt.title('Histograma de una VA con distribucion Poisson-Aceptacion y rechazo')

# densidad maxima
pmf_max = poisson.pmf(np.arange(0, ran), l).max()

# Grafica de la densidad
pmf_values = poisson.pmf(x, l)
plt.plot(x, pmf_values, 'r-', ms=8, lw=2, alpha=0.6, label='Poisson')
plt.legend(loc='best', frameon=False)


# test
def runtestUDM(numeros, a):
    tMuestra = np.size(numeros)
    secuencia_con_signos = []
    media = np.mean(numeros)
    n1, n2 = 0, 0
    for i in range(0, tMuestra):
        if numeros[i] > media:
            secuencia_con_signos.append('1')
            n1 += 1
        if numeros[i] < media:
            secuencia_con_signos.append('0')
            n2 += 1
    corridas = 1
    for i in range(0, len(secuencia_con_signos) - 1):
        if secuencia_con_signos[i] != secuencia_con_signos[i + 1]:
            corridas += 1
    mediaC = ((2 * n1 * n2) / (n1 + n2)) + 1
    varianzaC = ((2 * n1 * n2) * (2 * n1 * n2 - tMuestra)) / (pow(tMuestra, 2) * (tMuestra - 1))
    desvio = math.sqrt(varianzaC)
    z = abs((corridas - mediaC) / desvio)
    print(f"Datos de la prueba: Media = {mediaC} - Varianza = {varianzaC} - Corridas = {corridas}")

    print(f"El Valor estadistico de prueba es Z = {z}")
    Ztabla = round(sp.stats.norm.ppf(1 - a / 2), 3)
    print("Resultado del test con una confianza del", (1 - (a * 2)) * 100, "%:",
          "No pasa el test" if z > Ztabla else "Pasa el test")


# -------------------------------
runtestUDM(distPoisson, 0.025)

cant = 1000


def randEmpirica(numeros, min_x, lista_fr) -> list:
    n = len(lista_fr)
    a, b = min_x, min_x + n
    frec_rel = dict()

    max = __builtins__.max
    M = max(lista_fr)

    empiric = []
    for i in range(a, b):
        frec_rel.setdefault(i, lista_fr.pop(0))
    for U in numeros:
        while True:
            V = np.random.uniform(0, 1)
            T = trunc(a + (b - a) * V)
            if T not in frec_rel.keys():
                break
            if (M * U <= frec_rel[T]):
                empiric.append(T)
                break
    return empiric


pseudo = [np.random.uniform(0, 1) for _ in range(cant)]
lista = [0.092, 0.023, 0.168, 0.017, 0.014, 0.245, 0.019, 0.213, 0.114,
         0.085]  # numeros para probar, la suma de probabilidades debe ser igual a 1
plt.plot(lista, color='red')
R = randEmpirica(pseudo, 0, lista)
plt.hist(R, density=True, bins=10)
plt.ylabel("Densidad de ocurrencias")
plt.xlabel("Valor de la variable")
plt.title('Histograma de una VA con distribucion Empirica-Aceptacion y rechazo')
plt.show()

print(mean(R))


# test
def runtestUDM(numeros, a):
    tMuestra = np.size(numeros)
    secuencia_con_signos = []
    media = np.mean(numeros)
    n1, n2 = 0, 0
    for i in range(0, tMuestra):
        if numeros[i] > media:
            secuencia_con_signos.append('1')
            n1 += 1
        if numeros[i] < media:
            secuencia_con_signos.append('0')
            n2 += 1
    corridas = 1
    for i in range(0, len(secuencia_con_signos) - 1):
        if secuencia_con_signos[i] != secuencia_con_signos[i + 1]:
            corridas += 1
    mediaC = ((2 * n1 * n2) / (n1 + n2)) + 1
    varianzaC = ((2 * n1 * n2) * (2 * n1 * n2 - tMuestra)) / (pow(tMuestra, 2) * (tMuestra - 1))
    desvio = sqrt(varianzaC)
    z = abs((corridas - mediaC) / desvio)
    print(f"Datos de la prueba: Media = {mediaC} - Varianza = {varianzaC} - Corridas = {corridas}")

    print(f"El Valor estadistico de prueba es Z = {z}")
    Ztabla = round(sp.stats.norm.ppf(1 - a / 2), 3)
    print("Resultado del test con una confianza del", (1 - (a * 2)) * 100, "%:",
          "No pasa el test" if z > Ztabla else "Pasa el test")


# -------------------------------
runtestUDM(R, 0.025)
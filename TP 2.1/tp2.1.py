import random
import matplotlib.pyplot as plt
import numpy as np
import math
import scipy as sp
from scipy.stats import chi2


# TESTS
def runTestUD(numeros, a) -> list:
    tSec = np.size(numeros)
    secuencia_con_signos = []
    n1, n2 = 0, 0
    for i in range(len(numeros) - 1):
        if numeros[i] < numeros[i + 1]:
            secuencia_con_signos.append('1')
        else:
            secuencia_con_signos.append('0')
    r = 1
    for i in range(0, len(secuencia_con_signos) - 1):
        if secuencia_con_signos[i] != secuencia_con_signos[i + 1]:
            r += 1
    mediaC = 2 * tSec / 3
    varianzaC = (16 * tSec - 29) / 90
    desvio = math.sqrt(varianzaC)
    z = abs((r - mediaC) / desvio)
    Ztabla = round(sp.stats.norm.ppf(1 - a / 2), 3)
    print(f"El Valor Z en tabla =", Ztabla)
    print("Resultado del test con una confianza del", (1 - (a * 2)) * 100, "%:",
          "No pasa el test run UD" if z > Ztabla else "Pasa el test run UD")


# ---------------------------------
def runTestUDM(numeros, a):
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
    # print(f"Datos de la prueba: Media = {mediaC} - Varianza = {varianzaC} - Corridas = {corridas}")

    # print(f"El Valor estadistico de prueba es Z = {z}")

    Ztabla = round(sp.stats.norm.ppf(1 - a / 2), 3)
    print(f"El Valor Z en tabla =", Ztabla)
    print("Resultado del test con una confianza del", (1 - (a * 2)) * 100, "%:",
          "No pasa el test run  UDM" if z > Ztabla else "Pasa el test run UDM")


# -------------------------------

def calcular_frecuencias(lista, n) -> list:
    frecuencias, bordes = np.histogram(lista, bins=n)
    return frecuencias


def chiCuadradoTest(k, tInterv, numeros, a):
    # Contar el número de números aleatorios que caen en cada intervalo
    freqObs = np.zeros(k)
    tMuestra = len(numeros)
    freqObs = calcular_frecuencias(numeros, k)

    # Calcular las frecuencias esperadas
    freqEsp = tMuestra / len(freqObs)

    # Calcular el estadístico de prueba chi cuadrado

    chiCuaqLista = []
    for i in range(10):
        valor = ((freqObs[i] - freqEsp) ** 2) / freqEsp
        chiCuaqLista.append(valor)
    chiCuaqTotal = sum(chiCuaqLista)

    # Definir el número de grados de libertad
    df = k - 1

    # Calcular el valor crítico de chi cuadrado
    valorTabla = chi2.ppf(1 - a, df)

    # Imprimir los resultados del test de chi cuadrado
    # print("Número de grados de libertad:", df)
    print("Valor crítico de chi cuadrado:", valorTabla)
    # print("Estadístico de prueba chi cuadrado:", chiCuaqTotal)
    print("Resultado del test con una confianza del", (1 - (a * 2)) * 100, "%:",
          "No pasa el test ChiCuad" if chiCuaqTotal > valorTabla else "Pasa el test ChiCuad")


# ----------------------------------------


def pokerTest(numeros, a):
    # Define las frecuencias esperadas para cada mano de póker
    espTodosIguales = 0.01 * len(numeros)
    espUnaPareja = 0.297 * len(numeros)
    espDosParejas = 0.4495 * len(numeros)
    espTresIguales = 0.2401 * len(numeros)
    espTodosDiferentes = 0.0024 * len(numeros)

    # Inicializa las frecuencias observadas para cada mano de póker
    obsTodosIguales = 0
    obsUnaPareja = 0
    obsDosParejas = 0
    obsTresIguales = 0
    obsTodosDiferentes = 0

    # Realiza la prueba de póker en cada número
    for i in numeros:
        # Obtiene los primeros tres dígitos decimales del número
        digito = str(i - int(i))[2:5]

        # Cuenta el número de ocurrencias de cada dígito
        contDigitos = [digito.count(d) for d in digito]

        # Cuenta el número de parejas y el número de dígitos distintos
        contParejas = contDigitos.count(2)
        contDiferentes = contDigitos.count(1)

        # Evalúa a qué mano de póker pertenece el número
        if contDiferentes == 1:  # Todos los dígitos son iguales
            obsTodosIguales += 1
        elif contDiferentes == 3:  # Todos los dígitos son diferentes
            obsTodosDiferentes += 1
        elif contParejas == 1:  # Una pareja
            obsUnaPareja += 1
        elif contParejas == 2:  # Dos parejas
            obsDosParejas += 1
        elif contDiferentes == 2:  # Tres iguales
            obsTresIguales += 1

    # Calcula la estadística chi-cuadrado para cada mano de póker
    chiCuadradoTodosIguales = (pow((obsTodosIguales - espTodosIguales), 2)) / espTodosIguales
    chiCuadradoUnaPareja = (pow((obsUnaPareja - espUnaPareja), 2)) / espUnaPareja
    chiCuadradoDosParejas = (pow((obsDosParejas - espDosParejas), 2)) / espDosParejas
    chiCuadradoTresIguales = (pow((obsTresIguales - espTresIguales), 2)) / espTresIguales
    chiCuadradoTodosDistintos = (pow((obsTodosDiferentes - espTodosDiferentes), 2)) / espTodosDiferentes
    # print(chiCuadradoTodosIguales)
    # print(chiCuadradoUnaPareja)
    # print(chiCuadradoTresIguales)
    # print(chiCuadradoTodosDistintos)
    # print(chiCuadradoDosParejas)
    # Calcular la estadística de chi-cuadrado total.
    chiCuadrado = chiCuadradoTodosIguales + chiCuadradoUnaPareja + chiCuadradoDosParejas + chiCuadradoTresIguales + chiCuadradoTodosDistintos
    chi2Tabla = chi2.ppf(1 - 0.05, 5)
    print("El valor de chi cuadrado en tabla es:", chi2Tabla)
    print("Resultado del test con una confianza del", (1 - (a * 2)) * 100, "%:",
          "No pasa el test Poker" if chiCuadrado > chi2Tabla else "Pasa el test Poker")


# -------------------------------------------------------------

# GENERADORES
s = 54123
mod = 2 ** 30
mult = 25214903917
inc = 1442695040888963407


def gclMixto(s, mod, mult, inc, n) -> list:
    numeros = [s]
    for i in range(n - 1):
        numAl = (mult * numeros[i] + inc) % mod
        numeros.append(numAl)
    plt.title("Diagrama de dispersion GCL Mixto")
    plt.ylabel("Valor del numero x generdo")
    plt.xlabel("Numero x generado")
    plt.scatter(range(n), numeros, c="black", s=1)
    plt.show()
    return numeros


def gclMult(s, mod, mult, n) -> list:
    numeros = [s]
    for i in range(n - 1):
        numAl = (mult * numeros[i]) % mod
        numeros.append(numAl)
    plt.title("Diagrama de dispersion GCL Multiplicativo")
    plt.ylabel("Valor del numero x generdo")
    plt.xlabel("Numero x generado")
    plt.scatter(range(n), numeros, c="black", s=1)
    plt.show()
    return numeros


def cuadradosMedios(s, n):
    largo = len(str(s))
    numeros = []
    for i in range(0, n):
        cuad = str(s * s)
        while True:
            if len(cuad) < largo * 2:
                cuad = "0" + cuad
            else:
                break
        s = int(cuad[slice(int(-3 * largo / 2), int(-largo / 2))])
        numeros.append(float('0.' + str(s)))
    plt.title("Diagrama de dispersion Cuadrados Medios")
    plt.ylabel("Valor del numero x generdo")
    plt.xlabel("Numero x generado")
    plt.scatter(range(n), numeros, c="black", s=1)
    plt.show()
    return numeros


# ---------------------------------------------------
n = 1000
numCD = cuadradosMedios(1908, n)
numGS = gclMixto(s, mod, mult, inc, n)
numGM = gclMult(s, mod, mult, n)
a = 0.025
print("cuadrados medios")
pokerTest(numCD, a)
runTestUD(numCD, a)
runTestUDM(numCD, a)
tIntCD = np.ptp(numCD)
chiCuadradoTest(10, tIntCD, numCD, a)

print("GCL simple")
pokerTest(numGS, a)
runTestUD(numGS, a)
runTestUDM(numGS, a)
tIntGS = np.ptp(numGS)
chiCuadradoTest(10, tIntGS, numGS, a)

print("GCL Mult")
pokerTest(numGM, a)
runTestUD(numGM, a)
runTestUDM(numGM, a)
tIntGM = np.ptp(numGM)
chiCuadradoTest(10, tIntGM, numGM, a)

print("RandInt de Python")


def genPython(n) -> list:
    nPY = []
    for i in range(n):
        nPY.append(random.randint(0, n))
    plt.title("Diagrama de dispersion Python")
    plt.ylabel("Valor del numero x generdo")
    plt.xlabel("Numero x generado")
    plt.scatter(range(n), nPY, c="black", s=1)
    plt.show()
    return nPY


nPY = genPython(n)
pokerTest(nPY, a)
runTestUD(nPY, a)
runTestUDM(nPY, a)
tIntPY = np.ptp(nPY)
chiCuadradoTest(10, tIntPY, nPY, a)
#!/usr/bin/python3
from grafo import Grafo
from funciones import *
import sys
sys.setrecursionlimit(100000)
import resource
resource.setrlimit(resource.RLIMIT_STACK,(resource.RLIM_INFINITY,resource.RLIM_INFINITY))

def crear_grafo(archivo):
    grafo = Grafo(True)
    with open(archivo, encoding="utf8") as file:
        for linea in file:
            linea = linea.split("\t")
            v = linea[0].rstrip('\n')
            grafo.agregar_vertice(v)
            for link in linea[1::]:
                x = link.rstrip('\n')
                grafo.agregar_vertice(x)
                grafo.agregar_arista(v,x)
    return grafo

def listar_operaciones():
    print("camino")
    print("navegacion")
    print("rango")
    print("conectados")
    print("lectura")
    print("ciclo")
    print("diametro")

def imprimir_camino(art1,recorrido,costo):
    if(bool(recorrido) == False):
        print("No se encontro recorrido")
        return
    print(art1,end ='')
    for i in recorrido[-2::-1]:
        print(" ->",i,end ='')
    print("")
    print("Costo:",costo)

def imprimir_navegacion(lista,articulo):
    print(articulo,end='')
    if(lista != None):
        for link in lista:
            print(" ->",link,end ='')
    print("")

def imprimir_conectados(lista):
    for art in lista[:-1]:
        print(art,end =', ')
    print(lista[-1])

def imprimir_lectura(lista):
    if lista != None:
        x = lista[0]
        lista.remove(x)
        for i in reversed(lista):
            print(i, end=", ")
        print(x)
    else:
        print("No existe forma de leer las paginas en orden")

def imprimir_ciclo(lista,articulo):
    if(lista != None):
        for link in lista:
            print(link,"-> ",end ='')
    print(articulo)

def ejecutar_comando(grafo, comando, cfcs, datos_diametro):
    if(comando[0] == "listar_operaciones"):
        listar_operaciones()
    if(comando[0] == "navegacion"):
        x = navegacion(grafo, comando[1])
        imprimir_navegacion(x,comando[1])
    if(comando[0] == "camino"):
        x = comando[1].split(",")
        recorrido, costo = camino(grafo, x[0], x[1])
        imprimir_camino(x[0], recorrido, costo)
    if(comando[0] == "rango"):
        x = comando[1].split(",",1)
        x = rango(grafo,x[0],int(x[1]))
        print(x)
    if(comando[0] == "conectados"):
        imprimir_conectados(cfc(grafo,comando[1],cfcs))
    if(comando[0] == "lectura"):
        lista_vertices = comando[1].split(",")
        imprimir_lectura(orden_topologico(grafo,lista_vertices))
    if(comando[0] == "ciclo"):
        x = comando[1].split(",")
        lista = backtracking_ciclo_largo_n(grafo, x[0], int(x[1]))
        if lista != None:
            imprimir_ciclo(lista,x[0])
        else:
            print("No se encontro recorrido")
    if(comando[0] == "diametro"):
        if bool(datos_diametro) == False:
            x,y = diametro(grafo)
            recorrido, costo = camino(grafo, x, y)
            datos_diametro.append(x)
            datos_diametro.append(recorrido)
            datos_diametro.append(costo)
            imprimir_camino(x,recorrido, costo)
        else:
            imprimir_camino(datos_diametro[0], datos_diametro[1], datos_diametro[2])

def main():
    archivo = sys.argv[1]
    grafo = crear_grafo(sys.argv[1])
    cfcs = []
    datos_diametro = []
    while True:
        try:
            comando = input().split(" ",1)
        except EOFError:
            break
        ejecutar_comando(grafo, comando,cfcs, datos_diametro)
    return 0

main()

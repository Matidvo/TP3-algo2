import heapq
import sys
sys.setrecursionlimit(100000)
import resource
resource.setrlimit(resource.RLIMIT_STACK,(resource.RLIM_INFINITY,resource.RLIM_INFINITY))
from grafo import Grafo
from grafo import Cola
from grafo import Pila

def camino(grafo, origen, destino):
    """
    Utiliza BFS para conseguir una lista con el camino de un vertice a otro
     y su distancia y los devuelve.
    Si no hay camino, devuelve una lista vacia y 0.
    Args:
        grafo: el grafo que contiene los vertices y aristas con los que trabaja la funcion
        origen (any): Vertice del cual se desea partir en el recorrido
        destino (any): Vertice en el cual el recorrido debe terminar
    Returns:
        recorrido: Lista del recorrido del camino del origen al destino
        si ese camino no existe es una lista vacia
        orden[destino]: El numero de vertices por los que paso el recorrido
        (entero positivo)
    """
    visitados = set()
    padres = {}
    orden = {}
    q = Cola()
    visitados.add(origen)
    padres[origen] = None
    orden[origen] = 0
    q.encolar(origen)
    while q.esta_vacia() == False:
        v = q.desencolar()
        for w in grafo.obtener_adyacentes(v):
            if w not in visitados:
                visitados.add(w)
                padres[w] = v
                orden[w] = orden[v] + 1
                q.encolar(w)
            if w == destino:
                break
    recorrido = []
    x = destino
    if x not in padres.keys():
        return recorrido,0
    recorrido.append(x)
    while padres[x] != None:
        recorrido.append(padres[x])
        x = padres[x]
    return recorrido, orden[destino]


def navegacion(grafo,origen):
    """
    Devuelve una lista con todos los primeros adyacentes
    de los vertices que va navegando a partir del origen
    Args:
        grafo: Grafo que contiene los vertices y aristas con los que trabaja la funcion
        origen (any): Vertice del cual se desea partir en el recorrido
    Returns:
        recorrido: Lista que contiene el recorrido de la navegacion
    """
    if grafo.existe_vertice(origen):
        v = list(grafo.obtener_adyacentes(origen))[0]
        recorrido = []
        recorrido.append(v)
        i = 0
        while i < 19 and grafo.tiene_adyacentes(v):
            v = grafo.obtener_adyacentes(v)[0]
            recorrido.append(v)
            i += 1
        return recorrido
    else: return

def rango(grafo, origen, rango):
    """
    Utiliza BFS para averigura el numero de vertices que estan a la distancia
    "rango" del origen.
    Args:
        grafo: Grafo que contiene los vertices y aristas con los que trabaja la funcion
        origen (any): vertice respecto al cual se calcula la distancia
        rango( entero positivo): la distancia exacta a la que un vertice debe estar para ser contado
    Returns:
        en_rango: numero de vertices que se encuentran a la distancia del rango
        del origen(entero positivo)
    """
    visitados = set()
    orden = {}
    orden[origen] = 0
    visitados.add(origen)
    en_rango = 0
    q = Cola()
    q.encolar(origen)
    while not q.esta_vacia():
        v = q.desencolar()
        for w in grafo.obtener_adyacentes(v):
            if w not in visitados:
                orden[w] = orden[v] + 1
                if orden[w] > rango:
                    break
                visitados.add(w)
                q.encolar(w)
                if orden[w] == rango:
                    en_rango += 1
    return en_rango
'''
    Funcion recursiva, usar el llamado inicial.
    Devuelve una lista con todos los vertices de la componente fuertemente conexa
    a la que pertenece el vertice pasado en su primera llamada.
    Args:
        los de la llamada original, o creados por esta.
    Returns:
        nueva_cfc: Una lista con todos los vertices de la componente fuertemente
        conexa a la que pertenece v
'''
def cfc_rec(grafo, v, visitados, pila, apilados, orden, mas_bajo, cfcs, indice):
    visitados.add(v)
    pila.apilar(v)
    apilados.add(v)
    mas_bajo[v] = orden[v]
    for w in grafo.obtener_adyacentes(v):
        if w not in visitados:
            orden[w] = indice[0] + 1
            indice[0] += 1
            cfc_rec(grafo, w, visitados, pila, apilados, orden, mas_bajo, cfcs, indice)
            mas_bajo[v] = min(mas_bajo[v], mas_bajo[w])
        elif w in apilados:
            mas_bajo[v] = min(mas_bajo[v], mas_bajo[w])
    if mas_bajo[v] == orden[v]:
        nueva_cfc = []
        w = pila.desapilar()
        apilados.remove(w)
        nueva_cfc.append(w)
        while w != v:
            w = pila.desapilar()
            apilados.remove(w)
            nueva_cfc.append(w)
        cfcs.append(nueva_cfc)
        return nueva_cfc
'''
    Crea las estructuras necesarias para la llamada recursiva de cfc y luego la llama.
    Si la cfc del vertice indicado ya fue calculada previamente y está en la lista
    pasada por parametro, la devuelve sin calcular nada.
    Args:
        grafo: Grafo que contiene los vertices y aristas con los que trabaja la funcion
        v: Vertice del cual se quiere calcular su componente fuertemente conexa
        cfcs:lista con las cfcs calculadas previamente
    Returns:
        cfc: Una lista con todos los vertices de la componente fuertemente conexa a
        la que pertenece v
'''
def cfc(grafo,v,cfcs):
    for i in cfcs:
        if v in i:
            return i
    visitados = set()
    pila = Pila()
    apilados = set()
    orden = {}
    mas_bajo = {}
    indice = [0]
    orden[v] = 0
    return cfc_rec(grafo, v, visitados, pila, apilados, orden, mas_bajo, cfcs, indice)

'''
    Le asigna los grados iniciales a los vertices para calcular su orden topologico
    Args:
        grafo: Grafo que contiene los vertices y aristas con los que trabaja la funcion
        lista_vertices: Lista que contiene los vertices de los cuales se va a calcular
        su orden topologico
    Returns:
        grados: diccionario con el grado de todos los vertices en la lista
'''
def grados_iniciales(grafo,lista_vertices):
    grados = {}
    for v in lista_vertices:
        grados[v] = 0
    for v in lista_vertices:
        for w in lista_vertices:
            if w in grafo.obtener_adyacentes(v):
                grados[w] += 1
    return grados
'''
    Obtiene el orden en el que deben ser recorridos los vertices en la lista
    respetando el orden de precedencia. Si tal orden no existe devuelve None
    El metodo es un algoritmo bfs por grados
    Args:
        grafo: Grafo que contiene los vertices y aristas con los que trabaja la funcion
        lista_vertices: la lista de vertices que se debe devolver ordenada
    Returns:
        resultado: la lista de vertices ordenada en base a su orden topologico
'''
def orden_topologico(grafo,lista_vertices):
    grados = grados_iniciales(grafo,lista_vertices)
    q = Cola()
    for v in lista_vertices:
        if grados[v] == 0:
            q.encolar(v)
    resultado = []
    while not q.esta_vacia():
        v = q.desencolar()
        resultado.append(v)
        for w in lista_vertices:
            if w in grafo.obtener_adyacentes(v):
                grados[w] -= 1
                if grados[w] == 0:
                    q.encolar(w)
    if len(resultado) == len(lista_vertices):
        return resultado
    else:
        return None


'''
    Llamada recursiva de la funcion de backtracking. Utiliza dfs para recorrer
     recursivamente el grafo y formar un ciclo de largo n. Si no es posible
     formar semejante ciclo devuelve None
    Args:
        los mismos que backtracking o generados por la llamada de esta.
    Returns:
        Una lista con los elementos del recorrido en el orden que se recorrieron
'''
def dfs_ciclo_largo_n_rec(grafo, v, origen, n, visitados, camino_actual):
    visitados.add(v)
    if len(camino_actual) == n:
        if origen in grafo.obtener_adyacentes(v):
            return camino_actual
        else: return None
    for w in grafo.obtener_adyacentes(v):
        if w in visitados:continue
        solucion = dfs_ciclo_largo_n_rec(grafo, w, origen, n, visitados, camino_actual + [w])
        if solucion is not None:
            return solucion
    visitados.remove(v)
    return None
'''
    Obtiene un recorrido de largo n que empieza y termina en el vertice
    pasado por parámetro. Si no es posible formar semejante recorrido devuelve None
    Args:
        grafo: Grafo que contiene los vertices y aristas con los que trabaja la funcion
        origen: El vertice en el cual el ciclo debe empezar y terminar
        n: el largo que debe tener el recorrido
    Returns:
        Una lista con los elementos del recorrido en el orden que se recorrieron
'''
def backtracking_ciclo_largo_n(grafo, origen, n):
    return dfs_ciclo_largo_n_rec(grafo, origen, origen, n, set(),[origen])

'''
    Recorre todo el grafo partiendo de un vertice y devuelve donde termina
    el camino minimo mas largo de ese vertice y cual es el largo de este
    Args:
        grafo: Grafo que contiene los vertices y aristas con los que trabaja la funcion
        origen: El vertice para el cual se calcula el camino
    Returns:
    mayor_destino: El vertice con el camino minimo mas largo respecto al origen
    mayor_orden: El largo del camino al mayor_destino
'''
def bfs(grafo,origen):
    visitados = set()
    orden = {}
    orden[origen] = 0
    visitados.add(origen)
    mayor_orden = 0
    mayor_destino = ""
    q = Cola()
    q.encolar(origen)
    while not q.esta_vacia():
        v = q.desencolar()
        for w in grafo.obtener_adyacentes(v):
            if w not in visitados:
                orden[w] = orden[v] + 1
                if orden[w] > mayor_orden:
                    mayor_orden = orden[w]
                    mayor_destino = w
                visitados.add(w)
                q.encolar(w)
    return mayor_destino,mayor_orden

'''
    Busca el camino minimo mas largo del grafo, y devuelve los vertices inicial y final
    de este
    Args:
        grafo: Grafo que contiene los vertices y aristas con los que trabaja la funcion
    Returns:
        vertice_inicial: El vertice inicial del camino minimo mas largo del grafo
        vertice_final: El vertice final del camino minimo mas largo del grafo
'''
def diametro(grafo):
    mayor_costo = 0
    for v in grafo.obtener_vertices():
        final,costo = bfs(grafo,v)
        if costo > mayor_costo:
            mayor_costo = costo
            vertice_inicial = v
            vertice_final = final
    return vertice_inicial,vertice_final

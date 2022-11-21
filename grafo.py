import random
class Cola:
    def __init__(self):
        # invariante:
        # si la cola está vacía => frente = ultimo = None
        # si la cola no está vacía => frente != None y ult != None
        self.frente = None
        self.ultimo = None

    def encolar(self, dato):
        nuevo = _Nodo(dato)
        if self.ultimo == None:
            # cola vacía
            self.ultimo = nuevo
            self.frente = nuevo
        else:
            self.ultimo.prox = nuevo
            self.ultimo = nuevo

    def desencolar(self):
        """
        Desencola un elemento y lo devuelve.
        Pre: la cola no puede estar vacía.
        """
        dato = self.frente.dato
        self.frente = self.frente.prox
        if self.frente is None:
            self.ultimo = None
        return dato

    def esta_vacia(self):
        return self.frente is None

    def ver_frente(self):
        """Pre: la cola no es vacía"""
        return self.frente.dato

class Pila:
    def __init__(self):
        '''
        Inicializa una nueva pila, vacía
        '''
        self.tope = None
        self.largo = 0

    def apilar(self, dato):
        '''
        Agrega un nuevo elemento a la pila
        '''
        nodo = _Nodo(dato, self.tope)
        self.tope = nodo
        self.largo += 1

    def desapilar(self):
        '''
        Desapila el elemento que está en el tope de la pila
        y lo devuelve.
        Pre: la pila no está vacía.
        Pos: el nuevo tope es el siguiente elemento al tope anterior
        '''
        if self.esta_vacia():
            raise ValueError("pila vacía")
        dato = self.tope.dato
        self.tope = self.tope.prox
        self.largo -= 1
        return dato

    def largo(self):
        return self.largo

    def ver_tope(self):
        '''
        Devuelve el elemento que está en el tope de la pila.
        Pre: la pila no está vacía.
        '''
        if self.esta_vacia():
            raise ValueError("pila vacía")
        return self.tope.dato

    def esta_vacia(self):
        '''
        Devuelve True o False según si la pila está vacía o no
        '''
        return self.tope is None



class _Nodo:
    def __init__(self, dato, prox=None):
        self.dato = dato
        self.prox = prox


class Grafo:
    def __init__(self, dirigido, vertices_iniciales = None):
        """
        Devuelve un objeto grafo

        Args:
            dirigido (bool): Indica si el grafo es dirigido o no.
            vertices_iniciales (list, optional): Lista de vertices con los cuales se desea inicializar el grafo. Defaults to None.
        """
        self.dirigido = dirigido
        self.lista_adyacencia = {}

        # Inicializo los vertices iniciales
        if vertices_iniciales:
            for vertice in vertices_iniciales:
                self.lista_adyacencia[vertice] = {}

    def agregar_vertice(self, vertice):
        """
        Agrega el vertice al grafo, en caso de ya existir no hace nada.

        Args:
            vertice (any): vertice a agregar
        """
        if not vertice in self.lista_adyacencia:
            self.lista_adyacencia[vertice] = {}

    def agregar_arista(self, vertice1, vertice2, peso=1):
        """
        Agrega una arista entre el <vertice1> y el <vertice2>, por defecto de peso 1.

        Args:
            vertice1 (any): Vertice inicial
            vertice2 (any): Vertice final
            peso (int, optional): Peso de la arista. Defaults to 1.
        """
        if not vertice1 in self.lista_adyacencia: return
        if not vertice2 in self.lista_adyacencia: return

        self.lista_adyacencia[vertice1][vertice2] = peso

        if not self.dirigido:
            self.lista_adyacencia[vertice2][vertice1] = peso

    def existe_arista(self, vertice1, vertice2):
        """
        Devuelve una tupla indicando si la arista existe y en dicho caso su peso

        Args:
            vertice1 (any): Vertice inicial
            vertice2 (any): Vertice final

        Returns:
            tuple: (bool indicando si el vertice existe, peso de la arista)
        """
        diccionario = self.lista_adyacencia.get(vertice1, {})
        peso = diccionario.get(vertice2, None)

        if peso is None: return (False, 0)
        return (True, peso)

    def eliminar_arista(self, vertice1, vertice2):
        """
        Elimina la arista que conecta <vertice1> con <vertice2> en caso de existir.

        Args:
            vertice1 (any): Vertice inicio
            vertice2 (any): Vertice final
        """
        # Elimino la arista v1->v2
        self.lista_adyacencia[vertice1].pop(vertice2, None)

        # En caso del grafo ser no dirigido, elimina la arista v2->v1
        if not self.dirigido:
            self.lista_adyacencia[vertice2].pop(vertice1, None)

    def eliminar_vertice(self, vertice):
        """
        Elimina el vertice y todas las aristas relacionadas a el.

        Args:
            vertice (any): Vertice a eliminar
        """
        # Si el vertice no se encuentra en la lista de adyacencias termino la funcion
        if not vertice in self.lista_adyacencia: return

        # Elimino el vertice de la lista de adyacencia
        self.lista_adyacencia.pop(vertice, None)

        # Le digo al resto de los vertices que ya no existe
        for v in self.lista_adyacencia.values():
            v.pop(vertice, None)

    def obtener_vertices(self):
        """
        Obtener todos los vertices del grafo

        Returns:
            list: Lista con todos los vertices del grafo
        """
        resultado = []

        for vertice in self.lista_adyacencia.keys():
            resultado.append(vertice)


        return resultado

    def existe_vertice(self, id):
        """
        Se recibe por parametro un vertice y se retorna un booleano indicando si existe o no.
        """
        if(id in self.lista_adyacencia):
            return True
        else:
            return False

    def obtener_adyacentes(self, vertice):
        """
        Devuelve una lista con todos los vertices adyances al <vertice>

        Args:
            vertice (any): Vertice del cual se desea obtener los adyacentes

        Returns:
            list: Lista de adyacentes al <vertice>
        """
        resultado = []

        for v in self.lista_adyacencia.get(vertice,{}):
            resultado.append(v)

        return resultado

    def tiene_adyacentes(self,vertice):
        if(self.existe_vertice(vertice) == False):
            return False
        if(len(self.lista_adyacencia[vertice]) > 0):
            return True
        else:
            return False

    def __getitem__(self, arg):
        vertices = list(self.lista_adyacencia.keys())
        return vertices[0]

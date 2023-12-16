import random
from turtle import color


class Flood:
    """
    Clase para administrar un tablero de N colores.
    """

    def __init__(self, alto, ancho):
        """
        Genera un nuevo Flood de un mismo color con las dimensiones dadas.

        Argumentos:
            alto, ancho (int): Tamaño de la grilla.
        """
        self.alto = alto
        self.ancho = ancho
        self.color_actual = 1
        self.tablero = self.crear_tablero(alto, ancho, self.color_actual)
        self.cantidad_colores = 1
        self.cantidad_colores_adyacentes = 0
    
    def crear_tablero(self, alto, ancho, color):
        tablero = []
        for _ in range(alto):
            fila_nueva=[]
            for _ in range(ancho):
                fila_nueva.append(color)
            tablero.append(fila_nueva)
        return tablero
    

    def mezclar_tablero(self, n_colores):
        """
        Asigna de forma completamente aleatoria hasta `n_colores` a lo largo de
        las casillas del tablero.

        Argumentos:
            n_colores (int): Cantidad maxima de colores a incluir en la grilla.
        """
        for i in range(self.alto):
            for j in range(self.ancho):
                self.tablero[i][j] = random.randint(1, n_colores)
        self.cantidad_colores = n_colores
        self.color_actual = self.tablero[0][0]


    def obtener_color(self, fil, col):
        """
        Devuelve el color que se encuentra en las coordenadas solicitadas.

        Argumentos:
            fil, col (int): Posiciones de la fila y columna en la grilla.

        Devuelve:
            Color asignado.
        """
        return self.tablero[fil][col]


    def obtener_posibles_colores(self):
        """
        Devuelve una secuencia ordenada de todos los colores posibles del juego.
        La secuencia tendrá todos los colores posibles que fueron utilizados
        para generar el tablero, sin importar cuántos de estos colores queden
        actualmente en el tablero.

        Devuelve:
            iterable: secuencia ordenada de colores.
        """
        return list(range(1, self.cantidad_colores + 1))



    def dimensiones(self):
        """
        Dimensiones de la grilla (filas y columnas)

        Devuelve:
            (int, int): alto y ancho de la grilla en ese orden.
        """
        return (self.alto, self.ancho)


    def cambiar_color(self, color_nuevo):
        """
        Asigna el nuevo color al Flood de la grilla. Es decir, a todas las
        coordenadas que formen un camino continuo del mismo color comenzando
        desde la coordenada origen en (0, 0) se les asignará `color_nuevo`

        Argumentos:
            color_nuevo: Valor del nuevo color a asignar al Flood.
        """
        if color_nuevo == self.color_actual:
            return
        self._cambiar_color(color_nuevo)
        self.color_actual = color_nuevo
            

    
    def _cambiar_color(self, color_nuevo, fila = 0, columna = 0):
        if not (0 <= fila < self.alto and 0 <= columna < self.ancho and self.tablero[fila][columna] == self.color_actual):
            return 
        self.tablero[fila][columna] = color_nuevo 
        for direccion in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            self._cambiar_color(color_nuevo, fila + direccion[0], columna + direccion[1])
        

    def clonar(self):
        """
        Devuelve:
            Flood: Copia del Flood actual
        """
        clon = Flood(self.alto, self.ancho)
        clon.color_actual, clon.tablero, clon.cantidad_colores = self.color_actual, [fila.copy() for fila in self.tablero], self.cantidad_colores
        return clon


    def esta_completado(self):
        """
        Indica si todas las coordenadas de grilla tienen el mismo color

        Devuelve:
            bool: True si toda la grilla tiene el mismo color
        """
        for i in range(self.alto):
            for j in range(self.ancho):
                if self.tablero[i][j] != self.color_actual:
                    return False
        return True
    
    def contar_cantidad_colores_adyacentes(self):
        self.cantidad_colores_adyacentes = 0
        copia = self.clonar()
        copia._contar_cantidad_colores_adyacentes()
        return copia.cantidad_colores_adyacentes
    
    def _contar_cantidad_colores_adyacentes(self, fila = 0, columna = 0):
        if not (0 <= fila < self.alto and 0 <= columna < self.ancho and self.tablero[fila][columna] == self.color_actual and self.tablero[fila][columna] != "contado"):
            return
        self.tablero[fila][columna] = "contado"
        self.cantidad_colores_adyacentes += 1
        for direccion in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            self._contar_cantidad_colores_adyacentes(fila + direccion[0], columna + direccion[1])


        



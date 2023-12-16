from flood import Flood
from pila import Pila
from cola import Cola


class JuegoFlood:
    """
    Clase para administrar un Flood, junto con sus estados y acciones
    """

    def __init__(self, alto, ancho, n_colores):
        """
        Genera un nuevo JuegoFlood, el cual tiene un Flood y otros
        atributos para realizar las distintas acciones del juego.

        Argumentos:
            alto, ancho (int): Tamaño de la grilla del Flood.
            n_colores: Cantidad maxima de colores a incluir en la grilla.
        """
        self.flood = Flood(alto, ancho)
        self.flood.mezclar_tablero(n_colores)
        self.mejor_n_movimientos, _ = self._calcular_movimientos()
        self.n_movimientos = 0
        self.pasos_solucion = Cola()
        self.movimientos_deshacer = Pila()
        self.movimientos_rehacer = Pila()
        



    def cambiar_color(self, color):
        """
        Realiza la acción para seleccionar un color en el Flood, sumando a la
        cantidad de movimientos realizados y manejando las estructuras para
        deshacer y rehacer

        Argumentos:
            color (int): Nuevo color a seleccionar
        """

        self.n_movimientos += 1
        jugada = self.flood.clonar()
        self.movimientos_rehacer = Pila()
        self.movimientos_deshacer.apilar(jugada)
        self.flood.cambiar_color(color)
        if not self.pasos_solucion.esta_vacia() and self.pasos_solucion.ver_frente() == color:
            self.pasos_solucion.desencolar()
        else:
            self.pasos_solucion = Cola()

    def deshacer(self):
        """
        Deshace el ultimo movimiento realizado si existen pasos previos,
        manejando las estructuras para deshacer y rehacer.
        """
        if self.movimientos_deshacer.esta_vacia():
            return
        self.movimientos_rehacer.apilar(self.flood.clonar())
        self.flood = self.movimientos_deshacer.desapilar()
        self.n_movimientos -= 1
        self.pasos_solucion = Cola()


    def rehacer(self):
        """
        Rehace el movimiento que fue deshecho si existe, manejando las
        estructuras para deshacer y rehacer.
        """
        if self.movimientos_rehacer.esta_vacia():
            return
        self.movimientos_deshacer.apilar(self.flood.clonar())
        self.flood = self.movimientos_rehacer.desapilar()
        self.n_movimientos += 1
        self.pasos_solucion = Cola()


    def _calcular_movimientos(self):
        """
        Realiza una solución de pasos contra el Flood actual (en una Cola)
        y devuelve la cantidad de movimientos que llevó a esa solución.

        Se clona el Flood creado, y luego en un ciclo definido por los colores, se clona nuevamente 
        y se verifica cuál es el color que más movimientos realizaría al flood. Una vez obtenido el color más
        efectivo, se realiza el movimiento en el primer flood clonado, y se repite el mismo procedimiento
        hasta que el flood esté completo, guardando cada paso (color efectivo) en una cola.

        Devuelve:
            int: Cantidad de movimientos que llevó a la solución encontrada.
            Cola: Pasos utilizados para llegar a dicha solución
        """
        flood_aux = self.flood.clonar()
        movimientos_total = 0
        cola_solucion = Cola()
        while not flood_aux.esta_completado():
            cantidad_colores_adyacentes = 0
            color_efectivo = 0
            for color_actual in flood_aux.obtener_posibles_colores():
                intento = flood_aux.clonar()
                intento.cambiar_color(color_actual)
                cantidad_intento_colores_adyacentes = intento.contar_cantidad_colores_adyacentes()
                if cantidad_colores_adyacentes < cantidad_intento_colores_adyacentes:
                    cantidad_colores_adyacentes = cantidad_intento_colores_adyacentes
                    color_efectivo = color_actual
            flood_aux.cambiar_color(color_efectivo)
            movimientos_total += 1
            cola_solucion.encolar(color_efectivo)
        return movimientos_total, cola_solucion
        

     


              

            


    def hay_proximo_paso(self):
        """
        Devuelve un booleano indicando si hay una solución calculada
        """
        return not self.pasos_solucion.esta_vacia()


    def proximo_paso(self):
        """
        Si hay una solución calculada, devuelve el próximo paso.
        Caso contrario devuelve ValueError

        Devuelve:
            Color del próximo paso de la solución
        """
        return self.pasos_solucion.ver_frente()


    def calcular_nueva_solucion(self):
        """
        Calcula una secuencia de pasos que solucionan el estado actual
        del flood, de tal forma que se pueda llamar al método `proximo_paso()`
        """
        _, self.pasos_solucion = self._calcular_movimientos()


    def dimensiones(self):
        return self.flood.dimensiones()


    def obtener_color(self, fil, col):
        return self.flood.obtener_color(fil, col)


    def obtener_posibles_colores(self):
        return self.flood.obtener_posibles_colores()


    def esta_completado(self):
        return self.flood.esta_completado()

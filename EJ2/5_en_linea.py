import gamelib

ANCHO_VENTANA = 300
ALTO_VENTANA = 300
DIMENSION = 10
JUGADOR1 = "O"
JUGADOR2 = "X"
ESPACIO = " "
INICIO_TABLERO = 50
FIN_TABLERO = 260
DIMENSION_CELDA = (FIN_TABLERO - INICIO_TABLERO) // DIMENSION

def juego_mostrar(juego, turno_jugador):
    """Actualizar la ventana"""
    gamelib.draw_text('5 en línea', 150, 20)
    mostrar_tablero()
    mostrar_fichas(juego)  
    gamelib.draw_text(f"Turno {turno_jugador}", 150, 280) 

def mostrar_tablero():
    for i in range(INICIO_TABLERO, FIN_TABLERO + 1, DIMENSION_CELDA):
        gamelib.draw_line(INICIO_TABLERO, i, FIN_TABLERO, i)
        gamelib.draw_line(i, INICIO_TABLERO, i, FIN_TABLERO)

def mostrar_fichas(juego):
    for j in range(len(juego)):
        for k in range(len(juego[0])):
            gamelib.draw_text(f"{juego[j][k]}", (INICIO_TABLERO + DIMENSION_CELDA * k) + DIMENSION_CELDA // 2, (INICIO_TABLERO + DIMENSION_CELDA * j) + DIMENSION_CELDA // 2)

def juego_crear():
    """Inicializar el estado del juego"""
    tablero = []
    for _ in range(DIMENSION):
        fila_nueva=[]
        for _ in range(DIMENSION):
            fila_nueva.append(ESPACIO)
        tablero.append(fila_nueva)
    return tablero

def juego_actualizar(juego, x, y, turno_jugador):
    """Actualizar el estado del juego

    x e y son las coordenadas (en pixels) donde el usuario hizo click.
    Esta función determina si esas coordenadas corresponden a una celda
    del tablero; en ese caso determina el nuevo estado del juego y lo
    devuelve.
    """
    if INICIO_TABLERO < x < FIN_TABLERO and INICIO_TABLERO < y < FIN_TABLERO:
        fila, columna = coordenada_a_indice(x,y)
        if juego[fila][columna] == ESPACIO:
            return insertar_ficha(juego, fila, columna, turno_jugador), proximo_turno(turno_jugador)
    return juego, turno_jugador

def insertar_ficha(juego, fila, columna, turno_jugador):
        juego[fila][columna] = turno_jugador
        return juego

def proximo_turno(turno_jugador):
    if turno_jugador == JUGADOR1:
        return JUGADOR2
    else:
        return JUGADOR1

def coordenada_a_indice(x,y):
    """
    Recibe la posición del tablero en coordenadas (x, y) de los pixels, y
    devuelve su ubicación en celdas de una lista de listas.
    """ 
    return (y - INICIO_TABLERO) // DIMENSION_CELDA, (x - INICIO_TABLERO) // DIMENSION_CELDA
    

def main():
    juego = juego_crear()
    turno_jugador = JUGADOR1
    # Ajustar el tamaño de la ventana
    gamelib.resize(ANCHO_VENTANA, ALTO_VENTANA)

    # Mientras la ventana esté abierta:
    while gamelib.is_alive():
        # Todas las instrucciones que dibujen algo en la pantalla deben ir
        # entre `draw_begin()` y `draw_end()`:
        gamelib.draw_begin()
        juego_mostrar(juego, turno_jugador)
        gamelib.draw_end()

        # Terminamos de dibujar la ventana, ahora procesamos los eventos (si el
        # usuario presionó una tecla o un botón del mouse, etc).

        # Esperamos hasta que ocurra un evento
        ev = gamelib.wait()

        if not ev:
            # El usuario cerró la ventana.
            break

        if ev.type == gamelib.EventType.KeyPress and ev.key == 'Escape':
            # El usuario presionó la tecla Escape, cerrar la aplicación.
            break

        if ev.type == gamelib.EventType.ButtonPress:
            # El usuario presionó un botón del mouse
            x, y = ev.x, ev.y # averiguamos la posición donde se hizo click
            juego, turno_jugador = juego_actualizar(juego, x, y, turno_jugador)

gamelib.init(main)
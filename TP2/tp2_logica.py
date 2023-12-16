import gamelib
import csv
from random import choice, randint, randrange

INICIO_TABLERO = 0
FIN_TABLERO = 400
DIMENSION = 8
DIMENSION_CELDA = FIN_TABLERO // DIMENSION
ESPACIO = " "
REINTENTAR = "z"
BOARD = "desktop/TP2/img/board.gif"

def nuevo_nivel():
    res = {}
    res["nivel"] = 1
    return res

def cadena_a_booleano(cadena):
    if cadena == "false":
        return False
    return True

def movimientos_de_piezas(archivo_origen):
    """
    Recibe el archivo.csv de los movimientos, y los separa en un diccionario donde cada clave es la pieza,
    y el valor una lista de tuplas con los movimientos
    """
    res = {}
    with open(archivo_origen) as origen:
        for fila in csv.reader(origen):
            pieza, movimiento, extensible = fila[0], fila[1], fila[2]
            mov_x, mov_y = movimiento.split(";")
            mov_x, mov_y = int(mov_x), int(mov_y)
            res[pieza] = res.get(pieza, [])
            res[pieza].append((mov_x, mov_y))
            if cadena_a_booleano(extensible):
                for i in range(1, DIMENSION):
                    extensible_x, extensible_y = i * mov_x, i * mov_y
                    res[pieza].append((extensible_x, extensible_y))
        return res

def tablero_crear():
    tablero = []
    for _ in range(DIMENSION):
        fila_nueva=[]
        for _ in range(DIMENSION):
            fila_nueva.append(ESPACIO)
        tablero.append(fila_nueva)
    return tablero

def movimiento_aleatorio_disponible(tablero, movimientos, pieza, fila, columna):
    """
    Recibe el tablero, los movimientos, la pieza, y su ubicación, y devuelve otra ubicación aleatoria 
    permitida para la próxima pieza
    """
    while True:
        movimiento_pieza = movimientos[pieza]
        fila_nueva, columna_nueva = movimiento_pieza[randrange(len(movimiento_pieza))]
        try:
            if tablero[fila_nueva + fila][columna_nueva + columna] == ESPACIO and fila + fila_nueva >= 0 and columna + columna_nueva >= 0:
                return fila_nueva + fila, columna_nueva + columna
        except:
            continue

def juego_nuevo(movimientos, juego):
    '''inicializa el estado del juego para el numero de nivel dado'''
    tablero = tablero_crear()
    fila, columna, pieza_inicial = randint(0, DIMENSION-1), randint(0, DIMENSION-1), choice(list(movimientos.keys()))
    tablero[fila][columna], pieza_actual = pieza_inicial, pieza_inicial
    fila_pieza_inicial, columna_pieza_inicial = fila, columna
    for _ in range(juego["nivel"] + 1):
        fila, columna = movimiento_aleatorio_disponible(tablero, movimientos, pieza_actual, fila, columna)
        pieza_actual = choice(list(movimientos.keys()))
        tablero[fila][columna] = pieza_actual
    juego["tablero"], juego["fila pieza actual"], juego["columna pieza actual"] = tablero, fila_pieza_inicial, columna_pieza_inicial
    return juego

def juego_mostrar(juego, movimientos):
    '''dibuja la interfaz de la aplicación en la ventana'''
    gamelib.draw_begin()
    dibujar_tablero(juego["nivel"])
    dibujar_pieza_actual(juego["tablero"], juego["fila pieza actual"], juego["columna pieza actual"])
    dibujar_piezas_restantes(juego, movimientos)
    gamelib.draw_end()

def dibujar_tablero(nivel):
    """
    Dibuja el tablero junto al texto de la interfaz
    """
    gamelib.draw_image(BOARD, 0, 0)
    gamelib.draw_text("SHAPE SHIFTER CHESS", 100, 415, size=10, bold=True, italic=True)
    gamelib.draw_text(f"Nivel: {nivel}", 47, 440, size=10, bold=True)
    gamelib.draw_text(f"Salir: Esc", 270, 415, size=10, bold=True)
    gamelib.draw_text(f"Reintentar: {REINTENTAR}", 282, 440, size=10, bold=True)

def dibujar_piezas_restantes(juego, movimientos):
    """
    Recorre el tablero y dibuja las piezas, menos la inicial.
    """
    for j in range(len(juego["tablero"])):
        for k in range(len(juego["tablero"][0])):
            dibujar_pieza_blanca(juego, j, k, movimientos)

def dibujar_pieza_actual(juego, fila, columna):
    """
    Dibuja la pieza a moverse, la cual es de color rojo.
    """
    if juego[fila][columna] != ESPACIO:
        gamelib.draw_image(f"desktop/TP2/img/{juego[fila][columna]}_rojo.gif", DIMENSION_CELDA * columna + 5, DIMENSION_CELDA * fila + 5)
    
def dibujar_pieza_blanca(juego, fila, columna, movimientos):
    """
    Dibuja la pieza que no se va a mover, y si la pieza actual puede comerla, dibuja un recuadro rojo alrededor
    de la misma
    """
    tablero, fila_inicial, columna_inicial = juego["tablero"], juego["fila pieza actual"], juego["columna pieza actual"]
    if tablero[fila][columna] != ESPACIO and (fila != fila_inicial or columna != columna_inicial):
        if tablero[fila][columna] != ESPACIO and es_movimiento_permitido(tablero[fila_inicial][columna_inicial], fila, columna, fila_inicial, columna_inicial, movimientos):
            gamelib.draw_rectangle(columna * DIMENSION_CELDA + 2, fila * DIMENSION_CELDA + 2, (columna + 1) * DIMENSION_CELDA + 1, (fila + 1) * DIMENSION_CELDA + 2, outline='red', fill="", width=5)
        gamelib.draw_image(f"desktop/TP2/img/{tablero[fila][columna]}_blanco.gif", DIMENSION_CELDA * columna + 5, DIMENSION_CELDA * fila + 5)

def coordenada_a_indice(x,y):
    """
    Recibe la posición del tablero en coordenadas (x, y) de los pixels, y
    devuelve su ubicación en celdas de una lista de listas.
    """ 
    return (y - INICIO_TABLERO) // DIMENSION_CELDA, (x - INICIO_TABLERO) // DIMENSION_CELDA

def es_movimiento_permitido(pieza_actual, fila, columna, fila_actual, columna_actual, movimientos):
    movimientos_pieza = movimientos[pieza_actual]
    for movimiento in movimientos_pieza:
        movimiento_x, movimiento_y = movimiento
        if fila_actual + movimiento_y == fila and columna_actual + movimiento_x == columna:
            return True
    return False

def juego_actualizar(juego, x, y, movimientos):
    """
    Determina si las coordenadas corresponden a una celda
    del tablero; en ese caso determina el nuevo estado del juego y lo
    devuelve.
    """
    tablero, fila_pieza_actual, columna_pieza_actual = juego["tablero"], juego["fila pieza actual"], juego["columna pieza actual"]
    if INICIO_TABLERO < x < FIN_TABLERO and INICIO_TABLERO < y < FIN_TABLERO:
        fila, columna = coordenada_a_indice(x,y)
        if tablero[fila][columna] != ESPACIO and es_movimiento_permitido(tablero[fila_pieza_actual][columna_pieza_actual], fila, columna, fila_pieza_actual, columna_pieza_actual, movimientos):
            tablero[fila_pieza_actual][columna_pieza_actual] = ESPACIO
            juego["tablero"], juego["fila pieza actual"], juego["columna pieza actual"] = tablero, fila, columna 
    return juego

def nivel_completado(juego):
    tablero, fila_pieza_actual, columna_pieza_actual = juego["tablero"], juego["fila pieza actual"], juego["columna pieza actual"]
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            if tablero[i][j] != ESPACIO and (i != fila_pieza_actual or columna_pieza_actual != j):
                return False
    return True

def guardar_partida(archivo, juego):
    """
    Recibe un archivo (si no existe, lo crea) y guarda la partida del último nivel comenzado.
    """
    tablero, fila_actual, columna_actual, nivel = juego["tablero"], juego["fila pieza actual"], juego["columna pieza actual"], juego["nivel"]
    with open(archivo, "w") as archivo:
        for i in range(DIMENSION):
            for j in range(DIMENSION):
                if tablero[i][j] != ESPACIO and (i != fila_actual or j != columna_actual):
                    archivo.write(f"{tablero[i][j]},{i},{j},no_actual\n")   
        archivo.write(f"{tablero[fila_actual][columna_actual]},{fila_actual},{columna_actual},{nivel}")

def cargar_partida(archivo):   

    """
    Recibe el archivo donde se guardó el último nivel, y lo devuelve.
    """
    tablero = tablero_crear()
    juego = {}
    with open(archivo) as archivo:
        for linea in csv.reader(archivo):
            if not linea:
                break
            pieza, fila, columna, es_actual = linea[0], linea[1], linea[2], linea[3]
            if es_actual != "no_actual":
                fila_actual, columna_actual, nivel = fila, columna, es_actual
            tablero[int(fila)][int(columna)] = pieza
        juego["tablero"], juego["nivel"], juego["fila pieza actual"], juego["columna pieza actual"] = tablero, int(nivel), int(fila_actual), int(columna_actual)
        return juego

def preguntar_cargar_checkpoint():
    while True:
        cargar_partida = input("Desea cargar ultima partida jugada? s/n: ")
        if cargar_partida == "s":
            return True
        if cargar_partida == "n":
            return False

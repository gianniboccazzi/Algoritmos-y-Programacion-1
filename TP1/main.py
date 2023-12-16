
from random import choices

def ubicacion_espacio_matriz(lista):
    """
    Recibe una matriz por parámetro y devuelve la ubicacion (fila, columna) del espacio vacio
    """
    for filas in range(len(lista)):
        for columnas in range(len(lista[0])):
            if lista[filas][columnas] == " ":
                return filas, columnas

def armar_tablero(filas, columnas, movimientos_aleatorios, MOV_IZQUIERDA, MOV_DERECHA, MOV_ARRIBA, MOV_ABAJO):
    """
    Recibe la cantidad de filas, columnas y movimientos aleatorios (numeros positivos) establecidos como variable 
    constante del programa, y devuelve el tablero mezclado en dichas condiciones.
    """
    tablero = []
    contador = 0
    for i in range(filas):
        nueva_fila = []
        for j in range(columnas):
            contador += 1
            if contador == filas * columnas:
                nueva_fila.append(" ")
            else:    
                nueva_fila.append(contador)
        tablero.append(nueva_fila)    
    return mezclar_aleatorio(tablero, movimientos_aleatorios, MOV_IZQUIERDA, MOV_DERECHA, MOV_ARRIBA, MOV_ABAJO)

def movimiento(lista, filas, columnas, suma_fila, suma_columna):
    """
    Recibe una lista de listas (tablero) , la ubicación en filas-columnas del espacio en dicho tablero, y
    las coordenadas de la ubicacion del lugar a moverse respecto del espacio.
    Cambia de lugar el espacio con el numero en coordenadas (suma_fila, suma_columna) y devuelve la lista
    """
    lista[filas][columnas], lista[filas + suma_fila][columnas + suma_columna] = lista[filas + suma_fila][columnas + suma_columna], lista[filas][columnas]
    return lista

def mover_tablero(lista, direccion, MOV_IZQUIERDA, MOV_DERECHA, MOV_ARRIBA, MOV_ABAJO):
    """
    Recibe por parametro la lista de listas(tablero) y la direccion(jugada) por la cual se va a mover.
    la función busca donde está el espacio en el tablero, y dependiendo la dirección, revisa si
    ese movimiento es valido dentro del tablero. Devuelve la lista con las jugadas realizadas.
    """
    fila_espacio, columna_espacio = ubicacion_espacio_matriz(lista)
    if direccion[0] == MOV_ARRIBA and fila_espacio < len(lista)-1:
        movimiento(lista, fila_espacio, columna_espacio, 1, 0)
    elif direccion[0] == MOV_IZQUIERDA and columna_espacio < len(lista[0])-1:
        movimiento(lista, fila_espacio, columna_espacio, 0, 1)
    elif direccion[0] == MOV_ABAJO and fila_espacio > 0:
        movimiento(lista, fila_espacio, columna_espacio, -1, 0)
    elif direccion[0] == MOV_DERECHA and columna_espacio > 0:
        movimiento(lista, fila_espacio, columna_espacio, 0, -1)
    return lista

def mezclar_aleatorio(lista, movimientos_aleatorios, MOV_IZQUIERDA, MOV_DERECHA, MOV_ARRIBA, MOV_ABAJO):
    """
    Recibe la lista de listas(tablero) y una cantidad de movimientos aleatorios y devuelve la misma
    con movimientos aleatorios.
    """
    while True:
        for _ in range(movimientos_aleatorios):
            direccion = choices(["a", "w", "d" ,"s"])
            mover_tablero(lista, direccion, MOV_IZQUIERDA, MOV_DERECHA, MOV_ARRIBA, MOV_ABAJO)
        if not esta_ordenado(lista):
            break
    return lista
   
def imprimir_interfaz(tablero, mov_izquierda, mov_derecha, mov_arriba, mov_abajo, movimientos_realizados, movimientos_aleatorios):
    """
    Recibiendo por parametro el tablero(lista), los controles a utilizar para realizar jugadas, la cantidad 
    de movimientos realizados y los movimientos aleatorios que se hicieron para armar el tablero.
    Imprime el interfaz del juego
    """
    print("=== Fifteen ===")
    for i in range(len(tablero)):
        for j in range(len(tablero[0])):
            if j == len(tablero[i])-1:
                print(str(tablero[i][j]).center(6))
            else:
                print(str(tablero[i][j]).center(6), end="|")
    print(f"Controles: {mov_arriba}, {mov_izquierda}, {mov_abajo}, {mov_derecha} ")
    print("Salir del juego: o")
    print(f"Movimientos realizados: {movimientos_realizados}/{movimientos_aleatorios * 5}")

def pedir_jugada(mov_izquierda, mov_derecha, mov_arriba, mov_abajo):
    """
    Pide una entrada al usuario, chequea que sea una entrada valida dentro del juego utilizando
    los controles de movimiento del juego, y si lo es, devuelve la entrada
    """
    movimientos_aceptados = f"{mov_abajo}{mov_izquierda}{mov_arriba}{mov_derecha}o"
    while True:
        jugada = input("Entrada: ")
        if not jugada:
            continue
        for i in range(len(jugada)):
            if not jugada[i] in movimientos_aceptados:
                break
        else:
            return jugada

def actualizar_tablero(tablero, jugada, MOV_IZQUIERDA, MOV_DERECHA, MOV_ARRIBA, MOV_ABAJO):
    """
    Recibe el tablero y la jugada, y actualiza el tablero con cada una de las jugadas.
    """
    for direccion in jugada:
        mover_tablero(tablero, direccion, MOV_IZQUIERDA, MOV_DERECHA, MOV_ARRIBA, MOV_ABAJO)
    return tablero

def esta_ordenado(tablero):
    """
    Por medio de un contador, verifica que el tablero esté ordenado y el elemento inferior derecho sea un espacio
    En caso de serlo, devuelve True
    """
    contador = 0
    for i in range(len(tablero)):
        for j in range(len(tablero[0])):
            contador += 1
            if tablero[i][j] != contador:
                if i == len(tablero)-1 and j == len(tablero[0])-1 and tablero[len(tablero)-1][len(tablero[0])-1] == " ":
                    return True
                return False

def imprimir_victoria():
    print("Felicidades! Ganaste!")

def imprimir_derrota():
    print("Perdiste!")



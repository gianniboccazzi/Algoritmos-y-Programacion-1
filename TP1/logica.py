import main
FILAS = 3
COLUMNAS = 3
MOV_IZQUIERDA = "a"
MOV_DERECHA = "d"
MOV_ARRIBA = "w"
MOV_ABAJO = "s"
MOV_ALEATORIOS = 40
LIMITE_MOVIMIENTOS = MOV_ALEATORIOS * 5

def fifteen():
    movimientos_realizados = 0
    tablero = main.armar_tablero(FILAS, COLUMNAS, MOV_ALEATORIOS, MOV_IZQUIERDA, MOV_DERECHA, MOV_ARRIBA, MOV_ABAJO)
    main.imprimir_interfaz(tablero, MOV_IZQUIERDA, MOV_DERECHA, MOV_ARRIBA, MOV_ABAJO, movimientos_realizados, MOV_ALEATORIOS)
    while True:
        jugada = main.pedir_jugada(MOV_IZQUIERDA, MOV_DERECHA, MOV_ARRIBA, MOV_ABAJO)
        if "o" in jugada:   #Si la jugada del usuario incluye "o", finaliza el juego
            return print("Adios!")
        tablero = main.actualizar_tablero(tablero, jugada, MOV_IZQUIERDA, MOV_DERECHA, MOV_ARRIBA, MOV_ABAJO)
        for _ in range(len(jugada)):
            movimientos_realizados += 1  #Suma los movimientos realizados con la cantidad de caracteres de la jugada
        main.imprimir_interfaz(tablero, MOV_IZQUIERDA, MOV_DERECHA, MOV_ARRIBA, MOV_ABAJO, movimientos_realizados, MOV_ALEATORIOS)
        if movimientos_realizados > LIMITE_MOVIMIENTOS:
            return main.imprimir_derrota()
        if main.esta_ordenado(tablero):
            return main.imprimir_victoria()
fifteen()
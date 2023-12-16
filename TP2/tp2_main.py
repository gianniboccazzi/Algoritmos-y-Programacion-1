import gamelib
import tp2_logica

ANCHO_VENTANA = 400
ALTO_VENTANA = 460
REINTENTAR = "z"
SALIR = "Escape"
ARCHIVO_MOVIMIENTOS = "desktop/TP2/movimientos.csv"
ARCHIVO_CHECKPOINT = "checkpoint.csv"
    
def main():
    gamelib.title("Shape Shifter Chess")
    gamelib.resize(ANCHO_VENTANA, ALTO_VENTANA)
    try:
        movimientos = tp2_logica.movimientos_de_piezas(ARCHIVO_MOVIMIENTOS)
    except:
        return gamelib.say("El archivo de movimientos no se encuentra en la ruta especificada. Modifique la ruta y vuelva a intentarlo.")
    if not tp2_logica.preguntar_cargar_checkpoint():
        juego = tp2_logica.nuevo_nivel()
        juego = tp2_logica.juego_nuevo(movimientos, juego)
    else:
        try:
            juego = tp2_logica.cargar_partida(ARCHIVO_CHECKPOINT)
        except:
            gamelib.say("No tenés partidas guardadas anteriormente.")
            juego = tp2_logica.nuevo_nivel()
            juego = tp2_logica.juego_nuevo(movimientos, juego)
    tp2_logica.guardar_partida(ARCHIVO_CHECKPOINT, juego)
    
    while gamelib.is_alive():
        tp2_logica.juego_mostrar(juego, movimientos)
        ev = gamelib.wait()
        if not ev:
            break
        if ev.type == gamelib.EventType.KeyPress and ev.key == SALIR:
            break
        elif ev.type == gamelib.EventType.KeyPress and ev.key == REINTENTAR:
            juego = tp2_logica.cargar_partida(ARCHIVO_CHECKPOINT)
            continue    
        if ev.type == gamelib.EventType.ButtonPress:
            x, y = ev.x, ev.y 
            juego = tp2_logica.juego_actualizar(juego, x, y, movimientos)
        if tp2_logica.nivel_completado(juego):
            juego["nivel"] += 1
            juego = tp2_logica.juego_nuevo(movimientos, juego)
            tp2_logica.guardar_partida(ARCHIVO_CHECKPOINT, juego)
gamelib.init(main)
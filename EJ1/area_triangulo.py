from vectores import diferencia, producto_vectorial, norma

def area_triangulo(x1, y1, z1, x2, y2, z2, x3, y3, z3):
    """Recibe 3 puntos en el espacio y devuelve el área del triangulo que conforman"""
    # Se hace la diferencia para obtener los vectores AB y AC
    vector_AB_x, vector_AB_y, vector_AB_z = diferencia(x2, y2, z2, x1, y1, z1)
    vector_AC_x, vector_AC_y, vector_AC_z = diferencia(x3, y3, z3, x1, y1, z1)
    # Ahora que ya están los vectores, se calcula el producto vectorial
    producto_vectorial_ABAC_x, producto_vectorial_ABAC_y, producto_vectorial_ABAC_z = producto_vectorial(vector_AB_x, vector_AB_y, vector_AB_z, vector_AC_x, vector_AC_y, vector_AC_z)
    # Con el producto vectorial, se calcula  la norma
    norma_producto_vectorial = norma(producto_vectorial_ABAC_x, producto_vectorial_ABAC_y, producto_vectorial_ABAC_z)
    resultado_area_triangulo = norma_producto_vectorial / 2
    return resultado_area_triangulo

assert area_triangulo(3, 4, 2, 3, 2, 4, 7, 3, 2) == 5.744562646538029
assert area_triangulo(5, 3, 6, -2, 6, 1, 2, 3, 7) == 11.979148550710939
assert area_triangulo(1, 0, 0, 0, 0, 0, 0, 0, 1) == 0.5
    


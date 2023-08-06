from .Funciones import encontrar_bordes
"""
    encontrar_bordes(imagen,tipo_umbral,color_borde,ancho_borde)
    ->imagen_bordeada, bordes
    
    Funcion realizada por los alumnos: 
    Cordoba Pablo Ezequiel y Romero Coronado Paul Andrés
    
    Esta funcion encuentra los bordes de una imagen.
    Devuelve la imagen con los bordes dibujados y una matriz con las coordenadas
    de los bordes
    
    imagen: imagen fuente
    tipo_umbral (string): "b" - binaria
                          "binv" - binaria inversa
                          "t" - truncado
                          "tz" - to zero
                          "tzinv" - to zero inversa
    color_borde (string): "r" - rojo
                          "g" - verde
                          "b" - azul
                          "y" - amarillo
                          "c" - cyan
                          "m" - magenta
                          "o" - naranja
                          "yg" - amarillo_verde
                          "cg" - cyan_verde
                          "cb" - cyan_azul
                          "p" - morado
                          "rm" - rosado/fucsia (rojo_magenta)
    ancho_borde (int): ancho del borde a dibujar
    
 """
import cv2
import numpy as np


def encontrar_bordes(imagen,tipo_umbral,tipo_contorno,color_borde,ancho_borde):
        
    """
   	encontrar_bordes(imagen,tipo_umbral,tipo_contorno,color_borde,ancho_borde)
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
   						  
   	tipo_contorno (string): "ext" - bordes externos
   							"list" - todos los contornos (sin relacion de jerarquia)
   							"ccomp" - contornos externos e internos (huecos)[jerarquia de 2 niveles]
   							"tree" - todos los contornos (con relación de jerarquía)
   
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
   						  "k" - negro
   	ancho_borde (int): ancho del borde a dibujar
"""
    # Si la imagen es a color, 
    # len(imagen.shape[:]) = 3
    # si es en escala de grises
    # len(imagen.shape[:]) = 2
    #---------- 
    escala_color = len(imagen.shape[:])
    #----------
    
    img_aux = np.copy(imagen)
    if (escala_color==3):
        imagen1 = cv2.cvtColor(img_aux, cv2.COLOR_BGR2GRAY)
    else:
        imagen1 = np.copy(imagen)
    #Una vez en escala de gris, se binariza la imagen mediante binarizacion OTSU.
    #Por eso, la variable tipo_umbral indica el tipo de umbralizacion que se quiere aplicar
    
    #Umbralizacion binaria
    if(tipo_umbral=='b'):
        ret,thresh = cv2.threshold(imagen1,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    
    #Umbralizacion binaria inversa
    elif (tipo_umbral=='binv'):
        ret,thresh = cv2.threshold(imagen1,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    
    #Umbralizacion Trunc
    elif(tipo_umbral=='t'):
        ret,thresh = cv2.threshold(imagen1,0,255,cv2.THRESH_TRUNC+cv2.THRESH_OTSU)
    
    #Umbralizacion Tozero    
    elif(tipo_umbral=='tz'):
        ret,thresh = cv2.threshold(imagen1,0,255,cv2.THRESH_TOZERO+cv2.THRESH_OTSU)
    
    #Umbralizacion Tozero inversa
    elif(tipo_umbral=='tzinv'):
        ret,thresh = cv2.threshold(imagen1,0,255,cv2.THRESH_TOZERO_INV+cv2.THRESH_OTSU)     
    #En el caso de que la imagen de entrada ya se encuentre binarizada, poner
    #en la variable tipo_umbral "none" para no aplicar binarizacion.
    
    #Se encuentran los contornos de la imagen:
    
    if (tipo_contorno=='ext'): #Solo los contornos externos
        contornos, hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    elif (tipo_contorno=='list'): #Todos los contornos (sin relacion de jerarquia)
        contornos, hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
   
    elif (tipo_contorno=='ccomp'): #Contornos externos e internos (huecos)[jerarquia de 2 niveles]
        contornos, hierarchy = cv2.findContours(thresh,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
   
    elif (tipo_contorno=='tree'): #Todos los contornos (con relación de jerarquía)
        contornos, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    if (escala_color==2):
        img_aux = cv2.cvtColor(imagen1, cv2.COLOR_GRAY2BGR)
    
    #Por ultimo, se dibuja los contornos de la imagen fuente,
    #se necesita que previamente este en color
    
    if (color_borde=='r'): #Rojo
        cv2.drawContours(img_aux, contornos, -1, (0,0,255), ancho_borde)
        
    elif (color_borde=='g'): #Verde
        cv2.drawContours(img_aux, contornos, -1, (0,255,0), ancho_borde)
        
    elif (color_borde=='b'): #Azul
        cv2.drawContours(img_aux, contornos, -1, (255,0,0), ancho_borde)
        
    elif (color_borde=='y'): #Amarillo
        cv2.drawContours(img_aux, contornos, -1, (0,255,255), ancho_borde)
        
    elif (color_borde=='c'): #Cyan
        cv2.drawContours(img_aux, contornos, -1, (255,255,0), ancho_borde)
    
    elif(color_borde=='m'): #Magenta
        cv2.drawContours(img_aux, contornos, -1, (255,0,255), ancho_borde)
    
    elif(color_borde=='o'): #Naranja
        cv2.drawContours(img_aux, contornos, -1, (0,125,255), ancho_borde) 
        
    elif(color_borde=='yg'): #Amarillo-Verde
        cv2.drawContours(img_aux, contornos, -1, (0,255,125), ancho_borde)
        
    elif(color_borde=='cg'): #(Cyan-Verde)
        cv2.drawContours(img_aux, contornos, -1, (125,255,0), ancho_borde) 
        
    elif(color_borde=='cb'): #(Cyan-Azul)
        cv2.drawContours(img_aux, contornos, -1, (255,125,0), ancho_borde)

    elif(color_borde=='p'): #Morado
        cv2.drawContours(img_aux, contornos, -1, (255,0,125), ancho_borde) 
    
    elif(color_borde=='rm'): #Rosado/Fucsia (Rojo-Magenta)
        cv2.drawContours(img_aux, contornos, -1, (125,0,255), ancho_borde)
                    
    elif(color_borde=='k'): #Negro
        cv2.drawContours(img_aux, contornos, -1, (0,0,0), ancho_borde) 
    
    return img_aux,contornos
import cv2
import numpy as np

def encontrar_bordes(imagen,tipo_umbral,color_borde,ancho_borde):
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
    
    #Se encuentran los contornos de la imagen
    contornos, hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    
    #Si la imagen de entrada estaba en escala de grises, se lo pasa a color
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
    
    return img_aux,contornos
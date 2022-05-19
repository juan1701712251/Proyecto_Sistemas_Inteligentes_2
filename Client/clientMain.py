from datetime import datetime

import cv2
import numpy as np
from Cutter import Cut
import os


nameWindow="Calculadora"
idNum = 0
fecha = datetime.now()
idCarpeta = 'Crops\\'+'CROP_FOLDER_'+fecha.strftime('DAY_%d_%m_%Y_HOUR_%H_%M_%S')
# Crear la carpeta
os.mkdir(idCarpeta)

def nothing(x):
    pass

def constructorVentana():
    cv2.namedWindow(nameWindow)
    cv2.createTrackbar("min",nameWindow,150,255,nothing)
    cv2.createTrackbar("max", nameWindow, 240, 255, nothing)
    cv2.createTrackbar("kernel", nameWindow, 0, 100, nothing)
    cv2.createTrackbar("areaMin", nameWindow, 5000, 10000, nothing)

def calcularAreas(figuras):
    areas=[]
    for figuraActual in figuras:
        areas.append(cv2.contourArea(figuraActual))
    return areas

def detectarForma(imagen):
    imagenGris = cv2.cvtColor(imagen,cv2.COLOR_BGR2GRAY)
    # imagenHSV = cv2.cvtColor(imagen,cv2.COLOR_BGR2HSV)
    # cv2.imshow("GRIS", imagenGris)
    # cv2.imshow("HSV",imagenHSV)

    min = cv2.getTrackbarPos("min", nameWindow)
    max = cv2.getTrackbarPos("max", nameWindow)

    bordes = cv2.Canny(imagenGris,min,max)

    tamañoKernel = cv2.getTrackbarPos("kernel", nameWindow)
    kernel = np.ones((tamañoKernel, tamañoKernel), np.uint8)
    bordes = cv2.dilate(bordes, kernel)

    # Filtro Gaussiano
    #blur = cv2.GaussianBlur(imagenGris,(5,5),0)
    #bordesBlur = cv2.Canny(imagenGris, min, max)
    #bordesBlur = cv2.dilate(bordesBlur, kernel)

    # cv2.imshow("bordes",bordes)
    # cv2.imshow("blur", bordesBlur)


    # Detección de la Figura
    figuras, jerarquia = cv2.findContours(bordes,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    areas = calcularAreas(figuras)
    areaMin = cv2.getTrackbarPos("areaMin", nameWindow)
    i = 0

    ROIsResult = []
    for figuraActual in figuras:
        if areas[i] >= areaMin:
            vertices = cv2.approxPolyDP(figuraActual, 0.05 * cv2.arcLength(figuraActual, True), True)
            mensaje = ''
            lv = len(vertices)
            if lv == 3:
                mensaje = 'triangulo'
            elif lv == 4:
                ROIsResult.append(figuraActual)
                mensaje = 'cuadrado'

            cv2.putText(imagen, mensaje, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.drawContours(imagen, [figuraActual], 0, (0, 0, 255), 2)
        i += 1
    return imagen, ROIsResult[:1]



# Apertura de la cámara
video = cv2.VideoCapture(0)
bandera = True
constructorVentana()


def recortarImagen(image,contours,idCarpeta,idNum):
    recortador = Cut()
    return recortador.crop(image,contours,idCarpeta,idNum)


while bandera:
    _,imagen = video.read()
    imagenCopia = np.copy(imagen)
    imagenContornos, countoursResultado = detectarForma(imagen)
    cv2.imshow("WebCam",imagenContornos)
    # Para programa
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        bandera = False
    elif k == 99:
        idNum = recortarImagen(imagenCopia,countoursResultado,idCarpeta,idNum)

video.release()
cv2.destroyAllWindows()
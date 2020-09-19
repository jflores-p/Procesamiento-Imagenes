import cv2
import numpy as np
import time


# valores HSV 

ROJO_LIMITE_BAJO = np.array([0, 0, 0])
ROJO_LIMITE_ALTO = np.array([15, 255, 255])

VERDE_LIMITE_BAJO = np.array([74, 0, 0])
VERDE_LIMITE_ALTO = np.array([120, 255, 255])

MORADO_LIMITE_BAJO = np.array([125, 0, 0])
MORADO_LIMITE_ALTO = np.array([180, 255, 255])


def  harryPotter(rutaVideo="", rutaAudio=""):
    # se carga la fuente del video
    if rutaVideo != "":
        video = cv2.VideoCapture(rutaVideo)
    else:
        video = cv2.VideoCapture(0)


    time.sleep(1)
    planoTrasero = 0

    # almacenando unas imagenes para reemplazar el fondo
    for i in range(60):
        videoSinTerminar, planoTrasero = video.read()
        if not videoSinTerminar:
            continue

    planoTrasero = np.flip(planoTrasero, axis=1)

    while(video.isOpened()):
        # captura de imagen actual
        videoSinTerminar, fotograma = video.read()
    
        if videoSinTerminar:
            fotograma = np.flip(fotograma, axis=1)
            # pasando de modelo BGR a HSV
            cpy = cv2.cvtColor(fotograma, cv2.COLOR_BGR2HSV)
            
            # mascara
            mascara1 = cv2.inRange(cpy, ROJO_LIMITE_BAJO, ROJO_LIMITE_ALTO) 

            # mascara del color a reemplazar
            mascara2 = cv2.inRange(cpy, MORADO_LIMITE_BAJO, MORADO_LIMITE_ALTO) 
            #mascara2 = cv2.inRange(cpy, VERDE_LIMITE_BAJO, VERDE_LIMITE_ALTO) 

            # sobreponiendo las mascaras
            mascara1 = mascara1 + mascara2
            # erosiona: borra un color a menos de que este este completamente rodeadeo por su mismo color
            # dilata: agrega una capa del mismo color a la silueta
            # morphologyEx: erosiona luego dilata
            mascara1 = cv2.morphologyEx(mascara1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2)

            # dilata una vez mas para que no se vea un borde del color a borrar 
            mascara1 = cv2.dilate(mascara1,np.ones((3, 3), np.uint8), iterations=2)
            
            # invierte los bits de la matriz
            mascara2 = cv2.bitwise_not(mascara1)

            # guarda los valores identicos en la misma posicion
            res1 = cv2.bitwise_and(planoTrasero, planoTrasero, mask = mascara1)
            res2 = cv2.bitwise_and(fotograma, fotograma, mask = mascara2)
            # junta el resultado de ambas modificaciones con el mismo valor de importancia
            finalOutput = cv2.addWeighted(res1, 1, res2, 1, 0)

            cv2.imshow("Magia de Harry Potter", finalOutput)
        else:
            print("LOOP")
            video.set(cv2.CAP_PROP_POS_FRAMES, 0)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    video.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    rutaVideo = "Tarea2.mp4"
    
    harryPotter(rutaVideo)


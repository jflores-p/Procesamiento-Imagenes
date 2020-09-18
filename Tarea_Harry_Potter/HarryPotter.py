import cv2
import numpy as np
import time

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

    for i in range(60):
        videoSinTerminar, planoTrasero = video.read()
        if not videoSinTerminar:
            continue

    planoTrasero = np.flip(planoTrasero, axis=1)

    while(video.isOpened()):
        videoSinTerminar, fotograma = video.read()
    
        if videoSinTerminar:
            fotograma = np.flip(fotograma, axis=1)
            cpy = cv2.cvtColor(fotograma, cv2.COLOR_BGR2HSV)
            
            mask1 = cv2.inRange(cpy, ROJO_LIMITE_BAJO, ROJO_LIMITE_ALTO) 

            # setting the lower and upper range for mask2  
            mask2 = cv2.inRange(cpy, MORADO_LIMITE_BAJO, MORADO_LIMITE_ALTO) 
            #mask2 = cv2.inRange(cpy, VERDE_LIMITE_BAJO, VERDE_LIMITE_ALTO) 

            mask1 = mask1 + mask2

            mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2)
            mask1 = cv2.dilate(mask1,np.ones((3, 3), np.uint8), iterations=2)
            mask2 = cv2.bitwise_not(mask1)

            res1 = cv2.bitwise_and(planoTrasero, planoTrasero, mask = mask1)
            res2 = cv2.bitwise_and(fotograma, fotograma, mask = mask2)
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


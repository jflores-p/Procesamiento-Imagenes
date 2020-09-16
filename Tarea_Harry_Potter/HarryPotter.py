import cv2
import numpy as np
import matplotlib.pylab as plt

def plotImage(layout, img, text):
    plt.subplot(layout)
    plt.axis('off')
    plt.title(text)
    plt.imshow(img, cmap='gray')

def hacerTransparente


def  harryPotter(rutaVideo="", rutaAudio=""):
    # se carga la fuente del video
    if ruta_video != "":
        video = cv2.VideoCapture(rutaVideo)
    else:
        video = cv2.VideoCapture(0)

    while(True):
        videoSinTerminar, fotograma = video.read()
    
        if videoSinTermina:
            cpy = fotograma.copy()
            cpy = cv2.cvtColor(cpy, cv2.COLOR_RGB2BGR)

            cpy[:,:,2] = 0
            cpy[:,:,1] = 0

            cv2.imshow("Magia de Harry Potter", cpy)
        else:
            print("LOOP")
            video.set(cv2.CAP_PROP_POS_FRAMES, 0)

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break


    video.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    rutaVideo = "Tarea2.mp4"
    
    harryPotter(rutaVideo)


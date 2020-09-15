import cv2
import numpy as np
from pygame import mixer

# aplicacion de correlacion de Pearson
# cada vez que se mencione 'matriz', se hace referencia a un arreglo de 'n' dimensiones 
def dif_entre_fotogramas(fotograma_ant, fotograma_post):
    # resta los arreglos del fotograma actual y el fotograma anterior para tener sus varianzas
    dif = fotograma_post - fotograma_ant

    # aplica la funcion del coeficiente de correlacion de Pearson a cada alemento de la matriz,
    # regresa una matriz del las mismas dimensiones, donde cada elemento de la matriz
    # es el coeficiente resultado de dicha posicion de la matriz original
    pearson = np.corrcoef(dif)

    # se saca la media de la matriz de los coeficientes para obtener valor general de los cambios
    # ocurridos entre un fotograma y otro
    media = np.sum(pearson) / (dif.shape[0] * dif.shape[1])
    
    # retornamos la media
    return media

    
# inicializar la musica
def init_music(ruta_audio):
    mixer.init()
    mixer.music.load(ruta_audio)
    mixer.music.play(-1)
    mixer.music.set_volume(0)

# separa la matriz de la imagen segun los filtros
def partir_imagen_mitad_v(arr_fuente, GRIS=True, LADO='d'):
    width = len(arr_fuente[0])
    
    # copia la matriz tomando todo el 'alto' y la mitad derecha del 'ancho'
    if LADO == 'd':
        arr_destino = arr_fuente[:, width//2:width]

    # copia la matriz tomando todo el 'alto' y la mitad izquierda del 'ancho'
    elif LADO == 'i':
        arr_destino = arr_fuente[:, 0:width//2]

    # convierte la matriz de 3 dimensiones RGB a 1 dimension Escala-de-grises
    if GRIS:
        arr_destino =  cv2.cvtColor(arr_destino, cv2.COLOR_RGB2GRAY)

    return arr_destino

# funcion principal de la demostracion
def  tikTok(ruta_video="", ruta_audio="", estandar_de_cambio=0.028):
    # se carga la fuente del video
    if ruta_video != "":
        video = cv2.VideoCapture(ruta_video)
    else:
        video = cv2.VideoCapture(0)

    # inicializa la musica, en teoria funciona, pero nunca se cerraba en mi computadora,
    # asi que todo lo relacionado con el 'mixer.music' esta comentado
    #init_music(ruta_audio)
    
    # establece el primer fotograma, como referencia para el inicio del ciclo
    # se vuelve obsoleto, ya que no se muestra
    _, primer_fotograma =  video.read()
    gris_prev = partir_imagen_mitad_v(primer_fotograma)

    # loop principal
    while(True):
        video_sin_terminar, fotograma = video.read()

        if video_sin_terminar: 
            # se extraen las dos partes de la imagen buscada
            rgb_actual = partir_imagen_mitad_v(fotograma, GRIS=False, LADO='i')
            gris_actual = partir_imagen_mitad_v(fotograma)
            
            # si la diferencia entre fotogramas es superior a una media minima (valor que corresponde a un cambio minimo en las matrices en promedio)
            # significa que hubo un cambio significativo de un fotograma a otro
            # por lo tanto suena la musica
            if dif_entre_fotogramas(gris_prev, gris_actual) > estandar_de_cambio:
                print("movimiento considerble")
                #mixer.music.set_volume(1)
            else:
                print("\n")
                #mixer.music.set_volume(0)

            # actualizamos el fotograma anterior
            gris_prev = gris_actual
            
            # convertimos la matriz de grises a tres dimensiones para poder juntarla con la imagen a color
            gris_actual = cv2.merge((gris_actual, gris_actual, gris_actual))
            
            # juntamos las imagenes
            img_actual = cv2.hconcat((rgb_actual, gris_actual))

            # mostramos las imagenes concatenadas
            cv2.imshow("hello", img_actual)
        
        # si el video acaba, se repite
        else:            
            print("LOOP")
            video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
        # condicion de salida, que termina la musica(de estar sonando)
        # cambiar el waitkey para que se reproduzca mas rapido o mas lento el video
        if cv2.waitKey(1) & 0xFF == ord('q'):
            #mixer.music.stop()
            break

    # cierra el archivo del video
    video.release()
    # cierra la donde se mostraban las imagenes 
    cv2.destroyAllWindows()


if  __name__ == "__main__":

    ruta_video = "Tarea1.mp4"
    ruta_audio = "Take_on_me.wav"
    media_de_cambio = 0.027

    tikTok(ruta_video, ruta_audio, media_de_cambio)

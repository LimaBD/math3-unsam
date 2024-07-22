import cv2
from ffpyplayer.player import MediaPlayer
import os
import time
import traceback

PANTALLA_ANCHO = 1920
PANTALLA_ALTO = 1080
MULTIPLE_PANTALLAS = False
CON_FUNDIDO = False
REDIMENCIONAR_VIDEOS = False
BASE_PATH = os.path.dirname(__file__)

def abrir_captura(video):
    """Abre un video y devuelve el objeto de video"""
    if video.startswith("/"):
        video = video[1:]
    if not video.lower().startswith("c"):
        video = os.path.join(BASE_PATH, video)
    cap = cv2.VideoCapture(video)
    if not cap.isOpened():
        raise Exception(f"Error abriendo video {video}")
    return cap

def leer_frame(cap):
    """Lee un frame de un video, si no hay, devuelve el ultimo"""
    reproduciendo, frame = cap.read()
    if not reproduciendo:
        cap.set(cv2.CAP_PROP_POS_FRAMES, cap.get(cv2.CAP_PROP_FRAME_COUNT)-1)
        _, frame = cap.read()
    return reproduciendo, frame

def leer_frame_en_loop(cap):
    """Obtiene frame de video, si no hay, vuelve al principio"""
    reproduciendo, frame = cap.read()
    if not reproduciendo:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        _, frame = cap.read()
    return reproduciendo, frame

class Ventana:

    def __init__(self, nombre):
        """Inicializa una ventana"""
        self.nombre = nombre
        self.ancho = PANTALLA_ANCHO
        self.alto = PANTALLA_ALTO
        cv2.namedWindow(self.nombre, cv2.WINDOW_NORMAL)
        self.posicion(0, 0)
        self.dimensiones(self.ancho, self.alto)

    def titulo(self, titulo):
        """Cambia el titulo de la ventana"""
        cv2.setWindowTitle(self.nombre, titulo)
        return self

    def posicion(self, x, y):
        """Cambia la posicion de la ventana"""
        cv2.moveWindow(self.nombre, int(x), int(y))
        return self

    def dimensiones(self, ancho, alto):
        """Cambia las dimensiones de la ventana"""
        self.ancho = int(ancho)
        self.alto = int(alto)
        cv2.resizeWindow(self.nombre, self.ancho, self.alto)
        return self

    def hacer_pantalla_completa(self):
        cv2.namedWindow(self.nombre)
        cv2.namedWindow(self.nombre, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(self.nombre, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        return self

    def mostrar(self, frame, resize):
        if resize:
            frame = cv2.resize(frame, (self.ancho, self.alto))
        cv2.imshow(self.nombre, frame)

class Reproductor:

    def __init__(self):
        """Inicializa las ventanas"""
        self.ventana_principal = Ventana('Principal')
        self.ventana_derecha = Ventana('Opcion derecha')
        self.ventana_izquierda = Ventana('Opcion izquierda')
        #
        self.redimenciar_ventanas = REDIMENCIONAR_VIDEOS
        if MULTIPLE_PANTALLAS:
            self.ventana_principal \
                .posicion(0, 0) \
                .hacer_pantalla_completa()
            self.ventana_derecha \
                .posicion(-PANTALLA_ANCHO, 0) \
                .hacer_pantalla_completa()
            self.ventana_izquierda \
                .posicion(+PANTALLA_ALTO, 0) \
                .hacer_pantalla_completa()
        else:
            ventana_ancho = PANTALLA_ANCHO // 3
            ventana_altura = PANTALLA_ALTO // 2
            self.ventana_principal \
                .posicion(ventana_ancho, 0) \
                .dimensiones(ventana_ancho, ventana_altura)
            self.ventana_derecha \
                .posicion(ventana_ancho+ventana_ancho/2, ventana_altura) \
                .dimensiones(ventana_ancho, ventana_altura)
            self.ventana_izquierda \
                .posicion(ventana_ancho/2, ventana_altura) \
                .dimensiones(ventana_ancho, ventana_altura)
            self.redimenciar_ventanas = True

    def obtener_opciones(self, camino):
        opcion_derecha = None
        opcion_izquierda = None
        if camino.derecho and camino.izquierdo:
            opcion_derecha = camino.derecho
            opcion_izquierda = camino.izquierdo
        elif camino.centro:
            opcion_derecha = camino.centro
            opcion_izquierda = camino.centro
        else:
            raise Exception("Camino sin opciones")
        return opcion_derecha, opcion_izquierda

    def set_titulo_ventanas(self, camino):
        opcion_derecha, opcion_izquierda = self.obtener_opciones(camino)
        self.ventana_principal.titulo(camino.nombre)
        self.ventana_derecha.titulo(f"Opcion derecha de: {opcion_derecha.nombre}")
        self.ventana_izquierda.titulo(f"Opcion izquierda de: {opcion_izquierda.nombre}")

    def reproducir(
            self,
            camino,
            captura_opciones_al_reproducir,
            captura_en_pausa,
            imagen_fundido
            ):
        """Reproduce video en 3 ventanas diferentes"""
        assert isinstance(camino, Camino)
        print(
            "==========================================================\n"
            f"Camino titulo: {camino.nombre}\n"
            )
        camino_resultado = None
        self.set_titulo_ventanas(camino)
        opcion_derecha, opcion_izquierda = self.obtener_opciones(camino)
        # Seleccionamos la captura inicial del video principal
        indice_video_principal = 0
        captura_principal, audio_principal = camino.obtener_video_audio(indice_video_principal)
        audio_principal.set_pause(False)
        # Empezamos la reproduccion de video
        pausa = False
        reproduciendo_principal = True
        # Flags para mostrar el fundido
        derecha_seleccionada = False
        izquierda_seleccionada = False
        fundido_frames_restantes = 1
        while True:
            # Mostramos el fundido si se selecciono una opcion
            if derecha_seleccionada:
                _, frame_izquierda = leer_frame_en_loop(captura_opciones_al_reproducir)
                frame_derecha = imagen_fundido
            elif izquierda_seleccionada:
                _, frame_derecha = leer_frame_en_loop(captura_opciones_al_reproducir)
                frame_izquierda = imagen_fundido
            # Videos de las opciones secundarias cuando
            # finalizo de reproducir el video principal
            elif not reproduciendo_principal:
                _, frame_derecha = leer_frame_en_loop(opcion_derecha.video_opcion)
                _, frame_izquierda = leer_frame_en_loop(opcion_izquierda.video_opcion)
            # Videos de las opciones secundarias cuando esta en pausa
            elif pausa:
                _, frame_en_pausa = leer_frame_en_loop(captura_en_pausa)
                frame_derecha = frame_en_pausa
                frame_izquierda = frame_en_pausa
            # Videos de las opciones secundarias cuando se
            # esta reproduciendo el video principal
            else:
                _, frame_opciones_al_reproducir = leer_frame_en_loop(captura_opciones_al_reproducir)
                frame_derecha = frame_opciones_al_reproducir
                frame_izquierda = frame_opciones_al_reproducir
            # Mostramos los frames de las opciones
            self.ventana_derecha.mostrar(frame_derecha, self.redimenciar_ventanas)
            self.ventana_izquierda.mostrar(frame_izquierda, self.redimenciar_ventanas)
            # Al haber seleccionado una opcion, no queremos que se
            # cambien los frames o se presione otra cosa
            if derecha_seleccionada or izquierda_seleccionada:
                if fundido_frames_restantes > 0:
                    fundido_frames_restantes -= 1
                    _ = cv2.waitKey(25)
                    continue
                else:
                    break
            # Carga los frames de la ventana principal
            # Para pausar no actualizamos el frame principal y listo
            if not pausa:
                reproduciendo_principal, frame_principal = leer_frame(captura_principal)
                self.ventana_principal.mostrar(frame_principal, self.redimenciar_ventanas)
                if not reproduciendo_principal:
                    audio_principal.set_pause(True)
                    # Cargamos siguiente video principal si hay
                    if indice_video_principal + 1 < len(camino.videos):
                        indice_video_principal += 1
                        captura_principal, audio_principal = camino.obtener_video_audio(indice_video_principal)
                        audio_principal.set_pause(False)
                        reproduciendo_principal = True
            # Seteamos estado del audio
            audio_principal.set_pause((reproduciendo_principal and pausa) or not reproduciendo_principal)
            # Acciones de teclas
            key = cv2.waitKey(25) & 0xFF
            if key:
                if key == ord('q'): # para salir
                    camino_resultado = None
                    break
                if reproduciendo_principal and key == ord('p'): # para pausar
                    pausa = not pausa
                    continue
                if key == ord('a'): # para ir a la izquierda
                    camino_resultado = opcion_izquierda
                    izquierda_seleccionada = True
                    if not CON_FUNDIDO:
                        break
                    continue
                if key == ord('d'): # para ir a la derecha
                    camino_resultado = opcion_derecha
                    derecha_seleccionada = True
                    if not CON_FUNDIDO:
                        break
                    continue
                if camino.con_padre and key == ord('v'): # para volver al video anterior
                    camino_resultado = camino.padre
                    break
                if key == ord('r'): # para reiniciar el video
                    camino_resultado = camino
                    break
        audio_principal.set_pause(True)
        audio_principal.close_player()
        return camino_resultado

class Camino:

    def __init__(self, nombre, con_padre=True):
        self.nombre = nombre
        self.videos = None
        self.audios = None
        self.video_opcion = None
        self.con_padre = con_padre
        self.padre = None
        self.centro = None
        self.izquierdo = None
        self.derecho = None

    def set_videos(self, videos):
        assert isinstance(videos, list)
        self.videos = []
        self.audios = []
        for video in videos:
            self.videos.append(abrir_captura(video))
            self.audios.append(video) # NOTE: no funciona bien si instanciamos el MediaPlayer aca
        return self

    def set_video_opcion(self, video):
        assert isinstance(video, str)
        self.video_opcion = abrir_captura(video)
        return self

    def set_padre(self, camino):
        if self.con_padre:
            assert isinstance(camino, Camino)
            self.padre = camino
        return self

    def set_izquierdo(self, camino):
        assert isinstance(camino, Camino)
        camino.set_padre(self)
        self.izquierdo = camino
        return self

    def set_derecho(self, camino):
        assert isinstance(camino, Camino)
        camino.set_padre(self)
        self.derecho = camino
        return self

    def set_centro(self, camino):
        assert isinstance(camino, Camino)
        camino.set_padre(self)
        self.centro = camino
        return self

    def liberar_recursos(self):
        if self.videos:
            for video in self.videos:
                video.release()
        if self.audios:
            for audio in self.audios:
                audio.close_player()
        if self.centro:
            self.centro.liberar_recursos()
        if self.izquierdo:
            self.izquierdo.liberar_recursos()
        if self.derecho:
            self.derecho.liberar_recursos()

    def obtener_video_audio(self, index):
        video = self.videos[index]
        video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        # NOTE: Instaciamos aca el MediaPlayer para evitar problemas con el audio
        audio = MediaPlayer(self.audios[index])
        audio.set_pause(True)
        return video, audio

class Senderos:

    def __init__(self):
        self.reproductor = Reproductor()
        self.camino_inicial = self.construir_caminos()
        self.cap_en_pausa = abrir_captura("videos/PAUSA.avi")
        self.cap_opciones_durante_reproduccion = abrir_captura("videos/MENU_test.mp4")
        self.fundido_imagen = cv2.imread(os.path.join(BASE_PATH, "imagenes/Blanco.png"))

    def construir_caminos(self):
        # Caminos que tendremos
        menu = Camino("menu", con_padre=False)
        sotano = Camino("sotano")
        examinar = Camino("examinar")
        ignorar = Camino("ignorar")
        dejar_ir = Camino("dejar ir")
        insistir = Camino("insistir")
        recordar = Camino("recordar")
        olvidar = Camino("olvidar")
        irse = Camino("irse")
        suicidarse = Camino("suicidarse")

        # Agregamos los videos principales de cada camino
        menu.set_videos(["videos/MENU_test.mp4"])
        sotano.set_videos(["videos/radio 1_2_parte1.mp4", "videos/radio 1_2_parte2.mp4", "videos/radio 1_2_parte3.mp4"])
        examinar.set_videos(["videos/Camino3_Examinar.avi"])
        ignorar.set_videos(["videos/Camino3_Ignorar.avi"])
        dejar_ir.set_videos(["videos/4_Dejar_ir.avi"])
        insistir.set_videos(["videos/4_interactuar.avi"])
        recordar.set_videos(["videos/8_FINAL.mp4"])
        olvidar.set_videos(["videos/7_FINAL.mp4"])
        irse.set_videos(["videos/6_FINAL.mp4"])
        suicidarse.set_videos(["videos/FINAL4_AUTO_AGUA.avi"])

        # Agregamos los videos de opcion para cada camino
        sotano.set_video_opcion("videos/MENUPRINCIPAL.mp4")
        examinar.set_video_opcion("videos/EXAMINAR.avi")
        ignorar.set_video_opcion("videos/IGNORAR.avi")
        dejar_ir.set_video_opcion("videos/DEJAR IR.avi")
        insistir.set_video_opcion("videos/INSISTIR.avi")
        recordar.set_video_opcion("videos/RECORDAR.avi")
        olvidar.set_video_opcion("videos/OLVIDAR.avi")
        irse.set_video_opcion("videos/IRSE.avi")
        suicidarse.set_video_opcion("videos/SUICIDARSE.avi")

        # Unimos los caminos
        comienzo = menu
        menu.set_centro(sotano)
        sotano.set_izquierdo(examinar).set_derecho(ignorar)
        examinar.set_centro(dejar_ir)
        ignorar.set_centro(insistir)
        dejar_ir.set_izquierdo(recordar).set_derecho(olvidar)
        insistir.set_izquierdo(irse).set_derecho(suicidarse)
        recordar.set_centro(menu)
        olvidar.set_centro(menu)
        irse.set_centro(menu)
        suicidarse.set_centro(menu)

        return comienzo

    def reproducir(self):
        siguiente_camino = self.camino_inicial
        while True:
            siguiente_camino = self.reproductor.reproducir(
                siguiente_camino,
                self.cap_opciones_durante_reproduccion,
                self.cap_en_pausa,
                self.fundido_imagen
            )
            if siguiente_camino is None:
                break

    def liberar_recursos(self):
        self.camino_inicial.liberar_recursos()
        self.cap_en_pausa.release()
        self.cap_opciones_durante_reproduccion.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    senderos = Senderos()

    # Se reproduce infinitamente hasta
    # que se presione Ctrl+C
    while True:
        try:
            senderos.reproducir()
        except KeyboardInterrupt:
            break
        except Exception as e:
            print("==========================================================")
            print("Se reiniciara en 5 segundos debido a un error")
            traceback.print_tb(e.__traceback__)
            time.sleep(5)

    senderos.liberar_recursos()

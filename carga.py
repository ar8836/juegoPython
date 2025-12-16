# Este sera una libreria de carga de imagenes y sonidos

import glfw
import pygame
import os
import time
from PIL import Image 
from OpenGL.GL import *

# =============== Directorios ===================
# Cambiar el directorio base a "/home/javier/Documentos/Programas/Python/"

RUTA_BASE = "/home/ariel/Programacion/Python/juegoPython"
# Sonidos funcionales pero solo son temporales, despues los cambiare por otros
RUTA_AMBIENTE1 = "/home/ariel/Programacion/Python/juegoPython/sounds/ambiente1.mp3"
RUTA_DISPARO1 = "/home/ariel/Programacion/Python/juegoPython/sounds/disparo1.mp3"
RUTA_RECARGA1 = "/home/ariel/Programacion/Python/juegoPython/sounds/recarga1.mp3"

# Variable global para almacenar el objeto de sonido de Pygame
sonido_disparo = None
sonido_recarga = None
va_hacia_la_derecha = False

def inicializar_pygame_sonido():
    """
    Inicializa el módulo de mezclador de Pygame y carga el efecto de sonido.
    """
    global sonido_disparo, sonido_recarga
    try:
        # Inicializar solo el módulo de mezclador (mixer) de Pygame
        pygame.mixer.init(44100, -16, 2, 2048)
        print(f"Buscando sonido en: {RUTA_DISPARO1}")

        if not os.path.exists(RUTA_DISPARO1):
            print(f"ERROR: Archivo de sonido no encontrado en la ruta: {RUTA_DISPARO1}")
            print(f"Asegúrate de que 'disparo1.mp3' esté en la carpeta 'sounds'.")
            return
        sonido_disparo = pygame.mixer.Sound(RUTA_DISPARO1)

        if not os.path.exists(RUTA_RECARGA1):
            print(f"ERROR: Archivo de sonido no encontrado en la ruta: {RUTA_RECARGA1}")
            print(f"Asegúrate de que 'recarga1.mp3' esté en la carpeta 'sounds'.")
            return
        sonido_recarga = pygame.mixer.Sound(RUTA_RECARGA1)

        # --- 2. CARGA Y REPRODUCCIÓN DE MÚSICA DE AMBIENTE1 (gestionado por mixer.music) ---
        print(f"Buscando música de ambiente en: {RUTA_AMBIENTE1}")
        if not os.path.exists(RUTA_AMBIENTE1):
            print(f"ERROR: Música de ambiente no encontrada en: {RUTA_AMBIENTE1}")
        else:
            # Cargar la música
            pygame.mixer.music.load(RUTA_AMBIENTE1)
            # Reproducir la música en bucle infinito (-1)
            pygame.mixer.music.play(-1)
            print("Música de ambiente iniciada en bucle.")

        print("Módulo de sonido de Pygame inicializado y sonido cargado.")

    except pygame.error as e:
        print(f"Error al inicializar Pygame Mixer o cargar el sonido: {e}")
        print("Verifica el archivo de sonido y la instalación de Pygame/SDL.")

def key_callback(window, key, scancode, action, mods):
    """
    Función de callback de teclado que reproduce el sonido al presionar ESPACIO.
    """
    global sonido_disparo, sonido_recarga

    # Solo procesamos eventos cuando la tecla es PRESIONADA o REPETIDA
    if action == glfw.PRESS or action == glfw.REPEAT:

        if key == glfw.KEY_SPACE:
            print("Tecla ESPACIO presionada. Reproduciendo sonido de disparo...")

            if sonido_disparo:
                # Reproducir el sonido
                sonido_disparo.play()
            else:
                print("Advertencia: El sonido no pudo ser cargado o inicializado.")

        if key == glfw.KEY_R:
            print("Tecla R presionada. Reproduciendo sonido de recarga del airma...")
            sonido_recarga.play()
        else:
            print("Advertencia: El sonido no pudo ser cargado o inicializado.")

        # Movimiento con teclas
        if key == glfw.PRESS:
            y += velocidad

        if key == glfw.PRESS:
            y -= velocidad

        if key == glfw.PRESS:
            x -= velocidad

        if key == glfw.PRESS:
            x += velocidad

        if key == glfw.KEY_ESCAPE:
            print("Escape presionado - Cerrando ventana")
            glfw.set_window_should_close(window, True)

        # Dibujar el sprite
        glBindTexture(GL_TEXTURE_2D, sprites[frame])
        dibujar_poligono(x, y, 0.15, 0.15)

# ======================= CARGAR FONDOS ==========================

def cargar_sprites_base(ruta_base_dir, num_imagenes):
    """ Función auxiliar para cargar una secuencia de sprites numerados 1.png a N.png. """
    ruta_base = os.path.join(os.path.expanduser('~'), ruta_base_dir)
    rutas = []
    
    for i in range(1, num_imagenes + 1):
        # Utilizando f-string para construir la ruta (e.g., .../cielo/1.png)
        ruta_completa = os.path.join(ruta_base, f"{i}.png")
        rutas.append(ruta_completa)
        
    sprites = [cargar_textura(r) for r in rutas]
    
    # Inicialización de variables de posición/animación
    frame = 0 
    velocidad_anim = 0.12
    ultimo_tiempo = time.time()
    x = 0.0 
    y = 0.0 
    velocidad = 0.03
    
    return sprites, x, y, velocidad, frame, velocidad_anim, ultimo_tiempo

def dibujar_escena():
    """
    Función de dibujo de la escena de OpenGL. Utiliza glBegin/glEnd.
    """
    # Establecer el color de fondo (negro)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    glBegin(GL_QUADS)
    glColor3f(1.0, 1.0, 1.0)
    glVertex2f(-0.2, 0.2)
    glVertex2f( 0.2, 0.2)
    glVertex2f( 0.2, -0.2)
    glVertex2f(-0.2, -0.2)
    glEnd()

def dibujar_poligono(x, y, w, h):
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(x - w, y - h)
    glTexCoord2f(1, 0); glVertex2f(x + w, y - h)
    glTexCoord2f(1, 1); glVertex2f(x + w, y + h)
    glTexCoord2f(0, 1); glVertex2f(x - w, y + h)
    glEnd()

def cargar_textura(ruta):
    """ Función para cargar textura, expandiendo el '~' en la ruta. """
    ruta_absoluta = os.path.expanduser(ruta)
    
    # Manejo de error si el archivo no existe
    if not os.path.exists(ruta_absoluta):
        print(f"ERROR: Archivo de textura no encontrado: {ruta_absoluta}")
        return 0 # Devolver 0 (ID de textura inválido)
        
    imagen = Image.open(ruta_absoluta).transpose(Image.FLIP_TOP_BOTTOM)
    img_data = imagen.convert("RGBA").tobytes()
    width, height = imagen.size

    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0,
                 GL_RGBA, GL_UNSIGNED_BYTE, img_data)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    return tex_id

def cargar_fondo():
    # Hay 40 imagenes en .../images/cielo que se llaman 1.png, 2.png, 3.png y asi hasta 40.png
    return cargar_sprites_base("Programacion/Python/juegoPython/images/cielo", 40)

def cargar_mc():    # Carga los sprites de animacion del "Main Character" mientras cae en picada.
    # Hay 40 imagenes en .../images/pato que se llaman 1.png, 2.png, 3.png y asi hasta 40.png
    return cargar_sprites_base("Programacion/Python/juegoPython/images/pato", 40)

def cargar_mc_principio():
    # Hay 25 imagenes en .../images/pato_acostado que se llaman 1.png, 2.png, 3.png y asi hasta 25.png
    return cargar_sprites_base("Programacion/Python/juegoPython/images/pato_acostado", 25)

def cargar_pantano_1():
    # Se necesita saber cuántas imágenes hay en total. Asumo 10 como ejemplo.
    return cargar_sprites_base("Programacion/Python/juegoPython/images/pantano_1", 10)

def cargar_pantano_2():
    # Se necesita saber cuántas imágenes hay en total. Asumo 10 como ejemplo.
    return cargar_sprites_base("Programacion/Python/juegoPython/images/pantano_2", 10)

def cargar_avion():
    # Hay 169 imagenes en .../images/avion
    return cargar_sprites_base("Programacion/Python/juegoPython/images/avion", 169)

def cargar_globo_a():
    # Hay 98 imagenes en .../images/globo_a
    return cargar_sprites_base("Programacion/Python/juegoPython/images/globo_a", 98)

def cargar_globo_m():
    # Hay 40 imagenes en .../images/globo_m
    return cargar_sprites_base("Programacion/Python/juegoPython/images/globo_m", 40)

def cargar_power1():
    # Hay 5 imagenes en .../images/power_azul
    return cargar_sprites_base("Programacion/Python/juegoPython/images/power_azul", 5)

def cargar_power2():
    # Hay 5 imagenes en .../images/power_morado
    return cargar_sprites_base("Programacion/Python/juegoPython/images/power_morado", 5)

def cargar_power3():
    # Hay 5 imagenes en .../images/power_rojo
    return cargar_sprites_base("Programacion/Python/juegoPython/images/power_rojo", 5)

# Esto lo debe de llevar ?????
def programa_principal():

    # Inicializar Pygame Mixer y cargar el sonido
    inicializar_pygame_sonido()

    # Inicializar GLFW y crear la ventana
    try:
        ventana = iniciar_ventana()
    except Exception as e:
        print(f"Error fatal al iniciar la ventana: {e}")
        pygame.mixer.quit()
        return

    # Registrar la función de callback de teclado
    glfw.set_key_callback(ventana, key_callback)

    # Bucle principal de renderizado
    while not glfw.window_should_close(ventana):

        # Dibujar la escena
        # dibujar_escena()

        # Intercambiar búferes para mostrar el resultado
        glfw.swap_buffers(ventana)

        # Procesar eventos (teclado, ratón, etc.)
        glfw.poll_events()

    # Terminar GLFW y Pygame Mixer
    pygame.mixer.quit()
    glfw.terminate()





















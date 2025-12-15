# Este sera una libreria de carga de imagenes y sonidos

"""
Programa que combina GLFW (para la ventana/OpenGL 3.3 Compatibility) y Pygame (para el sonido).
Muestra una ventana y reproduce el sonido al presionar la tecla ESPACIO.

Ruta del sonido: ~/Programacion/Python/juegoPython/sounds/disparo1.mp3
"""

import glfw
import pygame
import os

# --- Configuración de Archivos y Directorios ---

RUTA_AMBIENTE1 = "/home/ariel/Programacion/Python/juegoPython/sounds/ambiente1.mp3"
RUTA_DISPARO1 = "/home/ariel/Programacion/Python/juegoPython/sounds/disparo1.mp3"
RUTA_RECARGA1 = "/home/ariel/Programacion/Python/juegoPython/sounds/recarga1.mp3"

# Variable global para almacenar el objeto de sonido de Pygame
sonido_disparo = None
sonido_recarga = None

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

def iniciar_ventana():

    if not glfw.init():
        raise Exception("No se pudo iniciar GLFW")

    # Solicitamos una versión moderna (3.3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)

    # Forzamos el Perfil de Compatibilidad.
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_COMPAT_PROFILE)

    ventana = glfw.create_window(800, 600, "OpenGL 3.3 Compatibility + Sonido Pygame", None, None)

    if not ventana:
        glfw.terminate()
        raise Exception("No se pudo crear la ventana GLFW")

    glfw.make_context_current(ventana)
    return ventana

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

        if key == glfw.KEY_ESCAPE:
            print("Escape presionado - Cerrando ventana")
            glfw.set_window_should_close(window, True)

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


# Llamado al programa principal de control
if __name__ == "__main__":
    programa_principal()



















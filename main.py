"""
Programa que combina GLFW (para la ventana/OpenGL) y Pygame (para el sonido).
Muestra una ventana y reproduce un sonido al presionar la tecla ESPACIO.

Ruta esperada del sonido:
~/Programacion/Python/juegoPython/sounds/disparo.wav
"""

import glfw
from OpenGL.GL import *
import pygame
import os

# --- Configuración de Archivos y Directorios ---
# Obtener la ruta del directorio actual del script para construir la ruta del sonido.
# NOTA: En un entorno real, es mejor usar rutas absolutas o relativas al script principal.
DIRECTORIO_BASE = os.path.dirname(os.path.abspath(__file__))
# Si el script se ejecuta directamente desde el directorio:
# ~/Programacion/Python/juegoPython/
# La ruta del sonido será:
RUTA_SONIDO = os.path.join(DIRECTORIO_BASE, 'sounds', 'disparo.wav')
# Si el script estuviera, por ejemplo, en 'src/', ajústalo:
# RUTA_SONIDO = os.path.join(DIRECTORIO_BASE, '..', 'sounds', 'disparo.wav')
# Para este ejemplo, asumiremos que el script está al mismo nivel que la carpeta 'sounds'.

# Variable global para almacenar el objeto de sonido de Pygame
sonido_disparo = None


def inicializar_pygame_sonido():
    """
    Inicializa el módulo de mezclador de Pygame y carga el efecto de sonido.
    """
    global sonido_disparo
    try:
        # Inicializar solo el módulo de mezclador (mixer) de Pygame
        pygame.mixer.init() 
        print(f"Buscando sonido en: {RUTA_SONIDO}")
        
        # Cargar el sonido
        if not os.path.exists(RUTA_SONIDO):
            print(f"ERROR: Archivo de sonido no encontrado en la ruta: {RUTA_SONIDO}")
            print("Asegúrate de que 'disparo.wav' esté en la carpeta 'sounds'.")
            return
            
        sonido_disparo = pygame.mixer.Sound(RUTA_SONIDO)
        print("Módulo de sonido de Pygame inicializado y sonido cargado.")
        
    except pygame.error as e:
        print(f"Error al inicializar Pygame Mixer o cargar el sonido: {e}")
        print("Asegúrate de que el archivo de sonido no esté corrupto y que Pygame esté instalado correctamente.")


def iniciar_ventana():
    """
    Inicializa una ventana GLFW/OpenGL.
    :return: La ventana GLFW.
    """
    if not glfw.init():
        raise Exception("No se pudo iniciar GLFW")
    
    # Usamos GLUT como referencia, pero GLFW es el estándar moderno en Python.
    # El módulo 'PyOpenGL' (`from OpenGL.GL import *`) nos da las funciones de GLUT/OpenGL.
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    
    ventana = glfw.create_window(800, 600, "Ventana OpenGL con Sonido Pygame", None, None)
    
    if not ventana:
        glfw.terminate()
        raise Exception("No se pudo crear la ventana GLFW")
        
    glfw.make_context_current(ventana)
    return ventana


def key_callback(window, key, scancode, action, mods):
    """
    Función de callback de teclado que se llama cuando se presiona o suelta una tecla.
    """
    global sonido_disparo
    
    # Solo procesamos eventos cuando la tecla es PRESIONADA o REPETIDA
    if action == glfw.PRESS or action == glfw.REPEAT:
        
        if key == glfw.KEY_SPACE:
            print("Tecla ESPACIO presionada. Reproduciendo sonido...")
            
            if sonido_disparo:
                # Reproducir el sonido
                sonido_disparo.play()
            else:
                print("Advertencia: El sonido no pudo ser cargado o inicializado.")

        elif key == glfw.KEY_ESCAPE:
            print("Escape presionado - Cerrando ventana")
            glfw.set_window_should_close(window, True)
            
        else:
            print(f"Tecla presionada: {key}")


def dibujar_escena():
    """
    Función de dibujo de la escena de OpenGL. Dibuja un cuadrado simple.
    """
    # Establecer el color de fondo (negro)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    
    # Dibujar un cuadrado blanco simple en el centro
    glBegin(GL_QUADS)
    glColor3f(1.0, 1.0, 1.0)
    glVertex2f(-0.2, 0.2)
    glVertex2f( 0.2, 0.2)
    glVertex2f( 0.2, -0.2)
    glVertex2f(-0.2, -0.2)
    glEnd()


def programa_principal():
    
    # 1. Inicializar Pygame Mixer y cargar el sonido
    inicializar_pygame_sonido()
    
    # 2. Inicializar GLFW y crear la ventana
    ventana = iniciar_ventana()
    
    # 3. Registrar la función de callback de teclado
    glfw.set_key_callback(ventana, key_callback)
    
    # Bucle principal de renderizado
    while not glfw.window_should_close(ventana):
        
        # Dibujar la escena
        dibujar_escena()
        
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


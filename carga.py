import glfw
from OpenGL.GL import *
from PIL import Image
import os
import pygame

RUTA_BASE = "/home/ariel/Programacion/Python/juegoPython"

# Variables globales de sonido
sonido_disparo = None
sonido_recarga = None

def inicializar_sonido():
    """Inicializa el audio y la musica de fondo"""
    try:
        pygame.mixer.init(44100, -16, 2, 2048)
        ruta_musica = os.path.join(RUTA_BASE, "sounds/ambiente1.mp3")
        
        if os.path.exists(ruta_musica):
            pygame.mixer.music.load(ruta_musica)
            pygame.mixer.music.play(-1) # Loop infinito
            print("Musica cargada.")
        else:
            print(f"No se encontro musica en: {ruta_musica}")
            
    except Exception as e:
        print(f"Error de sonido: {e}")

def cargar_textura_individual(ruta):
    """Carga una sola imagen PNG como textura OpenGL"""
    try:
        # Correccion de ruta relativa a absoluta
        if "~" in ruta:
            ruta = os.path.expanduser(ruta)
            
        if not os.path.exists(ruta):
            # print(f"Falta archivo: {ruta}") # Descomentar para depurar
            return None

        img = Image.open(ruta)
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
        img_data = img.convert("RGBA").tobytes()
        w, h = img.size

        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        
        return tex_id
    except Exception as e:
        print(f"Error cargando {ruta}: {e}")
        return None

def cargar_animacion(nombre_carpeta, cantidad_maxima):
    """
    Sustituye a tus funciones cargar_mc, cargar_fondo, etc.
    Usa la logica del FOR que pidio tu maestro corregida.
    """
    lista_texturas = []
    
    # LOGICA CORREGIDA DEL MAESTRO:
    # Usamos un for, pero construimos la ruta correctamente con f-strings
    ruta_carpeta = os.path.join(RUTA_BASE, "images", nombre_carpeta)
    
    print(f"Cargando animacion: {nombre_carpeta}...")
    
    for i in range(1, cantidad_maxima + 1):
        # Correccion: En python se usa f"{i}.png" no + {i} +
        nombre_archivo = f"{i}.png"
        ruta_completa = os.path.join(ruta_carpeta, nombre_archivo)
        
        textura = cargar_textura_individual(ruta_completa)
        
        if textura is not None:
            lista_texturas.append(textura)
            
    return lista_texturas
